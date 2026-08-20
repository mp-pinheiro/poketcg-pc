import type { ExtensionAPI, ExtensionContext } from "@oh-my-pi/pi-coding-agent";

type FactoryState = {
	runId?: string;
	active: boolean;
};

function activeRun(ctx: ExtensionContext): boolean {
	let active = false;
	for (const entry of ctx.sessionManager.getBranch()) {
		if (entry.type !== "poketcg.factory.session.v1") continue;
		const value = entry as FactoryState;
		active = value.active === true;
	}
	return active;
}

async function runControl(
	cwd: string,
	op: string,
	request: Record<string, unknown>,
	signal: AbortSignal | undefined,
): Promise<{ code: number; stdout: string; stderr: string }> {
	const child = Bun.spawn(
		["python3", "tools/factory/control.py", op, "--request", JSON.stringify(request)],
		{ cwd, stdin: "ignore", stdout: "pipe", stderr: "pipe" },
	);
	const timeout = setTimeout(() => child.kill("SIGKILL"), 3_700_000);
	const abort = () => child.kill("SIGTERM");
	signal?.addEventListener("abort", abort, { once: true });
	try {
		const [code, stdout, stderr] = await Promise.all([
			child.exited,
			new Response(child.stdout).text(),
			new Response(child.stderr).text(),
		]);
		return { code, stdout, stderr };
	} finally {
		clearTimeout(timeout);
		signal?.removeEventListener("abort", abort);
	}
}
export default function factoryExtension(pi: ExtensionAPI) {
	const z = pi.zod;
	pi.registerTool({
		name: "factory",
		label: "Factory",
		description: "Execute one typed autonomous port-factory control operation.",
		parameters: z.object({
			op: z.enum([
				"preflight", "status", "reconcile", "frontier", "run-claim", "run-heartbeat",
				"run-release", "claim", "claim-heartbeat", "invalidate-attempts", "check",
				"record", "integrate", "forecast", "migrate", "complete",
			]),
			request: z.record(z.string(), z.unknown()).default(() => ({})),
		}),
		async execute(_toolCallId, params, signal, _onUpdate, ctx) {
			const result = await runControl(
				ctx.cwd,
				params.op,
				params.request,
				signal,
			);
			let payload: Record<string, unknown>;
			try {
				payload = JSON.parse(result.stdout.trim()) as Record<string, unknown>;
			} catch {
				payload = {
					schema: 1,
					op: params.op,
					status: "stop",
					error: { class: "ControlProtocol", detail: result.stderr || result.stdout, retry_at: null },
				};
			}
			if (params.op === "preflight" && payload.status === "ok") {
				const roles = ["@default", "@smol", "@slow", "@task"].map(role => ({
					role,
					model: pi.models.resolve(role)?.id ?? null,
					agent_name: role === "@smol" ? "port-generator-smol" : role === "@task" ? "port-generator-task" : null,
				}));
				const unresolved = roles.filter(role => role.model === null);
				if (unresolved.length > 0) {
					payload = {
						schema: 1,
						op: params.op,
						status: "stop",
						run_id: null,
						snapshot_sha256: null,
						data: { roles },
						error: {
							class: "ModelRole",
							detail: `unresolved model roles: ${unresolved.map(role => role.role).join(", ")}`,
							retry_at: null,
						},
					};
				} else {
					payload.data = { ...((payload.data as Record<string, unknown> | null) ?? {}), roles };
				}
			}
			if (payload.status !== "stop") {
				const active = params.op === "run-claim"
					? payload.status === "ok"
					: (params.op === "run-release" && payload.status === "ok")
						|| (params.op === "complete" && payload.status === "complete")
						? false
						: activeRun(ctx);
				pi.appendEntry<FactoryState>("poketcg.factory.session.v1", {
					active,
					runId: typeof payload.run_id === "string" ? payload.run_id : undefined,
				});
			}
			return {
				content: [{ type: "text", text: JSON.stringify(payload) }],
				details: { code: result.code, payload },
			};
		},
	});
	pi.on("tool_call", async (event, ctx) => {
		if (!activeRun(ctx)) return;
		if (["factory", "task", "hub"].includes(event.toolName)) return;
		return { block: true, reason: "active factory run permits only factory, task, and hub" };
	});
}

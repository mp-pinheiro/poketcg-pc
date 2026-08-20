import type { ExtensionAPI, ExtensionContext } from "@oh-my-pi/pi-coding-agent";

type FactoryState = {
	runId?: string;
	active: boolean;
};

type DeliveryEntry = {
	type: "poketcg.factory.delivery.v1";
	kind: "task-job" | "agent-message";
	id: string;
	agent_id: string;
	respawned_from: string | null;
	resolved_model: string;
	duration_ms: number;
	settled_at: string;
	usage: {
		input_tokens: null;
		output_tokens: null;
		cached_tokens: null;
		cost_usd: null;
		source: "omp-hub-v17.4-unavailable";
	};
	reply: string;
	used?: boolean;
};

function jsonFromText(value: unknown): Record<string, unknown> | null {
	if (typeof value !== "string") return null;
	try {
		const parsed = JSON.parse(value) as unknown;
		return parsed && typeof parsed === "object" ? parsed as Record<string, unknown> : null;
	} catch {
		return null;
	}
}

function textContent(content: unknown): string {
	if (!Array.isArray(content)) return "";
	return content
		.filter((part): part is { type: "text"; text: string } =>
			!!part && typeof part === "object" && (part as { type?: unknown }).type === "text"
			&& typeof (part as { text?: unknown }).text === "string")
		.map(part => part.text)
		.join("");
}

function deliveryFromToolResult(event: {
	toolName: string;
	input: unknown;
	content: unknown;
	details: unknown;
}): DeliveryEntry | null {
	const details = event.details && typeof event.details === "object"
		? event.details as Record<string, unknown>
		: {};
	const body = jsonFromText(textContent(event.content)) ?? {};
	const parsed = body.result && typeof body.result === "object"
		? body.result as Record<string, unknown>
		: body;
	const detailPayload = details.payload && typeof details.payload === "object"
		? details.payload as Record<string, unknown>
		: {};
	const detailResult = details.result && typeof details.result === "object"
		? details.result as Record<string, unknown>
		: {};
	const result = { ...details, ...detailPayload, ...detailResult, ...parsed };
	if (event.toolName === "task") {
		const id = typeof result.id === "string" ? result.id : null;
		const status = result.status;
		const duration = typeof result.durationMs === "number" ? result.durationMs : null;
		const model = typeof result.resolvedModel === "string" ? result.resolvedModel : null;
		const resultText = typeof result.resultText === "string" ? result.resultText : textContent(event.content);
		const agent = typeof result.agentId === "string" ? result.agentId
			: typeof result.agent_id === "string" ? result.agent_id : null;
		const respawnedFrom = typeof result.respawnedFrom === "string" ? result.respawnedFrom : null;
		const settledAt = typeof result.settledAt === "string" ? result.settledAt : new Date().toISOString();
		if (status !== "completed" || !id || duration === null || !model || !resultText || !agent) return null;
		return {
			type: "poketcg.factory.delivery.v1",
			kind: "task-job",
			id,
			agent_id: agent,
			respawned_from: respawnedFrom,
			resolved_model: model,
			duration_ms: duration,
			settled_at: settledAt,
			usage: {
				input_tokens: null,
				output_tokens: null,
				cached_tokens: null,
				cost_usd: null,
				source: "omp-hub-v17.4-unavailable",
			},
			reply: resultText,
		};
	}
	if (event.toolName !== "hub") return null;
	const waited = result.waited && typeof result.waited === "object"
		? result.waited as Record<string, unknown>
		: details.waited && typeof details.waited === "object"
			? details.waited as Record<string, unknown>
			: null;
	if (!waited || typeof waited.id !== "string" || typeof waited.from !== "string"
		|| typeof waited.ts !== "string" || typeof waited.body !== "string") return null;
	const input = event.input && typeof event.input === "object"
		? event.input as Record<string, unknown>
		: {};
	const ids = Array.isArray(input.ids) ? input.ids : [];
	if (!ids.includes(waited.id)) return null;
	const duration = typeof result.durationMs === "number" ? result.durationMs : 0;
	const model = typeof result.resolvedModel === "string" ? result.resolvedModel : "hub";
	return {
		type: "poketcg.factory.delivery.v1",
		kind: "agent-message",
		id: waited.id,
		agent_id: waited.from,
		respawned_from: null,
		resolved_model: model,
		duration_ms: duration,
		settled_at: waited.ts,
		usage: {
			input_tokens: null,
			output_tokens: null,
			cached_tokens: null,
			cost_usd: null,
			source: "omp-hub-v17.4-unavailable",
		},
		reply: waited.body,
	};
}

function activeRun(ctx: ExtensionContext): boolean {
	let active = false;
	for (const entry of ctx.sessionManager.getBranch()) {
		if (entry.type !== "poketcg.factory.session.v1") continue;
		const value = entry as FactoryState;
		active = value.active === true;
	}
	return active;
}

function newestUnusedDelivery(ctx: ExtensionContext): DeliveryEntry | null {
	for (const entry of [...ctx.sessionManager.getBranch()].reverse()) {
		if (entry.type !== "poketcg.factory.delivery.v1") continue;
		const value = entry as unknown as DeliveryEntry;
		if (value.used !== true) return value;
	}
	return null;
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
				"run-release", "claim", "claim-heartbeat", "invalidate-attempts", "join", "check",
				"record", "integrate", "forecast", "migrate", "complete",
			]),
			request: z.record(z.string(), z.unknown()).default(() => ({})),
		}),
		async execute(_toolCallId, params, signal, _onUpdate, ctx) {
			let joinedDelivery: DeliveryEntry | null = null;
			if (params.op === "join") {
				if (!activeRun(ctx)) {
					return {
						content: [{ type: "text", text: JSON.stringify({
							schema: 1, op: params.op, status: "stop",
							error: { class: "ActiveRun", detail: "join requires an active factory run", retry_at: null },
						}) }],
						details: { code: 1 },
					};
				}
				const delivery = newestUnusedDelivery(ctx);
				joinedDelivery = delivery;
				if (!delivery) {
					return {
						content: [{ type: "text", text: JSON.stringify({
							schema: 1, op: params.op, status: "stop",
							error: { class: "Delivery", detail: "no unused task or Hub delivery", retry_at: null },
						}) }],
						details: { code: 1 },
					};
				}
				const requested = params.request.delivery;
				if (requested !== undefined && JSON.stringify(requested) !== JSON.stringify(delivery)) {
					return {
						content: [{ type: "text", text: JSON.stringify({
							schema: 1, op: params.op, status: "stop",
							error: { class: "Delivery", detail: "join delivery is not the newest unused delivery", retry_at: null },
						}) }],
						details: { code: 1 },
					};
				}
				params = { ...params, request: { ...params.request, delivery } };
			}
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
				const roles = ["@smol", "@task"].map(role => ({
					role,
					model: ctx.models.resolve(role)?.id ?? null,
					agent_name: role === "@smol" ? "port-generator-smol" : "port-generator-task",
				}));
				const unresolved = roles.filter(role => role.model === null);
				const distinct = roles[0].model !== roles[1].model;
				if (unresolved.length > 0 || !distinct) {
					payload = {
						schema: 1,
						op: params.op,
						status: "stop",
						run_id: null,
						snapshot_sha256: null,
						data: { roles },
						error: {
							class: "ModelRole",
							detail: unresolved.length > 0
								? `unresolved model roles: ${unresolved.map(role => role.role).join(", ")}`
								: "smol and task roles resolve to the same model",
							retry_at: null,
						},
					};
				} else {
					payload.data = { ...((payload.data as Record<string, unknown> | null) ?? {}), roles };
				}
			}
			if (params.op === "join" && payload.status !== "stop" && joinedDelivery) {
				pi.appendEntry<DeliveryEntry>("poketcg.factory.delivery.v1", {
					...joinedDelivery,
					used: true,
				});
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
	pi.on("tool_result", async (event, ctx) => {
		if (!activeRun(ctx) || !["task", "hub"].includes(event.toolName) || event.isError) return;
		const delivery = deliveryFromToolResult({
			toolName: event.toolName,
			input: event.input,
			content: event.content,
			details: event.details,
		});
		if (delivery) pi.appendEntry<DeliveryEntry>("poketcg.factory.delivery.v1", delivery);
	});
	pi.on("tool_call", async (event, ctx) => {
		if (!activeRun(ctx)) return;
		if (["factory", "task", "hub"].includes(event.toolName)) return;
		return { block: true, reason: "active factory run permits only factory, task, and hub" };
	});
}

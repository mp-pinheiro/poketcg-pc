import { lstat, realpath } from "node:fs/promises";
import path from "node:path";
import type { ExtensionAPI, ExtensionContext } from "@oh-my-pi/pi-coding-agent";

type LaneCapability = {
	root: string;
	token: string;
};

type FactoryState = {
	runId?: string;
	snapshotSha256?: string;
	claimIds?: number[];
	landedRevision?: string;
};
const workerAgents: Record<string, true> = {
	"port-worker": true,
	"factory-helper": true,
};
const blockedWorkerTools: Record<string, true> = {
	"bash": true,
	"eval": true,
	"lsp": true,
	"browser": true,
	"web_search": true,
	"task": true,
	"factory": true,
};

function sessionAgent(ctx: ExtensionContext): string | undefined {
	for (const entry of ctx.sessionManager.getBranch()) {
		if (entry.type !== "session_init") continue;
		const value = entry as { agent?: unknown };
		if (typeof value.agent === "string") return value.agent;
	}
	return undefined;
}

function laneCapability(ctx: ExtensionContext): LaneCapability | undefined {
	for (const entry of ctx.sessionManager.getBranch()) {
		if (entry.type !== "session_init") continue;
		const value = entry as { task?: unknown };
		if (typeof value.task !== "string") continue;
		const root = /FACTORY_LANE_ROOT=([^\s]+)/.exec(value.task)?.[1];
		const token = /FACTORY_LANE_CAPABILITY=([0-9a-f]{64})/.exec(value.task)?.[1];
		if (root && token) return { root, token };
	}
	return undefined;
}

async function resolvedTarget(input: string): Promise<string | undefined> {
	const absolute = path.resolve(input);
	let current = absolute;
	for (;;) {
		try {
			return await realpath(current);
		} catch {
			const parent = path.dirname(current);
			if (parent === current) return undefined;
			current = parent;
		}
	}
}

async function insideLane(target: string, lane: LaneCapability): Promise<boolean> {
	const root = await realpath(lane.root).catch(() => undefined);
	const resolved = await resolvedTarget(target);
	if (!root || !resolved) return false;
	if (resolved !== root && !resolved.startsWith(`${root}${path.sep}`)) return false;
	let current = path.resolve(target);
	while (current !== path.dirname(current)) {
		const info = await lstat(current).catch(() => undefined);
		if (info?.isSymbolicLink()) return false;
		current = path.dirname(current);
	}
	return true;
}

function editTargets(input: Record<string, unknown>): string[] {
	const patch = typeof input.patch === "string" ? input.patch : "";
	return [...patch.matchAll(/^\[([^#\]\n]+)#[0-9A-F]{4}\]/gm)].map(match => match[1]);
}

function readTargets(toolName: string, input: Record<string, unknown>): string[] {
	if (toolName === "edit") return editTargets(input);
	const value = input.path;
	if (typeof value !== "string") return [];
	return value.split(";").filter(Boolean);
}

export default function factoryExtension(pi: ExtensionAPI) {
	const z = pi.zod;
	pi.registerTool({
		name: "factory",
		label: "Factory",
		description: "Execute one typed autonomous port-factory control operation.",
		parameters: z.object({
			op: z.enum(["preflight", "status", "reconcile", "frontier", "run-claim", "run-heartbeat", "run-release", "claim", "record", "integrate", "forecast", "migrate", "complete"]),
			request: z.record(z.string(), z.unknown()).default(() => ({})),
		}),
		async execute(_toolCallId, params, _onUpdate, ctx, signal) {
			const result = await ctx.exec(
				"python3",
				["tools/factory/control.py", params.op, "--request", JSON.stringify(params.request)],
				{ cwd: ctx.cwd, signal, timeout: 3_700_000 },
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
					payload.data = { ...(payload.data ?? {}), roles };
				}
			}
			if (payload.status !== "stop") {
				pi.appendEntry<FactoryState>("poketcg.factory.session.v1", {
					runId: typeof payload.run_id === "string" ? payload.run_id : undefined,
					snapshotSha256: typeof payload.snapshot_sha256 === "string" ? payload.snapshot_sha256 : undefined,
				});
			}
			return {
				content: [{ type: "text", text: JSON.stringify(payload) }],
				details: { code: result.code, payload },
			};
		},
	});
	pi.on("tool_call", async (event, ctx) => {
		const agent = sessionAgent(ctx);
		if (!agent || !workerAgents[agent]) return;
		if (blockedWorkerTools[event.toolName]) {
			return { block: true, reason: "factory worker capability denies this tool" };
		}
		if (!["read", "grep", "glob", "edit", "write"].includes(event.toolName)) return;
		const lane = laneCapability(ctx);
		if (!lane) return { block: true, reason: "factory worker has no lane capability" };
		const targets = readTargets(event.toolName, event.input);
		if (!targets.length) return { block: true, reason: "factory worker tool call has no lane target" };
		for (const target of targets) {
			if (target.includes("://") || target.startsWith("local://") || target.startsWith("artifact://")) {
				return { block: true, reason: "factory worker capability denies URL targets" };
			}
			if (!(await insideLane(target, lane))) {
				return { block: true, reason: "factory worker target escapes its lane" };
			}
		}
	});
}

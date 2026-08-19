import { createAgentSession, SessionManager } from "@oh-my-pi/pi-coding-agent";
import path from "node:path";

const root = path.resolve(import.meta.dir, "../..");
const stateDir = path.join(root, ".factory", "v2", "sessions");
const extension = path.join(root, ".omp", "extensions", "factory.ts");

type FactoryResponse = {
	schema: number;
	op: string;
	status: "ok" | "waiting" | "conflict" | "stop" | "complete";
	run_id: string | null;
	snapshot_sha256: string | null;
	data: Record<string, unknown> | null;
	error: { class: string; detail: string; retry_at: string | null } | null;
};

const CONTROL_TIMEOUT_MS: Record<string, number> = {
	record: 2_400_000,
	integrate: 5_400_000,
	migrate: 5_400_000,
};
const DEFAULT_CONTROL_TIMEOUT_MS = 600_000;

async function control(op: string, request: Record<string, unknown>): Promise<FactoryResponse> {
	const child = Bun.spawn(
		["python3", "tools/factory/control.py", op, "--request", JSON.stringify(request)],
		{ cwd: root, stdout: "pipe", stderr: "pipe" },
	);
	const limit = CONTROL_TIMEOUT_MS[op] ?? DEFAULT_CONTROL_TIMEOUT_MS;
	const timer = setTimeout(() => child.kill("SIGKILL"), limit);
	const [code, stdout, stderr] = await Promise.all([
		child.exited,
		new Response(child.stdout).text(),
		new Response(child.stderr).text(),
	]).finally(() => clearTimeout(timer));
	const lines = stdout.split("\n").map(line => line.trim()).filter(Boolean);
	for (const line of lines.reverse()) {
		if (!line.startsWith("{")) continue;
		try {
			return JSON.parse(line) as FactoryResponse;
		} catch {
			break;
		}
	}
	const stalled = code === null || code > 128;
	return {
		schema: 1,
		op,
		status: stalled ? "waiting" : "stop",
		run_id: null,
		snapshot_sha256: null,
		data: stalled ? { waiting_until: new Date(Date.now() + 60_000).toISOString(), waiting_reason: "control-stalled" } : null,
		error: {
			class: stalled ? "ControlStalled" : "ControlProtocol",
			detail: stderr || stdout || `control exited ${code}`,
			retry_at: null,
		},
	};
}
function sleep(milliseconds: number): Promise<void> {
	const { promise, resolve } = Promise.withResolvers<void>();
	setTimeout(resolve, milliseconds);
	return promise;
}

function nextWait(frontier: FactoryResponse): number {
	const value = frontier.data?.waiting_until;
	if (typeof value !== "string") return 60_000;
	const timestamp = Date.parse(value);
	if (!Number.isFinite(timestamp)) return 60_000;
	return Math.max(1_000, Math.min(60_000, timestamp - Date.now()));
}

async function main(): Promise<void> {
	const runId = crypto.randomUUID().replaceAll("-", "");
	const acquired = await control("run-claim", {
		run_id: runId,
		runner_instance: `${process.pid}`,
		lease_seconds: 600,
	});
	if (acquired.status === "conflict") {
		process.stdout.write(`${JSON.stringify(acquired)}\n`);
		return;
	}
	if (acquired.status !== "ok" || !acquired.data) {
		throw new Error(acquired.error?.detail || "could not acquire factory run lease");
	}
	const runClaimCommentId = acquired.data.run_claim_comment_id;
	if (typeof runClaimCommentId !== "number") {
		throw new Error("run claim response has no claim comment ID");
	}
	const manager = await SessionManager.create(root, stateDir);
	const { session, extensionsResult } = await createAgentSession({
		cwd: root,
		sessionManager: manager,
		modelPattern: "@default",
		toolNames: ["factory", "read", "grep", "glob", "eval", "task", "hub"],
		restrictToolNames: true,
		allowRestrictedCustomTools: true,
		additionalExtensionPaths: [extension],
	});
	if (extensionsResult.errors.length > 0) {
		const detail = extensionsResult.errors.map(entry => `${entry.path}: ${entry.error}`).join("; ");
		throw new Error(`factory extension failed to load: ${detail}`);
	}
	if (extensionsResult.extensions.length === 0) {
		throw new Error(`factory extension did not register: ${extension}`);
	}
	let released = false;
	const release = async (reason: string): Promise<void> => {
		if (released) return;
		released = true;
		await control("run-release", {
			run_id: runId,
			run_claim_comment_id: runClaimCommentId,
			reason,
		});
	};
	const stop = async (signal: string): Promise<void> => {
		await release(signal);
		await session.dispose();
		process.exit(0);
	};
	process.once("SIGINT", () => void stop("sigint"));
	process.once("SIGTERM", () => void stop("sigterm"));
	try {
		for (;;) {
			const heartbeat = await control("run-heartbeat", {
				run_id: runId,
				run_claim_comment_id: runClaimCommentId,
				lease_seconds: 600,
				phase: "planning",
			});
			if (heartbeat.status === "waiting") {
				await sleep(nextWait(heartbeat));
				continue;
			}
			if (heartbeat.status !== "ok") throw new Error(heartbeat.error?.detail || "run lease heartbeat failed");
			const reconciled = await control("reconcile", {
				adopt: true,
				run_id: runId,
				run_claim_comment_id: runClaimCommentId,
			});
			if (reconciled.status === "waiting") {
				await sleep(nextWait(reconciled));
				continue;
			}
			if (reconciled.status === "stop") throw new Error(reconciled.error?.detail || "artifact reconciliation stopped");
			const frontier = await control("frontier", {
				full: false,
				job_slots: 16,
				verifier_slots: 8,
			});
			if (frontier.status === "complete") {
				const completion = await control("complete", {
					run_id: runId,
					run_claim_comment_id: runClaimCommentId,
				});
				if (completion.status === "complete") {
					released = true;
					process.stdout.write(`${JSON.stringify(completion)}\n`);
					break;
				}
				if (completion.status === "stop") throw new Error(completion.error?.detail || "factory completion stopped");
				await sleep(nextWait(completion));
				continue;
			}
			if (frontier.status === "stop") throw new Error(frontier.error?.detail || "factory frontier stopped");
			if (frontier.status === "waiting") {
				await sleep(nextWait(frontier));
				continue;
			}
			await session.prompt([
				"Execute exactly one factory tick with the `factory` tool.",
				`Its ops: claim {run_id:"${runId}", run_claim_comment_id:${runClaimCommentId}, work_id, model_route},`,
				"then record {run_id, run_claim_comment_id, work_id, packet_sha256, claim_comment_id} for every finished attempt,",
				"and integrate {run_id, run_claim_comment_id, issue_numbers} when the frontier returns integration.",
				"claim returns the lane root, the owned paths and the exact prompt: dispatch it to a port-worker subagent",
				"(factory-helper when kind is repair) and record the attempt as soon as that subagent returns.",
				"Dispatch only the assignments below, never infer completion from an empty list, and never write files yourself.",
				JSON.stringify(frontier),
			].join("\n"));
		}
	} catch (error) {
		await release("runner-error");
		throw error;
	} finally {
		await session.dispose();
	}
}
if (import.meta.main) {
	if (Bun.argv.includes("--check-import")) {
		process.stdout.write("OMP SDK import: PASS\n");
	} else {
		await main();
	}
}

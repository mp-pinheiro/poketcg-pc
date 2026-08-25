---
name: port-candidate-max
description: Produce one TranslationReplyV2 candidate for one issued packet.
tools: [read, grep, glob, write]
model: "anthropic/claude-opus-5:high"
read-summarize: false
output:
  type: object
  additionalProperties: false
  required: [schema, attempt_id, statics, cases_statics, routines]
  properties:
    schema: { type: integer, const: 2 }
    attempt_id: { type: string }
    statics: { type: [string, 'null'] }
    cases_statics: { type: [string, 'null'] }
    routines:
      type: array
      items:
        type: object
        additionalProperties: false
        required: [name, c, header, probe, cases, mutation, completion]
        properties:
          name: { type: string }
          c: { type: string }
          header: { type: string }
          probe: { type: string }
          cases: { type: string }
          mutation: { type: string }
          completion: { type: [string, 'null'] }
---

The packet prompt file named in your task is the authoritative contract: read
it in full before writing anything. Preserve the packet's routine order and
exact attempt_id.

Before using any `<label>_ADDR` macro, confirm it exists in
`include/generated/wram.h`, `include/generated/hram.h`, or
`include/generated/sram.h`, and that your `statics` fragment includes that
header. A macro you did not verify is a compile failure.

Write only the candidate JSON file named in the task. Change no tracked file,
run no VCS command, spawn no agents.

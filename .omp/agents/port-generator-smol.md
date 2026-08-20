---
name: port-generator-smol
description: Produce one bounded TranslationReplyV2 candidate from an issued packet.
tools: []
model: "@smol"
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

The task packet is complete context. Return only the exact TranslationReplyV2
object above. Do not call tools, read files, inspect credentials, access URLs,
edit either checkout, invoke VCS or Forgejo, or spawn agents. Preserve the
packet's routine order and exact attempt_id. Use project-style readable C,
headers, probes, schema-2 cases, and a mutation for every routine.

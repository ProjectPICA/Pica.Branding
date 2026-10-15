# Page templates and quality bar

Every page the documentor creates or substantially rewrites follows one template and passes the quality bar.
Headings are fixed so readers learn where to look; omit a heading only when it is genuinely empty, and then
say "none" for Operations/Security/Open questions rather than dropping them.

## Quality bar (all page types)

1. **Purpose first.** The first paragraph says what this is and who needs it, in two sentences a newcomer
   follows without opening another page.
2. **Verifiable.** Every concrete claim (name, route, topic, setting, rule, number) traces to code,
   configuration or the live system. Cite it: repository, path, and the commit it was verified at, in the
   footer line. Unverifiable statements are written as "unverified" or left out; never plausible-sounding filler.
3. **Present tense, no history.** The page describes how things are now. Dates and "was changed to" belong in
   the work-log.
4. **Diagram where structure or flow exists.** Any multi-step flow, message exchange, topology or state
   machine gets a Mermaid diagram (` ```mermaid ` code block: `sequenceDiagram`, `flowchart`, `stateDiagram-v2`,
   `erDiagram`) plus two sentences of explanation. A diagram never replaces the prose.
5. **Consistent vocabulary.** Use the project's glossary terms (Overview / vocabulary page) exactly; define a
   new term on first use and add it to the glossary page.
6. **Connected.** At least two `<mention-page>` links to related pages, and the page is listed in its parent's
   index table with a one-line description.
7. **Scannable.** Tables for enumerations (endpoints, settings, jobs, roles), short paragraphs, no walls of
   text, no pasted diffs or logs, no machine-local paths.
8. **Footer.** Last line: `*Verified against <Repo> @ <short-sha> on YYYY-MM-DD · owner: <role or team>*`.
   Update it whenever the page is edited or re-checked.

## First line

`*<type> · <project> · created YYYY-MM-DD*` where type is one of `index`, `concept`, `reference`, `decision`,
`work-log`, `feature`, `guide`, `runbook`.

## Templates

### Architecture / system overview (`concept`)
Purpose and scope · Context (who and what it talks to) · Building blocks (table: component, responsibility,
technology, owner) · Key flows (one diagram each) · Data and state · Cross-cutting concerns (auth,
observability, resilience) · Constraints and trade-offs · Related pages · Open questions

### Component / unit reference (`reference`)
What it does and why it exists · Responsibilities and non-responsibilities · Interfaces (inbound: endpoints,
messages consumed; outbound: calls, messages published; table with contract and auth) · Internal structure
(layers, key types, one diagram if non-trivial) · Configuration (table: key, purpose, default, where set) ·
Dependencies · Failure modes and recovery · Testing · Operations (deployment, scaling, alerts, runbook link) ·
Related pages

### Message / API reference (`reference`)
Overview and conventions (auth, versioning, errors) · Table per area: route or topic, method, request and
response shape, auth policy, idempotency, producer/consumer · Error model · Examples (one request/response or
payload per non-obvious case)

### Feature (`feature`)
Summary and user value · Status (built / partial / not built, with the evidence) · Actors and permissions ·
Behaviour and business rules (numbered, testable) · Flow (diagram) · Edge cases · Components involved (links) ·
Acceptance criteria · Open questions

### Decision record (`decision`)
Context · Decision (one sentence) · Options considered (table: option, pros, cons, why rejected) ·
Consequences (good, bad, follow-ups) · Status (proposed / accepted / superseded by link) · Governs (links)

### Runbook / operations (`runbook`)
Purpose and when to use · Preconditions and access · Procedure (numbered, copy-pasteable commands with expected
output) · Verification (how to know it worked) · Rollback · Troubleshooting (symptom → cause → fix table) ·
Escalation / owner

### Infrastructure / pipeline (`reference`)
Topology (diagram) · Resources (table: name, type, environment, purpose, IaC location) · Pipelines (stages,
triggers, gates, secrets by name only) · Environments (table) · Identity and access · Cost / scaling notes ·
Known gaps

### Security / compliance (`reference`)
Scope · Threat surface and trust boundaries (diagram) · Authentication and authorisation (roles table) · Data
classification and handling · Controls and where enforced · Logging and audit · Known risks and mitigations ·
Review status

### Section index (`index`)
Summary of the section as it is today (3-5 sentences) · `Page | Contents` table, one row per child, ordered in
reading order · Related sections

### Day work-log entry (`work-log`)
Context · Root cause (bugs) · Change · Decision (with rejected alternative) · Pages updated or created (mentions)
· Tests · Outcome · Open items

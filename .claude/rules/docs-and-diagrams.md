---
paths:
  - "**/docs/**"
  - "**/*.md"
---

# Docs: diagrams are Mermaid

Draw every schematic — architecture, message flows, sequences, state machines, infra layouts — as a
```` ```mermaid ```` block (`flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, …). It renders
on GitHub, diffs as text and stays editable, unlike ASCII art or images.

- When you touch a page that still has an ASCII box diagram, convert it while you are there.
- Keep node labels short, and quote any label containing parentheses, slashes or colons — unquoted
  they break the parser. Check the block renders (GitHub preview or `npx -y @mermaid-js/mermaid-cli`).
- `Pica.Docs` diagrams claim to be *verified against source*: when you change one, check it against
  the current code, not against the old diagram.
- Docs describe the present. Rewrite a stale section; don't append a changelog to it.

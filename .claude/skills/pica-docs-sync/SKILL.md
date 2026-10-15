---
name: pica-docs-sync
description: Write a ProjectPICA code change back into the project documentation in Notion (the "Pica" docs — Overview router, section rows, day work-log) so the notes keep describing what the system does and why. Use after any change that alters behaviour, architecture, configuration, infrastructure or conventions; at the end of every pica-story run; and whenever asked to "update the docs", "sync the notes", "document this in Notion", "write the work log". Runs in an agent (documentor), in local, cloud and CI sessions alike.
---

# Pica docs sync

The Pica documentation is a wiki in Notion: knowledge is **distilled into topic pages at write time**,
so later questions are answered from structured pages instead of re-reading code. A sync updates every
page the change made stale, creates pages for genuinely new concepts, and writes the day's work-log.
It is not a log entry.

**Run it in an agent.** Launch `documentor` with inputs only: the repository (`git remote get-url
origin`), the diff range or working-tree state, and the issue. For a non-trivial change (new or changed
architecture, service, endpoint, infrastructure, domain rule, or any page created) then launch
`documentation-reviewer` with the same inputs plus the documentor's coverage report, and have the
documentor fix its BLOCKER and MAJOR findings. A change with nothing to document (typo, formatting,
dependency bump) needs no agent: say so in one line.

## Tools

Notion tools are named by operation: `notion-search`, `notion-fetch`, `notion-update-page`,
`notion-create-pages`. Their prefix depends on the session (the claude.ai Notion connector in local and
cloud sessions; a configured Notion MCP server in CI). If they are deferred, load them with ToolSearch.
Fetch `notion://docs/enhanced-markdown-spec` before writing content.

**No Notion tool in the session?** Do not improvise. List the pages that need updating, with what is now
false or missing on each, under "Docs to update" in the PR or the hand-back.

## Where the Pica docs live (found by title, never by a hard-coded link)

- `notion-search` for **"Pica · Overview"**: the Overview row of the *Docs* database. Its body is the
  router — it links every section. Start every sync there.
- The other section rows are titled `Pica · <Section>`:

| Section row | Holds |
|---|---|
| Overview | what Pica is, tech stack, documentation map |
| Product | features and their status |
| Architecture | system design, message flow, API reference |
| Decisions | architecture decision records |
| Domain | bounded contexts, entities, invariants, the `AddressRequest` lifecycle |
| Engineering | per-unit pages (one per repo/component), conventions, testing |
| Operations | Azure, pipelines, deployment, runbooks |
| Security | auth (Entra ID, B2C CIAM), roles, data handling |
| Work log | dated logs under month pages `YYYY-MM` |
| Archive | removed features and apps |

- Rows carry properties (`Project`, `Section`, `Type`, `Status`, `Owner`). Deeper pages are **sub-pages of
  a section row** (never new Docs rows, never at the teamspace root), and every child is listed in its
  parent's `Page | Contents` table with a one-line description.
- **`Pica.Docs` is repo-sourced.** Its `docs/` pages are imported into Notion with a provenance line
  `*reference · Pica · source: [Pica.Docs · <path>](<remote>/blob/<commit>/<path>) @ <commit>*`. Never
  hand-edit an imported page: change the repo, then re-import from `origin/main` into the same page.

**Never write a Notion URL or page id into a repository**, and never write a machine-local path
(`/Users/…`, `~/…`) into Notion. Name repositories by their GitHub remote.

## Crawl procedure

1. **Extract facts, not files.** From the diff: new/renamed/removed identifiers (handlers, endpoints,
   messages, jobs, config keys, tables, components, routes), changed behaviour and rules, changed topology,
   adopted conventions, decisions. These are the search terms.
2. **Map the territory.** Fetch the Overview router, then the index of every section the facts touch.
3. **Crawl.** For every fact, `notion-search` within the Overview's subtree for its identifiers and the old
   wording. Fetch every hit. Build a worklist: page → what is now false, incomplete or missing.
4. **Extend what exists.** `notion-fetch`, then `update_content` with the smallest exact `old_str` (or
   `insert_content` after a heading or row) so the page reads as current truth. Never `replace_content` a
   page with children. Never append "Update <date>" to a reference page.
5. **Create what is missing.** One concept per page, under the right section row, starting with
   `*<type> · Pica · created YYYY-MM-DD*` (`concept`, `reference`, `decision`, `feature`, `guide`), and
   immediately listed in the parent's table. Follow `page-templates.md` beside this file.
6. **Decisions** with a rejected alternative become an ADR page under `Pica · Decisions`, and go in the
   work-log.
7. **Work log last.** Under `Pica · Work log`, the month page `YYYY-MM` (create it if missing), the day page
   `YYYY-MM-DD - session work-log`: search for it first; append a `##` section if it exists, otherwise create
   it. Sections: Context / Root cause / Change / Decision / Tests / Outcome / Open items. Name the repository,
   the commit or PR, and mention every page you changed or created.
8. **Verify the writes.** Re-fetch each created page and each edited region: right parent, first line present,
   listed in the parent's table, mentions not plain text, no local path, no changelog text, escapes intact.

| The change… | Crawl and update |
|---|---|
| a service, job, queue, topic or message | Architecture (overview, message flow); Engineering unit page; Operations |
| an endpoint or contract | Architecture API reference; Engineering backend/web-app page; Domain if a rule moved |
| a domain rule, entity or state | Domain; Engineering validation pages; Product if visible |
| a feature | Product feature register and feature page; Overview if "what this is" changes |
| infra, pipelines, environments | Operations; Overview tech stack |
| auth, roles, data handling | Security; Architecture if the flow changes |
| a convention or test rule | Engineering conventions, testing |
| a removed feature or app | move its pages to Archive, drop them from indexes, fix pages that reference it |

## Notion gotchas

- Notion auto-links dotted names (`Pica.Docs`, `PICA.WebApp`) — fetch shows `[x](http://x)`; match that form
  in `old_str`.
- Escape literal `<`, `>`, `*`, `~`, `[`, `{`, `|` outside code; code fences and inline code are verbatim.
- Links between pages are `<mention-page url="…">Title</mention-page>`, never wikilinks.

## Rules

- **Crawl before you write.** A sync that touched only the work-log failed unless the coverage report shows
  the topic pages were checked and found current.
- **Distil, never dump.** No pasted diffs, logs or raw commit messages.
- **Truth over tidiness.** If the notes contradict the code, the code wins; fix the note and say so in the
  work-log.
- **Report** a coverage list: pages checked and current, pages updated (what changed), pages created, and
  anything left undone.

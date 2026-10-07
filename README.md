# claude-skills

Claude Code skills I use across projects. Project-agnostic by design — anything
specific to a codebase lives in that codebase, not here.

## Install

```
/plugin marketplace add skkap/claude-skills
/plugin install fly@skkap-skills
/plugin install shape-it@skkap-skills
/plugin install huddle@skkap-skills
```

## Catalog

Each plugin has its own README with the details.

| Plugin | Skill | Does |
|---|---|---|
| [`shape-it`](plugins/shape-it/README.md) | `shape-it` | Plan a piece of work; ask only what is expensive to get wrong |
| | `shape-it-lite` | The same, minus the domain model — for repos that carry none |
| | `domain` | Maintain the project's `DOMAIN.md` and `docs/decisions/` |
| | `domain-adopt` | Seed a model into a project that has none — **manual only** |
| [`fly`](plugins/fly/README.md) | `fly` | Get the current work onto a green pull request |
| [`huddle`](plugins/huddle/README.md) | `huddle` | Ask questions as a page in an agterm overlay — pictures, charts, sliders |

---

## The three files a project ends up carrying

Each is owned by the project, not the skill, and each exists so a skill can read
*only* that thing instead of re-deriving it from a `CLAUDE.md` that has absorbed
everything.

| File | Answers | Read by |
|---|---|---|
| `DOMAIN.md` | What is this project about, and what do we call it | `shape-it`, `domain` |
| `docs/decisions/` | Why is this setup the way it is | `shape-it`, `domain` |
| `CHECKS.md` | What does green mean here | `fly` |

None of them is scaffolded empty. Each is offered once, at the end of a session
that produced something to put in it.

## Credit

The domain model and decision-record conventions started from
[mattpocock/skills](https://github.com/mattpocock/skills) — `domain-modeling`,
`CONTEXT-FORMAT.md` and `ADR-FORMAT.md` in particular. What changed here: the
file is `DOMAIN.md` rather than `CONTEXT.md` (the word "context" collides with
"context window" in every sentence an agent writes about it); entries carry
`_Kinds_` and `_See_` alongside `_Avoid_`; relationships and cross-entity rules
are first-class sections rather than an undocumented habit; decisions live in
`docs/decisions/` rather than `docs/adr/`, because most of them are not
architectural; nothing assumes the project is made of source code; and the model
is wired into planning, so a settled term is never re-asked and a fresh answer is
written back the moment it settles.

## License

MIT

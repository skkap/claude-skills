# claude-skills

Claude Code skills I use across projects. Project-agnostic by design — anything
specific to a codebase lives in that codebase, not here.

## Install

```
/plugin marketplace add skkap/claude-skills
/plugin install fly@skkap-skills
/plugin install shape-it@skkap-skills
```

## Skills

| Plugin | Skill | Does |
|---|---|---|
| `shape-it` | `shape-it` | Plan a feature; ask only what is expensive to get wrong |
| `shape-it` | `domain` | Maintain the project's `DOMAIN.md` and `docs/adr/` |
| `fly` | `fly` | Get the current work onto a green pull request |

---

### `shape-it` — think a feature through before building it

Reads the codebase first, decides everything the repo can already answer, and
asks you only about the decisions that are expensive to reverse. Ends with a
written plan, not a conversation. It does not enter plan mode and does not
implement.

Three things it does differently:

**The test is reversibility, not difficulty.** A decision earns a question when
the repo cannot answer it *and* being wrong is costly to undo — schema and data
model, public routes and event names, vocabulary that leaks into the UI and the
API, scope boundaries, UI shape where there is no precedent, and business rules
that exist nowhere in the code. A tricky algorithm behind a stable interface is
cheap and gets decided for you; a column name in a shipped table is not. Anything
the repo already demonstrates is a citation, not a question.

**It shows its work on the silent decisions.** Letting an agent decide freely is
only safe if the calls it made alone are visible, so the plan carries a
*Decided without asking* section with the precedent for each. One wrong "obvious"
call otherwise poisons everything downstream, and that list is what makes it
cheap to catch.

**Questions are typed by where the answer goes.** Two kinds of answer outlive the
feature they were asked for, and each has a home:

| | Type | The question | Lands in |
|---|---|---|---|
| ◆ | **Domain** | What is this thing, what do we call it, what kinds are there, how does it relate, what is always true of it | `DOMAIN.md` |
| ▲ | **Decision** | Architecture, data model, public surface, technology lock-in, sync vs async — and deliberate no-s | `docs/adr/` |
| | *(untyped)* | Everything else — UI shape, ordering, scope trims inside this feature | the plan only |

The tag is not decoration. An untyped answer lives in one plan document and gets
re-asked the next time anyone touches the area; a ◆ answer is written to the file
every future session reads first. The split also makes it visible, at the moment
of asking, whether you are being asked about *the business* or about *the build* —
conflating those is what produces answers that sound decisive and settle nothing.

Domain questions are asked before decision questions, because you cannot sensibly
choose how to store a thing before agreeing what the thing is.

Questions arrive batched — up to four at once, each option stating its
consequence rather than its name, with a recommendation marked. Two rounds at
most; past that it is an interview. After each round it echoes back what it heard
in one line per question and hands you one open turn, so a qualifier that spans
several questions has somewhere to go — the picker's free-text box belongs to a
single question, and most corrections do not.

---

### `domain` — one set of words, written down once

The active discipline behind the ◆ tag, and usable on its own for a session with
no feature attached: *"we keep saying account and meaning three things — let's fix
that."*

> **`DOMAIN.md` says what is true about the business.
> An ADR says why the system is built the way it is.**

That line does the sorting. `DOMAIN.md` survives a rewrite in another language on
another stack; an ADR does not. *"A Shipment is one physical dispatch, and an
Order can produce several"* is domain. *"Order totals are stored rather than
recomputed from line items"* is a decision. *"The helper is called
`formatMoney`"* is neither, and belongs nowhere.

During a session it challenges a word that conflicts with an entry **in the
moment** rather than in a summary, proposes precise replacements for overloaded
ones, invents the edge-case scenario that forces a boundary to be exact, and
cross-checks against the code **in both directions** — code that contradicts a
stated rule, and entries nothing in the codebase references any more.

It writes an entry when the answer settles, in that turn. It never changes an
existing definition silently, because something is already built on the old
reading. And it creates files lazily, with content in hand — the offer to start a
`DOMAIN.md` comes at the *end* of a session, after the work, never as a
precondition for starting it.

#### `DOMAIN.md`

One file at the repo root. Four sections, only the first required:

```markdown
# Acme — Domain

Order fulfilment for wholesale customers.

## Language

**Shipment**:
One physical dispatch of goods, from one warehouse, on one day.
_Avoid_: delivery, parcel, consignment
_Kinds_: standard | express | pickup
_Rules_: A Shipment cannot be recalled once dispatched — a returned Shipment
becomes a Return.
_See_: [ADR-0007](docs/adr/0007-shipments-own-their-line-items.md), `src/fulfilment/shipment.ts`

## Relationships

- One **Order** produces one or more **Shipments**; a Shipment belongs to exactly
  one Order and cannot move between them.
- An **Invoice** covers one or more **Shipments**, which need not be from the
  same Order.

## Rules

- An Order cannot be cancelled once any of its Shipments has dispatched. The
  remaining Shipments can be, individually.

## Open questions

- Is a pickup a kind of Shipment, or its own entry?
```

`_Avoid_` is the line that stops drift — it names the synonyms that must not be
used, so two halves of a project cannot quietly adopt different words for one
thing. `_Kinds_` gets its own line because a closed set is the most expensive
item in the file: it becomes an enum in the schema, a set of values in the API
and a set of labels in the UI at the same time, and those three have to change
together. `_See_` is what keeps the model honest — an entry with no references is
either new or dead, and after a few months the entry alone will not tell you
which.

The business's own words win, including when they are not English. If the
business says 案件 rather than "matter", that is the entry, with a gloss in
parentheses; translating it for the model's benefit creates the second
vocabulary this file exists to prevent.

**Growing up:** a single `DOMAIN.md` graduates to a root `DOMAIN-MAP.md` plus
per-area `DOMAIN.md` files placed next to the code they describe. There is
exactly one growth path and no third shape — a model split two ways is worse than
one that is merely long. The trigger is not length alone: graduate when the file
passes roughly 150 lines *and* its terms fall into clusters that barely reference
each other.

The map's `## Between areas` section is where the real risk lives — two areas
sharing a word and meaning different things by it. One area owns a term, the
others reference it; the map says which, once.

#### `docs/adr/`

Sequentially numbered, `0001-slug.md`. One paragraph is a complete ADR:

```markdown
# Order totals are stored, not computed from line items

Tax rates and shipping rules change, and an order from two years ago must still
show the total the customer was actually charged — recomputing it produces a
different number every time the rules move. The total is written once at
placement and never recalculated; line items remain the audit trail.
```

An ADR is offered only when all three hold: **hard to reverse**, **surprising
without context**, and **the result of a real trade-off**. Each condition strips
a different kind of noise — reversible decisions get reversed rather than read,
unsurprising ones raise no question to answer, and a decision with no alternative
reads six months later as though a choice was made when none was.

Deliberate no-s live here too, which is why `shape-it` has no separate
out-of-scope file. Something considered and dropped needs a record for the same
reason the yes-s do: otherwise it gets proposed again every few months and the
reasoning is reconstructed by someone who was not there. That applies to the
**surprising** and the **recurring** no-s — routine scope trimming inside one
feature stays in that feature's plan.

Decisions are never edited into different decisions. A new ADR supersedes, and
the old one gains a `status:` line — the record of the fork is the whole value,
and rewriting it loses the reason the first answer looked right.

---

### `fly` — ship the current work as a green PR

Reads the repo's `CHECKS.md`, branches off the default branch, runs every check
that matches what changed, fixes what breaks, commits, pushes, and opens or
updates the pull request.

Two things it does differently:

**The repo owns what "green" means.** The check list isn't re-inferred from CI
config on every run — it's a file the repo carries, `CHECKS.md`, readable by
people and agents alike. No `CHECKS.md`? It derives the checks from CI workflows,
`CLAUDE.md`, or the toolchain, says in its report that it had to, and offers to
write the file so the next run is cheap and deterministic.

**Local checks are the gate; CI is the audit.** It finishes when the PR is open.
It takes one instant read of CI status on the way out and stops — no `gh run
watch`, no poll loop. Waiting on CI blocks indefinitely on a queued run, an
approval gate, or a workflow a path filter meant never to start, and watching
"the latest run" in a repo with several PR workflows is wrong more often than
it's right.

A CI failure that the local run should have caught is treated as a `CHECKS.md`
defect, fixed in the same PR.

#### `CHECKS.md`

One file at the repo root, one section per independently-scoped component:

````markdown
## 🖥️ Server
When: `server/**`
Dir: `server`
Setup: `poetry install --no-interaction`
Fix: `poetry run ruff format src tests`

```bash
poetry run ruff format --check src tests
poetry run lint
poetry run typecheck
poetry run pytest tests/ -n 4 --no-cov -q --tb=short
```
````

`When:` scopes it to what changed, `Setup:` guards against the stale-environment
"green locally, red in CI" split, `Fix:` makes formatter failures deterministic
instead of a guess. Full grammar in
[reference.md](plugins/fly/skills/fly/reference.md); writing one for an existing
repo in [adopting-a-repo.md](plugins/fly/skills/fly/adopting-a-repo.md).

---

## The three files a repo ends up carrying

Each is owned by the repo, not the skill, and each exists so a skill can read
*only* that thing instead of re-deriving it from a `CLAUDE.md` that has absorbed
everything.

| File | Answers | Read by |
|---|---|---|
| `DOMAIN.md` | What is this project about, and what do we call it | `shape-it`, `domain` |
| `docs/adr/` | Why is the system built this way | `shape-it`, `domain` |
| `CHECKS.md` | What does green mean here | `fly` |

None of them is scaffolded empty. Each is offered once, at the end of a session
that produced something to put in it.

## Credit

The domain model and ADR conventions started from
[mattpocock/skills](https://github.com/mattpocock/skills) — `domain-modeling`,
`CONTEXT-FORMAT.md` and `ADR-FORMAT.md` in particular. What changed here: the
file is `DOMAIN.md` rather than `CONTEXT.md` (the word "context" collides with
"context window" in every sentence an agent writes about it); entries carry
`_Kinds_` and `_See_` alongside `_Avoid_`; relationships and cross-entity rules
are first-class sections rather than an undocumented habit; and the model is
wired into planning, so a settled term is never re-asked and a fresh answer is
written back the moment it settles.

## License

MIT

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
| `shape-it` | `shape-it` | Plan a piece of work; ask only what is expensive to get wrong |
| `shape-it` | `domain` | Maintain the project's `DOMAIN.md` and `docs/decisions/` |
| `shape-it` | `domain-adopt` | Seed a model into a project that has none — **manual only** |
| `fly` | `fly` | Get the current work onto a green pull request |

`shape-it` and `domain` work on any project — a codebase, a company's records, a
knowledge vault, a research archive. Nothing in either depends on the material
being source code, and a records project usually has the vocabulary problem worse,
because prose tolerates two words for one thing far longer than a compiler does.

---

### `shape-it` — think the work through before building it

Reads the project first, decides everything it can already answer, and asks you
only about the decisions that are expensive to reverse. Ends with a written plan,
not a conversation. It does not enter plan mode and does not implement.

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
| 📖 | **Domain** | What is this thing, what do we call it, what kinds are there, how does it relate, what is always true of it | `DOMAIN.md` |
| ⚖️ | **Decision** | Architecture, data model, public surface, lock-in — technology, counterparty or legal — and deliberate no-s | `docs/decisions/` |
| | *(untyped)* | Everything else — UI shape, ordering, scope trims inside this piece of work | the plan only |

The tag is not decoration. An untyped answer lives in one plan document and gets
re-asked the next time anyone touches the area; a 📖 answer is written to the file
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

The active discipline behind the 📖 tag, and usable on its own for a session with
nothing else attached: *"we keep saying account and meaning three things — let's
fix that."*

> **`DOMAIN.md` says what is true about the subject.
> A decision record says why this setup is the way it is.**

That line does the sorting. `DOMAIN.md` survives rebuilding the whole thing from
scratch — different code, different tools, different filing system. A decision
record does not.

*"A Shipment is one physical dispatch, and an Order can produce several"* is
domain; *"order totals are stored rather than recomputed from line items"* is a
decision; *"the helper is called `formatMoney`"* is neither, and belongs nowhere.
The test does not change when the project is made of documents instead of code:
*"a Fiscal Year is the twelve months the company reports on, ending on the last
day of the year-end month"* is domain, *"the year-end is May, because it
maximises the first-year exemption and dodges the busy quarter"* is a decision,
and *"scans live in `legal/docs/`"* is neither.

During a session it challenges a word that conflicts with an entry **in the
moment** rather than in a summary, proposes precise replacements for overloaded
ones, and cross-checks against the material **in both directions** — material
that contradicts a stated rule, and entries nothing references any more. The
second direction is the one nobody checks and it costs one grep.

**To get a model out of a person it asks for a story, not a definition.** *"Walk
me through the last real one, start to finish — what came in, what you did, what
came out, and what went wrong that time."* Three things fall out of a narration
that no amount of asking for definitions produces: the words people use without
noticing, which are the settled vocabulary; the order of things, which is where
cardinality lives; and the rules — because nobody volunteers an invariant, they
volunteer *"—except that time when…"* halfway through a story. Then, and only
then, it invents the edge case that sits on a boundary the real story ran past.

**Rules are the most valuable lines in the file**, not the leftovers. A
definition says what a thing is; a rule says what you may not do with it, and
that is the half that changes behaviour. A model made only of definitions
produces work that is plausible and quietly wrong at the edges, because nothing
in it ever says no. So a rule has to be specific enough to be violated — *"nobody
signs off their own work"*, not *"we value alignment"* — and has to carry its
exception in the same breath, since a rule missing its exception gets discovered
as a bug.

It writes an entry when the answer settles, in that turn. It never changes an
existing definition silently, because something is already built on the old
reading — code, or a document already sent. And it creates files lazily, with
content in hand: the offer to start a `DOMAIN.md` comes at the *end* of a
session, after the work, never as a precondition for starting it.

**The exclusion that keeps the file short** is vocabulary the wider world owns.
General technical vocabulary (debounce, idempotency) is the familiar half; the
other is the general vocabulary of whatever field the project operates in —
articles of incorporation, withholding tax, GAAP, GDPR, a SAFE. Those are statute
or an industry's standard instrument, they are identical in every project that
touches them, and copying them into four `DOMAIN.md` files produces four versions
that drift. Where several projects need the same external vocabulary, one of them
owns the definition and the rest link to it. What belongs to a project is only
what *it* does with the term: *"the small-business exemption applies to us until
the Fiscal Year ending May 2028"* is domain; what that exemption *is* is not.

#### Markers

One set, defined here and used by all three skills — and it is **two independent
axes**, not one list of five. A line answers both.

*Where does this live?*

| | | |
|---|---|---|
| 📖 | **domain** → `DOMAIN.md` | the lexicon — what things are called |
| ⚖️ | **decision** → `docs/decisions/` | a choice that was weighed; alternatives existed |

*What do I need from you?*

| | | |
|---|---|---|
| ✅ | **nothing** | already written down, or two sources agree; shown so you can catch a wrong one, not confirm a right one |
| ⚠️ | **your attention** | something is broken — one word, two meanings, or two sources disagreeing |
| ❓ | **your answer** | a real gap; asked now, or parked in `## Open questions` |

They combine, and the second marker is what carries the information:

| | ✅ | ⚠️ | ❓ |
|---|---|---|---|
| **📖** | term already defined | one word, two meanings | term used, never defined |
| **⚖️** | already recorded, e.g. `0004` | two records disagree | a fork — you are being asked to pick |

`⚖️ ❓ retention window` is a decision *waiting to be made*; `⚖️ ✅ 0004` is one
*already on disk*.

They are not only for reports. Four moments get marked in ordinary prose: **📖**
the first time a term is used *because `DOMAIN.md` defines it*, **⚠️** the instant
a word in play conflicts with the model, **⚖️** when a call is made that belongs
in a decision record, and **✅** when a question turns out to be already answered
by an entry. That is what makes it visible that a plan is being built out of the
project's language rather than an improvised one — and it is checkable, because a
marker is a claim about what the model actually says.

Three rules stop it becoming decoration: mark the term and not every noun, one
marker per term per turn; never mark something you have not checked; and never
put ⚖️ on a reversible choice or ✅ on something merely mentioned. A response with
fifteen emoji is a response nobody scans.

**⚠️ is the one worth hunting.** A single word carrying two meanings is the most
expensive thing in a project's language and the thing nobody reports, because
each half looks correct from where it is used.

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
_See_: [0007](docs/decisions/0007-shipments-own-their-line-items.md), `src/fulfilment/shipment.ts`

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
together — or, outside code, a set of expense categories copied into a filing, a
spreadsheet and an accounting system. `_See_` is what keeps the model honest — an
entry with no references is either new or dead, and after a few months the entry
alone will not tell you which. It points at whatever the project is made of: a
source file, a scanned certificate, a decision record.

**The project's own words win, including when they are not English.** If the work
says *Sendung* rather than "shipment" — because the carrier's unit and yours are
not the same count — that is the entry; translating it for the model's benefit
creates the second vocabulary this file exists to prevent. Non-English headwords
are glossed once, on the entry: a short English meaning, plus a reading where the
script does not supply one. The gloss lives on the entry and nowhere else,
because a second gloss is a second definition waiting to disagree.

**Growing up:** a single `DOMAIN.md` graduates to a root `DOMAIN-MAP.md` plus
per-area `DOMAIN.md` files placed next to the material they describe. There is
exactly one growth path and no third shape — a model split two ways is worse than
one that is merely long. The trigger is not length alone: graduate when the file
passes roughly 150 lines *and* its terms fall into clusters that barely reference
each other.

The map's `## Between areas` section is where the real risk lives — two areas
sharing a word and meaning different things by it. Two questions settle most of
it: **who owns the term** (one area owns it, the others reference it) and **which
side is upstream** — whose changes force the other to react. They are not the
same question, and the second is the one people skip; ownership says where the
definition lives, upstream says where a change gets expensive. The map covers
areas *within* one
project; vocabulary shared between separate projects is the shared-reference case
above, not a map stretched across repository boundaries.

#### `docs/decisions/`

Sequentially numbered, `0001-slug.md`. A date and one paragraph is a complete
record:

```markdown
---
date: 2024-03-11
---

# Order totals are stored, not computed from line items

Tax rates and shipping rules change, and an order from two years ago must still
show the total the customer was actually charged — recomputing it produces a
different number every time the rules move. The total is written once at
placement and never recalculated; line items remain the audit trail.
```

In a codebase this artefact is usually called an **ADR** and lives in
`docs/adr/`. Same thing, one name here — half the decisions worth recording are
not architectural (a fiscal year-end, a registered office, a bank, a deliberate
no), and a project should not have to pick between two directories before it can
write one down. The most widely used ADR template,
[MADR](https://adr.github.io/madr/), reached the same conclusion from the other
direction: at 3.0.0 it renamed itself from *Markdown **Architectural** Decision
Records* to *Markdown **Any** Decision Records*.

**The date is required.** A decision is an answer to the rules, prices and
alternatives in force when it was made, and all of those move. *"The exemption
applies"* is a different claim in 2026 than in 2029. Numbering gives you order;
only the date gives you the world it was decided in.

A record is offered when **both** hold: **hard to reverse**, and **the result of
a real trade-off**. Reversible decisions get reversed rather than read, and a
decision with no alternative reads six months later as though a choice was made
when none was. **Surprising without context** is deliberately *not* a third
condition — it decides which record to write first when several qualify, because
those are the ones people go looking for, but requiring it throws away exactly
the unglamorous structural decisions that are most expensive to re-litigate.
"The primary bank is Aozora" surprises nobody and still needs a record.

Deliberate no-s live here too, which is why `shape-it` has no separate
out-of-scope file. Something considered and dropped needs a record for the same
reason the yes-s do (on a recurrence test rather than a reversibility one):
otherwise it gets proposed again every few months and the
reasoning is reconstructed by someone who was not there. That applies to the
**surprising** and the **recurring** no-s — routine scope trimming inside one
piece of work stays in that work's plan.

Decisions are never edited into different decisions. A new record supersedes, and
the old one gains a `status:` line — the record of the fork is the whole value,
and rewriting it loses the reason the first answer looked right. This is also why
a decisions *table* stops working past a dozen rows: a row cannot carry the
reasoning, cannot be superseded without being overwritten, and cannot be linked
to from an entry.

---

---

### `domain-adopt` — seeding a model into a project that has none

The vocabulary is already there, scattered through a `CLAUDE.md`, a README, a
decisions table and forty documents — which is nearly every project older than a
year. The ordinary discipline grows a model one term at a time; that is right for
daily use and would take another year here.

**It only runs when you ask for it by name.** That is the point of it being a
separate skill: it rewrites `CLAUDE.md` and creates files across the project, so
it has to be the session you wanted rather than a detour inside one — and a skill
that triggered on "this project has no `DOMAIN.md`" would fire exactly when it is
least welcome. `domain` keeps the *offer*, at the end of a session with the terms
in hand; this is what runs if you say yes.

Five steps — **explore → propose → ask → write → report** — and **nothing is
written until step four**.

The proposal step is what makes it safe. Seeding a file with thirty terms nobody
reviewed installs thirty definitions, and the wrong ones get copied by every
session afterwards — so the candidate model is shown whole first, with sources,
and marked:

```
📖 Terms — 14 candidates
  ✅ Member         equity holder in the company; not staff    CLAUDE.md, DECISIONS.md#5
  ⚠️ Engagement     "a signed contract" in overview.md,
                    "a piece of work" in operations/           2 sources disagree
  ❓ Matter         used 9×, defined nowhere

⚖️ Decisions — 6 of DECISIONS.md's 11 rows
  ✅ 0001  Fiscal year ends in May
  ✗ rows 3, 8, 9   facts, not decisions → moving to DOMAIN.md
```

Then it asks — one batched round, conflicts and expensive gaps only, never about
anything already marked ✅. Everything still ambiguous goes to `## Open questions`
rather than being resolved on the spot, because an adoption pass that becomes
forty questions is one that never gets run on the second project.

Converting an existing decisions log is **sorting**, not reformatting: a table
accumulates rows because a row is cheap, so half of them turn out to be facts
belonging in `DOMAIN.md`, or to-dos belonging where to-dos live. And vocabulary
*moves* out of `CLAUDE.md` rather than being copied out — instructions stay, a
one-line pointer replaces what left, because a summary left behind is a second
definition and it will be the one that drifts.

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

#### A complete example

Every section above shows fragments. `domain` ships one small project's model in
full — a `DOMAIN.md` and one of the decision records it links to — in
[EXAMPLE.md](plugins/shape-it/skills/domain/EXAMPLE.md). It is a design studio,
not a codebase, on purpose: the format does not depend on having source files,
and it is easier to see that when the example has none. About 70 lines covering a
whole business, which is the size a first model should be.

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

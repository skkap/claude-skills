# Changelog

## shape-it 1.3.0

**Say what the work is before asking anything about it.** Investigation gives the
agent a picture the operator cannot see, and the skill went straight from that to
a question round — so the first thing the operator was asked to do was answer
questions about a reading they had not seen. A misread stayed invisible until it
was already baked into a plan.

A new §3 states it back first: five short lines, no jargon, readable by someone
who has never opened the project. What this is; **why now**; what changes and for
whom; **what it costs to leave alone**; and how many questions are coming.

```
**Shipment splitting** — an order too large for one van currently fails at
checkout instead of going out in two.

Why now      Support is refunding roughly one order a week over this.
Effect       Large orders complete; customers see two deliveries, not an error.
If we don't  The failure stays silent — nothing logs it as a lost sale.
Ahead        4 questions: naming, cancellation, one API shape, one scope line.
```

It is a checkpoint, not a preamble — the cheapest possible moment to catch a
wrong understanding, because every question after it inherits the error.

Four rules keep it from becoming ceremony. It must be **derived, not echoed**: if
the five lines contain nothing the operator did not already type, §1 was not
finished. **Plain words only** — a framing only the team can read cannot be
checked by anyone else. **For a bug, the reason is the failure, not the defect**
("customers are charged twice and we refund by hand", not "the total is computed
twice"), which is also how a plan gets cancelled before it is written when the
honest answer is that the bug costs nothing. And the **question count is a
promise**, stated up front so the operator knows what they are committing to,
not a first guess to be revised upward.

Nothing unclear? It says so and skips the questions — a question round is not
proof of diligence.

The same five lines become the plan's `## What this is`, unrewritten. They were
agreed before a single question was asked, which makes them the one part of the
document already known to be right.

## shape-it 1.2.0

**The domain model stops assuming source code.** 1.1.0 was written for
codebases and said so in every load-bearing sentence: the sorting test was
*"still true after a rewrite on another stack"*, `_See_` wanted source files,
§3 cross-checked "against the code", and per-area models were placed "next to
the code they describe". None of that survives contact with a project made of
documents — a company's records, a knowledge vault, a research archive — which
is precisely where the vocabulary problem is worst, because prose tolerates two
words for one thing far longer than a compiler does.

The test is now *"still true if the whole thing were rebuilt from scratch"*, and
everywhere the skill said *the code* it says *the material* — whatever the
project actually consists of. Every rule kept its teeth; the worked examples now
come in pairs, one from a codebase and one from a company's records, sorted by
the same test.

### Getting a model out of a person: ask for a story

The skill was good at *policing* a model and thin at *eliciting* one — a single
paragraph on inventing edge cases, which is a technique for sharpening a boundary
you already know exists, not for finding one.

The primary move is now a narration: **"walk me through the last real one, start
to finish — what came in, what you did, what came out, and what went wrong that
time."** Three things fall out of a story that no amount of asking for
definitions produces: the words people use *without noticing*, which are the
settled vocabulary (a word produced in answer to "what do you call it?" is often
invented on the spot to be helpful); the order of things, which is where
cardinality and relationships live; and the rules, because nobody volunteers an
invariant — they volunteer *"—except that time when…"* halfway through. The
invented edge case still follows, but second: a real case gives you the middle,
and you invent only the boundary the story ran past.

`domain-adopt` gains the same move as the last step of its harvest. Documents
record what a project decided to write down, which is never the rules and rarely
the exceptions.

### Rules are the load-bearing lines, not the leftovers

`## Rules` was framed as the invariants left over after the per-entry ones — the
offcuts section. It is in fact the part that changes behaviour: a definition says
what a thing is, a rule says what you may not do with it, and a model made only
of definitions produces work that is plausible and quietly wrong at the edges
because nothing in it ever says no.

Three requirements now attach to a rule: state what is *forbidden* rather than
what is preferred (*"an Invoice is immutable once sent"*, not *"we try to avoid
editing invoices"* — nothing will honour a habit); give the exception in the same
breath, since a rule missing its exception gets discovered as a bug; and keep it
to one line, because a rule needing a paragraph is two rules or a decision that
wandered in.

### `docs/adr/` → `docs/decisions/`

One name, every project. Half the decisions worth recording are not
architectural — a fiscal year-end, a registered office, a bank, a deliberate no —
and a project should not have to decide which of two directories a decision goes
in before it can write it down. `ADR-FORMAT.md` becomes `DECISION-FORMAT.md` and
notes the ADR name once, as the codebase synonym. [MADR](https://adr.github.io/madr/)
reached the same conclusion from the other direction at 3.0.0, renaming itself
from *Markdown **Architectural** Decision Records* to *Markdown **Any** Decision
Records*.

The "what qualifies" list gained a second half for records projects: structural
choices once filed, who-is-what, counterparty lock-in, accounting and tax
treatments, instrument choices.

### The gate loses a condition, and gains a required date

The gate was three-part: hard to reverse, surprising without context, a real
trade-off. **Surprising** is demoted to a priority signal. It was doing exclusion
work the other two already do better, and it wrongly rejected exactly the
unglamorous structural decisions that cost the most to re-litigate — *"the
primary bank is Aozora"* is hard to reverse and had real alternatives, surprises
nobody, and in three years the question will be *why not the obvious one* with
nobody left who knows. Surprise now decides which record to write **first** when
several qualify, since those are the ones people go looking for.

`date:` frontmatter moves from optional to **required**. A decision is an answer
to the rules, prices and alternatives in force when it was made, and all of those
move; *"the exemption applies"* is a different claim in 2026 than in 2029.
Numbering gives you order, the date gives you the world it was decided in.

### New: `EXAMPLE.md`

Every file gave fragments and none gave a whole model, which is the one thing an
agent copying a format most needs. `domain` now ships a complete small project —
a `DOMAIN.md` plus one of the decision records it links to — at about 70 lines
covering an entire business. It is a design studio rather than a codebase on
purpose: nothing in the format depends on having source files, and that is easier
to see when the example has none.

### Between areas: ownership *and* direction

`DOMAIN-MAP.md` asked one question of a cross-area relationship — who owns the
term. It now asks two, the second being **which side is upstream**: whose changes
force the other to react. Ownership says where a definition lives; upstream says
where a change gets expensive, and they are not the same question. Where neither
side is upstream because both must move together, the map says that too — it is a
much more expensive relationship and should be visible as one.

This is the one thing taken from DDD's context mapping. The nine-pattern
catalogue (Conformist, Anticorruption Layer, Open Host Service…) is deliberately
left out: importing that vocabulary would violate the skill's own best rule —
vocabulary the wider world owns does not belong in a project's model — and a
`DOMAIN.md` for a small company should not require knowing what a Shared Kernel
is.

### Vocabulary the wider world owns

The old exclusion covered general *programming* vocabulary. It now covers the
general vocabulary of whatever field the project operates in — articles of
incorporation, withholding tax, GAAP, GDPR, a SAFE — for the same reason: they
are not yours, they are identical in every project that touches them, and copying
them into four `DOMAIN.md` files produces four versions that drift. Where several
projects need the same external vocabulary, one owns the definition and the rest
link. What belongs to a project is only what *it* does with the term.

### Non-English headwords are glossed, once

`DOMAIN.md` already said the project's own words win even when they are not
English. It did not say what that looks like. A non-English headword is now
glossed on the entry — a short English meaning, plus a reading where the script
does not supply one — and used bare thereafter. The gloss lives on the entry and
nowhere else, because a second gloss is a second definition waiting to disagree.

### One marker set, used in conversation

Findings, questions and reports carry markers on **two independent axes**, not
one list of five. *Where does this live* — **📖** domain, **⚖️** decision. *What
is needed from the operator* — **✅** nothing, **⚠️** your attention, **❓** your
answer. A line carries one of each, and the second is what does the work: `⚖️ ❓`
is a fork waiting to be picked, `⚖️ ✅` is one already on disk. Defining axis 2 by
the ask rather than by how finished the content feels is deliberate — "settled"
and "a decision" sound like the same claim and are not.

The 1.1.0 tags **◆** and **▲** are retired — two glyphs distinguished mainly by
being different shapes made the operator learn a private notation, and 📖 (the
lexicon) and ⚖️ (a choice that was weighed) say what they mean.

The four moments to mark in prose and the three rules against noise moved to
`MARKERS.md`, keeping the axis tables in `SKILL.md` where they have to be read
every time and the usage guidance where it is loaded on demand.

They are not only for reports. The skill now specifies four moments to mark in
ordinary prose: 📖 the first time a term is used *because `DOMAIN.md` defines
it*, ⚠️ the instant a word in play conflicts with the model, ⚖️ when a call is
made that belongs in a decision record, and ✅ when a question turns out to be
already answered by an entry. That is what makes it visible that a plan is being
built out of the project's language rather than an improvised one — and it is
checkable, since a marker is a claim about what the model says.

With three rules to stop it becoming decoration: mark the term and not every
noun, never mark something you have not actually checked, and never put ⚖️ on a
reversible choice or ✅ on something merely mentioned. A response with fifteen
emoji is one nobody scans.

### New skill: `domain-adopt`

The adoption pass moved out of `domain` into its own skill, invocable **only when
asked for by name**. It rewrites `CLAUDE.md` and creates files across a project;
that has to be the session the operator wanted, not a detour inside one — and a
skill whose description matches "this project has no `DOMAIN.md`" would fire
exactly when it is least welcome. `domain` keeps the *offer*, at the end of a
session, with the terms in hand; `domain-adopt` is what runs if the answer is
yes.

The procedure is five steps — **explore → propose → ask → write → report** — and
nothing is written until step four. The proposal step is what makes it safe:
seeding a file with thirty terms nobody reviewed installs thirty definitions, and
the wrong ones get copied by every session afterwards. The candidate model is
shown whole first, with sources and markers, before a file is touched.

Harvest runs in order of density (orientation files first — a parenthetical
definition or a "this is not X, it is Y" correction is an entry nearly written).
Sorting uses four buckets rather than three, the extra one being *stays where it
is*, which carries most of the volume. An existing decisions log is converted by
**sorting** rather than reformatting: a table accumulates rows because a row is
cheap, so half of them are facts belonging in `DOMAIN.md`, or to-dos belonging
where to-dos live. Vocabulary *moves* out of `CLAUDE.md` rather than being copied
out, leaving a pointer and not a summary.

It also names the failure mode. Every harvested term has an ambiguity in it, and
resolving all of them turns the pass into a forty-question interview that
guarantees it is never run on the next project. What is settled gets written
without asking, one batched round covers the conflicts and the expensive gaps,
and everything else goes to `## Open questions`.

### `shape-it`

Framing widened from "a feature" to "a piece of work", with the code examples
kept as examples. The ⚖️ tag now reads *lock-in — technology, counterparty or
legal*. Investigation reads "the nearest existing thing" rather than "the schema
and the API surface", which in a records project is the last time something like
this was done and what it produced.

## shape-it 1.1.0

**Answers that outlive the plan.** Every question `shape-it` asked landed in one
plan document, which meant the expensive ones got asked again the next time
anyone touched the area — and answered differently, because nothing recorded the
first answer. Across several repos that is how one project ends up with three
words for the same thing.

Questions are now typed by destination. **◆ Domain** — what a thing is, what it
is called, what kinds it comes in, how it relates, what is always true of it —
goes to `DOMAIN.md`. **▲ Decision** — architecture, data model, public surface,
technology lock-in, sync vs async, and deliberate no-s — goes to `docs/adr/`.
Everything else stays in the plan, which is correct for it. The tag is visible in
the question header, so it is clear at the moment of asking whether the subject
is the business or the build.

Domain questions are asked first: choosing how to store a thing before agreeing
what the thing is produces a confident answer to the wrong question, and a domain
answer routinely dissolves a technical fork that looked open.

`DOMAIN.md` and `docs/adr/` are now read at the *start* of investigation, ahead of
the schema and the neighbouring feature. A term already defined is a citation,
not a question.

### New skill: `domain`

The active discipline behind the ◆ tag, and invocable alone for a session with no
feature attached. Ships `DOMAIN-FORMAT.md` and `ADR-FORMAT.md`, so the formats
have one owner rather than being improvised per session — a `DOMAIN.md` written
to a private shape is worse than none, because the next session copies it.

The sorting rule is one line: **`DOMAIN.md` says what is true about the business;
an ADR says why the system is built the way it is.** Domain survives a rewrite on
another stack; a decision does not.

Behaviours worth naming: it challenges a conflicting word **in the moment**
rather than in an end-of-session summary, because by the summary the wrong word
is in a migration. It cross-checks against code **in both directions** — code
contradicting a stated rule, and entries nothing references any more, which is
the direction nobody checks. It never changes an existing definition silently,
since something is already built on the old reading. And it creates files lazily,
offering `DOMAIN.md` at the end of a session with the terms in hand, never as a
precondition for starting the work.

### The notes turn

`AskUserQuestion` gives one choice per question and a free-text box scoped to a
single question. A qualifier that spans the round — "yes, but only for the
express kind" — had nowhere to go, and the operator either dropped it or
derailed the round with it.

Each round now ends with the answers echoed back in the operator's terms, one
line per question, and one open turn. Echoing the *answer* rather than the option
label is what surfaces a misread while correcting it is still free. Once per
round, then move on.

### Derived from mattpocock/skills, with changes

`CONTEXT.md` → `DOMAIN.md`: "context" collides with "context window" in every
sentence an agent writes about the file. Entries gained `_Kinds_` (a closed set
becomes an enum, a set of API values and a set of UI labels simultaneously —
the most expensive line in the file) and `_See_` (an entry with no references is
either new or dead, and the entry alone will not say which). Relationships and
cross-entity rules became documented sections rather than an undocumented habit
of the upstream author's own file. Scope no longer has a separate home: a
deliberate no is a decision, and lands in `docs/adr/`.

## shape-it 1.0.0

**Plan a feature by asking only what is expensive to get wrong.** Planning fails
in two directions: an agent that asks nothing builds the wrong thing
confidently, and one that asks everything hands back the thinking it was given —
usually including questions the repository already answers.

The sorting test is reversibility rather than difficulty. A decision earns a
question only when the repo cannot answer it *and* undoing it later is costly:
schema, published surfaces, vocabulary that leaks into schema and UI and docs
at once, scope boundaries, UI shape without precedent, and business rules that
exist nowhere in the code. Everything else is decided, with the precedent cited.

Questions are batched multiple-choice rather than open dialogue — up to four at
once, recommendation marked, each option stating what happens rather than what
it is called, and previews for anything with a shape. Two rounds is the ceiling.

The plan carries a **Decided without asking** section. Deciding freely is only
safe when the silent calls are visible, and one wrong "obvious" call otherwise
propagates through everything built on it.

## fly 1.0.1

**Probe for `CHECKS.md` with `git ls-files`, not the filesystem.** macOS (APFS)
and Windows (NTFS) are case-insensitive by default, so `ls checks.md` and
`test -f CHECKS.MD` both succeed in a repo containing a correctly-named
`CHECKS.md` — every run on those platforms reported a phantom near-miss. A
warning that fires always is a warning nobody reads, which would have cost the
real signal: a genuinely misnamed file silently downgrading the run to
inference.

Found on the first live run, against a repo whose `CHECKS.md` was correct.

## fly 1.0.0

First release as a shared plugin. Previously a personal skill in `gpi-tools`.

### `CHECKS.md` replaces per-run CI derivation

The check list is now a file the repo owns, read as authority. Before, every run
re-derived the commands by reading the CI workflows — expensive on a repo with
several workflow files, non-deterministic between runs, and frequently wrong,
since path filters and OS matrix lanes don't map onto local commands.

Discovery falls back to CI workflows → `CLAUDE.md`/`AGENTS.md`/`CONTRIBUTING.md`
→ toolchain inference, names the source it used in the report, and offers to
write `CHECKS.md` from what it derived.

### Stopped waiting on CI

The old step 6 ran `gh run watch` on the newest run and looped until green. It
blocked indefinitely on queued runs and approval gates, watched a single run in
repos with several independent PR workflows, and on a change that triggered no
workflow watched the *previous* branch's run.

Now: one non-blocking `gh pr checks` on the way out, then stop. A CI failure the
local run missed is a `CHECKS.md` defect, fixed in the same PR.

### Robustness

- Preflight gates on repo, detached HEAD, `origin`, and `gh` auth — each failing
  with a named reason instead of an improvised workaround.
- Default branch resolved from `refs/remotes/origin/HEAD` instead of the
  network-bound `git remote show origin`.
- `gh pr edit` when a PR already exists, rather than a failing `gh pr create`.
- Rebase restricted to unpushed branches — the old advice contradicted the
  no-force-push guardrail.
- Per-command timeouts; bounded fix attempts; declared `Fix:` commands tried
  before model-authored repairs.
- Unrelated dirty files surfaced before staging.
- Suppressed checks (widened ignores, disabled rules, skipped tests) reported
  explicitly instead of passing as green.

### Defined output

Fixed report shape for both the shipped and stopped paths, always naming the
check source and anything suppressed. Three exit states: shipped, stopped,
nothing-to-do — the last re-reports instead of manufacturing an empty commit.

### Split into reference files

`SKILL.md` is the procedure; `adopting-a-repo.md`, `reference.md`, and
`troubleshooting.md` carry the detail, so the per-run read stays small.

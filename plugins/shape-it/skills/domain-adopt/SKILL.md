---
name: domain-adopt
description: "Seed a project's DOMAIN.md and docs/decisions/ from vocabulary already scattered through its CLAUDE.md, README, decision logs and documents — a one-off adoption pass that explores, proposes a candidate model, asks about the conflicts, writes, and reports. INVOKE ONLY WHEN EXPLICITLY ASKED: the operator says adopt, seed, bootstrap or set up a domain model for a project. Never start one as a side-effect of other work — it is a documentation session that rewrites CLAUDE.md, and it displaces whatever the operator actually asked for. For ongoing model maintenance during normal work, use the `domain` skill instead."
---

# domain-adopt — seeding a project's `DOMAIN.md`

The ordinary way a model grows is one term at a time, written the moment an
answer settles — that is the **`domain`** skill, and it is right for daily use.
It is useless for a project that has been running for two years: the terms are
already settled, already load-bearing, and already scattered across a
`CLAUDE.md`, a README, a decisions table and forty documents. Waiting for each to
come up again would take another two years.

Adoption is the deliberate one-off pass that lifts what is already there.

**Manual only.** This skill runs when the operator asks for it by name or asks in
so many words to adopt, seed or bootstrap a project's domain model. It never
starts on its own, never as a "while I'm here", and never because a session
happened to notice the project has no `DOMAIN.md` — noticing that is the
`domain` skill's job, and its offer belongs at the *end* of the work the operator
actually asked for. This pass rewrites `CLAUDE.md` and creates files across the
project; it has to be the session, not a detour inside one.

**One project per pass.** Rolling out across several is several passes, and the
second is much better than the first, because the first will have found what the
format does not yet handle.

| | file |
|---|---|
| This procedure | **this file** |
| The ongoing discipline, and the marker set | the **`domain`** skill |
| `DOMAIN.md` structure | `DOMAIN-FORMAT.md` in `domain` |
| Decision record structure and the gate | `DECISION-FORMAT.md` in `domain` |

Five steps, in order, and **nothing is written until step 4**:

| | |
|---|---|
| **1. Explore** | Survey the project and harvest candidates |
| **2. Propose** | Show the candidate model — before touching a file |
| **3. Ask** | One batched round on the conflicts and the expensive gaps |
| **4. Write** | `DOMAIN.md`, `docs/decisions/`, and the moves out of `CLAUDE.md` |
| **5. Report** | What was written, what is open, what was left alone |

---

## Markers

Two axes, defined by the **`domain`** skill. **Where it lives** — 📖 domain,
⚖️ decision. **What is needed from the operator** — ✅ nothing, ⚠️ your
attention, ❓ your answer. Every line of the proposal, the questions and the
report below carries one of each; the second is what tells the operator whether
they are being informed or asked.

⚠️ is the one to hunt for: a word carrying two meanings is what the whole pass
exists to catch.

---

## What "done" looks like

Not a complete model. A *usable* one: the ten to thirty terms that carry the
project, the decisions already made that nobody wants to re-argue, and an honest
`## Open questions` list.

A first `DOMAIN.md` that is right and short gets read and extended. One that
tries to be exhaustive is a second README, and inherits the problem the first one
has — that nothing can read *only* the vocabulary.

Two sizing tests, both cheap:

- **Would a competent newcomer to this field still need it explained?** If no, it
  is general vocabulary, owned by the wider world, and it stays out.
- **Has it ever been used in two senses, or under two names?** If yes, harvest it
  even if it seems obvious. Those are the entries that pay.

---

## 1. Explore

Derive it, don't invent it. In order — the early sources are dense because
someone already tried to explain the project to a newcomer, which is the same
job.

### Orientation files — `CLAUDE.md`, `README.md`, `overview.md`

The richest source, every time. Read the whole file, not the headings.

- **Parenthetical definitions.** *"a **matter** (one engagement for one client,
  from letter of engagement to final invoice)"*. Someone stopping mid-sentence to
  define a term has already identified it as project vocabulary — the entry is
  nearly written.
- **A table of parameters or key facts.** A company summary, a cap table, a set
  of standing parameters. Each row is either an entry (what the thing is) or a
  decision (which value was chosen, and why). Often both, and it splits.
- **Sentences that correct a word.** *"source notes; the polished version lives
  in…"*, *"this is not X, it is Y"*, *"use A internally, B externally"*. Every
  one of these is an `_Avoid_` line waiting to be written, and they are the
  highest-value harvest in the file — someone already hit the collision and
  wrote down the fix in the wrong place.

### Structure and index sections

A folder listing with a sentence per folder is two things at once: the areas of
the project, and a first pass at its nouns. The listing stays in `CLAUDE.md` as
navigation — the nouns in it come out.

### Decision logs, status files, "learnings" notes

`DECISIONS.md`, `STATUS.md`, a `log.md`, loose `*-decision.md` files at the root.
These hold decisions *and*, mixed in, a great deal of domain. Sorting them is
step 4.

### The names the project already uses

Recurring folder and file names, and the names of the things the project
repeatedly produces — a document type, a form, a report. A word the project has
named a folder after is a word it has already committed to.

In a codebase the same source is the schema: table names, enum values and column
names are the vocabulary that actually shipped.

### The material itself, for terms nothing defines

Grep a candidate term and read three hits. This is where the second meaning turns
up — the one that makes it worth an entry, and turns a ✅ into a ⚠️.

### The operator, for the case no document describes

Documents record what a project decided to write down, which is never the rules
and rarely the exceptions. So end the harvest with one request:

> *"Walk me through the last real one, start to finish — what came in, what you
> did, what came out, and what went wrong that time."*

One narration, in their words, in time order. It is the single highest-yield
source in this list and the only one that produces `## Rules`, because nobody
volunteers an invariant — they volunteer *"—except that time when…"* in the
middle of a story. It also exposes the words they use without noticing, which are
the settled vocabulary; a word produced in answer to *"what do you call it?"* is
often invented on the spot to help you.

Ask for **one** case, not a survey. If the project has obviously distinct kinds
of work, one of each, and no more — this is a harvest, not the interview §3 is
about to warn you off.

---

## 2. Propose — before writing anything

Show the candidate model and let the operator see it whole. This is the step that
makes adoption safe: seeding a file with thirty terms nobody reviewed installs
thirty definitions, and the wrong ones will be copied by every session after.

Say where you looked, then list candidates with markers, sources and one line of
definition each:

```
Explored: CLAUDE.md, README.md, overview.md, DECISIONS.md, legal/, payroll/
          (7 orientation files, 3 candidate areas)

📖 Terms — 14 candidates
  ✅ Member         equity holder in the company; not staff    CLAUDE.md, DECISIONS.md#5
  ✅ Fiscal Year    the twelve months reported on              overview.md
  ⚠️ Engagement     "a signed contract" in overview.md,
                    "a piece of work" in operations/           2 sources disagree
  ❓ Matter         used 9×, defined nowhere

⚖️ Decisions — 6 of DECISIONS.md's 11 rows
  ✅ 0001  Fiscal year ends in May
  ✅ 0002  Registered office is a virtual office, not the home address
  ❓ row 7  "use SMBC" — a decision with alternatives, or just a fact?
  ✗ rows 3, 8, 9   facts, not decisions → moving to DOMAIN.md
  ✗ rows 10, 11    open to-dos → staying where they are

Areas: single file. Terms cluster into legal / payroll but reference each
other constantly, so a map would split what belongs together.

Nothing is written and nothing leaves CLAUDE.md until you've seen this.
```

Keep the definitions to one line here. The proposal is for judging *coverage and
correctness of naming* — full entries come in step 4, and a proposal long enough
to need scrolling stops being reviewed.

---

## 3. Ask — one batched round

Use `AskUserQuestion`. **Up to four questions, one round; two if the answers open
something genuinely new.** Never more.

Ask about ⚠️ conflicts and about ❓ gaps where being wrong is expensive. Do not
ask about anything marked ✅ — if two sources agree, that is the definition, and
confirming it costs the operator a turn to say yes.

The same rules as any question this plugin asks: **lead with a recommendation and
mark it**, and make every option state its consequence rather than its name.

> ✗ `Engagement = a signed contract`
> ✓ `Engagement = a signed contract` — *delivery's "engagement" then needs its own
> word, probably Matter. Two entries, and `operations/` gets a rename.*

Then hand back one open turn, the answers echoed one line each, before writing
anything.

### Stop before it becomes an interview

The failure mode of an adoption pass is turning it into forty questions. Every
harvested term has an ambiguity in it somewhere; resolving all of them is a
week's work and guarantees the pass is never run on the next project.

So: **write what is already settled without asking**, ask only the expensive
handful, and send every remaining ❓ to `## Open questions` as a bullet naming
both readings. They will be answered better later, when they come up in real
work — which is exactly what the ongoing **`domain`** discipline is for. An
adoption pass that answers everything has done the next year's work badly instead
of this week's work well.

---

## 4. Write

### Sort into four buckets

Four in adoption, not three. The extra one carries most of the volume.

| Bucket | What |
|---|---|
| 📖 **`DOMAIN.md`** | What things are, what they are called, what kinds, how they relate, what is always true |
| ⚖️ **`docs/decisions/`** | Choices already made that clear the gate |
| **Stays where it is** | Instructions, navigation, and the documents themselves |
| **Nowhere** | Restatements of what the material already says |

**"Stays where it is" is not a failure to classify.** A response-style rule, a
folder index, a scanned certificate and a business plan are all doing their job
where they are. Adoption moves *vocabulary*, not content.

### Convert an existing decisions log

Mostly **sorting**, not reformatting — a table accumulates rows because a row is
cheap, so a good half of them turn out to be facts rather than decisions.

Row by row:

1. **Does it clear the gate** — hard to reverse, and a real trade-off with
   genuine alternatives? If yes → `docs/decisions/NNNN-slug.md`.
2. **If it fails the gate but states something true about the subject**, it is an
   entry or a rule in `DOMAIN.md`. *"The company is called Acme Holdings"* is a
   fact; *"chosen over Acme Group, which had no `.com` and collided with an
   existing registration"* is a decision. The same row often splits into both.
3. **If it fails the gate and states nothing durable**, it was a to-do. Leave it
   where to-dos live.

Then:

- **The notes column is usually the actual record.** The decision column holds
  the *what*; the reasoning is crammed into notes. That reasoning is the whole
  value — promote it to the body and let the title carry the what.
- **Number chronologically from `0001`,** by date, not by row order. Row numbers
  in a table are insertion order and mean nothing outside it.
- **Keep the dates**, in `date:` frontmatter. Legal and tax decisions are only
  interpretable against the rules in force when they were made.
- **Leave the old file as a pointer, or delete it — not both half-done.** A table
  still sitting next to the folder will keep receiving rows.

Loose `*-decision.md` files at the root are easier: already one file per
decision. Move, number, and check the title states the decision rather than the
topic.

### Move vocabulary out of `CLAUDE.md`

| | |
|---|---|
| **Leaves** | Definitions, glossed terms, "not X but Y" corrections, tables of what things are, rules about the subject |
| **Stays** | How to behave, response style, git conventions, tool choices, folder navigation, "read this before doing that" |

The distinction is genre, not topic. *"A Member is an equity holder, not staff"*
is domain wherever it currently sits. *"Gloss non-English terms on first use"* is
an instruction and belongs where instructions are.

When something leaves, `CLAUDE.md` gets one line pointing at where it went — not
a summary of it. A summary is a second definition, and it will be the one that
drifts.

---

## 5. Report

Same markers, one screen:

```
✅ Written
   DOMAIN.md            14 entries, 3 relationships, 2 rules
   docs/decisions/      6 records, 0001–0006, converted from DECISIONS.md
   CLAUDE.md            parameters table removed, one-line pointer left

❓ Open — 4, parked in DOMAIN.md § Open questions
   Matter vs Engagement after the rename
   Whether Pickup is a kind of Shipment or its own entry
   …

   Left alone: response style, git conventions, the folder index,
   DECISIONS.md rows 10–11 (open to-dos)
```

Then stop. The model is now something a session can read; it does not also need
to be finished.

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
format does not yet handle. Which only helps if you write that down — see
[§5](#5-report).

**A partial model is the normal starting point, not an obstacle.** The `domain`
skill offers adoption at the end of its sessions, so by the time anyone runs this
one there is often already a `DOMAIN.md` with a handful of entries in it. That is
a seed to build around, never something to replace: [§1](#1-explore) starts by
reading it.

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
| **3. Ask** | One batched round on the conflicts and the expensive gaps — *before writing* |
| **4. Write** | `DOMAIN.md`, `docs/decisions/`, and the moves out of `CLAUDE.md` and out of whatever writes |
| **5. Report** | What was written, what disagrees with what ships, what is open, what was left alone |

---

## Markers

Two axes, defined by the **`domain`** skill. **Where it lives** — 📖 domain,
⚖️ decision. **What is needed from the operator** — ✅ nothing, ⚠️ your
attention, ❓ your answer.

**Axis 2 is the one doing the work here.** It tells the operator whether they are
being informed or asked, which is the whole point of a proposal they have to
review. Axis 1 is mostly redundant in this skill's output — the proposal and the
report already separate terms from decisions into their own lists, so mark the
list once in its heading rather than every line inside it. In conversation the
full pairing still applies; that is `MARKERS.md`'s business, not this file's.

⚠️ is the one to hunt for: a word carrying two meanings is what the whole pass
exists to catch.

---

## What "done" looks like

Not a complete model. A *usable* one: the terms that carry the project, the
decisions already made that nobody wants to re-argue, and an honest
`## Open questions` list.

A first `DOMAIN.md` that is right and short gets read and extended. One that
tries to be exhaustive is a second README, and inherits the problem the first one
has — that nothing can read *only* the vocabulary.

**Size it per cluster, not per project: ten to thirty terms in each area the
project actually has.** A single-subject project lands near thirty and a mature
one with four or five genuine sub-vocabularies — a catalog, its chemistry, its
gamification, its search — lands near fifty without a word of padding. Counting
the whole file against thirty punishes exactly the projects this skill exists
for. Past about three clusters, ask whether `DOMAIN-MAP.md` and per-area files
would read better than one long file; the answer is often still no, when the
clusters reference each other constantly.

The two sizing *tests* below are what actually decide entry, and they outrank any
number:

- **Would a competent newcomer to this field still need it explained?** If no, it
  is general vocabulary, owned by the wider world, and it stays out.
- **Has it ever been used in two senses, or under two names?** If yes, harvest it
  even if it seems obvious. Those are the entries that pay.

---

## 1. Explore

Derive it, don't invent it. In order — the early sources are dense because
someone already tried to explain the project to a newcomer, which is the same
job.

### First: is there already a model?

Read `DOMAIN.md`, `DOMAIN-MAP.md` and `docs/decisions/` before anything else. A
seed left by an earlier `domain` session is the most authoritative source in the
project — every entry in it was settled *with the operator present*, which is
more than any document you are about to harvest can claim.

So it is not a draft to improve on:

- **Preserve existing entries verbatim.** Reword one and you have silently
  reopened a question that was already closed. If a seed entry now looks wrong,
  that is a ⚠️ for [§2](#2-propose--before-writing-anything), not an edit.
- **Match its voice.** A seeded file has already chosen how long a definition
  runs and how blunt a `_Rules_` line is. Copy that. House style beats
  `DOMAIN-FORMAT.md`'s examples wherever the two differ.
- **Build around it.** New clusters go beside the existing ones; keep its
  ordering, and let its `## Open questions` survive into the new file.
- **Carry its numbering forward.** Existing decision records keep their numbers;
  new ones continue the sequence. Never renumber.

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

### Verify every closed set against the live registry, never against prose

**Orientation files rot, and a two-year-old one is partly fiction.** This is the
step that separates harvesting from copying: a bulleted list in a markdown file
records what somebody believed once, while the enum, the `const` array, the
schema — or in a records project, the filing itself — is what is actually true
now. They drift apart silently, because nothing fails when prose goes stale.

So any `_Kinds_` line, any count, any "the six categories are…" gets read from
the registry and only from the registry. Expect hits: a real pass found a
`CLAUDE.md` advertising forty attributes in six categories where the code had
fifteen in three, and a second document repeating the same dead list.

A stale list is a finding, not just an input — it goes in the proposal as ⚠️,
because what to do about it ([§4](#4-write)) is the operator's call.

### The material itself, for terms nothing defines

Grep a candidate term and read three hits. This is where the second meaning turns
up — the one that makes it worth an entry, and turns a ✅ into a ⚠️.

### Prior sessions, where the project has them

Agent transcripts (`~/.claude/projects/<slug>/*.jsonl`), chat logs, PR review
threads, issue comments. Extract the **human** turns and read the corrections:

```
"no" · "actually" · "that's not what I" · "I meant" · "don't call it"
"we call it" · "wrong word" · "stop using" · "rather than"
```

This is a different class of source from everything above it. Documents record
what a project chose to write down; a transcript records **the moment somebody
was told they were wrong**, which is the raw material of an `_Avoid_` line. A
correction that already happened is a term that is already settled — it just
never found a home, and it is usually still lost.

A real pass recovered three entries this way, none of which existed in any
document: a correction that two words were being wrongly opposed to each other
(surviving only as a comment in a source file), a term the operator had defined
in passing with all three of its names, and a word the operator had themselves
flagged as ambiguous. Cost to the operator: nothing.

Filter the noise first — skill invocations and pasted prompts dominate the
byte count and none of it is the operator talking.

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

**When prior sessions substitute for this.** Where the project has a deep
transcript history, mine it *first* and treat the narration as optional: you are
after the operator's unrehearsed words and their corrections, and a year of
transcripts holds more of both than one retold case, at no cost to their time.
Where there is little or no history — a fresh repo, a records project, a
non-technical operator — the narration is irreplaceable and you should ask for
it. Know which situation you are in before deciding.

Either way, `## Rules` is the section that suffers when you skip the narration.
Transcripts yield vocabulary and corrections readily; invariants less so, because
an invariant surfaces mid-story rather than mid-correction. A thin `## Rules` at
the end of a pass is the signal that you owed the operator this question.

---

## 2. Propose — before writing anything

Show the candidate model and let the operator see it whole. This is the step that
makes adoption safe: seeding a file with thirty terms nobody reviewed installs
thirty definitions, and the wrong ones will be copied by every session after.

**Spend the proposal where review is needed, and nowhere else.** §3 says not to
ask about anything marked ✅; the same logic applies one step earlier. A ✅ term
is one two sources already agree on — it needs to be *visible* so the operator
can catch a wrong one, not *explained*. So:

- **✅ — name and cluster only.** A column of names under a heading, with a count.
- **⚠️ and ❓ — full detail.** Both readings, both sources, what each would cost.
  These are the lines the operator is actually being asked to read.

That asymmetry is what keeps the proposal to one screen on a project with fifty
candidates, which is the only way it gets read at all.

```
Explored: CLAUDE.md, README.md, overview.md, DECISIONS.md, legal/, payroll/,
          14 prior sessions (7 orientation files, 3 candidate areas)
Existing model: DOMAIN.md, 6 entries — preserved as-is, built around.

📖 Terms — 14 candidates
  ✅ 11, settled by two or more sources:
       legal    Member · Fiscal Year · Registered Office · Share Class
       payroll  Pay Run · Withholding · Year-End Adjustment
       filing   Blue Return · Consumption Tax Period · Invoice Number · Receipt

  ⚠️ Engagement    "a signed contract" in overview.md, "a piece of work"
                   in operations/ — 2 sources disagree, and the folder is
                   named after the second reading
  ⚠️ Category      the 6 listed in CLAUDE.md vs the 3 in the accounting export
                   — the doc has been stale since the 2024 restructure
  ❓ Matter        used 9×, defined nowhere

⚖️ Decisions — 6 of DECISIONS.md's 11 rows clear the gate

  #  decision                          reverse cost    alternatives named  verdict
  1  Fiscal year ends in May           amend articles  Dec, Mar            ✅ strong
  2  Registered office is virtual      re-file + fee   home address        ✅
  7  "Use SMBC"                        switch banks    none recorded       ❓ a fact?

  ✗ rows 3, 8, 9   facts, not decisions → moving to DOMAIN.md
  ✗ rows 10, 11    open to-dos → staying where they are

Areas: single file. Terms cluster into legal / payroll but reference each
other constantly, so a map would split what belongs together.

Nothing is written and nothing leaves CLAUDE.md until you've seen this.
```

Keep the definitions to one line. The proposal is for judging *coverage and
correctness of naming* — full entries come in step 4, and a proposal long enough
to need scrolling stops being reviewed.

### Grade the decisions here, in a table, before any are written

The two gate conditions in `DECISION-FORMAT.md` are easy to nod along to and hard
to apply to your own shortlist. Rendering them as columns — **reverse cost**,
**alternatives named**, **verdict** — forces the judgement to be made per record
rather than assumed for the batch, and it is the difference between six records
that earn their place and nine of which three are incident notes.

Two failure patterns the columns expose immediately:

- **No alternative in the "alternatives" column.** Then nothing was weighed and
  it is a fact, belonging in `DOMAIN.md`.
- **The reasoning already exists somewhere durable.** A choice explained at
  length in a `CLAUDE.md` that everyone reads does not need a third copy; writing
  one is the duplication this whole discipline exists to remove. Drop it and say
  why.

Marginal candidates go in the proposal with the verdict you would give them, so
the operator can overrule a call that is genuinely theirs. In a real pass the
operator killed a record from this table that had passed my own gate — that is
the review working, and it only happens if the table is shown.

---

## 3. Ask — one batched round

Use `AskUserQuestion`. **Up to four questions, one round; two if the answers open
something genuinely new.** Never more.

**The cap governs getting to the write, not the session.** It exists so the pass
cannot stall in front of the operator before producing anything — it is not a
budget for the conversation. If they widen the scope afterwards, challenge a
record, or ask for another sweep, that is new work and it gets its own questions.
Refusing to ask because "the round is used up" is a misreading.

Ask about ⚠️ conflicts and about ❓ gaps where being wrong is expensive. Do not
ask about anything marked ✅ — if two sources agree, that is the definition, and
confirming it costs the operator a turn to say yes.

**Reserve one question for the decision shortlist** whenever more than about five
records are proposed. Everything else in this step is about terms, and the result
is that decisions go from a one-line proposal to a written file with no review in
between — while being the harder judgement of the two. Ask about the marginal
ones by name, with the grading columns from §2 visible.

**Where the project has automated checks, ask whether the model should be
enforced.** A test that fails when an `_Avoid_` word appears in a prompt or a
string is the difference between a model that is followed and one that is
decoration — and it is also real churn, since existing violations must be cleaned
before it can go green. That trade is the operator's, and it will not occur to
them unless offered. Do not add such a test unasked.

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
| **Nowhere** | Restatements of what the material already says, and stale lists the registry contradicts |

**"Stays where it is" is not a failure to classify.** A response-style rule, a
folder index, a scanned certificate and a business plan are all doing their job
where they are. Adoption moves *vocabulary*, not content.

**Vocabulary that turns out to be stale is deleted, not corrected.** [§1](#1-explore)
will have caught lists that no longer match the registry. The instinct is to fix
them in place; don't. Correcting a stale list leaves a second copy of the
vocabulary, freshly accurate and free to drift again — which is precisely the
condition this pass exists to end. The list dies with the move, `DOMAIN.md` says
it once, and the old location gets the same one-line pointer everything else
gets.

The exception is a document whose *job* is to restate — a schema reference, an
API doc, a printed handbook. That is content, and it stays. Have it defer on
meaning, keep it accurate in its own terms, and say plainly which one wins when
they disagree.

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
- **Recover the date from version control when the source doesn't carry one.**
  A decision harvested out of prose has no date attached, and stamping it today
  is a small lie that makes the record uninterpretable — `DECISION-FORMAT.md`
  explains why the date is the load-bearing field. The history usually knows:

  ```bash
  git log --diff-filter=A --format=%ad --date=short -1 -- <the file it introduced>
  git log -S '<a distinctive phrase from the decision>' --format='%ad %s' --date=short -1
  ```

  In one pass this spread twelve records across six months instead of collapsing
  them onto one day, and the spread is itself informative — it shows which
  decisions were made under which constraints. Where nothing dates it, use the
  earliest date you can defend and say in the body that it is approximate.
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

### Point the things that *write* at the model

In a project where agents do the work — subagent prompts, skill instructions,
templates, briefing docs — those files carry their own copy of the vocabulary,
and it is the copy that does damage. A stale `CLAUDE.md` misleads a reader who
can push back; a stale prompt silently writes wrong data at scale.

This is not hypothetical. In a real pass the cause of a shipped data bug was a
term whose only definition lived in a UI description string: an extraction agent
read the narrow meaning there and mis-filed every facility that didn't match it.

So the same move as `CLAUDE.md`, applied to whatever writes:

- **Open the prompt with a requirement to read `DOMAIN.md`**, naming the
  collisions that bite this particular agent — not a generic pointer.
- **Delete the definitions it was carrying.** Keep the *operational* guidance
  that `DOMAIN.md` has no reason to hold: how to weigh evidence, which mistakes
  recur, what to do when sources conflict. Definition leaves; discipline stays.
  The line is genre again, exactly as with `CLAUDE.md`.
- **Say which wins.** "Where this prompt and `DOMAIN.md` disagree, `DOMAIN.md`
  wins and this prompt is stale."

⚠️ **Check what the test suite pins into those files before deleting anything.**
Prompts are sometimes guarded by parity tests asserting they contain particular
lists or definitions, and finding that out after the deletion means a broken
build and a confusing diff. Where a test pins content you were about to move,
leave it, and say so in the report — a passing guard is worth more than a tidier
prompt.

---

## 5. Report

Same markers, one screen:

```
✅ Written
   DOMAIN.md            14 entries, 3 relationships, 2 rules
   docs/decisions/      6 records, 0001–0006, converted from DECISIONS.md
                        dated from git history, 2024-03 → 2025-11
   CLAUDE.md            parameters table removed, one-line pointer left
   prompts/extract.md   feature definitions removed, cites DOMAIN.md

⚠️ Found disagreeing with what actually ships — 3
   CLAUDE.md listed 6 categories; the export has 3 (stale since the restructure)
   "Engagement" is the folder name and the wrong reading of the word
   two spellings of the same term on adjacent pages

❓ Open — 4, parked in DOMAIN.md § Open questions
   Matter vs Engagement after the rename
   Whether Pickup is a kind of Shipment or its own entry
   …

   Left alone: response style, git conventions, the folder index,
   DECISIONS.md rows 10–11 (open to-dos), the highlight definitions in
   extract.md (pinned by a parity test)
```

**The ⚠️ section is not optional and is often the most actionable thing here.**
A pass over a mature project always finds places where the shipped reality and
the written vocabulary have come apart — a stale list, a UI label using the word
the model rejects, dead strings for a thing that no longer exists. Those are
findings the operator can act on today, unlike the model itself, which pays out
later. Reporting them as a bare "left alone" buries them.

Then stop. The model is now something a session can read; it does not also need
to be finished.

### Before you finish: what didn't the format handle?

The claim at the top of this file — that the second pass is much better than the
first — is only true if the first one leaves a record. So close by asking
yourself, and telling the operator, in three or four lines:

- What source turned out to be worth more, or less, than its position in §1?
- What did you have to invent because no file specified it?
- Where did the procedure and the project actually disagree?

Then offer to fold it back into this skill. An adoption pass that improves the
skill has done two projects' work; one that doesn't has to be rediscovered from
scratch on the next repo.

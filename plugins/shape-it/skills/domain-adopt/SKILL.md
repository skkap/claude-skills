---
name: domain-adopt
description: "Seed a project's DOMAIN.md and docs/decisions/ from vocabulary already scattered through its CLAUDE.md, README, decision logs and documents — a one-off adoption pass that explores, proposes a candidate model, asks about the conflicts, writes, reports, and ends by listing everything in the project the model has just made wrong — variable and file names, documentation, prompts, published copy — as a backlog, never as a rename. Cuts a large project into one round per area rather than one pass. INVOKE ONLY WHEN EXPLICITLY ASKED: the operator says adopt, seed, bootstrap or set up a domain model for a project. Never start one as a side-effect of other work — it is a documentation session that rewrites CLAUDE.md, and it displaces whatever the operator actually asked for. For ongoing model maintenance during normal work, use the `domain` skill instead."
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

**One project per pass — and on a large project, one *area* per round.**
Rolling out across several projects is several passes, and the second is much
better than the first, because the first will have found what the format does not
yet handle. Which only helps if you write that down — see [§6](#6-report). Where
one project is itself too big for a sitting, the cut is by area and the mechanism
is [When the project is large](#when-the-project-is-large).

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

Six steps, in order. **Nothing is written until step 4, and nothing is
*renamed* at any point** — step 5 produces a list, not a diff.

| | |
|---|---|
| **1. Explore** | Survey the project and harvest candidates |
| **2. Propose** | Show the candidate model — before touching a file |
| **3. Ask** | One batched round on the conflicts and the expensive gaps — *before writing* |
| **4. Write** | `DOMAIN.md`, `docs/decisions/`, and the moves out of `CLAUDE.md` and out of whatever writes |
| **5. Align** | List what the model has just made wrong — names, files, docs, copy — sorted by what each costs to change |
| **6. Report** | What was written, what has to change, what disagrees with what ships, what is open |

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

## When the project is large

The six steps assume one sitting, and that holds to roughly forty candidate
terms. Past it three things fail at once: the proposal outgrows a screen, the
question round reaches maybe eight of twenty conflicts, and everything it cannot
reach lands in `## Open questions` — which at this size is not a queue, it is a
graveyard.

The pass does not get longer. It gets **cut**, and the unit of work stops being
one project and becomes **one area**.

| Round | What | Written |
|---|---|---|
| **0** | Cut into areas, then census | the ledger, and nothing in the project |
| **1…n** | §1–§4 and §6, one area per round | that area's `DOMAIN.md` and decisions |
| **n+1** | Reconcile across areas | `DOMAIN-MAP.md`, `## Between areas` |
| **n+2** | §5 — align | `docs/domain-alignment.md` |

**Every cap in this file is per round, not per pass.** Ten to thirty terms, four
questions, one screen of proposal — all correct for one area and all absurd
applied to a project with five. A round that ends having written one area's
vocabulary has succeeded; the next round is a fresh budget.

### Round 0 — cut, then census

**Decide the shape first.** On a small project, whether the model is one
`DOMAIN.md` or a `DOMAIN-MAP.md` plus per-area files is a footnote at the bottom
of the proposal. Here it is the first decision, because it is what the rounds are
cut along — and discovering in round four that two earlier rounds were describing
the same area is a rewrite of both.

Cut along what the material is already organised by: the top-level directories,
the folders of documents, the teams. Not along what would make a tidy diagram. If
the project's own layout does not suggest a cut, that is the answer — it is one
area and it is merely long.

**Then census, before defining anything.** This is the artefact that makes a
large pass cheaper than n small ones, and it is the only new mechanism at scale:
a table of every candidate term against every surface it appears on, with counts.

| surface | in a codebase | in a records project |
|---|---|---|
| **agent-facing** | prompts, skill files, agent templates, briefing docs | the same |
| **working prose** | docs, comments, commit messages, task notes | notes, memos, internal letters |
| **private names** | locals, test names, internal helpers | draft filenames, working sheets |
| **shared names** | exported symbols, types, files, directories, components, routes | document titles, folder names, form fields |
| **registry** | the enum, `const` array, schema or column that actually ships | the filing, the register, the accounting system |
| **published** | UI strings, i18n keys, public API fields, printed copy | filings, letters, contracts, anything sent |

```
term          agent  prose  private  shared  registry  published   verdict
project         6      44      31      12       —          9       ⚠️ vs Block
engagement      2      17       4       3       —          —       ⚠️ 2 readings
deliverable     3      21       8      14       1          4       ✅
handover        —       9       —       2       —          1       ✅
```

**Rank by spread, not by count.** A term appearing two hundred times inside one
module is that module's business. A term appearing thirty times across the
schema, the published copy and two prompts is the project's vocabulary — and it
is the one quietly carrying two meanings, because each surface acquired its
reading separately. Spread is the conflict signal; raw frequency is not.

The census is also what §5 is computed from. Build it once: the same six surfaces
sort two ways — by *where the word appears*, which is this table, and by *what it
costs to change it*, which is the alignment list. A second sweep at the end is
wasted work and will disagree with the first.

### Round n+1 — reconcile across areas

Only possible once every area's file is written, and it is where the most
valuable finding of the whole pass lives: **a headword that appears in two areas'
`DOMAIN.md` with two definitions.** No round can see that from the inside, which
is exactly why one word carrying two meanings survives in large projects for
years.

Diff the headwords. For every term in more than one area, `DOMAIN-MAP.md`'s
`## Between areas` gets the two questions `DOMAIN-FORMAT.md` names — who owns it,
and which side is upstream — answered from what the files actually say rather
than from what the layout suggests. Where the two definitions cannot both stand,
that is a ⚠️ and a question, not a merge you perform.

### Two working files, and only one belongs to the project

- **The ledger** — the area cut, the sources already swept, the census, each
  candidate's verdict, and each round's proposal file. It is scaffolding: it
  exists so round four does not re-harvest what round one already rejected, and
  it is worthless afterwards. It goes **outside the repository**, at
  `~/.local/share/domain-adopt/<repo>/`, for the same reason a plan does — a pass
  that spans a week should not put a week of its own bookkeeping in someone's
  `git status`.
- **`docs/domain-alignment.md`** — the output of §5. This one is the deliverable,
  other people and other sessions drain it, so it lives in the project.

Neither is needed on a small project. One sitting, six steps, no ledger.

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
names are the vocabulary that actually shipped. Widen it past the schema —
exported symbols and type names, component and directory names, route segments,
i18n keys, CLI flags, error codes, test fixture names. Every one of those is a
word somebody committed to, and the same inventory is what §5 is computed
against, so gather it once.

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

### Past about forty candidates, the proposal is a file

The compression above buys perhaps threefold, and then the screen runs out.
Beyond that, write the round's proposal to a markdown file, say where it is, and
hand back the turn — the operator reviews it in their own editor, term by term,
marking the ones they disagree with. It is the same content and the same
markers; only the medium changes, because a ninety-line proposal pasted into a
conversation is one that gets skimmed to the bottom and approved wholesale, which
is the failure this step exists to prevent.

The file is scaffolding, so it goes beside the ledger, outside the repository.
What comes back from it feeds §3: the terms they marked are the question round,
and the ones they did not are settled.

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

**And it is four questions per *round*, not per project.** On a project cut into
five areas that is five separate budgets spent five different weeks, which is the
whole reason for the cut — four questions spread across ninety terms would leave
the model unreviewed, and asking twenty in one sitting is the interview this step
is about to warn you off.

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

**Definitions only, here.** A prompt that also *uses* the wrong word in its
instructions is a §5 row, not a §4 edit — leave the word where it is for now, so
the two steps do not each half-fix the same file and leave neither auditable.

⚠️ **Check what the test suite pins into those files before deleting anything.**
Prompts are sometimes guarded by parity tests asserting they contain particular
lists or definitions, and finding that out after the deletion means a broken
build and a confusing diff. Where a test pins content you were about to move,
leave it, and say so in the report — a passing guard is worth more than a tidier
prompt.

---

## 5. Align — list what has to change; change nothing

The model now says **Block**, and the material says *project* in ninety places.
Those ninety places are the reason writing the model was worth doing, and acting
on them here is the fastest way to waste it: an adoption session that ends in a
four-hundred-file rename is a diff nobody reviews, attached to a model nobody
agreed to yet.

> **This step produces a list. It does not produce a diff.**

That is what makes it safe to keep inside the adoption pass rather than in a
session of its own. The list is drained later, by ordinary work, at whatever pace
the project can absorb — and it is **re-runnable**: every later `domain` session
that adds an `_Avoid_` line makes a few more rows, and regenerating the file is a
query, not a pass.

**It is a join, not a sweep.** The input is exactly two things — every `_Avoid_`
word in the model, and every headword the pass *renamed* — matched against the
census from round 0, or against a grep per word where the pass was small enough
not to need one. A word nobody rejected is not debt, however untidy it looks. §5
is not a general tidy-up and must not become one.

Distinct from §4, which is easy to confuse with it: §4 deletes **definitions**
from the files that carry them. §5 lists **wrong words**, everywhere, including
in those same files.

### Sort by blast radius, not by folder

The census's six surfaces, re-sorted by what changing one costs. This ordering is
the whole content of the step.

| # | Radius | Surfaces | What it costs | Default |
|---|---|---|---|---|
| **0** | Agent-facing | prompts, skill files, templates, briefing docs | nothing — edit the file | **rename** |
| **1** | Free | comments, task notes, internal docs, locals, test names | mechanical, one commit | **rename** |
| **2** | Internal contract | exported symbols, types, files, directories, components, i18n keys | compiles-or-fails; one commit per module | **rename** |
| **3** | Persisted | columns, enum values, stored JSON keys, record filenames, filings | migration and backfill | **decide** |
| **4** | Published | public API fields, routes, UI copy, printed documents, letters | breaks consumers | **leave** |

**Radius 0 is first because it is free and it is the one doing damage.** §4
already carries the evidence: a shipped data bug whose cause was a definition
living only in a UI description string, read by an extraction agent that then
mis-filed every record that did not match it. A stale `CLAUDE.md` misleads a
reader who can push back; a stale prompt writes wrong data at scale, silently,
and it is a one-line fix. Anything that puts it last has the economics backwards.

**Radius 4 is opt-in and its default is *leave*.** Published output is touched
only where the entry's `_Avoid_` line says *"in published copy too"* — the reach
rule in `DOMAIN-FORMAT.md`, doing precisely the job it was written for. A word
ambiguous across a whole project is usually unambiguous on the one page a reader
meets it, and rewriting good copy to settle an internal disambiguation problem
the reader does not have is how this discipline gets a bad name.

**Radius 3 and 4 rows that resolve to *no* earn a decision record.** *"The
`project_id` column keeps its name"* is a real decision — hard to reverse in the
sense that matters, weighed against a real alternative, and guaranteed to be
proposed again every year by someone who read `DOMAIN.md` and not the column. The
deliberate-no shape is in `DECISION-FORMAT.md`; the recurrence test is met by
construction here.

### The file

```md
# Domain alignment — Acme

Generated 2026-08-24 from DOMAIN.md. Drain it and delete it.
Radius 0–2 are cleanup. Radius 3–4 are decisions; do not act on them unasked.

## 0 · Agent-facing

- [ ] **Block** ← `engagement` · `prompts/extract.md`, `.claude/agents/filer.md` · 6
- [ ] **Deliverable** ← `artifact` · `prompts/review.md` · 3

## 2 · Internal contract

- [ ] **Block** ← `project` · `src/scheduling/` — 12 exports, 4 filenames, `ProjectCard.tsx` · 41
      Splits into two commits: the rename, then `ProjectCard` → `BlockCard`.
- [ ] **Rate** ← `price` · `src/billing/rates.ts` · 7

## 4 · Published — leave unless stated

- [x] **Block** ← `project` · 9 UI strings, `en.json` · **leave**
      `_Avoid_` binds working language only; "Project" is what the client calls
      their own thing and reads correctly on the page.
- [ ] **Sento** ← `not-onsen` phrasing · `about.html`, the printed leaflet · 2
      Entry binds published copy too — this one is a factual error, not a
      preference.
```

Four things every row carries, and it is unusable missing any of them:

- **The count.** A six-occurrence rename and a six-hundred-occurrence rename are
  different proposals. A backlog without counts gets estimated wrong every time
  somebody looks at it.
- **The locations**, concretely enough to start from — a directory and a shape,
  not "throughout the codebase".
- **The action**, chosen, not left open: rename, leave, or defer. A row with no
  action is a question, and questions belong in `## Open questions`.
- **A reason on every *leave*.** This is the one people skip and the one that
  decides whether the file is read twice. A bare `leave` gets re-litigated by the
  next person who opens `DOMAIN.md`, and they will reach a different answer,
  because you did not tell them why.

### Offer the guard; do not install it

Once radius 0–2 are drained, two checks stop the list regenerating:

- a test that fails when an `_Avoid_` word appears in working language, and
- a parity test per `_Kinds_` line, asserting the closed set in the model still
  matches the registry that ships it.

Both are worth having and neither is yours to add unasked — §3 already puts that
trade to the operator, and it is the same trade here with a number attached: the
guard cannot go green until the list above is drained, so proposing it while
radius 1 is still full is proposing a red build. Offer it in §6 as the thing that
follows the cleanup, not as part of it.

### Finished means empty and deleted

`docs/domain-alignment.md` is a queue. A half-drained one left in `docs/` for a
year is another copy of the vocabulary, freshly wrong, and that is the exact
condition this whole pass exists to end. When the rows are gone the file goes;
if the project tracks work elsewhere, move the radius 2+ rows there on day one
and keep only what is not yet dispatched.

---

## 6. Report

Same markers, one screen:

```
✅ Written
   DOMAIN.md            14 entries, 3 relationships, 2 rules
   docs/decisions/      6 records, 0001–0006, converted from DECISIONS.md
                        dated from git history, 2024-03 → 2025-11
   CLAUDE.md            parameters table removed, one-line pointer left
   prompts/extract.md   feature definitions removed, cites DOMAIN.md
   docs/domain-alignment.md
                        38 rows, nothing renamed — 6 radius 0 (prompts and
                        agent files: free, and the ones doing damage),
                        11 radius 1, 19 radius 2, 2 radius 4 both left
                        with reasons

⚠️ Found disagreeing with what actually ships — 3
   CLAUDE.md listed 6 categories; the export has 3 (stale since the restructure)
   "Engagement" is the folder name and the wrong reading of the word
   two spellings of the same term on adjacent pages

❓ Open — 4, parked in DOMAIN.md § Open questions
   Matter vs Engagement after the rename
   Whether Pickup is a kind of Shipment or its own entry
   …

❓ For you — should the model be enforced?
   An `_Avoid_` check plus a `_Kinds_` parity test, once radius 0–2 are
   drained. Real churn, and the only thing that stops the list regrowing.

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

**Say plainly that nothing was renamed.** The alignment list is the one part of
this report that reads like work already done, and it is not — it is work now
visible. An operator who believes the rename happened will find out from a grep
in three weeks.

**The list stays inside `✅ Written`, and the guard is a `❓`.** No new glyph for
"needs changing" — `docs/domain-alignment.md` is a file this pass wrote, which is
what `✅` means here, and whether to enforce the model is a question, which is
what `❓` means. A fifth marker would turn two axes back into one ranked list.

Then stop. The model is now something a session can read, and the project has a
list of where it disagrees with itself. Neither of those also needs to be
finished today.

### Before you finish: what didn't the format handle?

The claim at the top of this file — that the second pass is much better than the
first — is only true if the first one leaves a record. So close by asking
yourself, and telling the operator, in three or four lines:

- What source turned out to be worth more, or less, than its position in §1?
- Which radius in §5 was fullest, and was the ordering right for this project?
- What did you have to invent because no file specified it?
- Where did the procedure and the project actually disagree?

Then offer to fold it back into this skill. An adoption pass that improves the
skill has done two projects' work; one that doesn't has to be rediscovered from
scratch on the next repo.

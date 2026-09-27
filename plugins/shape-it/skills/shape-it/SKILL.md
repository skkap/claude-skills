---
name: shape-it
description: Plan a piece of work by investigating the project first, stating in plain words what the work is and what it costs to skip, then deciding everything the project can already answer and asking only the decisions that are expensive to reverse — data models, public surfaces, vocabulary, scope boundaries, UI shape, business rules. Works on a codebase or on a project made of documents and records. Reads the project's domain model and decision records so a settled term is never re-asked, and writes the answers back to them. Uses batched multiple-choice questions rather than open dialogue, then writes the plan to a markdown file — or onto the ticket, where the repo's instructions keep plans in a tracker — prints it in full, and ends with one question: implement here, open it in Plannotator, or hand it to land-it. Use when asked to plan a feature, think through an approach, scope work before building, or figure out what to build. Does not enter plan mode, and implements only when that is chosen at the end.
---

# shape-it — decide the obvious, ask what is expensive

Planning goes wrong in two directions. An agent that asks nothing builds the
wrong thing confidently. An agent that asks everything makes the operator do the
thinking they delegated — and asks half of it about things the repository already
answers.

> **Ask only what the repo cannot answer AND is expensive to get wrong.
> Decide everything else, and say what you decided.**

Both halves matter. The first keeps the questions few. The second keeps the
silent decisions auditable, which is what makes deciding freely safe.

And a third thing, which is what stops the same question being expensive twice:
**an answer that will matter again outlives the plan.** Vocabulary goes to
`DOMAIN.md`, hard-to-reverse choices go to `docs/decisions/`. Anything left only
in the plan has to be re-asked the next time someone touches this area.

| | file |
|---|---|
| The procedure | **this file** |
| `DOMAIN.md` / `DOMAIN-MAP.md` structure, decision record format | the **`domain`** skill |

## When this runs

The operator wants a piece of work thought through before anything is built.
They are **not** asking for plan mode and not asking for code — this produces a
written plan and stops.

Most often that piece of work is a feature in a codebase, and the examples below
assume one. It works the same on a project made of documents and records, where
the expensive-to-reverse decisions are filings, instruments and counterparties
rather than schemas and routes.

Not for: a one-line fix, a task whose shape is already settled, or work where the
operator has already told you the approach. Planning something obvious is its own
kind of waste.

---

## 1. Investigate before asking anything

**A question the project could have answered is a tax on the operator.** Most of
what feels like a design question has already been decided somewhere in the repo,
and the decision is usually load-bearing.

Read, in this order:

- **The thing itself** — the task file, the issue, the sentence they typed.
- **`DOMAIN.md`** — or `DOMAIN-MAP.md`, then the areas it points at. This is the
  project's vocabulary, its kinds, its relationships and its invariants, and it
  is the cheapest file in the repo to read. **A term defined here is a citation,
  not a question.**
- **`docs/decisions/`** — root and per-area. Titles alone are often enough; read
  the bodies of the two or three that touch this work. A decision already
  recorded removes that fork from the list.
- **`CLAUDE.md` / `AGENTS.md`**, and any path-scoped rules (`.claude/rules/`,
  nested `CLAUDE.md`). These are normative. A plan that contradicts one is wrong
  even if it works.
- **The nearest existing thing.** In a codebase: the schema, the API surface, the
  feature closest to this one. In a records project: the last time something like
  this was done, and what it produced. The closest neighbour is the strongest
  signal — if the project already does something similar, the shape of the new
  thing is mostly decided.
- **Prose buried in the material.** Comments that argue for a constraint, a note
  in a status file explaining why the obvious route was not taken. These are the
  ones nobody thinks to grep for, and they often pre-empt the exact question you
  were about to ask.

No `DOMAIN.md` and no `docs/decisions/`? Note it and carry on — do not stop to
propose writing them. That offer belongs at the end (§6), when you know what
would go in.

Come out of this able to say what already exists, what it constrains, and where
the genuine forks are.

---

## 2. Sort every open decision

Two axes, and both must point the same way before you ask.

|  | repo answers it | repo cannot answer it |
|---|---|---|
| **cheap to change** | decide | decide, note it |
| **expensive to change** | decide, cite the precedent | **ask** |

### Ask about these

- **Vocabulary.** What a thing is, what it is called, what kinds it comes in, how
  it relates to what already exists. Words leak into the schema, the API, the UI
  and the operator's own head at once, and renaming later touches all four.
- **Data model and schema.** Migrations are forward-only in most repos, and data
  written under the wrong shape outlives the decision that shaped it.
- **Public surface.** Route paths, event names, CLI flags, published API fields.
  Once something consumes them, changing them breaks the consumer.
- **Architecture and technology with lock-in.** Sync or async, one service or
  two, which library owns a concern. Not every dependency — the ones that would
  take a quarter to swap.
- **Scope boundaries.** Which half of the task is in, which is deferred. Silence
  about the expensive half reads as permission.
- **UI shape** where the repo has no precedent — one panel or two, a new page or
  a section. Cheap in code, expensive in habit once people learn it.
- **Business and domain rules.** Who may see what, what counts as done, what is
  billable, what the regulator requires. These are not in the code and you cannot
  derive them. When they are unclear, the cheapest way to get them is not a
  question but a narration: *"walk me through the last real one, start to
  finish."* Rules arrive as the exceptions people mention in passing, never as
  answers to "what are the rules?"

### Decide these yourself

- Anything the repo already demonstrates — file layout, naming, error handling,
  test framework, whether a helper gets extracted.
- Implementation detail no user will ever observe.
- Anything with a conventional default and a cheap reversal.
- Anything where you would be guessing equally either way **and** it is cheap to
  change. Guessing is fine when wrong is cheap; that is what "obvious" means here.

**A decision is not expensive because it is hard.** It is expensive because it is
hard to *undo*. A tricky algorithm behind a stable interface is cheap. A column
name in a shipped table is not.

### Before any question goes in the picker

A question must pass all three:

1. **Neither the project nor the input answers it** — not the code, not the
   ticket, not a record of an earlier decision.
2. **Getting it wrong means rework after the build** — a name or wording people
   will read, a business rule, a UI shape, a data shape, a public surface. A call
   that one later message could reverse for free does not qualify.
3. **You have no default you would defend.** If you would recommend an option and
   stand behind it, that is not a question — it is a decision. Make it, and list
   it under *Decided without asking*, where overturning it costs the operator one
   line.

**Zero questions is a normal outcome**, and for well-specified work the usual
one. A question round exists for real forks, not to show that forks were looked
for.

---

## 3. Say what this is, in plain words, before asking anything

Investigation has given you a picture the operator cannot see. State it back
before spending any of their attention on questions — **five short lines, no
jargon, readable by someone who has never opened this project.**

This is a checkpoint, not a preamble. If your understanding is wrong, every
question after it is wrong too, and this is the cheapest possible moment to find
out. It costs one screen and it is the only place a misread gets caught before
it is baked into a plan.

```
**Shipment splitting** — an order that is too large for one van currently fails
at checkout instead of going out in two.

Why now      Support is refunding roughly one order a week over this, and each
             one is a customer who tried to give us money and could not.
Effect       Large orders complete. Customers see two deliveries and two
             tracking numbers where they used to see an error.
If we don't  The failure stays silent — nothing logs it as a lost sale, so it
             will keep costing about that much indefinitely.
Ahead        4 questions: what a split order is called, whether the two halves
             can be cancelled separately, one API shape, one scope boundary.
```

| Line | What it must answer |
|---|---|
| **the opening sentence** | What this is, as you would say it to someone outside the project |
| **Why now** | What is actually wrong or wanted — the pressure behind it, not a restatement of the request |
| **Effect** | What changes, and for whom, once it is done |
| **If we don't** | What it costs to leave it alone. Often the most useful line on the screen |
| **Ahead** | How many questions are coming and what they are about |

Four things keep it honest:

- **Derive it, do not echo it.** Repeating the request back proves nothing. The
  value is in what the reading added — *"support refunds one a week"*, *"nothing
  logs it"*, *"the schema already has a `parent_order_id` nobody uses"*. If the
  five lines contain nothing the operator did not already type, you have not
  finished §1.
- **Plain words.** No file paths, no class names, no internal shorthand. If a
  term is genuinely load-bearing, it is a `DOMAIN.md` entry and you gloss it in
  four words. A framing only the team can read cannot be checked by anyone else,
  and cannot be pasted to a stakeholder.
- **For a bug, "why" is the failure, not the defect.** Not *"the total is
  computed twice"* but *"customers are charged twice and we refund it by hand"*.
  A bug that costs nothing is worth saying so about — that is a real answer, and
  it is how a plan gets cancelled before it is written.
- **Say the number and stand by it.** "Ahead: 4 questions" tells the operator
  what they are committing to before they start. It is also a promise: if the
  answers open a genuinely new fork you may ask a second round (§5), but the
  count is not a first guess to be quietly revised upward.

**If nothing passes the test in §2, say so and keep going.** The *Ahead* line
reads "no questions", and the plan follows in the same response. Do not stop to
have the five lines confirmed — they open the plan, where a misread is just as
visible and costs one message to correct.

---

## 4. Type each question by where its answer lands

Two of the things you ask about will still matter long after this feature ships,
and each has a home. Tag those questions; the tag is not decoration, it is the
destination.

| | Type | The question | Lands in |
|---|---|---|---|
| 📖 | **Domain** | What is this thing, what do we call it, what kinds are there, how does it relate to what exists, what is always true of it | `DOMAIN.md` |
| ⚖️ | **Decision** | Architecture, data model, public surface, lock-in — technology, counterparty or legal — and deliberate no-s | `docs/decisions/` |
| | *(untyped)* | Everything else — UI shape, ordering, scope trims inside this piece of work | the plan only |

The tag goes in the question's `header` (`📖 Domain`, `⚖️ Decision`), so the
operator can see at a glance that they are being asked about *the business* and
not about *the build* — and vice versa. Conflating those two is what produces
answers that sound decisive and settle nothing.

These two are the *destination* axis of the marker set the **`domain`** skill
defines. The other axis says what is needed from the operator — ✅ nothing,
⚠️ your attention, ❓ your answer — and the two combine: a `⚖️ ❓` is a fork you
are asking them to pick, a `⚖️ ✅` is one an existing record already settled. The
same set is used in ordinary prose throughout planning, not only in the picker.
In particular: mark
📖 the first time you use a term because `DOMAIN.md` defines it, ✅ when a
question turns out to be already answered by an entry or a record, and ⚠️ the
moment a word in play conflicts with one in the model. Those markers are what
make it visible that the plan is being built out of the project's own language
rather than a private one. The full rules, including when *not* to mark, are in
the `domain` skill.

**Ask 📖 before ⚖️.** You cannot sensibly ask how a thing should be stored before
agreeing what the thing is, and a domain answer routinely dissolves a technical
question that looked open. If both types are live, put the domain questions in
the first round.

An untyped question is not a lesser question — most rounds are mostly untyped.
It only means the answer's home is the plan.

---

## 5. Ask — batched, concrete, opinionated

Use `AskUserQuestion`. Not open dialogue: the operator picks rather than composes.

**One round of up to four questions.** Two rounds if the answers genuinely open a
new fork. Never more — past that it is an interview, and they delegated this to
avoid one.

**Lead with your recommendation** and mark it. You did the reading; say what you
would do. A neutral menu hands the thinking back.

**Every option states its consequence, not its name.** The label is what to call
it; the description is what happens if they pick it.

> ✗ `relates + duplicates`
> ✓ `relates + duplicates` — *two more enum values, no new tables. `/queue` must
> learn to ignore the new kinds, and the public API's `kind` field gains values
> existing clients have not seen.*

**Use previews for anything with a shape.** Schema fragments, API responses, UI
layouts, config. A decision about structure is much easier to make when the
structure is on screen. Previews are single-select only.

**Do not ask what you already know.** If the reading settled it, it is not a
question — it is a line in the plan.

### Then go straight to the plan

When the answers come back, write the plan. **No confirmation round** — no "anything
to correct or add?". The plan's *Decisions* section restates each answer in your
own words, one line each, and that is where a misread surfaces; a correction is
one message against a document, not a turn spent before it exists.

A second round is still allowed, but only when an answer opened a fork that
passes §2's test on its own.

---

## 6. Write the plan, then persist what outlives it

A document, not a conversation. It should be enough for someone else — or a
dispatched agent — to build from.

```markdown
# <feature>

## What this is
<The five lines from §3, as agreed — what it is, why now, effect, if we don't,
and what was asked. Not rewritten: they were checked with the operator before a
single question was asked, so they are the one part of this document already
known to be right.>

## Decisions
<Each answered question, and what was chosen. One line each. Mark the 📖 and ⚖️
ones with where the answer was written.>

## Decided without asking
<The calls made alone, with the precedent or the reason. This is the audit
list — short, but the operator must be able to catch a wrong "obvious".>

## Approach
<The shape of the work. Files, layers, order. What existing thing it follows.>

## Out of scope
<What was deliberately deferred, and why — so the omission reads as a decision.>

## Risks and unknowns
<What could still be wrong, and what would reveal it.>
```

**"Decided without asking" is not optional.** It is the price of being allowed to
decide freely. Keep it to the decisions that could plausibly have gone the other
way — not every naming choice.

Then place the typed answers:

- **📖 Domain answers → `DOMAIN.md`.** If the file exists, write them in now,
  following the `domain` skill's format. If it does not, list the terms the
  session settled and offer to start the file — **at the end, having done the
  work, never as a precondition for starting it.**
- **⚖️ Decision answers → `docs/decisions/`,** for the ones that clear the
  gate: hard to reverse, and a real trade-off with genuine alternatives.
  A decision that fails the gate stays in the plan and that is correct. The
  deliberate no-s from *Out of scope* are candidates too, on a recurrence test
  rather than a reversibility one — the ones that have come up before, or that a
  reasonable person would expect and be surprised to find missing. Not routine
  trimming.

Every decision record carries a `date:`. It is not optional; a decision is an
answer to the constraints in force when it was made.

Load the **`domain`** skill for either. Do not improvise the formats — a
`DOMAIN.md` written to a private shape is worse than none, because the next
session will read it and copy it.

If the answers contradicted something already in `DOMAIN.md` or an existing
decision record, that is not a silent overwrite: say what changed, and supersede
rather than edit.

---

---

## 7. Deliver it

### When the work is a ticket, the repo says where the plan goes

When the input names a ticket, or the repo's instructions (`AGENTS.md`,
`CLAUDE.md`) say its work is tracked as tickets, **those instructions decide**
where the plan lives and what happens to the ticket while it is being shaped —
they name the tracker, its commands, and the state a ticket takes during
planning. This skill names no tracker; do what they say, at the moment they say
it. What holds for any tracker:

- **Which ticket.** The one the input names. If it names none and the repo files
  work as tickets, search the tracker for the same work first, then file one with
  a specific title and the five lines as its description, and name any near-miss
  in your report. Never write the plan onto a ticket the input did not name —
  it replaces whatever plan that ticket had.
- **Acceptance criteria**, when the ticket has none: the criteria the plan
  implies — concrete, checkable, one line each. When it already has some, never
  replace them; if the plan disagrees with them, say so.
- **Never edit an existing description.**
- Keep a working copy at `~/.local/share/shape-it/<repo>/<slug>.md` — it is what
  Plannotator annotates — but report the **ticket and its URL** as where the
  plan lives.

When the repo's instructions say nothing about tickets, the plan is a file.

### Everywhere else, a file

**Never create a directory inside a repository to hold it.** Resolve in order:
an existing plans directory (`docs/plans/`, `plans/`, `.plans/`); a path the
operator named; otherwise `~/.local/share/shape-it/<repo>/<slug>.md`. Say the
full path, so it can be moved in one command if they want it committed. A plan
turning up unbidden in someone else's `git status` is its own small failure.

### Print it

Say where the plan lives — the path, or the ticket and its URL — then **print the
whole plan in your reply**. Not a summary, not the headings: the same text that
was written. The stored copy is what survives; the printed one is what actually
gets read in the next thirty seconds, and a plan nobody reads is a plan nobody
corrects.

### Then one question: what next

End with a single `AskUserQuestion`, recommendation first:

| Option | What happens when it is picked |
|---|---|
| **Implement here** | Build it in this session, following the plan. Usually the right default for work small enough to finish in one sitting. |
| **Open in Plannotator** | `plannotator annotate <working copy>`. Apply each annotation, say what changed, and write the revised plan back wherever it lives (the ticket, when it lives on one). Offer it only when `command -v plannotator` finds it. |
| **Start implementation with land-it** | Invoke `land-it` with the plan's path or the ticket, saying the plan was just approved here. It skips its own planning and its "Proceed?" and runs to a draft PR. Recommend it for ticket-sized work in a repo with a PR flow. |

**Skip the question when `land-it` invoked you** — it says so when it hands over,
and its gate is the handoff.

Anything the operator types instead of picking is a correction: apply it to the
plan (file and task), say what changed, and print only the sections that moved.

`DOMAIN.md` and `docs/decisions/` entries were already written in §6 as the
answers settled — they are the project's files, and a correction that changes a
term or a fork updates them too. Say so when it does.

---

## Guardrails

- **Do not enter plan mode.** This produces a plan, then asks one question.
- **Do not implement before the closing question**, and do not start "just the
  obvious part". Building starts only when it is chosen there.
- **Never ask a question that fails §2's test**, and never a confirmation round.
- **Do not ask more than two rounds.** If the picture is still unclear, say what
  is unclear and why, rather than continuing to interrogate.
- **Never ask what the project answers** — including `DOMAIN.md` and the decision
  records. If you find yourself asking about a convention or a term, you have not
  read enough.
- **Cite the project when you decide.** "Following `entry.status`" is checkable;
  "seemed natural" is not.
- **Never turn planning into documentation work.** Offering to write `DOMAIN.md`
  before the plan exists trades the thing they asked for against a thing they
  did not.

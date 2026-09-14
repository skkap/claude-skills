---
name: shape-it-lite
description: Plan a piece of work by investigating the project first, saying in plain words what it is and what skipping it costs, then asking only the decisions that are expensive to reverse — and finishing with a markdown plan written to a file — or onto the task, in a repo tracked in Zumino — printed in full, then one question: implement here, open it in Plannotator, or hand it to land-it. The stripped-down sibling of `shape-it`, for projects with no DOMAIN.md and no docs/decisions/ — it reads no domain model, writes none, and everything it settles lives in the plan. Use when asked to plan a feature, scope work before building, or think an approach through in a repo that carries no vocabulary or decision files, or one you cannot add them to. Does not enter plan mode, and implements only when that is chosen at the end.
---

# shape-it-lite — the questions and the plan, nothing else

Everything `shape-it` does, minus the half that assumes a project keeps a written
vocabulary and a decision log. Same reading, same reversibility test, same
batched questions. What is gone is the ◆/⚖️ typing, `DOMAIN.md`, and
`docs/decisions/` — and what is added is the ending: the plan is written to a
file and opened for you to mark up.

> **Ask only what the project cannot answer AND is expensive to get wrong.
> Decide everything else, and say what you decided.**

| | file |
|---|---|
| The procedure | **this file** |
| The full version, for a project with a domain model | the **`shape-it`** skill |

## When this runs, and when it does not

Use this when the project has **no `DOMAIN.md` and no `docs/decisions/`** — most
repos — or when it is not yours to add them to: a client's repository, someone
else's open-source project, anything where a vocabulary file would need six
other people to agree first.

Use **`shape-it`** instead when those files exist. Reading them is most of its
value, and skipping a `DOMAIN.md` that is sitting right there means re-asking
questions the project already answered in writing.

**Know what you are giving up.** Every answer here lives in one plan document.
The next person to touch this area will not find the vocabulary you settled or
the fork you resolved, and will ask again — possibly answering differently. That
is the correct trade for a repo you do not own. It is a bad trade for one you do,
and if you find yourself running this repeatedly on the same project, that
project wants `shape-it` and a `DOMAIN.md`.

Not for: a one-line fix, a task whose shape is settled, or work where the
approach has already been given. Planning something obvious is its own waste.

---

## 1. Investigate before asking anything

**A question the project could have answered is a tax on the operator.** Most of
what feels like a design question was decided somewhere in the repo already, and
the decision is usually load-bearing.

Read, in this order:

- **The thing itself** — the task file, the issue, the sentence they typed.
- **`CLAUDE.md` / `AGENTS.md` / `CONTRIBUTING.md`**, and any path-scoped rules.
  These are normative. A plan that contradicts one is wrong even if it works.
- **The nearest existing thing.** The schema, the API surface, the feature
  closest to this one. The closest neighbour is the strongest signal: if the
  project already does something similar, the shape of the new thing is mostly
  decided.
- **The README and any `docs/`.** In a project with no domain file, the
  vocabulary is here or nowhere — and the words it already uses are the words
  your plan should use.
- **Prose buried in the code.** Comments arguing for a constraint are the ones
  nobody greps for, and they often pre-empt the exact question you were about to
  ask.

Come out of this able to say what exists, what it constrains, and where the
genuine forks are.

---

## 2. Sort every open decision

Two axes, and both must point the same way before you ask.

|  | project answers it | project cannot answer it |
|---|---|---|
| **cheap to change** | decide | decide, note it |
| **expensive to change** | decide, cite the precedent | **ask** |

### Ask about these

- **Vocabulary.** What a thing is called. Words leak into the schema, the API and
  the UI at once, and renaming later touches all three. With no `DOMAIN.md` to
  check, the existing code and docs are your only precedent — use them.
- **Data model and schema.** Migrations are forward-only in most projects, and
  data written under the wrong shape outlives the decision that shaped it.
- **Public surface.** Route paths, event names, CLI flags, published fields.
  Once something consumes them, changing them breaks the consumer.
- **Architecture and technology with lock-in.** Not every dependency — the ones
  that would take a quarter to swap.
- **Scope boundaries.** Which half is in, which is deferred. Silence about the
  expensive half reads as permission.
- **UI shape** where there is no precedent. Cheap in code, expensive in habit
  once people learn it.
- **Business rules.** Who may see what, what counts as done, what is billable.
  These are not in the code and you cannot derive them.

### Decide these yourself

- Anything the project already demonstrates — file layout, naming, error
  handling, test framework, whether a helper gets extracted.
- Implementation detail no user will observe.
- Anything with a conventional default and a cheap reversal.
- Anything where you would be guessing equally either way **and** it is cheap to
  change. Guessing is fine when wrong is cheap.

**A decision is not expensive because it is hard.** It is expensive because it is
hard to *undo*. A tricky algorithm behind a stable interface is cheap. A column
name in a shipped table is not.

### Before any question goes in the picker

A question must pass all three:

1. **Neither the project nor the input answers it** — not the code, not the
   ticket, not a comment explaining an earlier choice.
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

A checkpoint, not a preamble. If your understanding is wrong, every question
after it is wrong too, and this is the cheapest moment to find out.

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

- **Derive it, do not echo it.** Repeating the request back proves nothing. If
  the five lines contain nothing the operator did not already type, §1 is not
  finished.
- **Plain words.** No file paths, no class names, no internal shorthand. A
  framing only the team can read cannot be checked by anyone else.
- **For a bug, "why" is the failure, not the defect.** Not *"the total is
  computed twice"* but *"customers are charged twice and we refund it by hand"*.
  A bug that costs nothing is worth saying so about — that is how a plan gets
  cancelled before it is written.
- **Say the number and stand by it.** It tells the operator what they are
  committing to. A second round is allowed if the answers open a genuinely new
  fork; the count is not a first guess to be quietly revised upward.

**If nothing passes the test in §2, say so and keep going.** The *Ahead* line
reads "no questions", and the plan follows in the same response. Do not stop to
have the five lines confirmed — they open the plan, where a misread is just as
visible and costs one message to correct.

---

## 4. Ask — batched, concrete, opinionated

Use `AskUserQuestion`. Not open dialogue: the operator picks rather than
composes.

**One round of up to four questions.** Two if the answers genuinely open a new
fork. Never more — past that it is an interview, and they delegated this to avoid
one.

**Lead with your recommendation** and mark it. You did the reading; say what you
would do. A neutral menu hands the thinking back.

**Every option states its consequence, not its name.**

> ✗ `relates + duplicates`
> ✓ `relates + duplicates` — *two more enum values, no new tables. `/queue` must
> learn to ignore the new kinds, and the public API's `kind` field gains values
> existing clients have not seen.*

**Use previews for anything with a shape** — schema fragments, API responses, UI
layouts. A decision about structure is far easier to make with the structure on
screen. Previews are single-select only.

**Ask about vocabulary first.** You cannot sensibly ask how a thing should be
stored before agreeing what the thing is, and a naming answer routinely dissolves
a technical question that looked open.

### Then go straight to the plan

When the answers come back, write the plan. **No confirmation round** — no "anything
to correct or add?". The plan's *Decisions* section restates each answer in your
own words, one line each, and that is where a misread surfaces; a correction is
one message against a document, not a turn spent before it exists.

A second round is still allowed, but only when an answer opened a fork that
passes §2's test on its own.

---

## 5. Write the plan down

A document, not a conversation. Enough for someone else — or a dispatched agent —
to build from.

### In a repo tracked in Zumino, the plan goes on the task

A repo is tracked in Zumino when it has a `.zumino.json` at its root, or when the
input is a task code (`ONS-14`). There the plan lives on the task, not in a file.
Load the **`zumino`** skill for the CLI.

- **Which task.** The one the input names. If it names none, create one —
  `zumino task create` with a specific title and the five lines as its
  description — after a `zumino find` for the same work, and name any near-miss
  in your report. Never put the plan on a task the input did not name: `--plan`
  replaces whatever plan it had.
- **The plan:** `zumino task spec <code> --plan "$(cat <working copy>)"`.
- **Acceptance criteria**, in a separate call — the CLI takes one section at a
  time. When the task has none, write the criteria the plan implies: concrete,
  checkable, one line each, so the task meets the queue's bar. When it already
  has some, never replace them; if the plan disagrees with them, say so.
- **Never edit an existing description.**
- Keep a working copy at `~/.local/share/shape-it/<repo>/<slug>.md` — it is what
  Plannotator annotates — but report the **task code and its URL** as where the
  plan lives.

### Everywhere else — where the file goes

**Never create a directory inside a repository to hold it.** This skill exists
partly for projects you do not own, and a new `docs/plans/` in a client's
checkout is exactly the file you were avoiding. Resolve in this order:

| # | If | Write to |
|---|---|---|
| 1 | the repo already has a plans directory (`docs/plans/`, `plans/`, `.plans/`) | there, as `<slug>.md` |
| 2 | the operator named a path | that path |
| 3 | otherwise | `~/.local/share/shape-it/<repo>/<slug>.md`, and say so |

Row 3 is the default and it is deliberate: the plan is an artefact of this
conversation, not of the repository, and it must not turn up in someone else's
`git status`. Say the full path in your report so it can be moved in one command
if they want it committed.

### The shape

```markdown
# <feature>

## What this is
<The five lines from §3, as agreed — what it is, why now, effect, if we don't,
and what was asked. Not rewritten: they were checked with the operator before a
single question was asked, so they are the one part of this document already
known to be right.>

## Decisions
<Each answered question and what was chosen. One line each.>

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
decide freely. Keep it to the calls that could plausibly have gone the other
way — not every naming choice.

**Nothing outlives this file.** There is no `DOMAIN.md` to write vocabulary to
and no `docs/decisions/` for the forks. If a term or a decision in here is one
the project will keep needing, say so in one line at the end of your report — it
is the honest signal that this project has outgrown the lite version.

---

## 6. Print it, then ask what next

### Print it

Say where the plan lives — the path, or the task code and URL — then **print the
whole plan in your reply**. Not a summary, not the headings: the same text that
was written. The stored copy is what survives; the printed one is what actually
gets read in the next thirty seconds, and a plan nobody reads is a plan nobody
corrects.

### Then one question: what next

End with a single `AskUserQuestion`, recommendation first:

| Option | What happens when it is picked |
|---|---|
| **Implement here** | Build it in this session, following the plan. Usually the right default for work small enough to finish in one sitting. |
| **Open in Plannotator** | `plannotator annotate <working copy>`. Apply each annotation, say what changed, and in a Zumino repo write the revised plan back with `--plan`. Offer it only when `command -v plannotator` finds it. |
| **Start implementation with land-it** | Invoke `land-it` with the plan's path or task code, saying the plan was just approved here. It skips its own planning and its "Proceed?" and runs to a draft PR. Recommend it for ticket-sized work in a repo with a PR flow. |

**Skip the question when `land-it` invoked you** — it says so when it hands over,
and its gate is the handoff.

Anything the operator types instead of picking is a correction: apply it to the
plan (file and task), say what changed, and print only the sections that moved.

---

## Guardrails

- **Do not enter plan mode.** This produces a plan, then asks one question.
- **Do not implement before the closing question**, and do not start "just the
  obvious part". Building starts only when it is chosen there.
- **Never ask a question that fails §2's test**, and never a confirmation round.
- **Do not ask more than two rounds.** If the picture is still unclear, say what
  is unclear and why, rather than continuing to interrogate.
- **Never ask what the project answers.** If you are asking about a convention,
  you have not read enough.
- **Cite the project when you decide.** "Following `entry.status`" is checkable;
  "seemed natural" is not.
- **Do not write a `DOMAIN.md` or `docs/decisions/`.** That is `shape-it`'s job,
  and creating either as a side effect of a planning session is the documentation
  chore the operator did not ask for. Recommending one at the end is fine.

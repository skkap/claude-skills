---
name: shape-it
description: Plan a feature by investigating the codebase first, deciding everything the repo can already answer, and asking only the decisions that are expensive to reverse — data models, public surfaces, vocabulary, scope boundaries, UI shape, business rules. Uses batched multiple-choice questions rather than open dialogue, then writes the plan. Use when asked to plan a feature, think through an approach, scope work before building, or figure out what to build. Does not enter plan mode and does not implement.
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

## When this runs

The operator wants a feature thought through before anything is built. They are
**not** asking for plan mode and not asking for code — this produces a written
plan and stops.

Not for: a one-line fix, a task whose shape is already settled, or work where the
operator has already told you the approach. Planning something obvious is its own
kind of waste.

---

## 1. Investigate before asking anything

**A question the codebase could have answered is a tax on the operator.** Most of
what feels like a design question has already been decided somewhere in the repo,
and the decision is usually load-bearing.

Read, in this order:

- **The thing itself** — the task file, the issue, the sentence they typed.
- **`CLAUDE.md` / `AGENTS.md`**, and any path-scoped rules (`.claude/rules/`,
  nested `CLAUDE.md`). These are normative. A plan that contradicts one is wrong
  even if it works.
- **The schema, the API surface, the existing feature nearest to this one.** The
  closest neighbour is the strongest signal: if the repo already does something
  similar, the shape of the new thing is mostly decided.
- **Prose in the code.** Comments that argue for a constraint are the ones people
  forget to grep for, and they often pre-empt the exact question you were about
  to ask.

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

- **Data model and schema.** Migrations are forward-only in most repos, and data
  written under the wrong shape outlives the decision that shaped it.
- **Public surface.** Route paths, event names, CLI flags, published API fields.
  Once something consumes them, changing them breaks the consumer.
- **Vocabulary.** Enum values, entity names, the words in the UI. They leak into
  the schema, the API, the docs and the operator's own head, and renaming later
  touches all four.
- **Scope boundaries.** Which half of the task is in, which is deferred. Silence
  about the expensive half reads as permission.
- **UI shape** where the repo has no precedent — one panel or two, a new page or
  a section. Cheap in code, expensive in habit once people learn it.
- **Business and domain rules.** Who may see what, what counts as done, what is
  billable, what the regulator requires. These are not in the code and you cannot
  derive them.

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

---

## 3. Ask — batched, concrete, opinionated

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

---

## 4. Write the plan

A document, not a conversation. It should be enough for someone else — or a
dispatched agent — to build from.

```markdown
# <feature>

## What this is
<2-3 sentences, plain language: what changes and for whom.>

## Decisions
<Each answered question, and what was chosen. One line each.>

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

---

## Guardrails

- **Do not enter plan mode.** This produces a plan as text and stops.
- **Do not implement**, and do not start "just the obvious part". The plan is the
  deliverable.
- **Do not ask more than two rounds.** If the picture is still unclear, say what
  is unclear and why, rather than continuing to interrogate.
- **Never ask what the repo answers.** If you find yourself asking about a
  convention, you have not read enough.
- **Cite the repo when you decide.** "Following `entry.status`" is checkable;
  "seemed natural" is not.

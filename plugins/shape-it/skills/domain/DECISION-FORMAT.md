# Decision record format

A **decision record** is a short note saying what was decided and why. Decision
records live in `docs/decisions/`, numbered sequentially: `0001-slug.md`,
`0002-slug.md`. Create the directory lazily, with the first one.

> **`DOMAIN.md` says what is true about the subject. A decision record says why
> this setup is the way it is.**

In codebases this artefact is usually called an **ADR** (architecture decision
record) and `docs/adr/` is the conventional directory. Same thing. One name is
used here, in every project, because half the decisions worth recording are not
architectural — a fiscal year-end, a registered office, a bank, a deliberate no —
and a project should not have to decide which of two directories a decision goes
in before it can write it down.

A decision record is not documentation of how things work — the material does
that, and the record would go stale within a month of trying. It records the
*fork*: that a choice existed, which way it went, and what made that the answer.
That stays true even after everything around it changes.

---

## Template

```md
---
date: YYYY-MM-DD
---

# {Short title, stated as the decision}

{1–3 sentences: the situation, what was decided, and why.}
```

A date and a paragraph. That is the whole requirement, and most records should be
exactly that.

```md
---
date: 2024-03-11
---

# Order totals are stored, not computed from line items

Tax rates and shipping rules change, and an order from two years ago must still
show the total the customer was actually charged — recomputing it produces a
different number every time the rules move. The total is written once at
placement and never recalculated; line items remain the audit trail.
```

```md
---
date: 2026-06-02
---

# Fiscal year ends in May

Incorporating in June makes a May year-end the longest possible first fiscal
year — close to twelve months — which maximises the small-business tax exemption
window before the first filing. It also keeps the year-end clear of the quarter
when every accountant is busy. Changing it later means amending the articles.
```

**Recover the date; don't stamp today's.** When you write a record as the
decision is made, the date is simply today. When you write one *afterwards* —
lifting a choice out of prose, or adopting a model into an existing project — it
is not, and today's date makes the record say something false about the world it
was decided in. The history usually knows:

```bash
git log --diff-filter=A --format=%ad --date=short -1 -- <file the decision introduced>
git log -S '<distinctive phrase>' --format='%ad %s' --date=short -1
```

Outside a repo the equivalents are the filing date, the email, the invoice, the
meeting note. Where genuinely nothing dates it, use the earliest date you can
defend and say in the body that it is approximate — an acknowledged estimate is
readable, a confident wrong date is not.

**The date is required, not optional.** A decision is an answer to the rules,
prices, constraints and alternatives in force when it was made — and every one of
those moves. Tax and legal decisions are uninterpretable without it: *"the
exemption applies"* is a different claim in 2026 than in 2029, and a reader who
cannot date the reasoning cannot tell whether to trust it or redo it. Technical
records age the same way more slowly. Numbering gives you order; only the date
gives you the world it was decided in.

Title the decision, not the topic. *"Order totals are stored"* and *"Fiscal year
ends in May"* tell a reader scanning the directory what they need; *"Order
totals"* and *"Fiscal year"* make them open the file to find out.

### Optional sections

Add one only when it carries something the paragraph cannot. Most decisions need
none.

| Section | Use it when |
|---|---|
| `status` frontmatter | The decision gets revisited — `proposed \| accepted \| deprecated \| superseded by 0011` |
| **Considered options** | A rejected alternative is worth remembering, because it will be proposed again |
| **Consequences** | A downstream effect is non-obvious and someone will otherwise trip on it |

---

## When a decision earns a record

Both of these, or skip it:

1. **Hard to reverse** — changing your mind later costs something real: a
   migration, a fee, a filing, a renegotiation, a quarter of work.
2. **A real trade-off** — there were genuine alternatives, and one was picked for
   stated reasons.

Each removes a different kind of noise. Reversible decisions do not need a record
because you will simply reverse them. And where there was no alternative, there
is nothing to record beyond "we did the obvious thing" — which reads, six months
later, as though a choice was made when none was.

### Surprise is a priority signal, not a third condition

A decision that is **surprising without context** — one where a future reader
looks at the result and asks *"why on earth is it like this?"* — is the record
someone will actually go and look for. So when several decisions qualify at once
and you are choosing what to write down first, write that one.

But it does not decide *whether*. "The primary bank is Aozora" is hard to reverse
and had real alternatives; nobody would be surprised by it, and it still needs a
record, because in three years the question will be *why not the one everyone
else uses* and the answer will have been reconstructed by someone who was not
there. Requiring surprise as a gate throws away exactly the unglamorous
structural decisions that are most expensive to re-litigate.

### What qualifies — in a codebase

- **Architectural shape.** Monorepo. Event-sourced write model with a projected
  read model. A separate gateway service instead of in-process provider calls.
- **Data model choices with migration cost.** One table or several. Denormalised
  or joined. Soft delete or hard.
- **Public surface.** Route shapes, event names, published field names — anything
  a consumer you do not control has already read.
- **Technology with lock-in.** Database, message bus, auth provider, deployment
  target, UI framework. Not every library — the ones that would take a quarter to
  swap.
- **Concurrency and consistency.** Sync or async, at-least-once or exactly-once,
  what is allowed to be eventually consistent. These are almost never visible in
  a diff and almost always expensive to change.
- **Boundary and ownership.** "Customer data is owned by the Customer area;
  everything else references it by id."

### What qualifies — in a company's or a person's records

The same two conditions, selecting a different list:

- **Structural choices, once filed.** Company form, share capital, year-end
  month, registered activities, registered office. All public on the register and
  all expensive to amend — the purest possible case for a record.
- **Who is what.** A family member as staff rather than an officer; one equity
  holder rather than two. These have tax and insurance consequences that outlive
  everyone's memory of the reasoning.
- **Money and counterparty lock-in.** Which bank, which accounting software,
  which registered-office provider, which payroll arrangement. Switching costs
  are real and the reason for the original pick is always reconstructed wrongly.
- **Accounting and tax treatments.** The account and tax category chosen for a
  recurring transaction, an amortisation policy for start-up costs, an FX rate
  convention. Consistency across years is the whole point, and consistency needs
  a written reason.
- **Instrument choices.** A SAFE rather than priced equity; a loan rather than a
  capital injection. Written down once, so the next one matches.

### Common to both

- **Deliberate deviation from the obvious path.** Hand-written SQL instead of the
  ORM, because X. A virtual office when the home address was free. Anything a
  reasonable reader would assume went the other way — this is what stops the next
  person "fixing" something deliberate.
- **Constraints invisible in the material.** A compliance rule that rules out a
  region. A partner contract that fixes a response-time budget. A benefit
  eligibility that depends on twelve months of prior enrolment.

### Deliberate no-s

Scope decisions belong here too. Something considered and deliberately left out
is a decision, and it needs a record for exactly the reason the yes-s do: without
one it gets proposed again every few months, and each time the reasoning is
reconstructed from scratch by someone who was not there.

```md
# No partial cancellation of an Order

Asked for three times and dropped each time. A partial cancellation has to
decide what happens to shipping already apportioned across the whole Order, and
every answer is wrong for some customer. Cutting an Order down is modelled as a
Return against the dispatched Shipments instead. Revisit if shipping moves to
per-line pricing.
```

A no clears the gate differently from a yes. **Hard to reverse** rarely applies —
you can always change your mind and build the thing — so the test that replaces
it is **recurrence**: the no has come up more than once, or a reasonable person
would expect the feature and be surprised to find it missing. Either of those,
plus a real trade-off, earns the record. Routine scope trimming inside a single
piece of work does not — that belongs in its plan, under *Out of scope*.

---

## Numbering and placement

Scan the target `docs/decisions/` for the highest number and add one. Numbers are
never reused, including for deleted records.

In a project with a `DOMAIN-MAP.md`, decisions sit at the level they bind:

- **`docs/decisions/` at the root** — anything crossing areas, or true of the
  whole project: the deployment target, how areas communicate, a shared id type;
  the company form, the fiscal year.
- **`<area>/docs/decisions/`** — decisions internal to one area, invisible
  outside it.

Numbering is per-directory. Two records may both be `0003` in different areas;
refer to them by path when it matters.

When in doubt, root. An area-local record that turns out to bind the whole
project is worse than a root record that turns out to be narrow, because nobody
outside the area will ever read it.

## Superseding

Never edit a decision into a different decision — the record of the fork is the
whole value, and rewriting it loses the reason the first answer looked right.

Write a new record, and add one line to the old one:

```md
---
status: superseded by 0011
---
```

If the entry in `DOMAIN.md` linked the old one under `_See_`, update the link in
the same change.

This is also why a decisions *table* — one row per decision in a single file —
stops working past about a dozen rows. A row cannot carry the reasoning, cannot
be superseded without being overwritten, and cannot be linked to from an entry.
Converting an existing one is covered by the **`domain-adopt`** skill.

# ADR format

An **architecture decision record** is a short note saying what was decided and
why. ADRs live in `docs/adr/`, numbered sequentially: `0001-slug.md`,
`0002-slug.md`. Create the directory lazily, with the first ADR.

> **`DOMAIN.md` says what is true about the business. An ADR says why the system
> is built the way it is.**

An ADR is not documentation of how the code works — the code does that, and the
ADR would go stale within a month of trying. It records the *fork*: that a choice
existed, which way it went, and what made that the answer. That stays true even
after the code around it changes.

---

## Template

```md
# {Short title, stated as the decision}

{1–3 sentences: the situation, what was decided, and why.}
```

That is the whole requirement. An ADR can be one paragraph, and most should be.

```md
# Order totals are stored, not computed from line items

Tax rates and shipping rules change, and an order from two years ago must still
show the total the customer was actually charged — recomputing it produces a
different number every time the rules move. The total is written once at
placement and never recalculated; line items remain the audit trail.
```

Title the decision, not the topic. *"Order totals are stored"* tells a reader
scanning the directory what they need; *"Order totals"* makes them open the file
to find out.

### Optional sections

Add one only when it carries something the paragraph cannot. Most ADRs need
none.

| Section | Use it when |
|---|---|
| `Status` frontmatter | The decision gets revisited — `proposed \| accepted \| deprecated \| superseded by ADR-NNNN` |
| **Considered options** | A rejected alternative is worth remembering, because it will be proposed again |
| **Consequences** | A downstream effect is non-obvious and someone will otherwise trip on it |

---

## When a decision earns an ADR

All three, or skip it:

1. **Hard to reverse** — changing your mind later costs something real.
2. **Surprising without context** — a future reader will look at the code and
   ask "why on earth is it like this?"
3. **A real trade-off** — there were genuine alternatives, and one was picked for
   stated reasons.

Each condition removes a different kind of noise. Reversible decisions do not
need a record because you will simply reverse them. Unsurprising ones raise no
question to answer. And where there was no alternative, there is nothing to
record beyond "we did the obvious thing" — which reads, six months later, as
though a choice was made when none was.

### What qualifies

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
- **Deliberate deviation from the obvious path.** Hand-written SQL instead of the
  ORM, because X. Anything a reasonable reader would assume went the other way —
  this is what stops the next engineer "fixing" something deliberate.
- **Constraints invisible in the code.** A compliance rule that rules out a
  region. A partner contract that fixes a response-time budget.

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

A no-ADR is worth writing when the no is **surprising** (a reasonable person
expects the feature) or **recurring** (it has come up more than once). Routine
scope trimming inside a single feature is not an ADR — it belongs in that
feature's plan, under *Out of scope*.

---

## Numbering and placement

Scan the target `docs/adr/` for the highest number and add one. Numbers are never
reused, including for deleted ADRs.

In a repo with a `DOMAIN-MAP.md`, decisions sit at the level they bind:

- **`docs/adr/` at the root** — anything crossing areas, or true of the system:
  the deployment target, how areas communicate, a shared id type.
- **`<area>/docs/adr/`** — decisions internal to one area, invisible outside it.

Numbering is per-directory. Two ADRs may both be `0003` in different areas; refer
to them by path when it matters.

When in doubt, root. An area-local ADR that turns out to bind the system is worse
than a root ADR that turns out to be narrow, because nobody outside the area will
ever read it.

## Superseding

Never edit a decision into a different decision — the record of the fork is the
whole value, and rewriting it loses the reason the first answer looked right.

Write a new ADR, and add one line to the old one:

```md
---
status: superseded by ADR-0011
---
```

If the entry in `DOMAIN.md` linked the old ADR under `_See_`, update the link in
the same change.

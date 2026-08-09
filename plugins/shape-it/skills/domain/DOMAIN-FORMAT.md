# `DOMAIN.md` format

One file, four sections, in this order. Every section is optional except
`## Language` — omit a heading until it has something under it.

```md
# {Project or area name} — Domain

{One or two sentences: what this project is about, in the operator's words.
Not what it is built with.}

## Language      ← the entries. Almost all of the file.
## Relationships ← how entries connect. The ontology.
## Rules         ← invariants that belong to no single entry.
## Open questions ← surfaced, not yet resolved. Visible without pretending to be settled.
```

---

## Entries

An entry is a thing the project is about, plus what is known about it. The
definition is required; the four qualifier lines are used only when they have
something to say.

```md
**Shipment**:
One physical dispatch of goods, from one warehouse, on one day.
_Avoid_: delivery, parcel, consignment
_Kinds_: standard | express | pickup
_Rules_: A Shipment cannot be recalled once dispatched — a returned Shipment
becomes a Return.
_See_: [ADR-0007](docs/adr/0007-shipments-own-their-line-items.md), `src/fulfilment/shipment.ts`
```

| Line | For | Rule |
|---|---|---|
| **definition** | What it *is* | One or two sentences. Define the thing, not what it does. Required. |
| `_Avoid_` | Words that mean this but should not be used | The rejected synonyms, comma-separated. This is the line that stops drift. |
| `_Kinds_` | A **closed** set of variants | `A \| B \| C`. Only when the set is closed — an open-ended list is not a kind. |
| `_Rules_` | What is always true of *this* entry | One line each. Cross-entry invariants go in `## Rules` instead. |
| `_See_` | Where this becomes real | ADRs, source files, external references. Links only, no commentary. |

**`_Kinds_` earns its own line because it is the most expensive thing here.** A
closed set becomes an enum in the schema, a set of values in the API, and a set
of labels in the UI simultaneously — three places that must be changed together
when the set changes. Writing the set down once is what makes the change
tractable; discovering it three times is what makes it not.

**`_See_` is what keeps the model honest.** An entry with no references is either
new or dead, and after a few months you cannot tell which from the entry alone.

Group entries under `###` subheadings once natural clusters emerge. A flat list
is fine while they are all one cohesive area.

---

## Relationships

The connections between entries — the part no single definition can carry.
Bullets, one per relationship, each naming both ends and the cardinality in
plain words.

```md
## Relationships

- One **Order** produces one or more **Shipments**; a Shipment belongs to exactly
  one Order and cannot move between them.
- An **Invoice** covers one or more **Shipments**, which need not be from the
  same Order.
- A **Customer** places Orders. The party billed and the party shipped to may
  differ; only the billed party is the Customer.
```

Say the cardinality and say the exception. *"An Invoice covers Shipments, which
need not be from the same Order"* is the half that decides a join table;
*"cannot move between them"* is the half that decides a constraint.

---

## Rules

Invariants that span entries and therefore belong to none of them. If a rule is
about one entry, it goes on that entry's `_Rules_` line — this section is for
what is left.

```md
## Rules

- An Order cannot be cancelled once any of its Shipments has dispatched. The
  remaining Shipments can be, individually.
- An Invoice is immutable once sent. A correction is a second Invoice, never an
  edit to the first.
```

These are the statements the code cannot tell you and the operator can. Keep
them to a line; a rule needing a paragraph is usually two rules, or a decision.

---

## Open questions

Ambiguities found and not yet resolved. Resolving one deletes the bullet and
edits the entry — this section is a queue, not an archive.

```md
## Open questions

- "Account" means the Customer in the schema and the login in the UI copy.
  Same thing, or two entries?
- Is a pickup a kind of Shipment, or its own entry? Currently a `kind` value,
  which makes it carry a warehouse and a carrier it does not have.
```

Resolved ambiguities are worth one line of history *inside the entry that
resolved them*, not a growing list here:

```md
**Customer**:
The party that pays for an Order…
_Avoid_: account, client, buyer — "account" previously meant this in the admin
UI and now means the login only.
```

---

## Writing rules

- **Be opinionated.** When several words exist for one concept, pick one and put
  the rest under `_Avoid_`. A model that lists alternatives without choosing has
  documented the problem rather than fixed it.
- **Define what it is, not what it does.** "An Invoice is a request for payment
  covering delivered goods" — not "Invoices are generated nightly and emailed."
- **One or two sentences.** A definition that needs a paragraph is usually two
  entries that have not been separated yet.
- **Project-specific only.** See the exclusion list in
  [SKILL.md §4](SKILL.md#4-what-does-not-belong-in-domainmd).
- **The business's own words win, including when they are not English.** If the
  business says 案件 rather than "matter", or *Sendung* rather than "shipment",
  that is the entry, with a gloss in parentheses. Translating a term for the
  model's benefit creates a second vocabulary, which is the problem this file
  exists to solve.

---

## `DOMAIN-MAP.md`

A repo with several areas gets a map at the root and a `DOMAIN.md` inside each
area, next to the code it describes.

```md
# Acme — Domain Map

## Areas

- [Ordering](./src/ordering/DOMAIN.md) — what a customer asked for, and for how much
- [Fulfilment](./src/fulfilment/DOMAIN.md) — picking, packing and dispatching it
- [Billing](./src/billing/DOMAIN.md) — invoicing, payment and correction

## Between areas

- **Ordering → Fulfilment**: Ordering emits `OrderPlaced`; Fulfilment decides how
  many Shipments it becomes. Ordering never knows about warehouses.
- **Fulfilment → Billing**: Billing invoices dispatched Shipments, not Orders.
  An Order with nothing dispatched has no Invoice.
- **Shared**: `CustomerId` and `Money` cross every boundary and are owned by
  Ordering.
```

The `## Between areas` section is doing the real work. Two areas that share a
word are the standing risk in a split model — if **Ordering** and **Billing**
both say "total" and mean different things (before and after tax), the map is
where that is either reconciled or explicitly allowed.

Ownership is the rule that resolves most of it: **one area owns a term, the
others reference it.** Say which, on the map, once.

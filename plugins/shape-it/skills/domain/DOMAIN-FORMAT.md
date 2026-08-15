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
_See_: [0007](docs/decisions/0007-shipments-own-their-line-items.md), `src/fulfilment/shipment.ts`
```

| Line | For | Rule |
|---|---|---|
| **definition** | What it *is* | One or two sentences. Define the thing, not what it does. Required. |
| `_Avoid_` | Words that mean this but should not be used | The rejected synonyms, comma-separated. This is the line that stops drift. |
| `_Kinds_` | A **closed** set of variants | `A \| B \| C`. Only when the set is closed — an open-ended list is not a kind. |
| `_Rules_` | What is always true of *this* entry | One line each. Cross-entry invariants go in `## Rules` instead. |
| `_See_` | Where this becomes real | Decision records, source files, documents, filings, external references. Links only, no commentary. |

**`_Kinds_` earns its own line because it is the most expensive thing here.** A
closed set becomes an enum in the schema, a set of values in the API, and a set
of labels in the UI simultaneously — three places that must be changed together
when the set changes. Outside code the same trap, differently dressed: a closed
set of expense categories, or of registered business activities, is copied into a
filing, a spreadsheet and an accounting system, and those must move together too.

**`_See_` is what keeps the model honest.** An entry with no references is either
new or dead, and after a few months you cannot tell which from the entry alone.
Point it at whatever the project is actually made of — a source file, a scanned
certificate, a decision record, a section of a business plan.

Group entries under `###` subheadings once natural clusters emerge. A flat list
is fine while they are all one cohesive area.

### Terms that are not in English

**The project's own words win.** If the work says *Sendung* rather than
"shipment", that is the entry. Translating a term for the model's benefit creates
a second vocabulary, which is the problem this file exists to solve.

Gloss the headword once, on the entry, in parentheses: a short English meaning,
plus a reading where the script does not supply one.

```md
**Sendung** (one consignment as dispatched, in the carrier's own sense):
The unit the carrier tracks and prices. Does not always match one Shipment —
a Shipment too large for one vehicle becomes two Sendungen.
_Avoid_: shipment — a Shipment is ours, a Sendung is the carrier's, and the
counts differ. This is exactly why the German word is kept.
_See_: `src/carriers/dhl.ts`
```

The gloss belongs on the entry and nowhere else — the entry *is* the one place
the term is defined, so a second gloss elsewhere is a second definition waiting
to disagree. Once glossed, the term is used bare throughout the rest of the file.

Where the script does not give the pronunciation — Japanese, Chinese, Arabic,
Cyrillic for a reader who does not have it — include the reading alongside the
meaning. A term the reader cannot say is a term they will avoid using, and a term
nobody says goes back to being translated.

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

**The most valuable lines in the file.** A definition tells a reader what a thing
is; a rule tells them what they are not allowed to do with it — and that is the
part that changes behaviour, human or otherwise. A model made entirely of
definitions produces work that is plausible and quietly wrong at the edges,
because nothing in it ever says *no*.

Invariants that span entries live here. If a rule is about one entry, it goes on
that entry's `_Rules_` line instead; this section is for what is left.

```md
## Rules

- An Order cannot be cancelled once any of its Shipments has dispatched. The
  remaining Shipments can be, individually.
- An Invoice is immutable once sent. A correction is a second Invoice, never an
  edit to the first.
```

These are the statements the material cannot tell you and the operator can. Three
things make a rule usable:

- **Say what is forbidden, not what is preferred.** *"An Invoice is immutable
  once sent"* is a rule. *"We try to avoid editing invoices"* is a habit, and
  nothing will honour it.
- **Give the exception in the same breath.** *"…the remaining Shipments can be,
  individually"* is half the rule. A rule with its exception missing gets
  discovered as a bug.
- **One line each.** A rule needing a paragraph is usually two rules, or a
  decision that has wandered in.

**They are mostly collected, not asked for.** Nobody volunteers an invariant. They
volunteer *"—well, except that one time when…"* in the middle of a story, which
is why walking a real case end to end is the technique that fills this section.
See [SKILL.md §3](SKILL.md#3-during-a-session).

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
- **Project-specific only.** General technical vocabulary and the general
  vocabulary of the field both stay out — see the exclusion list in
  [SKILL.md §4](SKILL.md#4-what-does-not-belong-in-domainmd). Where a term is
  shared across several projects, one of them owns the definition and the others
  link to it.
- **Gloss non-English headwords once, on the entry** — meaning, plus a reading
  where the script does not supply one.

---

## `DOMAIN-MAP.md`

A project with several areas gets a map at the root and a `DOMAIN.md` inside each
area, next to the material it describes.

```md
# Acme — Domain Map

## Areas

- [Ordering](./src/ordering/DOMAIN.md) — what a customer asked for, and for how much
- [Fulfilment](./src/fulfilment/DOMAIN.md) — picking, packing and dispatching it
- [Billing](./src/billing/DOMAIN.md) — invoicing, payment and correction

## Between areas

- **Ordering → Fulfilment**: Ordering emits `OrderPlaced`; Fulfilment decides how
  many Shipments it becomes. Ordering never knows about warehouses.
  _Ordering is upstream_ — it changes on its own schedule and Fulfilment adapts.
- **Fulfilment → Billing**: Billing invoices dispatched Shipments, not Orders.
  An Order with nothing dispatched has no Invoice.
  _Fulfilment is upstream._
- **Shared**: `CustomerId` and `Money` cross every boundary and are owned by
  Ordering. Changing either is a coordinated change, not a local one.
```

The `## Between areas` section is doing the real work. Two areas that share a
word are the standing risk in a split model — if **Ordering** and **Billing**
both say "total" and mean different things (before and after tax), the map is
where that is either reconciled or explicitly allowed.

Two questions resolve most of it, and both belong on the map:

- **Who owns the term?** One area owns it, the others reference it. Say which,
  once.
- **Which side is upstream?** Ownership says where the definition lives;
  *upstream* says whose changes force the other side to react. They are not the
  same question and the second one is the one people skip. An area can own a term
  and still be downstream of another for a different one — and knowing which way
  the pressure runs is what tells you where a change is expensive.

Name the direction in plain words. *"Ordering is upstream — it changes on its own
schedule and Fulfilment adapts"* carries everything a reader needs. Where neither
side is upstream because both must move together, say that too: it is a much
more expensive relationship and it should be visible as one.

The map covers areas *within one project*. Vocabulary shared between separate
projects is a different case and is handled by the shared-reference rule in
[SKILL.md §4](SKILL.md#4-what-does-not-belong-in-domainmd) — do not stretch a map
across repository boundaries to hold it.

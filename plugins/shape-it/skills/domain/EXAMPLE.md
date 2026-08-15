# A complete worked model

Every other file here gives fragments. This is one small project's model in full,
so the shape is visible at a glance — a `DOMAIN.md`, and one of the decision
records it links to.

The project is a two-person design studio doing client work. It is deliberately
not a codebase: the format is the same either way, and a records project makes it
obvious that none of this depends on having source files. Roughly the size a
first `DOMAIN.md` should be.

---

## `DOMAIN.md`

````md
# Fieldwork Studio — Domain

Independent design studio. We take on client work in fixed blocks, produce
things, and bill for them.

## Language

### The work

**Client**:
The organisation that signs the contract and pays. One legal entity.
_Avoid_: account, customer — "account" meant this in our old invoicing tool and
now means the login only.
_See_: `clients/`

**Contact**:
A named person at a Client. Several per Client; one is the approver.
_Rules_: Only the approver can sign off a Deliverable. If they leave mid-Block,
work pauses until a new approver is named.

**Block**:
One continuous stretch of committed work for one Client — a start date, an end
date, and an agreed number of days per week. The unit we sell.
_Avoid_: project, engagement, retainer. "Project" is the Client's word for the
thing they are building and rarely lines up with what we sold them; a Block may
cover half a project or three of them.
_Kinds_: discovery | build | support
_Rules_: A Block cannot be extended. More work is a new Block, so the rate can
change and either side can walk.
_See_: [0002](docs/decisions/0002-blocks-are-not-extended.md)

**Deliverable**:
A thing handed over inside a Block that the approver signs off. A file, a
document, a running site.
_Rules_: Signed off or not — there is no partial. Feedback that changes the shape
of a Deliverable makes a new one; it does not reopen the old.

**Handover**:
The end of a Block: everything transferred, access revoked, final Invoice issued.
_Rules_: A Block is not finished until Handover, even when the last Deliverable
was signed off weeks earlier. Unfinished Handovers are how we end up still
holding client credentials a year later.

### Money

**Rate**:
The day rate for one Block, agreed before it starts and fixed for its duration.
_Rules_: Rates are per Block, never per Client. A long-standing Client can be on
two different Rates in the same year and that is correct.

**Invoice**:
A request for payment covering one calendar month of one Block.
_Avoid_: bill
_Kinds_: interim | final
_Rules_: An Invoice is immutable once sent. A correction is a credit note plus a
second Invoice, never an edit.
_See_: [0004](docs/decisions/0004-monthly-invoicing-not-on-delivery.md)

**Write-off**:
Days worked inside a Block that we choose not to invoice.
_Rules_: A Write-off is recorded against the Block, not silently dropped. A Block
with a large one is a pricing problem we want to be able to see later.

## Relationships

- One **Client** has one or more **Contacts**; exactly one of them is the
  approver at any moment, and it may change mid-Block.
- One **Client** has zero or more **Blocks**, sequential or overlapping. A Block
  belongs to exactly one Client and cannot be transferred.
- One **Block** produces zero or more **Deliverables** and one or more
  **Invoices**. A Block that produced nothing still produces Invoices — we sell
  time, not output.
- An **Invoice** covers exactly one Block and one month. It never spans two
  Blocks, even for the same Client in the same month.

## Rules

- Work outside an open Block is unbilled and unprotected. If there is no Block,
  there is no work.
- Two Blocks for the same Client run independently: separate Rates, separate
  Invoices, separate Handovers. Nothing is netted between them.
- Nobody signs off their own work. The approver is always on the Client side.

## Open questions

- A Client that is a holding company with three operating brands — one Client
  with three sets of Contacts, or three Clients? Currently one, and the Invoices
  go to the wrong finance team about a third of the time.
- Is a fixed-price piece a Block with an implied day count, or its own entry? We
  have taken three and modelled each differently.
````

---

## `docs/decisions/0002-blocks-are-not-extended.md`

The record the **Block** entry links to. One paragraph and a date — which is what
most of them should be.

````md
---
date: 2025-09-30
---

# Blocks are not extended; more work is a new Block

Extending was the default for the first two years and it quietly removed every
decision point we had. A Block that has run for eleven months at a rate set in
month one cannot be repriced without a difficult conversation, and neither side
ever chose to have it. Ending and re-signing puts the rate, the scope and the
option to stop back on the table at a natural moment. The cost is real — a gap
between Blocks is unpaid, and clients dislike the paperwork.
````

Note what it does *not* contain: how Blocks are stored, what the contract
template says, or how the invoicing tool is configured. Those change; the fork —
*that extension was possible and we chose against it* — does not.

---

## What to copy from this

- **Entries lean on `_Avoid_` and `_Rules_` more than on the definition.** Every
  definition here is one sentence. The lines that earn their place are the ones
  that stop a wrong reading — *"project" is the Client's word and rarely lines
  up* — and the ones that forbid something.
- **The rules are specific enough to be violated.** *"Nobody signs off their own
  work"* can be checked. *"We value client alignment"* cannot, and would not have
  belonged here.
- **`## Open questions` is honest.** Two real ambiguities, each naming both
  readings and what the current fudge costs. That section being empty in a young
  model usually means nobody looked.
- **The whole thing is about 70 lines.** Well under the ~150 where it would be
  worth splitting into areas, and it covers a business completely.

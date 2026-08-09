---
name: domain
description: Build and sharpen a project's domain model — the things the project is about, what they are called, what kinds they come in, how they relate, and what is always true of them. Maintains DOMAIN.md (or DOMAIN-MAP.md plus per-area files in a large repo) and architecture decision records under docs/adr/. Use when pinning down terminology, resolving a word two parts of a project disagree on, recording a hard-to-reverse technical decision, or when another skill needs the domain model maintained rather than merely read.
---

# domain — one set of words, written down once

A project's words are load-bearing. They end up in the schema, the API, the UI
copy, the tests and the operator's own head at the same time, which is what makes
renaming one later so expensive — and what makes two halves of a project quietly
disagreeing about "place" or "entry" so costly to discover.

> **`DOMAIN.md` says what is true about the business.
> An ADR says why the system is built the way it is.**

That one line does most of the sorting. `DOMAIN.md` survives a rewrite in another
language on another stack; an ADR does not. If a statement would still be true
after you threw away all the code, it is domain. If it only makes sense given
this implementation, it is a decision.

**Reading the domain model is not this skill.** Any skill can open `DOMAIN.md`
during investigation — that is a one-line habit, not a discipline. This skill is
for *changing* the model: challenging a term, resolving an ambiguity, inventing
the scenario that forces a boundary to be precise, and writing the result down
the moment it settles.

| | file |
|---|---|
| The discipline | **this file** |
| `DOMAIN.md` / `DOMAIN-MAP.md` structure | [DOMAIN-FORMAT.md](DOMAIN-FORMAT.md) |
| ADR structure, numbering, the gate | [ADR-FORMAT.md](ADR-FORMAT.md) |

---

## 1. Find the model before adding to it

Two shapes, and the repo tells you which one it is:

```
Single area — most repos                 Multiple areas — large repos
/                                        /
├── DOMAIN.md                            ├── DOMAIN-MAP.md
├── docs/adr/                            ├── docs/adr/          ← system-wide
│   ├── 0001-stored-order-totals.md      └── src/
│   └── 0002-events-not-http.md              ├── ordering/
└── src/                                     │   ├── DOMAIN.md
                                             │   └── docs/adr/  ← area-local
                                             └── billing/
                                                 ├── DOMAIN.md
                                                 └── docs/adr/
```

Resolve in this order, stopping at the first hit:

| # | Found | Means |
|---|---|---|
| 1 | **`DOMAIN-MAP.md`** at the root | Multiple areas. Read it to find them; it also carries how they relate. |
| 2 | **`DOMAIN.md`** at the root | One area. This is the whole model. |
| 3 | Neither | One area, not yet written. Create it lazily — see §5. |

In a mapped repo, infer which area the current topic belongs to from the code
being discussed. If two areas both plausibly own the term, that is itself a
finding: say so and ask, because a term living in two areas with two meanings is
the exact failure the map exists to prevent.

**Only one growth path.** A single `DOMAIN.md` graduates to a `DOMAIN-MAP.md`
plus per-area `DOMAIN.md` files placed next to the code they describe. There is
no `docs/domain/` and no third shape — a model split two different ways is worse
than one that is merely long. Graduate when the single file passes roughly 150
lines *and* its terms fall into clusters that barely reference each other. Length
alone is not the trigger; a long list of tightly related terms is fine.

---

## 2. Sort what you learn

Everything you resolve lands in exactly one of three places.

| Where | What goes there | Test |
|---|---|---|
| **`DOMAIN.md`** | The things the project is about — what they are, what they are called, what kinds they come in, how they relate, what is always true of them | Still true after a full rewrite on another stack |
| **`docs/adr/`** | Hard-to-reverse technical choices, and deliberate no-s | Only makes sense given this implementation |
| **Nowhere** | Everything else | Reversible, or already obvious from the code |

Worked, on the same subject:

- *"A **Shipment** is one physical dispatch from one warehouse. An Order can
  produce several."* → **`DOMAIN.md`**. Logistics, not architecture.
- *"An Order cannot be cancelled once any of its Shipments has dispatched."*
  → **`DOMAIN.md`**. A rule about domain things, true regardless of how it is
  enforced.
- *"Order totals are stored on the row rather than computed from line items."*
  → **an ADR**. Meaningless without this database.
- *"Line items are JSONB because their shape varies by product type."* → **an
  ADR**. The *why* is domain-flavoured, but the statement is about storage.
- *"The helper is called `formatMoney`."* → **nowhere**. Reversible, and the code
  says it.

The third row matters as much as the first two. A model that absorbs everything
stops being read.

---

## 3. During a session

### Challenge on contact

When someone uses a word that conflicts with an entry, say so **in the moment**,
not in a summary at the end. *"`DOMAIN.md` defines a Customer as the party that
pays — you're describing the party the goods go to. Different thing, or does the
definition need to widen?"* Deferred challenges get lost, and by then the wrong
word is in a migration.

### Sharpen fuzzy words

Overloaded words are how two meanings enter a project under one name. Propose a
precise replacement rather than asking an open question: *"You're saying
'account' — that's the Customer in the schema and the login in the UI copy. Which
one do you mean here, and should one of them stop being called account?"*

### Stress-test with invented scenarios

Boundaries only become precise under a case that sits on them. Invent one.
*"An Order is cut down after one of its three Shipments dispatched. Is that the
same Order with a reduced total, or the original Order plus a Return?"* The
answer usually decides a relationship, a kind, and a schema column at once —
which is why it is worth the detour.

### Cross-check against the code, in both directions

- **Code contradicts what was said** → surface it. *"You said a Shipment can be
  moved to another Order, but `shipment.order_id` is written once at creation and
  never updated. Which is right?"*
- **An entry no longer appears in the code** → surface that too. A term nothing
  references is either dead vocabulary to delete, or a concept that got renamed
  in code and never in the model. Both are findings; neither shows up if you only
  ever check one direction.

### Write when it is resolved, not when it is mentioned

An entry goes in when the answer settles, in that turn. Do not batch — batched
entries get written from memory of the conversation rather than from the
conversation, and the qualifier that made the definition precise is the first
thing to go. Equally: a term merely *mentioned* is not resolved. Unresolved
things go under `## Open questions`, where they are visible without pretending to
be settled.

### Never change a definition silently

Editing an existing entry changes the project's language, and something is
already built on the old reading. Say what you are changing it from, what breaks
if the old meaning was relied on, and get agreement before writing. Adding a new
entry needs no such ceremony.

### Offer ADRs sparingly

Three conditions, all of them:

1. **Hard to reverse** — changing your mind later costs something real.
2. **Surprising without context** — a future reader will ask "why on earth is it
   like this?"
3. **A real trade-off** — there were genuine alternatives and one was picked for
   stated reasons.

Any one missing, skip it. Full guidance and the deliberate-no case in
[ADR-FORMAT.md](ADR-FORMAT.md).

---

## 4. What does not belong in `DOMAIN.md`

- **Implementation detail.** No table names, no function names, no frameworks, no
  file paths in a definition. An entry may *link* to code under `_See_`; it may
  not be *about* code.
- **General programming vocabulary.** Debounce, retry policy, feature flag,
  idempotency — a project can lean on all of them heavily and still not own them.
  The test: would someone with general engineering experience but no knowledge of
  *this business* need it explained? Only then does it belong.
- **Specs and roadmaps.** What the system will do next is a plan. `DOMAIN.md` is
  what it is about.
- **Anything already in `CLAUDE.md` as instruction.** Domain and instruction are
  different genres; duplicating one into the other guarantees they drift apart.

---

## 5. Creating the files

Lazily, and only with content in hand.

- **No `DOMAIN.md`, first term resolved** → create it with that term. Do not
  scaffold empty headings; an empty section is an invitation nobody accepts.
- **No `docs/adr/`, first ADR earned** → create the directory with `0001-`.
- **Offer, once, at the end** — never at the start. If a session surfaced terms
  worth keeping and the repo has no model, say which terms and offer to start the
  file. Opening with "shall we document the domain first?" converts the work the
  operator asked for into a documentation chore they did not.

Where a repo already carries its vocabulary informally — scattered through
`CLAUDE.md`, a README, a `docs/` note — say so and offer to lift it rather than
starting from nothing. Most repos have the material; what they lack is a file
that holds only that material, so something can read only that.

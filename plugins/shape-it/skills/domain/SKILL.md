---
name: domain
description: Build and sharpen a project's domain model — the things the project is about, what they are called, what kinds they come in, how they relate, and what is always true of them. Works on any project, code or not: a codebase, a company's records, a knowledge vault, a research archive. Maintains DOMAIN.md (or DOMAIN-MAP.md plus per-area files in a large project) and decision records under docs/decisions/, and defines the two-axis marker set other skills use — where a thing lives (domain, decision) and what is needed from the operator (nothing, attention, an answer). Use when pinning down terminology, resolving a word two parts of a project disagree on, recording a hard-to-reverse decision, or when another skill needs the domain model maintained rather than merely read. Bulk-seeding a model into a project that has none is the separate `domain-adopt` skill, invoked only on explicit request; this skill offers it at the end of a session and never starts it.
---

# domain — one set of words, written down once

A project's words are load-bearing. They end up in the schema, the API, the UI
copy and the tests at the same time — or in a filing, a contract, a spreadsheet
column and a letter to the tax office — and in the operator's own head besides.
That is what makes renaming one later so expensive, and what makes two halves of
a project quietly disagreeing about "place" or "entry" or "member" so costly to
discover.

> **`DOMAIN.md` says what is true about the subject.
> A decision record says why this setup is the way it is.**

That one line does most of the sorting. `DOMAIN.md` survives rebuilding the whole
thing from scratch — different code, different tools, different filing system. A
decision record does not. If a statement would still be true after you threw the
whole apparatus away and started again, it is domain. If it only makes sense
given the way you happen to have arranged things, it is a decision.

**This is not a code-only discipline.** The material a project is made of varies
— source files, or documents, filings, ledgers, notes — and nothing here depends
on which. Where this file says *the material*, read it as whatever your project
actually consists of. The vocabulary problem is identical either way, and a
records repo usually has it worse, because prose tolerates two words for one
thing far longer than a compiler does.

**Reading the domain model is not this skill.** Any skill can open `DOMAIN.md`
during investigation — that is a one-line habit, not a discipline. This skill is
for *changing* the model: challenging a term, resolving an ambiguity, inventing
the scenario that forces a boundary to be precise, and writing the result down
the moment it settles.

| | file |
|---|---|
| The discipline | **this file** |
| `DOMAIN.md` / `DOMAIN-MAP.md` structure | [DOMAIN-FORMAT.md](DOMAIN-FORMAT.md) |
| Decision record structure, numbering, the gate | [DECISION-FORMAT.md](DECISION-FORMAT.md) |
| A complete worked model, both files together | [EXAMPLE.md](EXAMPLE.md) |
| Marking in conversation, not just in reports | [MARKERS.md](MARKERS.md) |
| Seeding a model into a project that has none | the **`domain-adopt`** skill |

---

## Markers

One set, used by this skill, by **`domain-adopt`**, and by **`shape-it`**.

**Two independent axes.** They are not one list of five — they are two questions,
and a line answers both. Reading them as a single ranked list is the mistake to
avoid: ⚖️ and ✅ are not alternatives, they are answers to different questions.

**Axis 1 — where does this live?**

| | | Why this glyph |
|---|---|---|
| 📖 | **domain** → `DOMAIN.md` | The lexicon. What things are called. |
| ⚖️ | **decision** → `docs/decisions/` | A choice that was weighed. Alternatives existed. |

**Axis 2 — what do I need from you?**

| | | |
|---|---|---|
| ✅ | **nothing** | It is already written down, or two sources agree and that is simply the answer. Reported so you can catch a wrong one, not so you can confirm it. |
| ⚠️ | **your attention** | Something is broken: one word carrying two meanings, or two sources disagreeing. |
| ❓ | **your answer** | A real gap I cannot close. Asked now, or parked in `## Open questions`. |

Combine them:

| | ✅ | ⚠️ | ❓ |
|---|---|---|---|
| **📖** | term already defined | one word, two meanings | term used, never defined |
| **⚖️** | already recorded, e.g. `0004` | two records disagree | a fork — I am asking you to pick |

`⚖️ ❓ retention window` is a decision *waiting to be made*; `⚖️ ✅ 0004` is one
*already on disk*. Both are decisions; the second marker is the whole difference,
which is why axis 2 is never optional.

Define axis 2 by the **ask**, never by how finished the content feels. "This is
settled" and "this was a decision" sound like the same claim and are not — one
is about the record, the other about what you want from the reader.

**⚠️ is the one to hunt for.** A single word carrying two meanings is the most
expensive thing in any project's language and the thing nobody reports, because
each half looks correct from where it is used.

**Use them inline, in ordinary prose, not only in reports** — 📖 the first time
you use a term because the model defines it, ⚠️ the instant a word in play
conflicts with it, ⚖️ when you make a call that belongs in a record, ✅ when a
question turns out to be already answered. The four moments in full, the three
rules against noise, and the question-header rule are in
[MARKERS.md](MARKERS.md).

---

## 1. Find the model before adding to it

Two shapes, and the project tells you which one it is:

```
Single area — most projects                Multiple areas — large projects
/                                          /
├── DOMAIN.md                              ├── DOMAIN-MAP.md
├── docs/decisions/                        ├── docs/decisions/     ← project-wide
│   ├── 0001-stored-order-totals.md        └── src/
│   └── 0002-events-not-http.md                ├── ordering/
└── src/                                       │   ├── DOMAIN.md
                                               │   └── docs/decisions/
                                               └── billing/
                                                   ├── DOMAIN.md
                                                   └── docs/decisions/
```

The same two shapes in a records project — the areas are folders of documents
rather than folders of code, and nothing else changes:

```
/
├── DOMAIN-MAP.md
├── docs/decisions/          ← company-wide
├── payroll/
│   ├── DOMAIN.md
│   └── docs/decisions/
└── legal/
    ├── DOMAIN.md
    └── docs/decisions/
```

Resolve in this order, stopping at the first hit:

| # | Found | Means |
|---|---|---|
| 1 | **`DOMAIN-MAP.md`** at the root | Multiple areas. Read it to find them; it also carries how they relate. |
| 2 | **`DOMAIN.md`** at the root | One area. This is the whole model. |
| 3 | Neither | One area, not yet written. Create it lazily — see §5. |

In a mapped project, infer which area the current topic belongs to from the
material being discussed. If two areas both plausibly own the term, that is
itself a finding: say so and ask, because a term living in two areas with two
meanings is the exact failure the map exists to prevent.

**Only one growth path.** A single `DOMAIN.md` graduates to a `DOMAIN-MAP.md`
plus per-area `DOMAIN.md` files placed next to the material they describe. There
is no `docs/domain/` and no third shape — a model split two different ways is
worse than one that is merely long. Graduate when the single file passes roughly
150 lines *and* its terms fall into clusters that barely reference each other.
Length alone is not the trigger; a long list of tightly related terms is fine.

---

## 2. Sort what you learn

Everything you resolve lands in exactly one of three places.

| Where | What goes there | Test |
|---|---|---|
| **`DOMAIN.md`** | The things the project is about — what they are, what they are called, what kinds they come in, how they relate, what is always true of them | Still true if the whole thing were rebuilt from scratch |
| **`docs/decisions/`** | Hard-to-reverse choices, and deliberate no-s | Only makes sense given this particular setup |
| **Nowhere** | Everything else | Reversible, or already obvious from the material |

Worked, on one subject — a codebase:

- *"A **Shipment** is one physical dispatch from one warehouse. An Order can
  produce several."* → **`DOMAIN.md`**. Logistics, not architecture.
- *"An Order cannot be cancelled once any of its Shipments has dispatched."*
  → **`DOMAIN.md`**. A rule about domain things, true regardless of how it is
  enforced.
- *"Order totals are stored on the row rather than computed from line items."*
  → **a decision record**. Meaningless without this database.
- *"Line items are JSONB because their shape varies by product type."* → **a
  decision record**. The *why* is domain-flavoured, but the statement is about
  storage.
- *"The helper is called `formatMoney`."* → **nowhere**. Reversible, and the
  material says it.

And on one subject in a company's records, where the test works identically:

- *"A **Member** is a person holding equity in the company. An employee is
  **Staff**, never a Member."* → **`DOMAIN.md`**. Company law, true regardless of
  who is currently which. This is also the highest-value kind of entry: in
  ordinary English "member" reads as "member of the team", so the word arrives
  pre-broken and every reader repairs it differently.
- *"A **Fiscal Year** is the twelve months the company reports on. It ends on the
  last day of the year-end month."* → **`DOMAIN.md`**. Definitional.
- *"The year-end month is May — it maximises the first-year tax exemption window
  and avoids the quarter when every accountant is busy."* → **a decision
  record**. Same subject as the line above, opposite side of the test: which
  month was a choice with alternatives.
- *"The registered office is a virtual-office provider on the biweekly forwarding
  plan, not the founder's home."* → **a decision record**. Hard to reverse — it
  is on the public register and moving it is a paid filing.
- *"Scanned certificates live in `legal/docs/`."* → **nowhere**. Reversible, and
  the folder says it.

The third row matters as much as the first two. A model that absorbs everything
stops being read.

---

## 3. During a session

### Challenge on contact

When someone uses a word that conflicts with an entry, say so **in the moment**,
not in a summary at the end. *"`DOMAIN.md` defines a Customer as the party that
pays — you're describing the party the goods go to. Different thing, or does the
definition need to widen?"* Deferred challenges get lost, and by then the wrong
word is in a migration, or in a filing.

### Sharpen fuzzy words

Overloaded words are how two meanings enter a project under one name. Propose a
precise replacement rather than asking an open question: *"You're saying
'account' — that's the Customer in the schema and the login in the UI copy. Which
one do you mean here, and should one of them stop being called account?"*

### Walk one real case, end to end

**The highest-yield question in domain modelling is "tell me about the last real
one, start to finish."** Not a definition request — a narration, in time order,
in the operator's own words: who did what, what arrived, what was produced, what
went wrong that time.

Ask for it whenever you are new to an area, whenever a definition keeps coming
out abstract, or whenever two people plainly mean different things and neither
can say why. It costs one turn and it is the difference between a model built
from what someone *says* the work is and one built from what the work *is*.

Three things fall out of a narration that no amount of asking for definitions
produces:

- **The words they actually use** — including the ones they use without noticing,
  which are the real vocabulary. A term someone reaches for mid-story is settled;
  a term they produce when asked "what do you call it?" is often invented on the
  spot for your benefit.
- **The rules, stated as exceptions.** People do not volunteer invariants; they
  volunteer *"—well, except that time when the invoice came in before the work
  was signed off."* Every "except" in a narration is a rule, and rules are the
  most valuable content in the file (see [DOMAIN-FORMAT.md](DOMAIN-FORMAT.md)).
- **The order of things**, which is where relationships and cardinality live. One
  of these produces several of those; this can't happen before that.

Take the narration, then read it back as entries and rules and let them correct
it. The correction is the model.

### Then stress-test with an invented scenario

A real case gives you the middle. Boundaries only become precise under a case
that sits *on* them, and real life rarely supplies one on demand — so invent it.
*"An Order is cut down after one of its three Shipments dispatched. Is that the
same Order with a reduced total, or the original Order plus a Return?"* The
answer usually decides a relationship, a kind, and a schema column at once —
which is why it is worth the detour. In a records project the same move: *"The
invoice arrives in June but the work was done in May, and the year ends in May.
Which Fiscal Year does it belong to?"*

### Cross-check against the material, in both directions

- **The material contradicts what was said** → surface it. *"You said a Shipment
  can be moved to another Order, but `shipment.order_id` is written once at
  creation and never updated."* Or: *"You said contractors are never Members, but
  `DECISIONS.md` row 5 lists one under Members."* Which is right?
- **An entry no longer appears anywhere** → surface that too. A term nothing
  references is either dead vocabulary to delete, or a concept that got renamed
  in the material and never in the model. Both are findings; neither shows up if
  you only ever check one direction.

This is the direction nobody checks, and it is cheap: grep the term.

### Write when it is resolved, not when it is mentioned

An entry goes in when the answer settles, in that turn. Do not batch — batched
entries get written from memory of the conversation rather than from the
conversation, and the qualifier that made the definition precise is the first
thing to go. Equally: a term merely *mentioned* is not resolved. Unresolved
things go under `## Open questions`, where they are visible without pretending to
be settled.

### Never change a definition silently

Editing an existing entry changes the project's language, and something is
already built on the old reading — code, or a document already sent. Say what you
are changing it from, what breaks if the old meaning was relied on, and get
agreement before writing. Adding a new entry needs no such ceremony.

### Offer decision records sparingly

Two conditions, both required:

1. **Hard to reverse** — changing your mind later costs something real: a
   migration, a fee, a filing, a renegotiation.
2. **A real trade-off** — there were genuine alternatives and one was picked for
   stated reasons.

Either one missing, skip it. **Surprising without context** is not a third
condition — it is what decides *ordering* when several qualify at once, because
the surprising ones are the records someone will actually go looking for. A
decision that is hard to reverse and had real alternatives earns a record whether
or not anyone would be surprised by it. Full guidance and the deliberate-no case
in [DECISION-FORMAT.md](DECISION-FORMAT.md).

---

## 4. What does not belong in `DOMAIN.md`

- **Implementation and filing detail.** No table names, no function names, no
  frameworks, no file paths in a definition — and equally no form numbers, no
  folder layouts, no "which drawer it is in". An entry may *link* to the material
  under `_See_`; it may not be *about* it.

- **Vocabulary the wider world owns.** This is the exclusion that keeps the file
  short, and it has two faces:

  - *General technical vocabulary* — debounce, retry policy, feature flag,
    idempotency. A project can lean on all of them heavily and still not own
    them.
  - *General vocabulary of the field the project operates in* — articles of
    incorporation, withholding tax, GAAP, GDPR, a SAFE. These are statute, or an
    industry's standard instrument. They are not yours, they are the same in
    every project that touches them, and copying them into four `DOMAIN.md` files
    produces four versions that drift.

  The test for both: would someone with general experience of the field, but no
  knowledge of *this project*, need it explained? Only then does it belong.

  **Where several projects need the same external vocabulary, write it once and
  link.** One shared reference — a glossary file in whichever project is its
  natural home — referenced from each `DOMAIN.md` that needs it. Referencing is
  not duplicating: the shared file owns the term, the domain model owns only what
  *this* project does with it. *"The small-business exemption applies to us until
  the Fiscal Year ending May 2028"* is domain; what that exemption *is* is not.

- **Specs and roadmaps.** What the project will do next is a plan. `DOMAIN.md` is
  what it is about.

- **Anything already in `CLAUDE.md` as instruction.** Domain and instruction are
  different genres; duplicating one into the other guarantees they drift apart.
  Note the direction of the fix, though: if vocabulary is currently *living* in
  `CLAUDE.md`, it should move out rather than be copied out — which is the
  **`domain-adopt`** skill's job, not something to start mid-session.

---

## 5. Creating the files

Lazily, and only with content in hand.

- **No `DOMAIN.md`, first term resolved** → create it with that term. Do not
  scaffold empty headings; an empty section is an invitation nobody accepts.
- **No `docs/decisions/`, first decision earned** → create the directory with
  `0001-`.
- **Offer, once, at the end** — never at the start. If a session surfaced terms
  worth keeping and the project has no model, say which terms and offer to start
  the file. Opening with "shall we document the domain first?" converts the work
  the operator asked for into a documentation chore they did not.

### When the project already has the material

Most projects do. The vocabulary is scattered through `CLAUDE.md`, a README, an
`overview.md`, a decisions table, a status file — present, load-bearing, and in
no one place. What they lack is a file holding *only* that, so something can read
only that.

Say so, name a few of the terms you saw, and offer — then stop. Lifting them is a
deliberate one-off pass with its own five-step procedure, and it lives in a
separate skill, **`domain-adopt`**, precisely so it cannot start by accident. It
rewrites `CLAUDE.md` and creates files across the project; that has to be the
session the operator asked for, not a detour inside one.

Your job here is the offer, and the offer belongs at the *end*. If they say yes,
that is the next session.

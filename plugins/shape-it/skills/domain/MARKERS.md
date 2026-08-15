# Using the markers in conversation

The two axes are defined in [SKILL.md](SKILL.md#markers). This file is the rest:
when to mark in ordinary prose, and when not to.

Markers are not report formatting. They are how the project's own language stays
visible while you work — and how the operator can tell, without reading closely,
whether a line needs them.

---

## The four moments

- **Citing an entry.** When you use a term because `DOMAIN.md` defines it, mark
  it 📖 the first time in a turn: *"the 📖 Shipment here is a single dispatch, so
  three of these are three rows."* This is the difference between using the
  project's word and having improvised one that sounds similar.

- **Hitting a conflict.** ⚠️, in the moment, mid-sentence, never saved for a
  summary: *"⚠️ you're using Customer for the delivery address — `DOMAIN.md` has
  it as the paying party."* By the summary the wrong word is already in a
  migration.

- **Making a call that will outlive the conversation.** ⚖️ when you decide
  something that belongs in `docs/decisions/`, whether or not you write the
  record in that turn — so the operator can catch it while it is still cheap.

- **Answering from the model rather than from inference.** ✅ when a question is
  already settled by an entry or a record: *"✅ already decided — 0004 says
  totals are stored."* That is a citation, and it should read as one.

## Three rules against noise

1. **Mark the term, not every noun.** One marker per term per turn, at first use.
   A paragraph with six 📖 in it is a paragraph nobody scans.
2. **Never mark something you have not checked.** 📖 asserts the model actually
   says this. If you are reaching for the word from memory of the conversation,
   it is unmarked prose.
3. **A marker is a claim, so it is falsifiable.** ⚖️ on a reversible choice, or
   ✅ on something merely mentioned, trains the operator to ignore all of them.

## In question headers

`AskUserQuestion` caps a `header` at 12 characters, so use `📖 Domain` and
`⚖️ Decision`. If a header would overflow, **drop the emoji and keep the word** —
never substitute a different glyph. One set, everywhere, or it is not a set.

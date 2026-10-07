---
name: huddle
description: Ask the user a question as a rich page in an agterm HTML overlay instead of the built-in AskUserQuestion tool. Standard components cover choices (up to 9 options, grey subtitles, Recommended badges with reasons, pros/cons, details), answers that are visuals (diagrams, charts, images, wireframes, colour/radius/spacing/type samples), sliders with a live preview for values that are a matter of taste (radius, gap, colour, speed, size), several questions in one page with a review of the answers, and a free-text box on every question; context as markdown, mermaid, charts, stat tiles, tables, code and diffs; keyboard throughout; extendable with HTML, SVG and JavaScript for anything specific to the question. The agent writes a small JSON spec (or one `huddle q` line) and gets the answer back as JSON. Use whenever you need a decision or input from the user while running inside agterm (AGTERM_ENABLED=1), and whenever the user says huddle, "ask me visually", "show me the options", or asks for a question with diagrams, charts, pictures or sliders.
---

# huddle — ask the user with a page, not a prompt

One command opens the question over **your own** agterm session, waits for the answer, and prints it as
JSON. The runtime (layout, styles, charts, diagrams, sliders, keyboard) is prebuilt; you describe the
question.

```bash
H=~/.claude/skills/huddle/scripts/huddle
```

Run it with the Bash tool's `timeout: 600000`. It waits up to 570 s, then exits 4 with the page still open
(see [Waiting](#waiting)).

## Fastest: one line

```bash
$H q "Which store for sessions?" "*Redis|already runs the job queue" "Postgres table|no new service" "Stateless JWT|cannot revoke"
```

Each option is `Label|subtitle`, a leading `*` marks it recommended. `--multi` for multi-select,
`--context "markdown"` for a paragraph under the question, `--title` for the topic line above it.

## Normal: a JSON spec on stdin

```bash
$H - <<'JSON'
{
  "title": "Session storage",
  "prompt": "Where should sessions live?",
  "context": "Sessions live in process memory, so every deploy logs everyone out.",
  "options": [
    {"id": "redis", "label": "Redis", "subtitle": "Managed, TTL per key",
     "recommended": "Already running for the job queue",
     "pros": ["Sub-ms reads"], "cons": ["Another moving part"]},
    {"id": "pg", "label": "Postgres table", "subtitle": "One table, expiry index"}
  ]
}
JSON
```

## Write the question first

The prompt is the biggest thing on the page; everything else supports it.

- `prompt`: **one short, direct question**, ideally under 12 words, ending in `?` or an imperative
  ("Tune the card style until it looks right"). The user should know what to do from it alone.
- `title`: the topic in two to five words ("Session storage"). Shown small above the prompt.
- `hint`: one line under the prompt saying what matters or how to answer. Not a second question.
- `context` / `body`: the evidence — numbers, a diagram, a diff. Shown under the prompt.
- `header`: one or two words per question, for the tabs and the review list.

## Pick the component for the question

| The answer is… | Use | Template |
| --- | --- | --- |
| one of a few alternatives | options, `layout: "list"` | `pick` |
| alternatives whose trade-offs matter | `layout: "compare"` (side by side, pros/cons visible) | `tradeoffs` |
| a visual (a diagram, a layout, a sample) | options with `preview` → `grid` | `architecture`, `layouts`, `design-tokens` |
| yes / no / later | `layout: "inline"` | `confirm` |
| several items from a list | `mode: "multi"`, `min`/`max` | `checklist` |
| a number or colour that is a matter of taste, with no standard step to choose from (radius, gap, hue, speed, size, weight, delay) | **`controls`** — sliders with a live preview | `tune` |
| words | `mode: "text"` | `text` |
| several related decisions | `questions: [...]` — tabs, then a review of every answer | `design-tokens` |

When there *are* standard values (4/8/16 px, a design-system scale), offer them as options with previews.
When the value is continuous or purely taste, give sliders: the user sees the result while dragging.
Combine them: options to pick a direction, then a `controls` question to fine-tune it (see `demos/ui-kit`).

`$H templates` lists the templates (`~/.claude/skills/huddle/templates/<name>.json`); copy one and fill it.
`$H demo NAME` opens one, as do the larger showcases in `demos/` (`motion`, `ui-kit`, `auth-flow`,
`rollout`, `pricing`) — read those for combinations.

## The answer

```json
{"status": "answered", "pageID": "…",
 "answers": {"answer": {"selected": ["redis"], "labels": ["Redis"], "text": "but only for prod"}}}
```

- `answers` is keyed by question id (`answer` for a single-question spec, `q1`, `q2`… when unnamed).
- `selected` lists option ids in display order; `text` is present only when the user typed something —
  it may come **alone** (their own answer) or **with** a selection (a note on it). Read both.
- A `controls` question adds `values` (`{"radius": 12, "hue": 174, "shadow": true}`). `selected` holds a
  preset only if the user kept it untouched; `from` names the preset they started from and then changed.
- `extra` appears when page JavaScript called `api.setExtra(...)`.
- Exit 0 `status: "chat"` (with `text`): the user pressed **Discuss in chat** — they want to talk it
  through in the terminal. Stop and ask there; do not pick for them.
- Exit 2 `status: "dismissed"`: closed unanswered (⌘W). Treat as "not now": don't re-open the same
  question in a loop; say what you need in the terminal.
- Exit 3: not inside agterm and no browser fallback — use AskUserQuestion.

## Spec reference

Top level: `title`, `subtitle`, `source` (replaces "Claude is asking"), `context` (blocks),
`width: "narrow"` (for short questions), `submitLabel`, `chat: false` (hide Discuss in chat), `script`
(JS, see [Extending](#extending)), `style`, `review`, `size` (see [Look, size and review](#look-size-and-review)),
and **either** the fields of one question **or** `questions: [...]` (tabs, answered in order).

Question: `id`, `header`, `prompt`, `hint`, `body` (blocks), `recommendation` (markdown banner naming the
overall pick), `mode` (`single` default · `multi` · `text`; `tune` is implied by `controls`), `min`/`max`
(multi), `layout` (`list` · `grid` · `compare` · `inline`; default `grid` when any option has a
`preview`, `inline` for presets, else `list`), `columns`, `expanded: true` (open every option's details),
`optional: true` (may submit empty), `text` (`false` to drop the free-text box, or
`{label, placeholder, required, multiline, value}`).

Option: `id`, `label`, `subtitle` (grey line), `recommended` (`true`, or a string = the reason, shown
under it), `badge` (replaces the "Recommended" word), `tags` (small chips: effort, risk), `pros`, `cons`,
`detail` (blocks, behind "details"), `preview` (a block shown as the card's visual), `default: true`
(preselected), `values` (on a `controls` question: a preset). Strings may stand in for options:
`"options": ["Yes", "No"]`.

### Controls (sliders with a live preview)

```json
{
  "title": "Dashboard cards",
  "prompt": "Tune the card style until it looks right",
  "controls": [
    {"id": "radius", "label": "Corner radius", "min": 0, "max": 28, "value": 8, "unit": "px"},
    {"id": "hue", "label": "Accent", "type": "hue", "value": 220},
    {"id": "speed", "label": "Duration", "min": 100, "max": 1200, "step": 20, "value": 300, "unit": "ms"},
    {"id": "weight", "label": "Title weight", "type": "select", "options": ["500", "600", "700"], "value": "600"},
    {"id": "shadow", "label": "Shadow", "type": "toggle", "value": false, "on": "0 6px 18px rgba(0,0,0,.3)", "off": "none"},
    {"id": "brand", "label": "Brand colour", "type": "color", "value": "#0d9488"}
  ],
  "preview": {"html": "<div style='border-radius:var(--radius);background:hsl({hue} 65% 45%);box-shadow:{shadow};font-weight:{weight};transition:all var(--speed)'>Sample</div>"},
  "baseline": true,
  "options": [{"id": "soft", "label": "Soft", "values": {"radius": 14, "shadow": true}}]
}
```

- Control `type`: `range` (default; `min`, `max`, `step`, `unit`) · `hue` (0–360, rainbow track) ·
  `color` (picker, `#rrggbb`) · `select` (segmented, `options`) · `toggle` (`on`/`off` are the strings it
  substitutes; default `"1"`/`"0"`).
- In `preview` (any block), `{id}` is replaced by the raw value (`12`, `#0d9488`, `600`) and `var(--id)`
  carries the unit (`12px`, `300ms`). The preview re-renders on every change, which also replays CSS
  animations; `r` or the ⟳ button replays without a change.
- `baseline: true` (or a label string) shows the starting values beside the live one ("Now" | "Yours").
- `options` with `values` are presets: picking one moves the sliders.
- Each slider has ↺ to return to its starting value.
- Optional linking: a `preview` may read earlier answers on the same page — `{@qid}` is the option id
  chosen on question `qid` (comma-joined for multi), `{@qid.label}` its label, `{@qid.ctl}` a slider value
  from another controls question. Use it when the fine-tuning should apply to what was just picked
  (`demos/motion`); skip it when the questions are independent.

### Blocks

Used in `context`, `body`, `detail`, `preview`. A plain string is markdown (`**bold**`, `*em*`,
`` `code` ``, lists, `> quote`, `[link](https://…)`, fenced code). Any block takes `title`, `caption` and
`card: true`.

| Block | Shape |
| --- | --- |
| markdown | `"text"` or `{"md": "text"}` |
| diagram | `{"mermaid": "flowchart LR\n A --> B"}` — any mermaid type (flowchart, sequence, class, state, ER, gantt, gitGraph). In labels avoid `#` (starts an entity: `#1` truncates the line) and `%` (comment marker in gantt); add `todayMarker off` to a gantt |
| chart | `{"chart": {"type": "bar"\|"line"\|"area"\|"hbar"\|"donut"\|"pie", "labels": [...], "series": [{"name", "values"}], "unit": " ms", "marks": [{"value", "label"}], "highlight": 0}}` — `values` alone for one series |
| stat tiles | `{"stats": [{"label", "value", "delta", "good": true\|false\|null, "sub"}]}` |
| image | `{"image": "/abs/or/relative.png", "height": 160, "fit": "cover"}` — local files are embedded automatically |
| code / diff | `{"code": "…", "lang": "ts"}`, `{"diff": "@@ …\n+added\n-removed"}` |
| table | `{"table": {"columns": [...], "rows": [[...]]}}`, `{"kv": {"key": "value"}}` |
| callout | `{"callout": "markdown", "tone": "ok"\|"warn"\|"bad"}` |
| design samples | `{"radius": 12}`, `{"gap": 16, "items": 4, "direction": "column"}`, `{"colors": ["#hex", {"name", "value"}]}`, `{"type": {"family", "size", "weight", "tracking", "text"}}`, `{"style": {css}, "text": "…"}` |
| layout | `{"row": [block, block]}` side by side; a list of blocks stacks |
| svg / html / js | see [Extending](#extending) |

## Extending

The standard components cover most questions. When a question needs something they don't — a real
component rendered in the user's product style, an animation, typography in a particular script, a
filterable list — build it into that question, not into the skill:

- `{"html": "…"}` / `{"svg": "…"}` — raw markup as a block or an option's `preview`. `<style>` and CSS
  animations work. Use the theme variables inside `style=`: `--fg`, `--bg`, `--accent`, `--ok`,
  `--warn`, `--bad`, `--magenta`, `--cyan`, `--muted`, `--line`, `--line-strong`, `--panel`, `--panel-2`.
  They follow the user's terminal theme; hardcode colours only when the colour *is* the question.
- `{"js": "code"}` — runs as `function(el, api)`; draw into `el`. The top-level `script` runs once with
  `api`. `api.setExtra(questionId, value)` (returned as `extra`), `api.setText(questionId, text)`,
  `api.select(questionId, optionId)`, `api.submit()`, `api.block(spec)` / `api.chart(spec)` (render a
  standard block), `api.md(text)`, `api.css("--accent")` (resolved colour).
- Prefer `controls` over hand-written sliders: they come with keyboard, reset, presets, baseline and the
  review screen for free.
- Escape nothing in normal fields — the runtime escapes text. `html`, `svg` and `js` are raw: never paste
  outside text (an issue body, a log line) into them; put it in markdown or `code` instead.

## How the user answers

`1`–`9` choose (toggle in multi; presets on a controls question) · arrows / `hjkl` move · `Space` picks
· `Enter` submits (or next question, or the review) · `Tab` or `/` jumps into the text box, `Esc` leaves
it, `⌘Enter` sends from it · on a controls question `↓` enters the sliders, `↑`/`↓` move between them,
`←`/`→` adjust, `r` replays · `[` `]` switch questions · `e` / `E` details · `⌥Enter` Discuss in chat ·
`?` shows every key · double-click an option to choose and submit · ⌘W dismisses. On the review screen:
`⏎` sends, `1`–`9` jumps back to that question, `Esc` returns.

## Look, size and review

The user's defaults live in `defaults.json` beside this file (style `refined`, a floating panel at 90% of
the session, review `auto`). Leave them alone unless a question needs otherwise; override per call with a
flag or per spec with the same key:

- `style`: `refined` (soft cards) · `minimal` (hairline rows) · `bold` (big type, filled choice) ·
  `terminal` (monospace). `--style NAME`.
- `size`: percent of the session pane as a floating panel, `"auto"` (66–90% by content) or `"full"`.
  `--size N`, `--full`.
- `review`: the answer list shown before sending — each choice, a thumbnail of a visual one, slider
  values with the live preview, and the user's note. `auto` = when the page has several questions, or a
  note was typed on a choice question · `always` · `never`. `--review MODE`. Question tabs also show the
  answer so far ("Radius · 14 px + note").

## Behaviour you can rely on

- Opens over **your** session (`$AGTERM_SESSION_ID`), never the one the user is looking at, and does not
  switch them to it unless you pass `--follow`. While it waits, the sidebar shows the amber blinking
  "asking" triangle (the same glyph a built-in question gets); it goes back to "working" when answered.
  `--no-status` leaves the glyph alone.
- `--chromeless` hides the overlay's title strip.
- Outside agterm it serves the page on `127.0.0.1` and opens the default browser; the answer comes back
  the same way. `--browser` forces that path inside agterm.
- Mermaid is downloaded once to `~/.cache/huddle/` on first use; offline, diagrams show as source.
- Generated pages land in `$TMPDIR/huddle/` and are pruned after a day. `$H render spec.json -o out.html`
  builds one without opening it (for checking a spec).

## Waiting

Default wait is 570 s so it fits one Bash call. When it exits 4 with `"status": "pending"`, the page is
still up: run `$H wait <pageID>` to keep waiting. For a question the user may take long over, run
`$H … --no-wait` (prints the `pageID` at once) and later `$H wait <pageID>`, or run the whole command with
the Bash tool's `run_in_background: true` — you are notified when the user answers. In the background,
add `--timeout 86400`: the 570 s default exists only for foreground calls. A timed-out wait leaves the
"asking" glyph up, since the question is still open.

## Recommending

- Recommend when you have a view, and say **why** in the `recommended` string; mark more than one when
  more than one is genuinely good. Use `recommendation` for a one-line verdict above the options.
- Up to 6 options reads well; 7–9 only for lists of peers (versions, files).
- Subtitles carry the one fact that distinguishes an option; pros/cons carry the rest.
- Batch related questions into one page (`questions`) rather than opening several in a row.

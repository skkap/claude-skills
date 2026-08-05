# claude-skills

Claude Code skills I use across projects. Project-agnostic by design — anything
specific to a codebase lives in that codebase, not here.

## Install

```
/plugin marketplace add skkap/claude-skills
/plugin install fly@skkap-skills
```

## Skills

### `fly` — ship the current work as a green PR

Reads the repo's `CHECKS.md`, branches off the default branch, runs every check
that matches what changed, fixes what breaks, commits, pushes, and opens or
updates the pull request.

Two things it does differently:

**The repo owns what "green" means.** The check list isn't re-inferred from CI
config on every run — it's a file the repo carries, `CHECKS.md`, readable by
people and agents alike. No `CHECKS.md`? It derives the checks from CI workflows,
`CLAUDE.md`, or the toolchain, says in its report that it had to, and offers to
write the file so the next run is cheap and deterministic.

**Local checks are the gate; CI is the audit.** It finishes when the PR is open.
It takes one instant read of CI status on the way out and stops — no `gh run
watch`, no poll loop. Waiting on CI blocks indefinitely on a queued run, an
approval gate, or a workflow a path filter meant never to start, and watching
"the latest run" in a repo with several PR workflows is wrong more often than
it's right.

A CI failure that the local run should have caught is treated as a `CHECKS.md`
defect, fixed in the same PR.

#### `CHECKS.md`

One file at the repo root, one section per independently-scoped component:

````markdown
## 🖥️ Server
When: `server/**`
Dir: `server`
Setup: `poetry install --no-interaction`
Fix: `poetry run ruff format src tests`

```bash
poetry run ruff format --check src tests
poetry run lint
poetry run typecheck
poetry run pytest tests/ -n 4 --no-cov -q --tb=short
```
````

`When:` scopes it to what changed, `Setup:` guards against the stale-environment
"green locally, red in CI" split, `Fix:` makes formatter failures deterministic
instead of a guess. Full grammar in
[reference.md](plugins/fly/skills/fly/reference.md); writing one for an existing
repo in [adopting-a-repo.md](plugins/fly/skills/fly/adopting-a-repo.md).

## License

MIT

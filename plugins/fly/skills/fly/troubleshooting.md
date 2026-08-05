# Troubleshooting

## Preflight

**`origin/HEAD` is unset** — `git symbolic-ref refs/remotes/origin/HEAD` returns
nothing, so the default branch can't be resolved. Common on shallow clones and old
checkouts.

```bash
git remote set-head origin --auto
```

Do not substitute `git remote show origin`. It's a network call: it hangs offline,
behind a proxy, and on a VPN that's half up — turning a local operation into an
indefinite stall.

**Detached HEAD** — stop. Committing here produces work reachable from nothing.
Ask which branch it should land on; `git switch -c <name>` only once that's answered.

**`gh` not authenticated** — `gh auth status` fails. Everything through §5 still
works; §6 onward doesn't. Run the local checks and commit, then stop and report
that the PR needs `gh auth login`. Don't push a branch you can't open a PR for
without saying so.

**No `origin`** — a local-only repo. Checks and commit still apply. Say clearly
that nothing was pushed.

## Checks

**A check needs a service that isn't running.** Docker down, no database, no
fixture container. `Needs:` documents this but doesn't enforce it. Report it as a
**failed** check with the missing precondition named — never as a skip. "Tests
skipped because Docker was down" reported as green is precisely the lie the report
contract exists to prevent.

**A check is flaky.** Re-run once. If it passes, say so in the report — a flake
that's silently retried into green is a flake nobody ever fixes. If it fails again,
treat it as a real failure. Never quarantine a test to get a green run.

**A check hangs.** The `Timeout:` budget fires and it's reported as a failure with
the elapsed time. If it hangs reproducibly, that's a finding worth reporting, not
worth waiting out — the default 15m already errs generous.

**`Setup:` fails.** Fail the whole section; don't run its checks against a stale
environment. A lockfile that won't install is usually a real defect on the branch,
not an environment quirk to work around.

**The fix budget ran out.** Two attempts past `Fix:`, still red. Stop. Report the
failing command, the relevant output, and what was tried. A third and fourth
attempt on a check that isn't converging rarely converges — and it buries the
output that would let someone else solve it in one look.

## Push and PR

**Protected branch rejects the push.** Expected on a default branch — that's the
protection working. Create a feature branch and push that. Never `--force`, never
`--no-verify`.

**A PR already exists.** Update it (`gh pr edit`), don't open a second. Its
description must cover **all** commits on the branch, not just the newest.

**The PR is closed or merged, but the branch has new commits.** Don't reopen and
don't force a new PR onto the same branch silently. Say what's there and ask.

**Push rejected as non-fast-forward.** The remote branch has commits yours doesn't
— usually another machine or a teammate. Do not force-push. Fetch, look at what's
there, and report it. Resolving this is a decision, not a step.

## CI

**`gh pr checks` exits 8.** That's "pending", not an error. Report the pending
count and finish. Do not add `--watch`; do not loop.

**`gh pr checks` reports no checks at all.** Usually path filters — the change
touched nothing any workflow subscribes to. Worth one line in the report ("no
workflows subscribe to these paths"), because it's occasionally a *mistake* in the
filters rather than a correct skip.

**CI failed on something the local run passed.** The interesting case, and the one
with a defined response:

1. Read the actual failure — `gh run view <id> --log-failed`. Never guess from a
   job name.
2. Fix the code.
3. **Add the missing check to `CHECKS.md`, in the same PR.** This is the step that
   makes the loop close. Without it, the same gap recurs on the next branch.

Common causes worth checking first: CI installs from the lockfile while you
installed incrementally; CI runs a matrix lane for a platform you don't build; CI
runs a repo-level guard script that lives outside every app's toolchain; a build
step exists in CI and not locally.

**CI is red on master too.** Then it isn't your branch. Say so and stop — don't
absorb an unrelated breakage into this PR.

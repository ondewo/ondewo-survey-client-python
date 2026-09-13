# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Working Principles

Behavioral guidelines to reduce common mistakes. They bias toward caution over speed; for trivial tasks, use judgment.

### Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### Surgical changes

Touch only what you must. Clean up only your own mess.

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that _your_ changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: every changed line should trace directly to the user's request.

### Goal-driven execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and
clarifying questions come before implementation rather than after mistakes.

## Logging

```python
from loguru import logger as log
```

- **Levels:** `log.trace()`, `log.debug()`, `log.info()`, `log.warning()`, `log.error()`, `log.exception()`. Choose by
  hotness/verbosity — `trace` for per-token / hot-path detail, `debug` for routine method entry/exit, `info` for notable
  lifecycle events, `warning` / `error` / `exception` for problems.
- **Interpolate with f-strings, not loguru's `{}` positional args.** Consistent with the Code Style rule, use
  `f"…{value}"`; only add the `f` prefix when the string actually interpolates (`"START: …"` with no params stays a
  plain string).
- **`START:` / `DONE:` bracketing.** Wrap a method (or other notable operation) with a `START:` line at entry and a
  `DONE:` line at exit, both naming `ClassName: method_name` (append `: param={value}` context where useful):

  ```python
  log.debug("START: IntentBertClassifier: predict")
  ...
  log.debug(f"DONE: IntentBertClassifier: predict. Elapsed time: {perf_counter() - start_time:.5f}")
  ```

- **Timing uses `perf_counter()`, rendered `:.5f`.** Measure elapsed time with `time.perf_counter()` captured as a start
  value and subtracted at the `DONE:` line; always format the elapsed value with the `:.5f` spec:

  ```python
  from time import perf_counter

  start_time: float = perf_counter()
  ...
  log.info(f"DONE: SESSION SERVICER: DetectIntent. Elapsed time: {perf_counter() - start_time:.5f}")
  ```

  Never measure a duration with `time.time()` — reserve `time.time()` for wall-clock timestamps (epoch seconds persisted
  to a DB / proto, unique-id or filename stamps). `perf_counter()` has an undefined epoch and must not be stored or
  compared across processes.

## Docstrings

Google-style, triple double-quotes:

```python
"""
Short imperative summary line.

Args:
    param_name (type):
        Description of the parameter.

Returns:
    type:
        Description of the return value.

Raises:
    ExceptionType:
        When this exception is raised.
"""
```

## Git Commits

- **Never include Claude as author or co-author** in commit messages, PR descriptions, or any other text. Do not add
  `Co-Authored-By: Claude…` trailers, "Generated with Claude Code" footers, or any similar attribution.
- The user's own git author identity (already configured in git) is the only identity that should appear on commits.
- This rule overrides the default Claude Code commit-template guidance.
- **Never prepend the JIRA ticket ID** (e.g. `[OND211-2386]`) to the commit subject yourself. The `giticket` pre-commit
  hook reads the ticket from the branch name (`(feature|bugfix|support|hotfix)/<TICKET>-…`) and prepends `[<ticket>]`
  (with a trailing space) automatically. Writing the prefix manually produces a duplicate like
  `[OND211-2386] [OND211-2386] feat: …`. Write the subject as plain Conventional Commits (`feat: …`, `fix(scope): …`,
  `docs(types): …`) and let the hook add the prefix on commit.

## General Principles

- Follow existing patterns before introducing new abstractions.
- Keep changes minimal and consistent with surrounding code.
- Validate inputs early with descriptive, context-rich error messages.
- Use context managers for files, sockets, and thread pools.
- Prefer region comments for grouping methods in files that already use them.
- End edited Markdown and YAML files with a trailing newline.

## Release gotchas (hard-won this session)

These bit us during the 6.14.0 release. Keep them in mind when releasing.

- **Trust the registry, not the log.** `make release_all_clients` wraps each client in `|| echo "Already released …"`, so a _failed_ release is reported as "done". After any release, verify the GitHub release **and** the published package (PyPI / npm) directly.
- **`npm install failed after 5 attempts` in a release log is usually a red herring** — that text is the echo _inside_ the docker `RUN for i in 1..5; do npm install …` retry loop, not a real failure (`npm install` succeeds → `#10 DONE`). Look further down for the real error (a TTY error, an eslint failure, a `setup.py` error).
- **Codegen must run TTY-free.** The `docker run` that invokes the proto-compiler must not pass `-it` — non-interactively it fails with `cannot attach stdin to a TTY-enabled container because stdin is not a terminal`. Fix the script (drop `-it`), or run the whole release under a pseudo-TTY: `script -qc 'make …' /dev/null`.
- **Release Makefiles print secrets.** Some `docker run … -e <TOKEN>=…` recipe lines lack a leading `@`, so `make` echoes the expanded token. Rotate any token printed during a release; fix by prefixing the recipe line with `@`.
- The release auto-pulls the **latest** `ondewo-proto-compiler` tag.
- **npm package names are inconsistent** — e.g. the JS client publishes as `@ondewo/ondewo-nlu-client-js` (double `ondewo`), not `@ondewo/nlu-client-js`. Check `src/package.json`'s `name` before querying npm.
- **PyPI build needs setuptools.** The release image (`Dockerfile.utils`) is `python:3.12-slim`, which bundles no `setuptools`, so `python setup.py sdist bdist_wheel` dies with `ModuleNotFoundError: No module named 'setuptools'`. `Dockerfile.utils` must `pip install … setuptools wheel`.

## Python tooling — uv + ruff + mypy + pyproject.toml (this session's refactor)

This repo was migrated off `setup.py` / `.flake8` / `mypy.ini` to a single **pyproject.toml** with **uv**, **ruff**, and **mypy**. Going forward:

- **Build backend stays setuptools** (for PyPI compatibility). Build with `python -m build --no-isolation` or `uv build` — NOT `python setup.py sdist bdist_wheel` (setup.py is deleted). `Dockerfile.utils` installs `twine setuptools wheel build`.
- **Dependencies via uv + a committed `uv.lock`.** CI runs `uv sync --extra dev --frozen`. To add/change a dep: edit `[project.dependencies]`/`[project.optional-dependencies].dev` in pyproject.toml then `uv lock`.
- **Lint is ruff** (`[tool.ruff]`, line-length 120, generated `*_pb2*` excluded) — `uv run ruff check .`. flake8 is gone.
- **mypy config lives in `[tool.mypy]`.** Do **NOT** re-create `mypy.ini` — it silently _shadows_ the pyproject config. Generated `*_pb2*` modules get `ignore_errors` overrides.
- **Do NOT re-add `setup.py`** — with setuptools>=61 it conflicts with `[project]` on duplicated metadata.
- **PEP 625**: the sdist is now underscore-normalised (`ondewo_<name>-<v>.tar.gz`); anything that greps the tarball name by hand must use underscores.
- The version-bump release target edits the version in **pyproject.toml** (not setup.py); the release stages `pyproject.toml uv.lock`.

## uv migration — completed conversion (this session)

The repo is now fully on **uv** (not just pyproject.toml):

- `make setup_developer_environment_locally` bootstraps uv (installs it if missing), runs `uv sync --extra dev` (creates `.venv` + installs all runtime+dev deps + pre-commit), then `uv run pre-commit install`. **No conda** — the old `create_conda_env`/`setup_conda_env` scaffolding was removed.
- Every Makefile target uses uv: `uv sync --extra dev` (deps), `uv run pytest`/`ruff`/`mypy` (tools), `uv build` (wheel). No `pip install`, no `python -m build`, no `python setup.py`.
- New targets: `make ruff` / `make ruff_fix` / `make ruff_format` / `make mypy`. The `flake8` target is **removed**.
- Removed for good: `requirements.txt`, `requirements-dev.txt`, `setup.cfg` — deps + tool config live in `pyproject.toml`. Do **not** re-add them.
- `Dockerfile.utils` installs uv (`COPY --from=ghcr.io/astral-sh/uv`) and builds with uv; it no longer `COPY`s `requirements.txt`.
- **`[tool.mypy] python_version` must be `3.12`** wherever numpy 2.x is on the mypy path — its PEP-695 `type X = …` stubs fail to parse on < 3.12.
- The release `git commit` uses **`--no-verify`** so pre-commit hooks never gate an automated release.
- **Validated by a real PyPI publish** — `ondewo-t2s-client 6.5.0` was built with `uv build` and uploaded via twine end-to-end; the uv release pipeline works.

## GitHub Actions — `tests` is a REQUIRED gate, not advisory

`.github/workflows/tests.yml` (job `unit-tests`) runs on **every push to every branch** (`branches: ["**"]`) and on
every pull request. Its four checking steps all block: a frozen `uv sync`, `ruff`, `mypy`, and a pytest run carrying
`--cov-fail-under=100`. Treat a red run as a broken build, and reproduce it locally **before** pushing.

- **Check the real run, don't guess** — there is no `gh` CLI on the dev boxes, so ask the API for the checked-out SHA:

  ```bash
  SHA=$(git rev-parse HEAD)
  curl -s "https://api.github.com/repos/ondewo/ondewo-survey-client-python/actions/runs?head_sha=$SHA" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['total_count'], [(r['run_number'], r['status'], r['conclusion']) for r in d['workflow_runs']])"
  ```

  `total_count: 0` means **no run exists for that commit** (never pushed, or the run was deleted) — which is not the
  same as "it passed", and must never be reported as green.

- **The exact local reproduction, copied from the workflow — `--frozen` and all:**

  ```bash
  uv python install 3.12
  uv sync --extra dev --frozen
  uv run --frozen ruff check .
  uv run --frozen mypy ondewo
  uv run --frozen pytest tests/unit -q \
    --cov=ondewo.survey.utils.keycloak \
    --cov=ondewo.survey.client.client_config \
    --cov=ondewo.survey.client.client \
    --cov=ondewo.survey.client.async_client \
    --cov=ondewo.survey.client.services_interface \
    --cov=ondewo.survey.client.async_services_interface \
    --cov-report=term-missing \
    --cov-report=xml \
    --cov-fail-under=100
  ```

  The `make ruff` / `make mypy` / `make test` targets are close but **not** the gate — copy the commands from the
  workflow file rather than approximating them, and keep every `--cov=` argument: dropping one silently shrinks the
  measured set (see the fail-open note below).

- **Never drop `--frozen`.** A non-frozen `uv sync` / `uv run` re-resolves dependencies on the fly, so it installs a
  set `uv.lock` does not describe and a stale lock passes locally and fails in CI. `uv sync --extra dev --frozen` is
  therefore also the assertion that `uv.lock` still matches `pyproject.toml` — after editing `[project.dependencies]`
  or the `dev` extra, run `uv lock` (the `uv-lock` pre-commit hook does the same) or this step fails first.

- **The coverage gate uses dotted `--cov=<module>` arguments, and that form FAILS OPEN — measured here.** Naming a
  module that the suite never imports does **not** score it 0 %; it vanishes from the table entirely, leaving only
  `CoverageWarning: Module <name> was never imported. (module-not-imported)`, and `--cov-fail-under=100` is then
  computed over what is left — so the gate reports 100 % while measuring less than it claims. Consequences:
  - That warning line is the only signal. A `module-not-imported` warning in the CI log means the gate silently
    stopped covering something; fix the import (or the module path), never the threshold.
  - The gate covers **exactly the six modules listed** — the Keycloak/D18 auth helper plus client/config/interfaces.
    That is deliberate (the repo is ~95 % generated `*_pb2*` stubs), but it means a new hand-written module is
    ungated until someone adds a `--cov=` line for it. Adding the module to the workflow is part of adding the module.
  - The filesystem-scanned counter-check is the **package** form, which does report unimported files at 0 %:
    `uv run --frozen pytest tests/unit -q --cov=ondewo --cov-report=term-missing`. Today it shows the four thin
    service wrappers `ondewo/survey/client/services/{async_,}{fhir,survey}.py` at 71 % — outside the gate by design,
    not a regression.

- **There is no `.python-version`, so a local `uv sync` grabs the newest interpreter it can find while CI runs 3.12.**
  Locally that resolved to 3.14.6. Pin the interpreter for a faithful run: `uv sync --extra dev --frozen -p 3.12` and
  `uv run --frozen -p 3.12 …` (point `UV_PROJECT_ENVIRONMENT` at a scratch path to keep your everyday `.venv`). This
  is not cosmetic for a 100 % gate — **the set of lines it measures is interpreter-dependent**: coverage counts 144
  statements in `ondewo/survey/utils/keycloak.py` on 3.12 and 143 on 3.14, because PEP 649 deferred annotations make
  the bare `status_code: int` annotation in the `TokenResponse` Protocol no longer an executed statement on 3.14.
  Both are at 100 % today, but a line that only exists on CI's interpreter can only fail on CI's interpreter.

## Releasing: preflight and the traps that have actually bitten

Written after a release program across every ONDEWO client in one session. Each item below
cost real time or a broken artefact; every statement is derived from THIS repo's Makefile.

### Before you touch the version, check the released tag is in `master`

Releases here are cut from a `release/<version>` branch and are **not always merged back**, so
`master` can be missing work that is already published — and because a later version number
sorts above the unmerged one, a consumer upgrading silently loses it. The ondewo-nlu-client-python
7.1.0 release was exactly this: it shipped from a `master` that had never seen 7.0.5's
offline-token hand-off, so PyPI's newest release was a regression against its predecessor.

```bash
latest=$(git tag --sort=-v:refname | head -1)
git merge-base --is-ancestor "$latest" master && echo "in master" || echo "NOT in master -- merge first"
```

A fast-forward (`git merge --ff-only <tag>`) is the common case. A true merge needs care: resolve
metadata toward `master` and keep BOTH release-note sections, newest first — a reader upgrading
from the older line still needs the older entry.

### `git add` on a dirty submodule stages the WRONG commit

This repo has submodules (`ondewo-proto-compiler`, `ondewo-survey-api`). If a submodule's working
tree is dirty, `git add <submodule>` stages **its current HEAD**, not the pointer you resolved
during a merge — silently regressing it to an older commit. `git checkout master -- <submodule>`
fixes the index but the next `git add` re-breaks it. Move the working tree instead:

```bash
want=$(git ls-tree master <submodule> | awk '{print $3}')
git -C <submodule> checkout -q "$want" && git add <submodule>
```

### The release notes are sliced by an EXACTLY-CASED heading

`CURRENT_RELEASE_NOTES` slices `RELEASE.md` with a perl range. In THIS repo the opening
pattern is, verbatim:

```text
Release ONDEWO Survey Python Client ${ONDEWO_SURVEY_VERSION}
```

So the heading of a new entry must read exactly `## Release ONDEWO Survey Python Client <version>`. **This wording is
not consistent across the ONDEWO repos** — some say `... <Name> Client`, some `... Client
<Name>` with the words reversed, the API repos say `... API` with no `Client` at all, and the
casing varies (`Js`, `Nodejs`, `Typescript`, `Survey`). Do not carry a heading over from a
sibling repo. Copy the PREVIOUS entry in this file and change only the version, or read the
pattern above out of the Makefile.

A heading that does not match yields an **empty slice**, and the GitHub release is then
created with empty notes or fails outright. Verify before releasing:

```bash
grep -c '^## Release ONDEWO Survey Python Client ' RELEASE.md     # must be >= 1 for your new version
```

### Publish order decides how a partial failure is recovered

`make release` in this repo runs:

1. `create_release_branch`
2. `create_release_tag`
3. `release_to_github_via_docker`
4. `push_to_pypi_via_docker`
5. `push_to_pypi`

The **PyPI publish happens LAST**. So a failure before it means nothing shipped, but the
branch, tag and GitHub release may already exist — and `spc` will then refuse a re-run. Recover
by running only the remaining step, not the whole target.

### Verify against the registry, with the REAL package name

This package publishes as **`ondewo-survey-client`**, which is not always the repository name — the JS client
publishes as `@ondewo/ondewo-nlu-client-js` (doubled `ondewo`), so a lookup by repo name returns
a 404 that reads like a failed release. Check the name in the manifest first, then:

```bash
curl -s https://pypi.org/pypi/ondewo-survey-client/json | python3 -c "import sys,json;print(json.load(sys.stdin)['info']['version'])"
```

### The `mypy` pre-commit hook is `language: system`

It runs whatever `mypy` is on `PATH`, so a `git commit` outside the project venv fails with
`Executable mypy not found` even though `uv run mypy` passes. Commit with the venv on `PATH`
rather than reaching for `--no-verify`:

```bash
PATH="$PWD/.venv/bin:$PATH" git commit -m "..."
```

### The release prints credentials — read the log BEFORE you scrub it

`make ondewo_release` clones `ondewo-devops-accounts` and passes the registry and GitHub tokens on
the make command line, so they are echoed into the console and into any transcript capturing it.
This is a known and accepted property of the shared release path: do **not** re-plumb the recipe.
Redirect the run to a file, read it through a filter, and shred the file afterwards — and read it
**before** shredding, or a genuine failure is lost with the secrets:

```bash
umask 077; make ondewo_release > /tmp/rel.log 2>&1; echo "RC=$?"
grep -avE 'TOKEN|PASSWORD|USERNAME|_authToken' /tmp/rel.log | tail -20   # read FIRST
shred -u /tmp/rel.log; rm -rf ondewo-devops-accounts                     # then scrub
```

### Run the release from `master`, and check with `git branch --show-current`

A release ends by checking out `release/<version>`, and **nothing checks you out back**. Start the
next release from that leftover checkout and `git commit` + `git push` land on the OLD release
branch: the new `release/<version>` is cut from it, the tag points into it, and `master` never sees
the release at all. Measured on ondewo-csi-client-typescript 5.5.1 -- npm had it, the tag had it,
and `origin/master` was still at 5.5.0. Recovery was a fast-forward (`git merge --ff-only
release/5.5.1`), which worked only because nothing else had moved; a diverged `master` needs a real
merge.

```bash
git branch --show-current            # must print master BEFORE `make ondewo_release`
```

### The release `git add` list is an ALLOW-LIST, so anything outside it ships but is never committed

`make build` writes files the release target then stages from a fixed list of paths. Anything the
build touches that is not on that list reaches the registry and is **absent from the tag of that
same version** -- two different things under one name, with nothing anywhere reporting it.

Both directions have bitten: a hand-written directory the build copies into the package, and a
tracked file the build regenerates. Whatever `make build` writes, either stage it or prove the
release does not need it.

The general check costs nothing:

```bash
git status --porcelain    # MUST be empty after a release; anything left is published-but-uncommitted
```

### `git commit` exits 1 on a clean tree and takes the whole target down with it

If the release content was already committed by hand, `git commit` finds nothing to commit, returns
1, and make abandons the target -- **before** the publish, the branch, the tag and the GitHub
release -- while printing only `nothing to commit, working tree clean`. Read as a build failure it
sends you hunting a compile error that is not there. The line is prefixed with `-` so the step is
advisory; `spc` still refuses an existing branch or tag, so the guard cannot mask a double release.

### Write the RELEASE.md section BEFORE releasing, or the release body is silently empty

`CURRENT_RELEASE_NOTES` slices RELEASE.md between the heading naming this exact version and the next
`*****` separator. No heading means an EMPTY slice, `gh release create -n ""` succeeds, and you get a
release with no notes and no error anywhere. ondewo-nlu-client-js and -typescript 7.1.1 shipped that
way and had to be repaired after the fact.

```bash
cat RELEASE.md | perl -ne 'print if /<the exact heading> <version>/../^\*{5}/' | wc -l   # must be > 0
```

### Verify the three artefacts separately -- they fail independently

GitHub's release API returned 500 twice in one session, leaving the registry and the tag correct and
**no release object at all** (nlu-client-js and -angular 7.1.1); `gh release create` after the fact
repairs it without touching the artefact.
The index is also eventually consistent: a fresh
release can read as absent for a minute, and `uv lock` reports that as `no version of <pkg>==<v>
... requirements are unsatisfiable`. That is the cache, not the index -- `uv lock --refresh-package
<pkg>` resolves it. Do not burn a version number over it.

```bash
curl -s https://pypi.org/pypi/<pkg>/json | python3 -c 'import sys,json;print(json.load(sys.stdin)["info"]["version"])'
git tag --list <version> ; gh release view <version> --json body --jq '.body|length'
```

# Git Branching, Pull Requests, Reviews & GitHub Actions — Practice Walkthrough

**Goal:** go through the full real-world loop once, end to end, on a throwaway
repo, so the mechanics stop feeling unfamiliar. Do every step yourself, in
your own terminal, on your own GitHub account — typing the commands is the
whole point.

Attached: `git-practice.zip` — a tiny skeleton project (`calc.py` + a test +
a CI workflow file) to use as the practice target. Unzip it wherever you keep
projects.

---

## Part 1 — Get the repo onto GitHub

1. Go to github.com, click **New repository**. Name it `git-practice`, leave
   it public or private (doesn't matter), and — important — do **not** check
   "Add a README" (you already have one in the zip, and starting empty avoids
   a merge conflict on your very first push).

2. In your terminal, `cd` into the unzipped `git-practice` folder and turn it
   into a git repo:
   ```
   git init
   git add .
   git commit -m "Initial commit"
   ```
   `git init` creates the hidden `.git` folder that makes this a repo.
   `git add .` stages every file (tells git "include these in the next
   commit"). `git commit` actually records that snapshot, with a message
   describing it.

3. Connect your local repo to the one on GitHub and push it. GitHub shows you
   this exact command after creating the repo (under "…or push an existing
   repository from the command line") — it'll look like:
   ```
   git remote add origin https://github.com/<your-username>/git-practice.git
   git branch -M main
   git push -u origin main
   ```
   `git remote add origin <url>` tells your local repo where "GitHub" is.
   `git push -u origin main` uploads your `main` branch there; `-u` remembers
   this pairing so future pushes can just be `git push`.

At this point, refresh the GitHub page — your files should be there.

---

## Part 2 — Branch, change, commit

Never edit `main` directly for a real change — you branch off, make the
change, and bring it back via a pull request. That's the whole workflow this
exercise is about.

4. Create and switch to a new branch:
   ```
   git checkout -b add-multiply
   ```
   This branches off wherever you currently are (`main`) and switches you
   onto the new branch in one step. Think of a branch as a parallel version
   of the code you can experiment on without touching `main`.

5. Make an actual change. Open `calc.py` and add a new function:
   ```python
   def multiply(a, b):
       return a * b
   ```
   Then add a matching test in `tests/test_calc.py`:
   ```python
   from calc import multiply

   def test_multiply():
       assert multiply(2, 3) == 6
   ```

6. Commit it:
   ```
   git add .
   git commit -m "Add multiply function"
   ```

7. Push the branch (note: not `main` — your new branch name):
   ```
   git push -u origin add-multiply
   ```

---

## Part 3 — Open a pull request

8. Go to your repo on GitHub. It'll show a banner: "add-multiply had recent
   pushes — Compare & pull request." Click it. (If you don't see the banner,
   go to the **Pull requests** tab → **New pull request** → pick
   `add-multiply` as the branch to merge into `main`.)

9. Give it a title and description (in a real team, this is where you
   explain *what* changed and *why*, for the reviewer's benefit), then click
   **Create pull request**.

10. Watch what happens next: GitHub Actions kicks off automatically because
    of the CI workflow file already in the repo (`.github/workflows/ci.yml`)
    — you'll see a yellow dot next to your commit, then a green check (or red
    ✗) once it finishes. That's your test suite running on GitHub's servers,
    not your machine — proof the code works somewhere other than "on my
    computer."

---

## Part 4 — Review it (practicing solo)

With no teammate handy, you can still practice the review mechanics:

11. On the PR page, click the **Files changed** tab. This is the diff view —
    green lines added, red lines removed. This is what a reviewer actually
    looks at.

12. Hover over a line and click the **+** that appears to leave a comment on
    that specific line — practice leaving one, e.g. "should we handle
    division too?"

13. Click **Review changes** (top right of Files changed) and try both
    **Comment** and **Approve** once each, just to see what each does to the
    PR page.

---

## Part 5 — Merge and clean up

14. Back on the **Conversation** tab, once CI is green, click **Merge pull
    request** → **Confirm merge**. This brings your branch's commits into
    `main`.

15. Delete the branch — GitHub offers a button right after merging. Branches
    are meant to be short-lived; deleting a merged one is normal, not
    destructive (its commits now live permanently in `main`'s history).

16. Sync your local machine with what just happened on GitHub:
    ```
    git checkout main
    git pull
    git branch -d add-multiply
    ```
    `git pull` fetches the merge you just did on GitHub. `git branch -d`
    deletes your local copy of the now-merged branch.

---

## Part 6 — Break it on purpose

Doing this once is what actually teaches you to read a CI failure instead of
panicking at one.

17. New branch, `git checkout -b break-a-test`. Edit `calc.py` so `add`
    returns the wrong thing (`return a + b + 1`). Commit, push, open a PR.

18. Watch CI turn red. Click into the failed check → **Details** to see the
    actual `pytest` output and find the assertion that failed.

19. Fix the bug in the same branch, commit, push again (same branch, same
    PR — no need to open a new one). Watch CI go green. Then merge.

---

## Notes on the CI file itself

`.github/workflows/ci.yml` (already included in the zip) is what makes Part 3
and Part 6 happen automatically:

```yaml
on:
  push:
  pull_request:
    branches: [main]
```
This says "run on every push, and also whenever a PR targets `main`" — so
both your regular commits and pull requests trigger it.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install pytest
      - run: pytest -v
```
Each `step` is one action on a freshly-spun-up virtual machine: get the code,
install Python, install `pytest`, run the tests. If any step exits with an
error, the whole run is marked failed (the red ✗ you saw in Part 6).

---

## Video resources (only if you want a visual walkthrough)

I haven't watched these personally, so treat them as a starting point to
skim rather than a guarantee — but they match this exact workflow and come
from reasonably well-established channels:

- [Pull Requests and Branch Policies (Git & GitHub for Beginners Course)](https://www.youtube.com/watch?v=9msxeWtQxtY) — covers the branch → PR → review part specifically.
- [GitHub Actions Tutorial for Beginners – CI/CD Pipeline from Scratch (2026)](https://www.youtube.com/watch?v=0PbxpIao_EU) — covers the Actions/YAML part specifically.

If you only read one non-video source, GitHub's own docs are the most
reliable reference for exact syntax as it changes over time:
[GitHub Actions quickstart](https://docs.github.com/en/actions/get-started/quickstart).

---

## Summary of every command used

```
git init
git add .
git commit -m "message"
git remote add origin <url>
git branch -M main
git push -u origin main

git checkout -b <branch-name>
git push -u origin <branch-name>

git checkout main
git pull
git branch -d <branch-name>
```

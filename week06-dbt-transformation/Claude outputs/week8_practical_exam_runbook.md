# Week 8 Practical Exam Runbook
Docker → docker-compose → tests → CI → data quality — build order, ready to reproduce from memory.

Assumption: laptop-only environment, no real cloud warehouse — Postgres locally (via
Docker) is your "warehouse." If the exam gives you a different setup, the *shape*
of every file below stays the same; only connection details change.

---

## 0. Before you touch code: project skeleton

```
myproject/
  src/
    __init__.py
    pipeline.py
  tests/
    test_pipeline.py
  dbt_project/
    models/
      staging/
        schema.yml
  .github/workflows/
    ci.yml
  Dockerfile
  docker-compose.yml
  requirements.txt
  .pre-commit-config.yaml
  .env.example
  .gitignore
  data_quality_checklist.md
```
Create every folder up front (`mkdir -p src tests dbt_project/models/staging .github/workflows`)
so you're never fighting "file not found" mid-exam.

---

## 1. Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home appuser
USER appuser

CMD ["python", "src/pipeline.py"]
```
Say-out-loud definitions if asked (Section G, Q20 style):
- **Image**: the built, frozen snapshot from this Dockerfile — a template.
- **Container**: a running instance of an image.
- **Layer**: each instruction (`FROM`, `COPY`, `RUN`) adds one cached layer; unchanged layers are reused on rebuild, which is why `requirements.txt` is copied and installed *before* the rest of the code.
- **Volume**: a folder on your real disk mounted into the container so data survives after the container stops (used in docker-compose below for Postgres).
- **Network**: docker-compose automatically puts all its services on one shared network, so containers can reach each other by service name (e.g. `db`) instead of an IP.
- **Registry**: where built images are stored/shared (Docker Hub, or a private one) — `docker push`/`docker pull`.

---

## 2. docker-compose.yml

```yaml
services:
  pipeline:
    build: .
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: pipeline_user
      POSTGRES_PASSWORD: pipeline_pass
      POSTGRES_DB: pipeline_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```
Run with `docker-compose up -d`. Check both containers with `docker ps`.

---

## 3. requirements.txt

```
pytest
ruff
dbt-postgres
```

## 4. .env.example (copy to `.env`, never commit `.env` itself)

```
DB_HOST=db
DB_USER=pipeline_user
DB_PASSWORD=pipeline_pass
DB_NAME=pipeline_db
```

## 5. .gitignore

```
__pycache__/
*.pyc
.venv/
.env
```

---

## 6. Unit test — tests/test_pipeline.py

```python
from src.pipeline import add, subtract

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2
```
Run: `pytest -v`

---

## 7. dbt tests — dbt_project/models/staging/schema.yml

```yaml
version: 2

models:
  - name: stg_orders
    columns:
      - name: order_id
        data_tests:
          - not_null
          - unique
      - name: status
        data_tests:
          - accepted_values:
              values: ["pending", "shipped", "delivered", "cancelled"]

sources:
  - name: raw
    tables:
      - name: orders
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```
Run: `dbt test` (and `dbt source freshness` for the freshness block).

---

## 8. .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
      - id: ruff-format

  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.1.1
    hooks:
      - id: sqlfluff-lint
        files: \.sql$
```
Activate once: `pip install pre-commit && pre-commit install`

---

## 9. GitHub Actions — .github/workflows/ci.yml (the big one, built as separate jobs)

```yaml
name: CI

on:
  push:
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install ruff
      - run: ruff check .

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest -v

  dbt-build:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: ci
          POSTGRES_PASSWORD: ci
          POSTGRES_DB: ci_db
        ports: ["5432:5432"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install dbt-postgres
      - run: dbt test --project-dir dbt_project
```
Say-out-loud summary if asked to *design* this (Section G, Q19 style): "one job per concern
(lint, test, dbt), each runs on its own fresh Ubuntu VM, triggered on every push and every
PR into main; a Postgres service container gives dbt something real to test against."

---

## 10. Prove CI catches errors (do this once, on purpose)

1. Break something true: change `assert add(2, 3) == 5` to `== 6`.
2. Commit, push. Watch the `test` job go red in the Actions tab.
3. Fix it back, commit, push. Watch it go green.
4. Keep both commits in your history (or a screenshot of the red run) — that's your proof.

---

## 11. data_quality_checklist.md (deliverable — fill honestly)

```markdown
# Data Quality Checklist
- [x] Row count check — fails if result set is unexpectedly empty
- [x] Not-null check — order_id, status
- [x] Uniqueness check — order_id
- [x] Accepted values check — status in [pending, shipped, delivered, cancelled]
- [x] Freshness check — orders source, warn 12h / error 24h
- [ ] Anomaly check (day-over-day swing) — not implemented yet
```

---

## 12. If asked to explain the secret-leak scenario (Section G, Q21 style)

A key got committed to GitHub and broke production. Plain-words answer:

**Prevention**: `.gitignore` the `.env` file so secrets never get staged in the first
place; use `pre-commit` with a secret-scanning hook to block the commit even if someone
forgets; never hardcode credentials in a Dockerfile or source file — always read from
env vars (`os.environ`).

**Recovery, in order**: (1) rotate/revoke the leaked credential immediately at the
source (e.g., regenerate the DB password or API key) — the git history still has the
old value forever, so deleting the file doesn't undo the leak. (2) remove it from git
history if it must not remain visible (`git filter-repo` or GitHub's secret-removal
tools — mention this exists, don't need to execute it live). (3) check logs/observability
for any unauthorized use of the credential during the exposure window. (4) add a
branch-protection rule requiring PR review + passing CI (including a secret scanner) so
this can't happen again silently.

---

## Fastest self-test

Set a timer for 45–60 minutes. From a totally empty folder, without looking at this
file, try to reproduce steps 0–9 from memory. Then open this file and diff what you
missed — that gap is exactly what to drill again before the 28th.

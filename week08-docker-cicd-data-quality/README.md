# Week- 8 Learning Details

**Docker** – packs my code and everything it needs (Python, libraries) into one box called an "image," so it runs the same way on any computer.

**docker-compose** – starts multiple things together with one command. Mine starts my pipeline and a database at the same time.

**Unit tests (pytest)** – small checks that prove a function gives the right answer. If someone breaks the code later, these catch it.

**Linting (ruff)** – checks that code is written neatly (spacing, unused imports), not whether it works.

**CI / GitHub Actions** – automatically runs my tests and checks every time I push code to GitHub, so mistakes get caught right away instead of being discovered later.

**dbt tests** – checks the actual data, not the code. Things like: is this column ever empty when it shouldn't be, are there duplicate IDs, are values only ever what's expected.

**Data quality checklist** – a simple list of checks (row count, missing values, duplicates, allowed values, freshness) that prove data can be trusted before anyone uses it.

## What I built

- A Dockerfile and docker-compose.yml that run my simple pipeline and a Postgres database together.
- A GitHub Actions workflow "ci.yml" with 3 jobs: lint, test, dbt-build, all running automatically on every push.
- Real dbt tests running against a sample orders table.
- Proof CI actually works: I broke a test on purpose, watched it turn red then fixed it and watched it turn green again.

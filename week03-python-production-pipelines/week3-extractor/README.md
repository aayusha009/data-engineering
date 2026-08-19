# WEEK 3 EXTRACTOR
Fetches user data from the JSONPlaceholder API, validates it, and saves it to `data/raw/` as JSON and CSV.

## Structure

- `extractor/` — main package (`api_client.py` fetches with retry/logging, `models.py` validates with pydantic, `main.py` ties it together)
- `tests/` — pytest tests for the package
- `explore.py` — original Day 1-2 single-file script, kept for reference

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python -m extractor.main
```

## Test

```bash
pytest tests/
```

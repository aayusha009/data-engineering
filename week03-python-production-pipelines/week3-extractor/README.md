# WEEK 3 EXTRACTOR
Fetches user data from the JSONPlaceholder API, validates it, and saves it to `data/raw/` as JSON and CSV.

## Structure

- `extractor/` — main package (`api_client.py` fetches with retry/logging, `models.py` validates with pydantic, `main.py` ties it together)
- `tests/` — pytest tests for the package
- `explore.py` — original Day 1-2 single-file script, kept for reference

## What each file does

- extractor/__init__.py — empty file, just marks this folder as a package
- extractor/api_client.py — APIClient class: fetches users from the API, retries on failure, logs what happens
- extractor/models.py — UserRecord (Pydantic model) + validate_users(): checks the data is shaped correctly
- extractor/main.py — the entry point: creates the client, fetches, validates, saves raw + processed data
- tests/test_models.py — tests that validation correctly accepts good records and rejects bad ones
- tests/test_api_client.py — tests the API client using a mocked (fake) response, no real internet needed
- requirements.txt — list of packages needed to run this project
- data/raw/ — untouched API response, saved before any processing
- data/processed/ — cleaned/validated data, saved after validation
  
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

# Dataset Used — Week 2

## dvdrental (PostgreSQL sample database)

All Week 2 practice queries were run against the standard PostgreSQL
"dvdrental" sample database — a simulated DVD rental store chain with
599 customers, 1,000 films, 16 categories, 16,044 rentals, and ~14,500
payments.

Core tables used: `customer`, `film`, `category`, `rental`, `payment`
(plus supporting/lookup tables: `inventory`, `film_category`, `store`,
`address`, `city`, `country`).

## How to load it locally

**1. Download the dataset:**
```bash
curl -L -O https://neon.com/postgresqltutorial/dvdrental.zip
```

**2. Unzip it (produces `dvdrental.tar`):**
```bash
unzip dvdrental.zip
```

**3. Create a fresh database:**
```bash
psql -U postgres -c "CREATE DATABASE dvdrental;"
```

**4. Restore the data (uses `pg_restore`, since `.tar` is a binary
dump format — not `psql -f`):**
```bash
pg_restore -U postgres -d dvdrental dvdrental.tar
```

**5. Verify the load:**
```bash
psql -U postgres -d dvdrental -c "SELECT COUNT(*) FROM customer;"   # expect 599
psql -U postgres -d dvdrental -c "SELECT COUNT(*) FROM rental;"     # expect 16044
```

## Note

The raw `dvdrental.tar` file is not committed to this repo — it's a
binary database dump, which git handles poorly (bloats repo size,
produces meaningless diffs). Instead, this file documents how to
reproduce the dataset locally in a few commands.

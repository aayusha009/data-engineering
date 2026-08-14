# Week 2 Notes — Window Functions & Deduplication

## Window Functions

A window function lets you calculate something across a group of rows
**without collapsing those rows together** — unlike `GROUP BY`, which
squashes everything into one summary row per group, a window function
keeps every row visible and just adds a new calculated column.

The basic shape:
```sql
FUNCTION() OVER (PARTITION BY some_column ORDER BY another_column)
```

- `PARTITION BY` restarts the calculation every time this column's
  value changes (like a mini `GROUP BY`, but without collapsing rows).
- `ORDER BY` controls what order the calculation happens in.

**Ranking functions** (`ROW_NUMBER`, `RANK`, `DENSE_RANK`) all number
rows within each partition, but handle *ties* differently:

| Function      | Behavior on a tie                          |
|---------------|---------------------------------------------|
| `ROW_NUMBER()`| Ignores ties, keeps counting: 1, 2, 3, 4     |
| `RANK()`      | Tied rows get the same number, then skips ahead: 1, 1, 3, 4 |
| `DENSE_RANK()`| Tied rows get the same number, no skipping: 1, 1, 2, 3 |

**Running totals** use the same `OVER()` syntax with an aggregate
function like `SUM()`, `AVG()`, or `COUNT()`, combined with `ORDER BY`
inside the window — this makes the calculation accumulate row by row
instead of producing one final number.

## Deduplication

Two main patterns:

1. **Keep one row per group (most common in real pipelines)** — number
   rows within each group using `ROW_NUMBER()`, ordered by whichever
   column defines "latest" or "first," then filter to `WHERE rn = 1`
   in an outer query/CTE. This is how you'd find "each customer's most
   recent order" or "the current version of a changing record."

2. **Find true exact-duplicate rows** — group by every column that
   should make a row unique, and use `HAVING COUNT(*) > 1` to flag any
   combination that appears more than once. This catches accidental
   duplicate inserts, not just related records.

## Sessionization (Gaps and Islands)

A specific real-world application combining `LAG()` and running totals:
group a person's timestamped activity into separate "sessions," where
a new session starts whenever the time gap since their last action
exceeds a chosen threshold.

Three steps: (1) calculate the gap since the previous row using
`LAG()`, (2) flag rows where that gap is large enough to start a new
session, (3) run a `SUM()` over that flag to turn the 1/0 markers into
actual incrementing session numbers.

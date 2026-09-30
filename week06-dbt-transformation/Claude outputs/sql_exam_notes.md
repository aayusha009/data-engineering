# SQL quick notes

GROUP BY gives one row per group. Window function keeps all rows and adds something extra to each.

WHERE filters before grouping. HAVING filters after grouping, use it for COUNT or SUM conditions.

After GROUP BY, order by the alias name, not the raw column.

ROW_NUMBER never repeats a number. RANK repeats and skips ahead. DENSE_RANK repeats and does not skip.

CTE means build the result first with WITH, then filter it in the query below.

Latest record per person: ROW_NUMBER by group, order by date descending, keep rn = 1.

Duplicate means every column matches exactly. Number them, delete where rn is more than 1.

Don't use a window function if GROUP BY alone already gives one row per group.

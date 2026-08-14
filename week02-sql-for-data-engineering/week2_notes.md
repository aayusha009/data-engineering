Week 2 Notes — Window Functions & Deduplication

Window Functions

The SQL window function helps in performing calculations across a set of rows that are related to the current row, without collapsing the result into one single value. Window functions are generally used for variety of tasks such as aggregates, ranking and running totals. 
Two clauses of window functions are:
Partition by: It works like group by clause. Divides the data in groups using PARTITION BY ().
Order by: This clause specifies the order of rows within each group using ORDER BY ().
With the help of above mentioned clauses, functions such as SUM (), AVG (), ROW_NUMBER (), RANK (), and DENSE_RANK () can be applied as per the need.

Syntax:
SELECT column_name1
WINDOW_FUNCTION (column_name2)
OVER (PARTITION BY column_name3 
ORDER BY column_name4 ) AS column_new
FROM table_name;
Where, 
•	window_function : aggregates such as [sum(), avg(), row_number(), rank(), etc.
•	column_name1: columns to display
•	column_name2: column used by window function
•	column_name3: column for grouping
•	column_name4: column for ordering
•	new_column: alias for window function result
•	table_name: to select the data from

Aggregate window functions calculate aggregates over a window of rows while retaining individual rows. Common aggregate functions include:
•	SUM(): Sums values within a window.
•	AVG(): Calculates the average value within a window.
•	COUNT(): Counts the rows within a window.
•	MAX(): Returns the maximum value in the window.
•	MIN(): Returns the minimum value in the window.

Ranking window functions provide rankings of rows within a partition based on specific criteria. Common ranking functions include:
•	RANK(): Assigns ranks to rows, skipping ranks for duplicates. Example: 1,2,2,4,5,5,7.
•	DENSE_RANK(): Assigns ranks to rows without skipping rank numbers for duplicates. Example: 1,2,2,3,4,5,5,6.
•	ROW_NUMBER(): Assigns a unique number to each row in the result set. Example: 1,2,3,4,5,6.

Deduplication

There are two different problems people call "deduplication":
1. A mistake,  the exact same row got saved twice by accident. Example: the same order, with the same customer and amount, appears twice in the table. This shouldn't have happened, it's a data error.
How to find it: group by every column, count how many times each combination shows up, and flag anything that shows up more than once.
sql query
SELECT column1, column2, COUNT(*)
FROM table_name
GROUP BY column1, column2
HAVING COUNT(*) > 1;

2. Not a mistake, just too many real rows, only want one. Example: a customer has 5 real rentals, all correct, but you only want to see their most recent one.
How to do it: number each customer's rows in order, then keep only the row numbered 1.
sql
WITH numbered AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY some_date DESC) AS rn
    FROM table_name
)
SELECT * FROM numbered WHERE rn = 1;


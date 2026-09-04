## week04-data-modeling-analytics

## Key Topics 

- Normalization - It is basically rules for keeping a database clean and not repeating the data. For my practical work, I have used star schema.

- Dimensional modeling (facts, dimensions, grain) - A fact is something that happened, like a student enrolling. A dimension is the details around it, like who and when. Grain means what one row actually represents. In my fact_enrollment table, one row = one student enrolled in one course.

- Measures - CREDITS is a measure that can be added up, like total credits per branch, so it's an additive measure.

- Star vs snowflake schema - Star schema keeps one fact table in the middle with simple tables around it. Snowflake schema splits those tables up more and needs more joins. I used star schema.

- Slowly Changing Dimensions (SCD) - Type 1 just overwrites old data, no history kept. Type 2 keeps the old row and adds a new one, so history is kept. I used Type 1 for most columns, and Type 2 only for Branch, since a student's branch changing matters for old reports.

- Conformed dimensions and bus matrix - This means reusing the same dimension table across multiple fact tables so reports stay consistent. I only have one fact table right now, but student_dim and course_dim are built so they could be reused later if I add more fact tables.

- Event modeling - Wide events put everything into one row. Entity-event hybrid keeps facts and dimensions separate and joins them. I used entity-event hybrid since it fits SQL better.


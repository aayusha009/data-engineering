
## Domain: College 
## Business processes

In college, when the registration opens every semester, a student is able to select a course and submit an enrollment. This creates a record linking the student to the course he/she has registered for that semester. Two entities are involved in this process: the person enrolling (student_dim), and the course (what the students are enrolling into – course_dim). 

During enrollment process, the system records which student enrolled, which student enrolled in which course, the date, and the number of credits of the particular course. This is exactly what the fact_enrollment table captures, with one row being able to represent one student’s enrollment in one course. Tracking enrollments this way allows the college to analyze the pattern of enrollments over time and identify which courses are in demand over time.

Analytical questions for the above-mentioned domain and business processes are listed below:

•	How many students enrolled in 2026 for branch cse core ? 

•	How many students enrolled in courses over 3 credits in the month of may 2026 ?

•	Which course had the highest total enrollment count in 2026?


## SQL DDL for facts and dimensions

Create table student_dim(
STUDENT_ID int primary key,
STUDENT_NAME varchar(50),
ADDRESS varchar(50),
EMAIL varchar (50),
BRANCH varchar (50)
);

Create table course_dim(
COURSE_ID int primary key, 
COURSE_NAME varchar(50) not null,
CREDITS int not null
);

Create table fact_enrollment(
ENROLLMENT_ID int primary key,
ENROLLMENT_DATE date,
STUDENT_ID int REFERENCES student_dim(STUDENT_ID) not null,
COURSE_ID int REFERENCES course_dim(COURSE_ID) not null,
CREDITS int not null
);


## Document grain for each table

1.	fact_enrollment 
Grain: one row = one student enrolled in one course. Example: Student 101 enrolled in Course 205 on 2026-01-15, which is worth 3 credits.
2.	student_dim
Grain: one row = one student. Each student appears exactly once, regardless of how many courses they're enrolled in. Example: Student 101 = Aayusha, aayusha@email.com, CSE Core branch.
3.	course_dim
Grain: one row = one course. Each course appears exactly once, regardless of how many students are enrolled in it. Example: Course 205 = "Database Systems," worth 3 credits.

## SCD strategy note

•	Table: student_dim

Column - Branch: SCD type 2: Used in analytical question. Type 2 is used as it must preserve which branch a student was in at the time of each enrollment.

Columns - Address, Email, Student_name: SCD type 1: They are safe to overwrite as they don’t have any analytical dependency. 


•	Table: course_dim

Columns - Course_name, credits: SCD type 1: The analytical question does not depend on historical course names and for credits, historical value is already preserved inside fact_enrollment table at the time of each enrollment.


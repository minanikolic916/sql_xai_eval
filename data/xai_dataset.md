Schema 1:

WORKER (ID, name, surname, role, type_of_employment)
SKIES (ID, manufacturer, ski_model, length, category)
SKIER (ID, name, surname, gender, age, skier_level)
SKI_RENT (ID, worker_id, ski_id, skier_id, price, rent_date, rent_duration, price_reduction)

PK constraints:

Worker (id), skies(id), skier(id), ski_rent(id)

FK constraints:

worker_id -> worker(id)
ski_id -> skies(id)
skier_id -> skier(id)

NL_QUESTION 1:

Write an SQL query that lists ski manufacturers, models and lengths, as well as the number of occurrences in the ski rent records for all of the skies in the database. Sort the data in the descending order by the length of skies.

GOLD_QUERY:

SELECT MANUFACTURER, SKI_MODEL, LENGTH, COUNT(\*) AS SKI_INFO
FROM SKIES LEFT JOIN SKI_RENT ON SKIES.ID = SKI_RENT.SKI_ID
GROUP BY MANUFACTURER, SKI_MODEL, LENGTH
ORDER BY SKIES.LENGTH DESC;

STUDENT_SUBMISSIONS:

1. SELECT MANUFACTURER, SKI_MODEL, LENGTH AS SKI_INFO
   FROM SKIES JOIN SKI_RENT ON SKIES.ID = SKI_RENT.SKI_ID
   GROUP BY MANUFACTURER, SKI_MODEL, LENGTH
   ORDER BY SKIES.LENGTH ASC;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but there is no count function, no left join, just the inner join and the order is set to ascending and not descending.

2. SELECT MANUFACTURER, SKI_MODEL, LENGTH, COUNT(\*) AS SKI_DATA
   FROM SKIES LEFT JOIN SKI_RENT ON SKIES.ID = SKI_RENT.SKI_ID
   GROUP BY MANUFACTURER
   ORDER BY SKIES.LENGTH;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, there is a problem with the group by clause, not all columns that appear in the select are present in the group by function (except the aggregate function of course). The order is not specified, meaning that it is automatically ascending and not descending.
Oracle error: ORA-00979: not a GROUP BY expression

3. SELECT MANUFACTURER, LENGTH AS SKI_DATA
   FROM SKIES JOIN SKI_RENT ON SKIES.ID = SKI_RENT.SKI_ID
   ORDER BY SKIES.LENGTH DESC;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but there isn’t a count function, no left join, just inner join and there isn’t a group by clause. In the select statement, a column regarding the ski model is also missing.

4. SELECT MANUFACTURER, SKI_MODEL
   FROM SKIES LEFT JOIN SKI_RENT ON ID = SKI_RENT.SKI_ID
   SORT BY SKIES.LENGTH;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, there is a missing column in the select statement, missing count aggregation function as well as missing the group by clause. The order is wrong, the sort by keyword is used and not the order by. The order is also not specified as descending, making it ascending by default.
Oracle_error: ORA-00933: SQL command not properly ended

5. SELECT SKI_MODEL, LENGTH, MANUFACTURER, COUNT(\*) AS DATA_SKI
   FROM SKIES LEFT JOIN SKI_RENT ON SKIES.ID = SKI_RENT.SKI_ID
   GROUP BY MANUFACTURER, LENGTH, SKI_MODEL
   ORDER BY SKIES.LENGTH DESC;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the alias in the select is differently named, and the column ordering in the select statement is different.

NL_QUESTION 2:

Write an SQL query that lists the names, surnames and age (formatted in the same column, divided by a single blank space) of all skiers older than 25 that have rented the skies after the year 2022. Order the skiers by name in the ascending order.

GOLD_QUERY:

SELECT SKIER.NAME || ' ' || SKIER.SURNAME || ' ' || AGE AS SKIER_DATA
FROM SKIER JOIN SKI_RENT ON SKIER.ID = SKI_RENT.SKI_ID
WHERE SKIER.AGE > 25 AND RENT_DATE > '31-DEC-2022'
ORDER BY SKIER.NAME ASC;

STUDENT SUBMISSIONS:

1. SELECT SKIER.NAME || SKIER.SURNAME || AGE AS INFO_ABOUT_SKIER
   FROM SKIER JOIN SKI_RENT ON SKIER.ID = SKI_RENT.SKI_ID
   WHERE SKIER.AGE > 25
   ORDER BY SKIER.NAME DESC;

Grade_label: incorrect_semantic

Reason: The syntax is okay, but the concatenation in the select statement is missing blank spaces, the condition regarding the rental date is missing and the ordering is opposite (it should be ascending). The alias is different, but that is not problematic.

2. SELECT CONCAT(NAME, SURNAME,AGE) AS SKIER_DATA
   FROM SKIER JOIN SKI_RENT ON SKIER.ID = SKI_RENT.SKI_ID
   WHERE SKIER.AGE > 25 AND RENT_DATE > '31-DEC-2022';

Grade_label: incorrect_syntax

Reason: The concatenation in the select statement is not valid syntax, it can take just two parameters, not three like here. The ordering is missing.
Oracle_error: ORA-00909: invalid number of arguments

3. SELECT SKIER.NAME || ' ' || AGE AS SKIER_DATA
   FROM SKIER JOIN SKI_RENT ON SKIER.ID = SKI_RENT.SKI_ID
   ORDER BY SKIER.NAME ASC;

Grade_label: incorrect_semantic

Reason: The select statement is missing the surname column and the two conditions regarding the rental date and skier age are also missing.

4. SELECT NAME + SURNAME + AGE AS SKIER_DATA
   FROM SKIER, SKI_RENT
   WHERE SKIER.AGE > 25 AND RENT_DATE > 2022
   ORDER BY NAME;

Grade_label: incorrect_syntax

Reason: The select statement has a wrong concatenation operator +, the where statement with the join condition is missing, the condition regarding the rental date is not valid, it does not compare the date value but the actual number.
Oracle_error: ORA-00932: inconsistent datatypes: expected DATE got NUMBER

5. SELECT CONCAT(CONCAT(CONCAT(CONCAT(SKIER.NAME, ' '), SKIER.SURNAME), ' '), AGE) AS SKIER_CONCAT
   FROM SKIER JOIN SKI_RENT ON SKIER.ID = SKI_RENT.SKI_ID
   WHERE SKIER.AGE > 25 AND RENT_DATE > '31-DEC-2022'
   ORDER BY SKIER.NAME;

Grade_label: correct

Reason: The statement is both syntactically and semantically correct, it uses the concat function instead of the || operator, it specifies a different alias name and the ordering direction is not specified, but is ascending by default.

NL_QUESTION 3:

Write an SQL query that lists the names, role and type of employment for workers that have rented at least two pairs of skies that were eligible for price reduction.

GOLD QUERY:

SELECT WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT
FROM WORKER JOIN SKI_RENT ON WORKER.ID = SKI_RENT.WORKER_ID
WHERE PRICE_REDUCTION LIKE 'yes'
GROUP BY WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT
HAVING COUNT(\*) >= 2;

STUDENT SUBMISSIONS:

1. SELECT WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT as WORKER_INFO
   FROM WORKER JOIN SKI_RENT ON WORKER.ID = SKI_RENT.WORKER_ID
   GROUP BY WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing a condition regarding the price reduction as well as the having count statement.

2. SELECT WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT
   FROM WORKER JOIN SKI_RENT ON WORKER.ID = SKI_RENT.WORKER_ID
   GROUP BY WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT
   WHERE PRICE_REDUCTION LIKE 'yes'
   HAVING COUNT(\*) >= 2;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the order of the group by and where clause is not valid (the where clause needs to go before the group by).
Oracle_error: ORA-00933: SQL command not properly ended

3. SELECT WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT
   FROM WORKER JOIN SKI_RENT ON WORKER.ID = SKI_RENT.WORKER_ID
   WHERE PRICE_REDUCTION LIKE 'yes'
   HAVING COUNT(\*) > 2;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because there is not a group by statement and there is a having clause. The question also states at least two, not greater than two.
Oracle_error: ORA-00937: not a single-group group function

4. SELECT WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT
   FROM WORKER, SKI_RENT
   WHERE WORKER.ID = SKI_RENT.WORKER_ID AND PRICE_REDUCTION LIKE 'yes'
   GROUP BY WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT
   HAVING COUNT(\*) > 2;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but the problem is regarding the at least two formulation, not greater than two. The joins are utilized using the comma syntax, which is also a valid approach.

5. SELECT WORKER.NAME, TYPE_OF_EMPLOYMENT, ROLE
   FROM WORKER JOIN SKI_RENT ON WORKER.ID = SKI_RENT.WORKER_ID
   WHERE PRICE_REDUCTION LIKE 'yes'
   GROUP BY WORKER.NAME, ROLE, TYPE_OF_EMPLOYMENT
   HAVING COUNT(\*) >= 2;

Grade_label: correct

Reason: The query is both syntactically and semantically correct. The column order in the select is different, but that is not problematic.

NL_QUESTION 4:

Write an SQL query that updates the level of skiers (sets the value to advanced) that have rented at least one pair of skies manufactured by Nordica that were eligible for price reduction.

GOLD_QUERY:

UPDATE SKIER
SET SKIER_LEVEL = 'advanced'
WHERE SKIER.ID IN (SELECT SKIER_ID
FROM SKI_RENT JOIN SKIES ON SKIES.ID = SKI_RENT.SKI_ID
WHERE MANUFACTURER LIKE 'Nordica' AND PRICE_REDUCTION LIKE 'yes');

STUDENT SUBMISSIONS:

1. UPDATE SKIER
   SET SKIER_LEVEL = 'advanced'
   WHERE SKIER.ID IN (SELECT SKIER_ID
   FROM SKI_RENT JOIN SKIES ON SKIES.ID = SKI_RENT.SKI_ID
   WHERE MANUFACTURER LIKE 'Nordica' AND PRICE = 1);

Grade_label: incorrect_semantic
Reason: The query is syntactically correct but using the wrong column and value for comparing the price reduction eligibility (the price reduction column should be used, not price).

2. UPDATE SKIER
   SET SKIER_LEVEL = SKIER_LEVEL || 'advanced'
   WHERE SKIER.ID IN (SELECT SKIER_ID
   FROM SKI_RENT JOIN SKIES ON SKIES.ID = SKI_RENT.SKI_ID);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing the conditions regarding the manufacturer and price reduction eligibility. The level is not set to advanced, it is just concatenated to the previous value of the level column, which is not the intended scenario.

3. UPDATING SKIER
   TO SKIER_LEVEL = 'advanced'
   WHERE ID IN (SELECT SKIER_ID FROM SKI_RENT);

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, the update keyword is misspelled and the set keyword is replaced with to. The inner query is missing joins and two conditions regarding the manufacturer and price reduction eligibility.
Oracle_error: Unknown Command

4. UPDATE SKIER
   SET LEVEL = 'advanced'
   WHERE ID IN (SELECT SKIER_ID
   FROM SKI_RENT JOIN SKI ON SKI.ID = SKI_RENT.SKI_ID
   WHERE MANUFACTURER LIKE 'Nordica' AND PRICE_REDUCTION LIKE 'yes');

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct, the wrong table names for skies was specified (it needs to be SKIES not SKI). The wrong column name was used, it should be skier_level, not just level which is a reserved keyword in Oracle.
Oracle_error: ORA-01747: invalid user.table.column, table.column, or column specification

5. UPDATE SKIER
   SET SKIER_LEVEL = 'advanced'
   WHERE SKIER.ID IN (SELECT SKIER_ID
   FROM SKI_RENT, SKIES
   WHERE SKIES.ID = SKI_RENT.SKI_ID
   AND MANUFACTURER = 'Nordica' AND PRICE_REDUCTION = 'yes');

Grade_label: correct

Reason: The query is both syntactically and semantically correct, a different syntax for joins was used (from and where), which is also valid. The LIKE operator was substituted with the = operator which is also a correct approach.

Schema 2:

REALTOR (ID, name, surname, salary, years_of_service)
PROPERTY (ID, listing_name, location, construction_year, structure, parking)
TENANT (ID, name, surname, gender, age)
CONTRACT (ID, realtor_id, property_id, tenant_id, rental_date, price, contract_length)

PK constraints:

Realtor (id), property(id), tenant(id), contract(id)

FK constraints:

realtor_id -> realtor(id)
property_id -> property(id)
tenant_id -> tenant(id)

NL_QUESTION 1:

Write an SQL query that lists the name, location and construction year, as well as the total number of appearances in the contracts for every property in the database that has been rented for more than three months. Sort the data in the ascending order by the construction year.

GOLD_QUERY:

SELECT LISTING_NAME, LOCATION, CONSTRUCTION_YEAR, COUNT(\*) AS NO_OF_CONTRACTS
FROM PROPERTY JOIN CONTRACT ON PROPERTY.ID = CONTRACT.PROPERTY_ID
WHERE CONTRACT_LENGTH > 3
GROUP BY LISTING_NAME, LOCATION, CONSTRUCTION_YEAR
ORDER BY CONSTRUCTION_YEAR ASC;

STUDENT_SUBMISSIONS:

1. SELECT LISTING_NAME, LOCATION, CONSTRUCTION_YEAR
   FROM PROPERTY JOIN CONTRACT ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   ORDER BY CONSTRUCTION_YEAR ASCENDING;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, the ascending keyword is meant to be just asc. There is no count or group by and the contract length condition is missing.
Oracle_error: ORA-00933: SQL command not properly ended

2. SELECT LISTING_NAME, LOCATION, CONSTRUCTION_YEAR, COUNT(\*) AS NO_OF_CONTRACTS
   FROM PROPERTY JOIN CONTRACT ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE CONTRACT_LENGTH > 3;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, the count statement is being used without the group by. The order clause is also missing.
Oracle_error: ORA-00937: not a single-group group function

3. SELECT LISTING_NAME, CONSTRUCTION_YEAR, LOCATION
   FROM PROPERTY JOIN CONTRACT ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE CONTRACT_LENGTH > 2
   ORDER BY CONSTRUCTION_YEAR;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but the semantics are only partially correct, count and group by are missing. The contract length condition is wrong, the minimum for filtering is three months, not two. The column order in the select statement is different, but that is not problematic.

4. SELECT LISTING_NAME, LOCATION, CONSTRUCTION_YEAR, SUM(CONTRACT.ID)
   FROM PROPERTY JOIN CONTRACT ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE CONTRACT_LENGTH > 3
   GROUP BY LISTING_NAME, LOCATION, CONSTRUCTION_YEAR
   ORDER BY LOCATION;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but there is a sum aggregation function instead of count and the column in the order by clause is wrong (it needs to be construction year, not location). The order is not specified, but it is ascending by default, so that is not problematic by itself.

5. SELECT LISTING_NAME, LOCATION, CONSTRUCTION_YEAR, COUNT(\*)
   FROM PROPERTY JOIN CONTRACT ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE CONTRACT_LENGTH > 3
   GROUP BY LISTING_NAME, LOCATION, CONSTRUCTION_YEAR
   ORDER BY CONSTRUCTION_YEAR;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the alias for the count is not specified, but that was not explicitly mentioned in the problem statement. The order direction is also not specified, but is ascending by default.

NL_QUESTION 2:

Write an SQL query that lists the name, surname and salary (presented as a single column, divided by a single blank space), as well as the total price for all of the rentals for realtors that have a salary greater than 50000. Take into account only the properties that have been rented after the year 2023.

GOLD_QUERY:

SELECT REALTOR.NAME || ' ' || REALTOR.SURNAME || ' ' || SALARY AS REALTOR_INFO, SUM(PRICE) AS REALTOR_PROFIT
FROM REALTOR JOIN CONTRACT ON REALTOR.ID = CONTRACT.REALTOR_ID
WHERE SALARY > 50000 AND RENTAL_DATE > '31-DEC-2023'
GROUP BY REALTOR.ID, REALTOR.NAME, REALTOR.SURNAME, SALARY;

STUDENT_SUBMISSIONS:

1. SELECT NAME + SURNAME + SALARY AS REALTOR_INFO
   FROM REALTR JOIN CONTRACT ON REALTOR.ID = CONTRACT.REALTOR_ID
   WHERE SALARY > 50000;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the table name realtor is misspelled. The + operator is not a valid concatenation operator in Oracle SQL. The sum aggregation function with the group by is also missing. The condition regarding the rental date is not specified, just the salary.
Oracle_error: ORA-00942: table or view does not exist

2. SELECT REALTOR.NAME || ' ' || REALTOR.SURNAME || ' ' || SALARY AS REALTOR_INFO, COUNT(PRICE)
   FROM REALTOR JOIN CONTRACT ON REALTOR.ID = CONTRACT.REALTOR_ID
   WHERE SALARY > 50000 AND RENTAL_DATE > '31-DEC-2023'
   GROUP BY REALTOR.NAME, REALTOR.SURNAME, SALARY;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but the wrong aggregation function is used (count instead of sum). The group by should also include the realtor id. The alias for count is not used, but that is not explicitly stated so it’s not problematic.

3. SELECT REALTOR.NAME, REALTOR.SURNAME, SALARY AS DATA_REALTOR, SUM(PRICE)
   FROM REALTOR JOIN CONTRACT ON REALTOR.ID = CONTRACT.REALTOR_ID
   WHERE SALARY > 50000 AND RENTAL_DATE > 2023;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because an aggregate function (sum) is used without group by. The name, surname and salary are not displayed as a single column. Aliases aren't used, but that has not been explicitly said in the problem statement. The rental date comparison is not valid, the column is of type DATE, not INTEGER.
Oracle_error: ORA-00932: inconsistent datatypes: expected DATE got NUMBER

4. SELECT REALTOR.NAME || ' ' || REALTOR.SURNAME || ' ' || SALARY AS REALTORS, SUM(PRICE) AS PROFIT
   FROM REALTOR JOIN CONTRACT ON REALTOR.ID = CONTRACT.REALTOR_ID
   GROUP BY REALTOR.ID, REALTOR.NAME, REALTOR.SURNAME, SALARY;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but the conditions for both salary and rental date have not been specified.

5. SELECT REALTOR.NAME || ' ' || REALTOR.SURNAME || ' ' || SALARY, SUM(PRICE)
   FROM REALTOR JOIN CONTRACT ON REALTOR.ID = CONTRACT.REALTOR_ID
   WHERE RENTAL_DATE > '31-DEC-2023' AND SALARY > 50000
   GROUP BY REALTOR.ID, REALTOR.NAME, REALTOR.SURNAME, SALARY;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the aliases are not used, but that was not explicitly stated in the problem formulation.

NL_QUESTION 3:

Write an SQL query that lists the names and age of tenants that have rented at least two properties that have a parking space.

GOLD QUERY:

SELECT TENANT.NAME, AGE
FROM TENANT JOIN CONTRACT ON TENANT.ID = CONTRACT.TENANT_ID JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID
WHERE PARKING LIKE 'yes'
GROUP BY TENANT.ID, TENANT.NAME, AGE
HAVING COUNT(\*) > 1;

STUDENT SUBMISSIONS:

1. SELECT AGE, TENANT.NAME
   FROM TENANT JOIN CONTRACT ON TENANT.ID = CONTRACT.TENANT_ID JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE PARKING LIKE 'yes'
   HAVING COUNT(\*) > 1;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the group by clause is missing while the having count is being used. The order of columns in the select statement is not as the one specified in the problem statement, but that is not problematic.
Oracle_error: ORA-00937: not a single-group group function

2. SELECT NAME, AGE
   FROM TENANT, CONTRACT
   WHERE TENANT.ID = CONTRACT.TENANT_ID AND PARKING LIKE 'yes'
   GROUP BY TENANT.NAME, AGE
   HAVING COUNT(\*) > 1;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the parking column from the property table is used without joining the table itself. The group by also needs the tenant id to ensure uniqueness.
Oracle_error: ORA-00904: "PARKING": invalid identifier

3. SELECT TENANT.NAME, AGE
   FROM TENANT, CONTRACT, PROPERTY
   WHERE TENANT.ID = CONTRACT.TENANT_ID AND PROPERTY.ID = CONTRACT.PROPERTY_ID
   GROUP BY TENANT.ID, TENANT.NAME, AGE
   HAVING COUNT(\*) >= 2;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but missing the condition about the property parking availability. The table join is done with using the from and where syntax, which is also adequate.

4. SELECT TENANT.NAME, AGE
   FROM TENANT JOIN CONTRACT ON TENANT.ID = CONTRACT.TENANT_ID JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE PARKING LIKE 'yes'
   GROUP BY TENANT.NAME, AGE;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but missing the having count to ensure that at least two properties have been rented by a tenant. The group by is missing the tenant id to ensure uniqueness.

5. SELECT TENANT.NAME, AGE
   FROM TENANT JOIN CONTRACT ON TENANT.ID = CONTRACT.TENANT_ID JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE PARKING = 'yes'
   GROUP BY TENANT.ID, TENANT.NAME, AGE
   HAVING COUNT(\*) >=2;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the = operator is used instead of LIKE, but both are valid options.

NL_QUESTION 4:

Write an SQL query that updates the salary (adds ten percent) of realtors that have rented at least one property that was build after the year 2021.

GOLD QUERY:

UPDATE REALTOR
SET SALARY = SALARY \* 1.1
WHERE REALTOR.ID IN (SELECT REALTOR_ID
FROM CONTRACT JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID
WHERE CONSTRUCTION_YEAR > 2021);

STUDENT SUBMISSIONS:

1. UPDATE REALTOR
   SET SALARY = SALARY + 10
   WHERE REALTOR.ID IN (SELECT REALTOR_ID
   FROM CONTRACT JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE CONSTRUCTION_YEAR > 2021);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but the salary update has the wrong value (the 10 is just added, not utilized as 10 percent).

2. UPDATE REALTOR
   SET SALARY = SALARY \* 1.1
   WHERE REALTOR.ID IN (SELECT REALTOR_ID
   FROM CONTRACT JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing the construction year condition.

3. UPDATE SET SALARY
   WHERE ID IN (SELECT REALTOR_ID
   FROM CONTRACT JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID);

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, the update and set keywords are not used as intended (update needs the table name and set needs the new column values). The inner query does not incorporate the condition regarding the construction year of the property.
Oracle_error: SQL Error: ORA-00903: invalid table name

4. UPDATE REALTOR
   WHERE ID IN (SELECT REALTOR_ID
   FROM CONTRACT JOIN PROPERTY ON PROPERTY.ID = CONTRACT.PROPERTY_ID
   WHERE CONSTRUCTION_YEAR > 2021);

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, the set clause is missing after the update.
Oracle_error: ORA-00971: missing SET keyword

5. UPDATE REALTOR
   SET SALARY = SALARY \* 1.1
   WHERE REALTOR.ID IN (SELECT REALTOR.ID
   FROM REALTOR, CONTRACT, PROPERTY
   WHERE REALTOR.ID = CONTRACT.REALTOR_ID AND PROPERTY.ID = CONTRACT.PROPERTY_ID
   AND CONSTRUCTION_YEAR > 2021);

Grade_label: correct

Reason: The query is both syntactically and semantically correct but a different approach to joins was used. The realtor table does not explicitly need to be joined as the realtor id is present in the contract table.

Schema 3:

VETERINARIAN (ID, name, surname, specialization, years_of_experience, salary)
PET (ID, name, pet_type, allergies)
OWNER (ID, name, surname, city, phone)
EXAM (ID, veterinarian_id, pet_id, owner_id, exam_date, type_of_exam, duration, price, therapy_prescribed)

PK constraints:

Veterinarian (id), pet(id), owner(id), exam(id)

FK constraints:

veterinarian_id -> veterinarian(id)
pet_id -> pet(id)
owner_id -> owner(id)

NL_QUESTION 1:

Write an SQL query that updates the salary (adds ten percent) of those veterinarians who have more than three years of experience and had at least two exams that lasted over 20 minutes.

GOLD_QUERY:

UPDATE VETERINARIAN
SET SALARY = SALARY _ 1.1
WHERE VETERINARIAN.ID IN (SELECT VETERINARIAN.ID
FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
WHERE YEARS_OF_EXPERIENCE > 3 AND DURATION > 20
GROUP BY VETERINARIAN.ID
HAVING COUNT(_) > 1);

STUDENT_SUBMISSIONS:

1. UPDATE VETERINARIAN
   WHERE ID IN (SELECT ID
   FROM VETERINARIAN JOIN EXAM ON ID = EXAM.VETERINARIAN_ID
   WHERE YEARS_OF_EXPERIENCE > 3 AND DURATION > 20
   );

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct because the update statement is missing the SET clause. The ID column is being used without specifying the table name making it ambiguous (in the inner query). The group by and having clauses are also not present.
Oracle_error: ORA-00971: missing SET keyword

2. UPDATE VETERINARIAN
   SET SALARY = SALARY + 10
   WHERE VETERINARIAN.ID IN (SELECT VETERINARIAN.ID
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   GROUP BY VETERINARIAN.ID
   HAVING COUNT(\*) > 1);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but the set part needs 10 percent, not just 10. The conditions for the years of experience and duration are missing.

3. UPDATE VETERINARIAN
   SET SALARY = SALARY _ 1.1
   WHERE VETERINARIAN.ID IN (SELECT VETERINARIAN.ID
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   WHERE YEARS_OF_EXPERIENCE > 3 AND DURATION > 20
   HAVING COUNT(_) < 2);

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct because having count is used without the group by clause. The comparison in having count is also wrong (< 2 instead of > 1).
Oracle_error: ORA-00937: not a single-group group function

4. UPDATE VETERINARIAN
   SET SALARY = SALARY \* 1.1
   WHERE VETERINARIAN.ID IN (SELECT VETERINARIAN.ID
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   WHERE YEARS_OF_EXPERIENCE > 3 AND DURATION > 20
   );

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but missing the group by and having count clauses.

5. UPDATE VETERINARIAN
   SET SALARY = SALARY + 10/100*SALARY
   WHERE VETERINARIAN.ID IN (SELECT VETERINARIAN.ID
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   WHERE YEARS_OF_EXPERIENCE > 3 AND DURATION > 20
   GROUP BY VETERINARIAN.ID
   HAVING COUNT(*) > 1);

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the calculation for the salary is different, but correct.

NL_QUESTION 2:

Write an SQL query that lists the id, salary, total duration as well as the minimal duration of exams performed by veterinarians that have a salary greater than 30000. Sort the data in descending order by the veterinarian salary.

GOLD_QUERY:

SELECT VETERINARIAN.ID, SALARY, SUM(DURATION), MIN(DURATION)
FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
WHERE SALARY > 30000
GROUP BY VETERINARIAN.ID, VETERINARIAN.SALARY
ORDER BY SALARY DESC;

STUDENT_SUBMISSIONS:

1. SELECT VETERINARIAN.ID, SALARY
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   WHERE SALARY > 30000
   ORDER BY SALARY DESC;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but missing two aggregation functions regarding the total and minimal duration of an exam. The group by is also missing.

2. SELECT ID, SALARY, SUM(DURATION), MIN(DURATION)
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   WHERE SALARY > 30000
   ORDER BY SALARY DESC;

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct because aggregate functions are used without a group by statement. The id column is ambiguous, so the table name needs to be explicitly stated.
Oracle_error: ORA-00918: column ambiguously defined

3. SELECT VETERINARIAN.ID, SALARY, COUNT(DURATION)
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   WHERE SALARY > 30000
   GROUP BY VETERINARIAN.ID, VETERINARIAN.SALARY
   ORDER BY SALARY;

Grade_label: incorect_semantic

Reason: The query is syntactically correct, but is missing a MIN aggregate function, as well as the DESC keyword for the ordering. The count aggregate function was used instead of sum.

4. SELECT VETERINARIAN.ID, SALARY
   WHERE SALARY > 30000
   ORDER BY SALARY DESC;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the table joins are missing and the column names are being used. The two aggregate functions SUM and MIN as well as the group by clause are also missing.
Oracle_error: ORA-00923: FROM keyword not found where expected

5. SELECT VETERINARIAN.ID, SALARY, SUM(DURATION), MIN(DURATION)
   FROM VETERINARIAN, EXAM
   WHERE VETERINARIAN.ID = EXAM.VETERINARIAN_ID AND SALARY > 30000
   GROUP BY VETERINARIAN.ID, VETERINARIAN.SALARY
   ORDER BY SALARY DESC;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the table joins are implemented using FROM and WHERE clauses which is also valid.

NL_QUESTION 3:

Write an SQL query that creates a view that lists the name, years of experience and the total number of exams for veterinarians in the database that have more than five years of experience. Take into account only the exams where a therapy was prescribed to the pet.

GOLD_QUERY:

CREATE VIEW VET_STATS AS
SELECT VETERINARIAN.NAME, YEARS_OF_EXPERIENCE, COUNT(\*) AS exam_number
FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
WHERE YEARS_OF_EXPERIENCE > 5 AND THERAPY_PRESCRIBED LIKE 'yes'
GROUP BY VETERINARIAN.ID, VETERINARIAN.NAME, VETERINARIAN.YEARS_OF_EXPERIENCE;

STUDENT_SUBMISSIONS:

1. CREATE VIEW VETS AS
   SELECT VETERINARIAN.NAME, YEARS_OF_EXPERIENCE
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   WHERE YEARS_OF_EXPERIENCE > 5 OR THERAPY_PRESCRIBED LIKE 'yes';

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing a count aggregation function with group by. There is an OR instead of an AND operator for combining the conditions. A different alias has been used, but that is not problematic.

2. CREATE OR REPLACE VIEW INFO_VET AS
   SELECT VETERINARIAN.NAME, YEARS_OF_EXPERIENCE, COUNT(\*) as no_of_exams
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   GROUP BY VETERINARIAN.NAME, VETERINARIAN.YEARS_OF_EXPERIENCE;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but is missing two conditions regarding the veterinarian's years of experience as well as whereas the therapy was prescribed. The group by is missing the veterinarian id, to ensure the uniqueness. The create or replace view syntax was used, which is acceptable. A different alias has been used, but that is acceptable.

3.  CREATE VET_STATS AS
    SELECT VETERINARIAN.NAME, YEARS_OF_EXPERIENCE, COUNT(\*) AS exam_number
    FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
    WHERE YEARS_OF_EXPERIENCE > 5;

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct, the create view is not properly defined because the view keyword is missing. The group by clause is missing, as well as a condition for the therapy prescribed.
Oracle_error: ORA-00901: invalid CREATE command

4. CREATE VIEW VET_STATS AS
   SELECT VETERINARIAN.NAME, YEARS_OF_EXPERIENCE, COUNT(\*)
   WHER THERAPY_PRESCRIBED LIKE 'yes’;

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct, the where clause has a typo, there are no joins and no group by clause. The condition regarding years of experience is missing.
Oracle_error: ORA-00923: FROM keyword not found where expected

5. CREATE VIEW VETERINARIANS AS
   SELECT VETERINARIAN.NAME, YEARS_OF_EXPERIENCE, COUNT(\*) as exams
   FROM VETERINARIAN, EXAM
   WHERE VETERINARIAN.ID = EXAM.VETERINARIAN_ID AND YEARS_OF_EXPERIENCE > 5 AND THERAPY_PRESCRIBED LIKE 'yes'
   GROUP BY VETERINARIAN.ID, VETERINARIAN.NAME, VETERINARIAN.YEARS_OF_EXPERIENCE;

Grade_label: correct

Reason: The query both syntactically and semantically correct, the joins are formed using from and where clauses, which is also adequate. The aliases used are different, but that is valid.

NL_QUESTION 4:

Write an SQL query that deletes the exams that were performed on pets that have allergies by veterinarians earning more than 30000.

GOLD_QUERY:

DELETE FROM EXAM
WHERE VETERINARIAN_ID IN (SELECT VETERINARIAN.ID
FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID JOIN PET ON PET.ID = EXAM.PET_ID
WHERE ALLERGIES LIKE 'yes' AND SALARY > 30000);

STUDENT_SUBMISSIONS:

1. DELETE FROM EXAM
   WHERE VETERINARIAN_ID IN (SELECT VETERINARIAN.ID
   FROM VETERINARIAN, EXAM, PET
   WHERE VETERINARIAN.ID = EXAM.VETERINARIAN_ID AND PET.ID = EXAM.PET_ID
   AND SALARY > 30000);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing the condition regarding the pet allergies. The joins are implemented using the from and where clauses (comma syntax), which is also a valid approach.

2. DELETE FROM EXAM
   WHERE VETERINARIAN_ID IN (SELECT VETERINARIAN.ID
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID
   WHERE SALARY > 30000);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing the join regarding the pet table. Consequently, the condition regarding the pet allergies is also not present.

3. DELETE FROM EXAM
   WHERE ID IN (SELECT ID
   FROM VETERINARIAN JOIN EXAM ON VETERINARIAN.ID = EXAM.VETERINARIAN_ID JOIN PET ON PET.ID = EXAM.PET_ID
   WHERE ALLERGIES LIKE 'yes' AND SALARY > 30000);

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the id column is ambiguous meaning that the table name should explicitly be stated.
Oracle_error: ORA-00918: column ambiguously defined

4. DROP FROM EXAM
   WHERE VETERINARIAN_ID IN (SELECT VETERINARIAN.ID FROM VETERINARIAN);

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the wrong keyword is used for deletion (drop and not delete). The inner query does not have any joins, it just selects all of the ids from the veterinarian table.
Oracle_error: ORA-00950: invalid DROP option

5. DELETE FROM EXAM
   WHERE VETERINARIAN_ID IN (SELECT VETERINARIAN.ID
   FROM VETERINARIAN, EXAM, PET
   WHERE VETERINARIAN.ID = EXAM.VETERINARIAN_ID AND PET.ID = EXAM.PET_ID
   AND ALLERGIES = 'yes' AND SALARY > 30000);

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the joins are implemented using the from and where syntax which is also valid. The comparison regarding the allergies column is done with the = operator instead of LIKE, which is also correct.

Schema 4:

COACH (ID, name, surname, specialization, number_of_active_members, provision_percentage)
PACKAGE (ID, package_name, duration_months, price, discount, target_group)
GYM_MEMBER (ID, name, surname, age, height, weight, status)
WORKOUT (ID, coach_id, package_id, gym_member_id, workout_date, place, duration, grade)

PK constraints:

Coach (id), package(id), gym_member(id), workout(id)

FK constraints:

coach_id -> coach(id)
package_id -> package(id)
gym_member_id -> gym_member(id)

NL_QUESTION 1:

Write an SQL query that creates a view that lists the name, surname (in a single column, divided by a blanc space) and average duration of a workout for gym members that are older than 30 years. Sort the data in descending order by the gym member surname.

GOLD_QUERY:

CREATE VIEW MEMBER_STATS AS
SELECT GYM_MEMBER.NAME || ' ' || GYM_MEMBER.SURNAME as name_surname, AVG(DURATION) AS avg_workout_duration
FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID WHERE AGE > 30
GROUP BY GYM_MEMBER.ID, GYM_MEMBER.NAME, GYM_MEMBER.SURNAME
ORDER BY GYM_MEMBER.SURNAME DESC;

STUDENT_SUBMISSIONS:

1. CREATE VIEW MEMBER_INFO AS
   SELECT GYM_MEMBER.NAME, GYM_MEMBER.SURNAME, AVERAGE(DURATION)
   FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   WHERE AGE > 30
   ORDER BY GYM_MEMBER.SURNAME DESC;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the average aggregate function is used without group by. The wrong keyword was used for the average aggregate function (AVERAGE, but AVG is correct). The name and surname are not displayed in a single column divided by a blank space. The alias for average isn't used. The alias for the view is different, but that is not problematic.
Oracle_error: ORA-00904: "AVERAGE": invalid identifier

2. CREATE VIEW MEMBERS AS
   SELECT NAME, SURNAME, AVG(DURATION)
   FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   GROUP BY NAME, SURNAME;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the alias for the average aggregation function does not exist. The group by also needs id because otherwise it won't be unique. The order by clause is missing. The age condition is also missing. The alias for the view is different, but that is not problematic.
Oracle_error: ORA-00998: must name this expression with a column alias

3. CREATE VIEW MEMBER_STATISTICS AS
   SELECT GYM_MEMBER.NAME || ' ' || GYM_MEMBER.SURNAME as name_surname
   FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   WHERE AGE > 30
   ORDER BY GYM_MEMBER.SURNAME DESC;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but missing the average aggregate function, meaning that the group by clause is also missing. The alias for the view is different, but that is also valid.

4. CREATE VIEW MEMBER_STATS AS
   SELECT GYM_MEMBER.NAME, GYM_MEMBER.SURNAME, AVG(DURATION) AS workout_avg
   FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   GROUP BY GYM_MEMBER.ID, GYM_MEMBER.NAME, GYM_MEMBER.SURNAME
   ORDER BY GYM_MEMBER.SURNAME;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but missing the age condition and the columns for name and surname are not displayed as a single column. The order direction is not specified, meaning that its ascending by default (descending was specified in the problem statement).

5. CREATE OR REPLACE VIEW DATA_MEMBERS AS
   SELECT GYM_MEMBER.NAME || ' ' || GYM_MEMBER.SURNAME as name_surname, AVG(DURATION) AS avg_stats
   FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   WHERE AGE > 30
   GROUP BY GYM_MEMBER.ID, GYM_MEMBER.NAME, GYM_MEMBER.SURNAME
   ORDER BY GYM_MEMBER.SURNAME DESC;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, but the create or replace view syntax was used, which is also correct. The table joins are implemented using the from and where clauses, which is also valid. The alias for the view is different, but that is valid.

NL_QUESTION 2:

Write an SQL query that updates the provision percentage (adds five to the previous value) of coaches that had at least five workouts longer than 30 minutes and didn't have a workout that had a grade lower than 3.

GOLD_QUERY:

UPDATE COACH
SET PROVISION_PERCENTAGE = PROVISION_PERCENTAGE + 5
WHERE COACH.ID IN (SELECT COACH.ID
FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID
WHERE DURATION > 30
GROUP BY COACH.ID
HAVING COUNT(\*) >= 5
MINUS
SELECT COACH.ID
FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID
WHERE GRADE >= 3);

STUDENT_SUBMISSIONS:

1. UPDATE PROVISION_PERCENTAGE = PROVISION_PERCENTAGE + 5
   WHERE COACH.ID IN (SELECT COACH.ID
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH.ID
   WHERE DURATION > 30
   GROUP BY COACH.ID
   );

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the SET and UPDATE clauses are not used properly (the SET is missing, and the UPDATE should not be used to specify the table in which the update happens). The inner query does not have a having count clause, just the group by and the part regarding the coaches that didn't have a grade lower than three isn't implemented.
Oracle_error: ORA-00971: missing SET keyword

2. UPDATE COACH
   SET PROVISION_PERCENTAGE = PROVISION_PERCENTAGE + 5
   WHERE COACH.ID IN (SELECT COACH.ID
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID
   WHERE DURATION > 30 AND GRADE >=3
   GROUP BY COACH.ID
   HAVING COUNT(\*) >= 5
   );

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but falsely combined the conditions for the workout duration and grade in the same part of the query.

3. UPDATE COACH
   SET PROVISION_PERCENTAGE = PROVISION_PERCENTAGE + 5
   WHERE COACH.ID IN ( SELECT COACH.ID
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID
   WHERE GRADE >= 3);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing the part of the query regarding the at least five workouts longer than 30 minutes.

4. UPDATE COACH
   SET PROVISION_PERCENTAGE = PROVISION_PERCENTAGE + 5
   WHERE ID IN (SELECT ID
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID
   WHERE DURATION > 30 AND GRADE >= 3);

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the id column is ambiguous. The inner query is not correct because all of the conditions are combined and there is no grouping and using the having count clause.
Oracle_error: ORA-00918: column ambiguously defined

5. UPDATE COACH
   SET PROVISION_PERCENTAGE = PROVISION_PERCENTAGE + 5
   WHERE COACH.ID IN (SELECT COACH.ID
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID
   WHERE DURATION > 30
   GROUP BY COACH.ID
   HAVING COUNT(\*) >= 5)
   AND COACH.ID NOT IN ( SELECT COACH.ID
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID
   WHERE GRADE >= 3);

Grade_label: correct

Reason: The query is both syntactically and semantically correct but the minus clause was not used which is valid because a different approach was implemented.

NL_QUESTION 3:

Write an SQL query that deletes the workouts that had been attended by at least three gym members older than 20 years that had a package with a price lower than 3500.

GOLD_QUERY:

DELETE FROM WORKOUT
WHERE WORKOUT.GYM_MEMBER_ID IN (SELECT GYM_MEMBER.ID
FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
JOIN PACKAGE ON PACKAGE.ID = WORKOUT.PACKAGE_ID
WHERE AGE > 20 AND PRICE < 3500
GROUP BY GYM_MEMBER.ID
HAVING COUNT(\*) >= 3
);

STUDENT_SUBMISSIONS:

1. DELETE FRM WORKOUT
   WHERE GYM_MEMBER_ID IN (SELECT GYM_MEMBER.ID
   FROM GYM_MEMBER
   WHERE AGE > 20
   );

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because from is misspeled. The inner query is also not valid, just the gym members older than 20 years are specified.
Oracle_error: ORA-00942: table or view does not exist

2. DELETE FROM WORKOUT
   WHERE WORKOUT.GYM_MEMBER_ID IN (SELECT GYM_MEMBER.ID
   FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   JOIN PACKAGE ON PACKAGE.ID = WORKOUT.PACKAGE_ID
   );

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing the conditions regarding the member age and package price. There is also no group by and having clause.

3. DELETE FROM WORKOUT
   WHERE WORKOUT.GYM_MEMBER_ID IN (SELECT GYM_MEMBER.ID
   FROM GYM_MEMBER JOIN WORKOUT ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   WHERE AGE > 20
   );

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing a join in the inner query regarding the package table (also the condition regarding the package price). The group by and having count clauses are also not to be found.

4. DELETE FROM WORKOUT
   WHERE WORKOUT.GYM_MEMBER_ID IN (SELECT GYM_MEMBER.ID
   WHERE AGE > 20 AND PRICE < 3500
   GROUP BY GYM_MEMBER.ID
   HAVING COUNT(\*) >= 3
   );

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because it is missing the two joins between the three tables (gym member, package and workout tables). The group by and having count are used, but they do not make sense in this context where the joins are not previously implemented.
Oracle_error: ORA-00923: FROM keyword not found where expected

5. DELETE FROM WORKOUT
   WHERE WORKOUT.GYM_MEMBER_ID IN (SELECT GYM_MEMBER.ID
   FROM GYM_MEMBER, WORKOUT, PACKAGE
   WHERE GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID AND PACKAGE.ID = WORKOUT.PACKAGE_ID
   AND AGE > 20 AND PRICE < 3500
   GROUP BY GYM_MEMBER.ID
   HAVING COUNT(\*) >= 3
   );

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the joins are implemented using the from and where combination which is also valid (comma syntax).

NL_QUESTION 4:

Write an SQL query that lists the id and name of coaches that had at least one workout with gym members taller than 200 cm that have an active status.

GOLD_QUERY:

SELECT COACH.ID, COACH.NAME
FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID JOIN GYM_MEMBER ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
WHERE height > 200 and status like 'active';

STUDENT_SUBMISSIONS:

1. SELECT COACH.ID, COACH.NAME
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID JOIN GYM_MEMBER ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing the conditions regarding the height and status of gym members.

2. SELECT COACH.ID, COACH.NAME
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID JOIN GYM_MEMBER ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   WHERE height > 200 and status like 'active'
   GROUP BY COACH.ID, COACH.NAME
   HAVING COUNT(\*) > 1;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but has a group by with a having count clause that specifies the wrong number of workouts (the problem statement said at least one, not greater than one).

3. SELECT ID, NAME
   FROM COACH, WORKOUT, GYM_MEMBER
   WHERE height > 200 and status like 'active';

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct because the column names used are ambiguous (coach and gym member have the id and name columns which are the same).
Oracle_error: ORA-00918: column ambiguously defined

4. SELECT coach.ID, coach.NAME
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID JOIN GYM_MEMBER ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER.id
   WHERE height > 200 and status like 'active';

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because wrong column name is specified (for the id of the gym member in the workout table).
Oracle_error: ORA-00904: "WORKOUT"."GYM_MEMBER"."ID": invalid identifier

5. SELECT COACH.NAME, COACH.ID
   FROM COACH JOIN WORKOUT ON COACH.ID = WORKOUT.COACH_ID JOIN GYM_MEMBER ON GYM_MEMBER.ID = WORKOUT.GYM_MEMBER_ID
   WHERE height > 200 and status like 'active'
   GROUP BY COACH.ID, COACH.name;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the column order in the select statement is different, but that is not a problem. There is an unnecessary group by clause, but that does not interfere with the correctness of the query.

Schema 5:

WAITER (ID, name, surname, salary)
MEAL (ID, name, meal_type, number_of_calories, gluten)
GUEST (ID, name, surname, city, phone, regular_customers)
ORDERS (ID, waiter_id, meal_id, guest_id, order_date, price, payment_method, tip)

PK constraints:

Waiter (id), meal(id), guest(id), orders(id)

FK constraints:

waiter_id -> waiter(id)
meal_id -> meal(id)
guest_id -> guest(id)

NL_QUESTION 1:

Write an SQL query that lists the name, type, number of calories and the total number of order occurrences for all meals that are gluten free and where the order was paid by card. Sort the data in ascending order by the number of calories and then in descending order by the type of meal.

GOLD_QUERY:

SELECT MEAL.NAME, MEAL_TYPE, NUMBER_OF_CALORIES, COUNT(\*) AS TOTAL_MEALS
FROM MEAL JOIN ORDERS ON MEAL.ID = ORDERS.MEAL_ID
WHERE GLUTEN = 'no' AND PAYMENT_METHOD = 'card'
GROUP BY MEAL.ID, MEAL.NAME, MEAL_TYPE, NUMBER_OF_CALORIES
ORDER BY NUMBER_OF_CALORIES ASC, MEAL_TYPE DESC;

STUDENT_SUBMISSIONS:

1. SELECT MEAL.NAME, MEAL_TYPE, NUMBER_OF_CALORIES
   FROM MEAL JOIN ORDERS ON MEAL.ID = ORDERS.MEAL_ID
   WHERE GLUTEN = 'no' AND PAYMENT_METHOD = 'card'
   ORDER BY NUMBER_OF_CALORIES;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but is missing the count aggregation function and subsequently the group by. The ordering is just done by one criteria, not two.

2. SELECT MEAL.NAME, MEAL_TYPE, NUMBER_OF_CALORIES, SUM(MEAL.ID) AS TOTAL_MEALS
   FROM MEAL JOIN ORDERS ON MEAL.ID = ORDERS.MEAL_ID
   GROUP BY MEAL.ID, MEAL.NAME, MEAL_TYPE, NUMBER_OF_CALORIES;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but using sum instead of count as the aggregation function. The conditions regarding the gluten and payment method are missing. The ordering is also missing.

3. SELECT NAME, TYPE
   FROM MEAL JOIN ORDERS ON MEAL.ID = ORDERS.MEAL_ID
   WHERE GLUTEN = 'no' AND PAYMENT_METHOD = 'card'
   ORDER BY TYPE DESC;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, the wrong column name was specified (type instead of meal type). The count and group by are missing and the order is done by a single column and not two as specified.
Oracle_error: ORA-00904: "TYPE": invalid identifier

4. SELECT MEAL.NAME, MEAL_TYPE
   WHERE GLUTEN = 'no' AND PAYMENT_METHOD = 'card'
   ORDER BY NUMBER_OF_CALORIES;

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct, there is no from clause. There is no count and group by and the order is done in terms of a single column.
Oracle_error: ORA-00923: FROM keyword not found where expected

5. SELECT MEAL.NAME, MEAL_TYPE, NUMBER_OF_CALORIES, COUNT(\*)
   FROM MEAL, ORDERS
   WHERE MEAL.ID = ORDERS.MEAL_ID AND GLUTEN LIKE 'no' AND PAYMENT_METHOD LIKE 'card'
   GROUP BY MEAL.ID, MEAL.NAME, MEAL_TYPE, NUMBER_OF_CALORIES
   ORDER BY NUMBER_OF_CALORIES ASC, MEAL_TYPE DESC;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the from and where clauses were used for implementing joins, which is a valid approach. The LIKE operator was used instead of = which is also correct.

NL_QUESTION 2:

Write an SQL query that deletes the orders that have been carried out at least twice by waiters that have a salary greater than 60000. Take into account only the orders with a price greater than 2500.

GOLD_QUERY:

DELETE FROM ORDERS
WHERE ORDERS.ID IN (SELECT ORDERS.ID
FROM ORDERS JOIN WAITER ON ORDERS.WAITER_ID = WAITER.ID
WHERE PRICE > 2500 AND SALARY > 60000
GROUP BY ORDERS.ID
HAVING COUNT(\*) > 1
);

STUDENT_SUBMISSIONS:

1. DELETE FROM ORDERS
   WHERE ORDERS.ID IN (SELECT ORDERS.ID
   FROM ORDERS JOIN WAITER ON ORDERS.WAITER_ID = WAITER.ID
   WHERE PRICE > 2500 AND SALARY > 60000);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but is missing the group by and having count clauses.

2. DELETE FROM ORDERS
   WHERE ORDERS.ID IN (SELECT ORDERS.ID
   FROM ORDERS JOIN WAITER ON ORDERS.WAITER_ID = WAITER.ID
   WHERE PRICE > 2500
   GROUP BY ORDERS.ID
   HAVING COUNT(\*) > 1
   );

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but is missing the condition regarding the waiter salary.

3. DELETE FRM ORDERS
   WHERE ORDERS.ID IN (SELECT ORDERS.ID
   FROM ORDERS JOIN WAITER ON ORDERS.WAITER_ID = WAITER.ID
   WHERE PRICE > 2500 AND SALARY > 60000
   );

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the FROM clause is misspelled. The group by and having count are also missing.
Oracle_error: ORA-00942: table or view does not exist

4. DELETE FROM ORDERS
   WHERE ID IN (SELECT ID
   FROM ORDERS JOIN WAITER ON ORDERS.WAITER_ID = WAITER.ID
   WHERE PRICE > 2500 AND SALARY > 60000
   GROUP BY ORDERS.ID
   HAVING COUNT(\*) > 1
   );

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the id column is ambiguous and the table name needs to be stated (in the inner query).
Oracle_error: ORA-00918: column ambiguously defined

5. DELETE FROM ORDERS
   WHERE ORDERS.ID IN (SELECT ORDERS.ID
   FROM ORDERS, WAITER
   WHERE ORDERS.WAITER_ID = WAITER.ID AND PRICE > 2500 AND SALARY > 60000
   GROUP BY ORDERS.ID
   HAVING COUNT(\*) > 1
   );

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the join is implemented using from and where clauses which is also valid.

NL_QUESTION 3:

Write an SQL query that updates the regular customer status (sets it to yes) of guests that have ordered less than three gluten free meals.

GOLD_QUERY:

UPDATE GUEST
SET REGULAR_CUSTOMERS = 'yes'
WHERE GUEST.ID IN (SELECT GUEST_ID
FROM ORDERS JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID
WHERE GLUTEN LIKE 'no'
GROUP BY GUEST_ID
HAVING COUNT(\*) < 3);

STUDENT_SUBMISSIONS:

1. UPDATE GUEST
   SET REGULAR_CUSTOMERS = 'yes'
   WHERE GUEST.ID IN (SELECT GUEST_ID
   FROM ORDERS JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID
   WHERE GLUTEN = 'no');

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but missing the group by and having count statements.

2. UPDATE GUEST
   SET REGULAR_CUSTOMERS = 'yes'
   WHERE GUEST.ID IN (SELECT GUEST_ID
   FROM ORDERS JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID
   GROUP BY GUEST_ID);

Grade_label: incorrect_semantic

Reason: The query is syntactically correct, but missing the condition regarding the gluten free meals as well as the having count statement.

3. UPDATE GUEST
   WHERE ID IN (SELECT GUEST_ID
   FROM ORDERS JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID
   WHERE GLUTEN LIKE 'no');

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct because the set clause after the update is missing. The group by and having count statements are missing.
Oracle_error: ORA-00971: missing SET keyword

4. UPDATE GUESTS
   SET REGULAR_CUSTOMERS = 'yes'
   WHERE GUEST.ID = (SELECT GUEST_ID
   FROM ORDERS JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID);

Grade_label: incorrect_syntax

Reason: The query is not syntactically correct because the wrong table name is specified (guests and not guest). Guest id is being compared with the = operator and not IN. The condition regarding gluten free meals, the group but as well as having count statements are missing.
Oracle_error: ORA-00942: table or view does not exist

5. UPDATE GUEST
   SET REGULAR_CUSTOMERS = 'yes'
   WHERE GUEST.ID IN (SELECT GUEST_ID
   FROM ORDERS JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID
   WHERE GLUTEN = 'no'
   GROUP BY GUEST_ID
   HAVING COUNT(\*) < 3);

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the = operator is used instead of LIKE which is also a valid approach.

NL_QUESTION 4:

Write an SQL query that lists the names and years of experience of waiters earning more than 50000 that served at least one high calorie meal (having more than 700 calories).

GOLD_QUERY:

SELECT WAITER.NAME, WAITER.SURNAME
FROM WAITER JOIN ORDERS ON WAITER.ID = ORDERS.WAITER_ID JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID
WHERE NUMBER_OF_CALORIES > 700 AND SALARY > 50000;

STUDENT_SUBMISSIONS:

1. SELECT WAITER.NAME, WAITER.SURNAME
   FROM WAITER JOIN ORDERS ON WAITER.ID = ORDERS.WAITER_ID JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing the conditions for the number of calories and salary.

2. SELECT WAITER.NAME, WAITER.SURNAME
   FROM WAITER JOIN ORDERS ON WAITER.ID = ORDERS.WAITER_ID
   WHERE SALARY > 50000;

Grade_label: incorrect_semantic

Reason: The query is syntactically correct but missing a join to the meal table and the condition regarding the number of calories.

3. SELECT WAITER
   FROM WAITER JOIN ORDERS ON WAITER.ID = ORDERS.WAITER_ID JOIN MEAL ON MEAL.ID = ORDERS.MEAL_ID
   WHERE NUMBER_OF_CALORIES > 700 AND SALARY > 50000;

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct because the wrong column name was specified in the select statement.
Oracle_error: ORA-00904: "WAITER": invalid identifier

4. SELECT WAITER.NAME, WAITER.SURNAME
   WHERE NUMBER_OF_CALORIES > 700 AND SALARY > 50000;

Grade_label: incorrect_syntax

Reason: The query is syntactically not correct because the table joins are not specified but the columns are used.
Oracle_error: ORA-00923: FROM keyword not found where expected

5. SELECT WAITER.NAME, WAITER.SURNAME
   FROM WAITER, ORDERS, MEAL
   WHERE WAITER.ID = ORDERS.WAITER_ID AND MEAL.ID = ORDERS.MEAL_ID
   AND NUMBER_OF_CALORIES > 700 AND SALARY > 50000;

Grade_label: correct

Reason: The query is both syntactically and semantically correct, the joins are implemented using the from and where clause which is also valid (comma based syntax).

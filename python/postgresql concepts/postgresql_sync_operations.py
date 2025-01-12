import psycopg2

""" This is a development postgresql file which serve me for experimental purposes.
I will explain here common and best practices methods for RDBMS and PostgreSQL specifically.
Starting from very basic syntax (but with best practices explanation)"""


# --------------------------------------------------------------------------------------------------------------------------- #

## CRUD Operations & Connection ##

try:
    connection = psycopg2.connect("dbname", "username", "password", "host_ip", "port")
    cursor = connection.cursor()                                    # regular basic cursor
    server_side_cursor = connection.cursor(name="big_data_cursor")  # server-side "smart" cursor, which allows to fetch data in chunk with cursor.fetchmany(num)
except Exception as e:
    raise Exception("cant connect to a database, error : ", str(e))


## READ ##
cursor.execute("SELECT * FROM TABLE")
rows = cursor.fetchall()
for row in rows:
    pass

# Server-Side cursor for big data efficient retrieval
server_side_cursor.execute("SELECT * FROM TABLE;")
while True:
    rows = server_side_cursor.fetchmany(1000)
    if rows:
        for row in rows:
            pass
    else:
        break


## Create (Insert) ##
cursor.execute("INSERT INTO TABLE (field1, field2, field3) VALUES (%s, %s, %s);", ("One", 2, 3.4))       # using placeholder prevent SQL injection.
connection.commit()


## Update ##
update_query = "UPDATE employees SET salary = %s WHERE name = %s;"
new_salary = (75000, "Alice")
cursor.execute(update_query, new_salary)
connection.commit()


## Delete ##
delete_query = "DELETE FROM employees WHERE name = %s;"
cursor.execute(delete_query, ("Alice",))
connection.commit()


# --------------------------------------------------------------------------------------------------------------------------- #


""" Basic Data retrival """

# orbder the rows in specific ascending / descending order and limit the result size.
orberby_query = "SELECT * FROM employees ORDER BY salary DESC LIMIT 5;"


"""" Pagination"""
" for big tables, if we want to retrieve chunks of data efficiently (or parts from the data) "
" we can use both SKIP & LIMIT syntax of keyset pagination which is more efficient "

# Retrieves 10 rows, starting from the 21st row
pagination_basic = "SELECT * FROM employees ORDER BY id LIMIT 10 OFFSET 20;"

# With large datasets or higher offsets, SQL’s OFFSET can become inefficient.
# The database needs to scan and skip rows up to the offset
pagination_keyset = "SELECT * FROM employees WHERE id > last_seen_id ORDER BY id LIMIT 10;"


" Aggregation Function: is a type of database function that processes multiple rows and returns a summarized or aggregated result."
" When an aggregation function is used across the entire dataset, it typically returns a single result." \
" When used with GROUP BY, it can produce multiple results, one for each group. "
table_aggregation = "SELECT AVG(salary) FROM employees;"

# all the field inside the select that haven't grouped, have to be wrapped with Aggregation function.
groupby_aggregation = "SELECT department, AVG(salary) FROM employees GROUP BY department;"

# HAVING is used like WHERE clause but after aggregation.
# SQL requires you to reference the AVG(salary) directly in the HAVING clause HAVING is evaluated before alias names are assigned.
having_query = "SELECT department, AVG(salary)  FROM employees  GROUP BY department  HAVING AVG(salary) > 60000;"


# --------------------------------------------------------------------------------------------------------------------------- #


""" Joins"""

"allow you to combine rows from multiple tables based on a related column. "
"it be can as intersection, union and partial union (left outer, right outer joins)."

## Inner ##
inner_join_query = """ SELECT tableA.name, tableB.name AS tableB_name FROM tableA INNER JOIN tableB ON tableA.department_id = tableB.id; """
# all the rows from table a and table b that equal in their values departemant_id in table A == id in table B


## Right ##
right_join_query = """ SELECT employees.name, departments.name AS department_name FROM employees RIGHT JOIN departments ON employees.department_id = departments.id; """
# returns all the departments with employees or NULL if no such employee had that specific department id.


# --------------------------------------------------------------------------------------------------------------------------- #

""" Subqueries: as we know, each select (read) query returns a table, we can use that table to query it. in that form, we are using subquery.
there are 2 types of sub queries, 1st in the WHERE clause (using some aggregation function), 2nd in the FORM clause (subquery which returns a table)."""

subquery_where_clause = """ SELECT name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees); """
subquery_from_clause = """ 
SELECT dept_name, avg_salary
FROM (SELECT department_id, AVG(salary) AS avg_salary FROM employees GROUP BY department_id ) AS dept_avg
JOIN departments ON departments.id = dept_avg.department_id; """


# --------------------------------------------------------------------------------------------------------------------------- #


""" CTE : Common Table Expressions """
" are used to simplify complex SQL queries, making them more readable and manageable. "

""" WITH cte_name AS (
    SELECT column1, column2
    FROM table
    WHERE conditions
)
SELECT * FROM cte_name; """

# search all the employees which there salary is higher than average salary in each specific department.
cte_example = """ WITH DeptAvg AS (
                    SELECT department_id, AVG(salary) AS avg_salary
                    FROM employees
                    GROUP BY department_id
                )
                
                SELECT e.name, e.salary, d.avg_salary
                FROM employees e
                JOIN DeptAvg d ON e.department_id = d.department_id
                WHERE e.salary > d.avg_salary;"""


# --------------------------------------------------------------------------------------------------------------------------- #


"""Windows Function"""

"A window function allows you to apply aggregate-like operations without grouping the data. It works on a range of rows "
"defined by the window, and each row will receive a result based on the context of that window."

"""
Components of a Window Function:
Window Function: The function you are applying (e.g., RANK(), ROW_NUMBER(), SUM(), AVG(), etc.).
OVER Clause: Defines the window over which the function is applied.
    PARTITION BY: Divides the result set into partitions (groups) before the window function is applied.
    ORDER BY: Defines the order of rows in each partition.
    ROWS or RANGE: Optional clauses that define the specific set of rows the function operates over (this is more advanced and not necessary for basic usage)."""

windows_function = " SELECT name, department, salary,  RANK() OVER(PARTITION BY department ORDER BY salary DESC) AS rank FROM employees;"
# This will result in a new table of name, department, salary and rank. the rank started from 1 and ties to the higher salary in per department.


# --------------------------------------------------------------------------------------------------------------------------- #
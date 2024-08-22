'''


    @Author: Shivraj Yelave
    @Date: 22-08-24
    @Last modified by: Shivraj Yelave
    @Last modified time: 22-08-24
    @Title: Database CURD Operations Script


'''

# Import required modules for SQL connection and environment variables management
import pyodbc  # Description: pyodbc is a Python library that allows you to connect to databases using ODBC
from dotenv import load_dotenv  # Description: Load environment variables from a .env file
import os  # Description: Provides a way to interact with the operating system

def main():
    # Description: Load environment variables from the .env file
    load_dotenv()

    # Description: Set up SQL connection parameters
    server = 'DESKTOP-ND5NF8I\SQLEXPRESS'  # SQL Server instance name
    database = 'covid_datasets'  # The database you want to connect to
    username = os.getenv('USER_NAME')  # Fetch the username from environment variables
    password = os.getenv('PASSWORD')  # Fetch the password from environment variables

    # Description: Create the connection string for connecting to SQL Server using ODBC Driver 17
    connection_string = f"""
        DRIVER={{ODBC Driver 17 for SQL Server}};
        SERVER={server};
        DATABASE={database};
        UID={username};
        PWD={password};
    """

    # Description: Establish a connection to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("IF OBJECT_ID('students', 'U') IS NOT NULL DROP TABLE students;")

    
    # Create the 'students' table
    cursor.execute("""
    CREATE TABLE students (
        StudentID INT PRIMARY KEY,
        FirstName NVARCHAR(50),
        LastName NVARCHAR(50),
        DateOfBirth DATE,
        GradeLevel INT,
        Major NVARCHAR(100)
    );
    """)
    conn.commit()  # Commit the CREATE TABLE statement
    print("Table 'students' created successfully.")

    # Insert sample data into the 'students' table
    cursor.execute("""
    INSERT INTO students (StudentID, FirstName, LastName, DateOfBirth, GradeLevel, Major)
    VALUES (1, 'Shiv', 'Yelave', '2002-12-13', 17, 'Mathematics'),
        (2, 'Deven', 'Gupta', '2003-12-23', 12, 'Physics'),
        (3, 'Ayush', 'Prayag', '2005-01-11', 10, 'Chemistry');
    """)
    conn.commit()  # Commit the INSERT statement
    print("Sample data inserted into 'students' table.")

    # Perform SELECT queries and fetch results
    cursor.execute("SELECT * FROM students;")
    rows = cursor.fetchall()  # Fetch all rows from the SELECT query
    print("All records from 'students' table:")
    for row in rows:
        print(row)

    cursor.execute("SELECT FirstName, LastName, Major FROM students;")
    rows = cursor.fetchall()  # Fetch all rows from the SELECT query
    print("Specific columns from 'students' table:")
    for row in rows:
        print(row)

    cursor.execute("SELECT * FROM students WHERE GradeLevel = 12;")
    rows = cursor.fetchall()  # Fetch all rows from the SELECT query
    print("Records for students in grade level 12:")
    for row in rows:
        print(row)

    # Update operations (no results to fetch)
    cursor.execute("UPDATE students SET Major = 'Computer Science' WHERE StudentID = 2;")
    conn.commit()  # Commit the UPDATE statement
    print("Updated Major for StudentID 2 to 'Computer Science'.")

    cursor.execute("UPDATE students SET GradeLevel = 12, Major = 'Biology' WHERE StudentID = 3;")
    conn.commit()  # Commit the UPDATE statement
    print("Updated GradeLevel and Major for StudentID 3.")

    # Delete operation (no results to fetch)
    cursor.execute("DELETE FROM students WHERE StudentID = 3;")
    conn.commit()  # Commit the DELETE statement
    print("Deleted record for StudentID 3.")

    # Close the cursor and connection to free resources
    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()  # Description: Entry point for executing the script

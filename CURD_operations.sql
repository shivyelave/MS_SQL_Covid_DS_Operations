CREATE DATABASE students;

USE students;


-- CURD OPERATIONS

-- C- Create
CREATE TABLE students (
    StudentID INT PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    DateOfBirth DATE,
    GradeLevel INT,
    Major NVARCHAR(100)
);

INSERT INTO students (StudentID, FirstName, LastName, DateOfBirth, GradeLevel, Major)
VALUES (1, 'Shiv', 'Yelave', '2002-12-13', 17, 'Mathematics'),
       (2, 'Deven', 'Gupta', '2003-12-23', 12, 'Physics'),
       (3, 'Ayush', 'Prayag', '2005-01-11', 10, 'Chemistry');

-- R- Read

SELECT * FROM students;

-- Retrieve specific columns
SELECT FirstName, LastName, Major FROM students;

-- Retrieve students in a specific grade level
SELECT * FROM students WHERE GradeLevel = 12;


-- U- Update


UPDATE students
SET Major = 'Computer Science'
WHERE StudentID = 2;

-- Update multiple fields
UPDATE students
SET GradeLevel = 12, Major = 'Biology'
WHERE StudentID = 3;

-- D- Delete

DELETE FROM students
WHERE StudentID = 3;




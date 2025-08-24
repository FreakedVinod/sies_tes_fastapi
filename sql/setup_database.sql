CREATE DATABASE sies_tes;
USE sies_tes;

-- Courses
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (stream_id) REFERENCES streams(id)
);

-- Classes
CREATE TABLE classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
);

-- Students
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(10) UNIQUE NOT NULL,
    class_id INT,
    password VARCHAR(255) NOT NULL,
    admission_year INT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE SET NULL
);

-- Streams
CREATE TABLE streams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Eligibility
CREATE TABLE eligibility (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    is_eligible BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

INSERT INTO streams (name) VALUES 
('Arts'),
('Science'),
('Commerce');

INSERT INTO courses (course_name, stream_id) VALUES
('B.A.M.M.C. (Bachelor of Arts in Mass Media and Communication)', 1),
('B.Sc. in Computer Science', 2),
('B.Sc. in Information Technology', 2),
('B.Sc. in Packaging Technology', 2),
('B.Sc. in Environmental Science', 2),
('B.Sc. in Data Science', 2),
('B.Com. (Bachelor of Commerce)', 3),
('B.Com. (Accounting & Finance)', 3),
('B.Com. (Banking & Insurance)', 3),
('B.Com. (Financial Markets)', 3),
('B.M.S. (Bachelor of Management Studies)', 3),
('B.Com. (Management Accounting with Finance)', 3),
('B.Com. (Entrepreneurship)', 3),
('M.Sc. in Computer Science', 2),
('M.Sc. in Information Technology', 2),
('M.Sc. in Environmental Science', 2),
('M.A. in Business Economics', 1),
('M.A. in Journalism and Mass Communication', 1),
('M.Com. (Advanced Accountancy)', 3),
('M.Com. in Business Management', 3);

INSERT INTO classes (class_name, course_id)
VALUES
('FYBMM', 1), ('SYBMM', 1), ('TYBMM', 1),
('FYBSCIT', 3), ('SYBSCIT', 3), ('TYBSCIT', 3),
('FYBSCCS', 2), ('SYBSCCS', 2), ('TYBSCCS', 2),
('FYBSCPT', 4), ('SYBSCPT', 4), ('TYBSCPT', 4),
('FYBSCES', 5), ('SYBSCES', 5), ('TYBSCES', 5),
('FYBSCDS', 6), ('SYBSCDS', 6), ('TYBSCDS', 6),
('FYBCOM', 7), ('SYBCOM', 7), ('TYBCOM', 7),
('FYBAF', 8), ('SYBAF', 8), ('TYBAF', 8),
('FYBBI', 9), ('SYBBI', 9), ('TYBBI', 9),
('FYBFM', 10), ('SYBFM', 10), ('TYBFM', 10),
('FYBMS', 11), ('SYBMS', 11), ('TYBMS', 11),
('FYBMAF', 12), ('SYBMAF', 12), ('TYBMAF', 12),
('FYBE', 13), ('SYBE', 13), ('TYBE', 13),
('PART1MABE', 17), ('PART2MABE', 17),
('PART1MAJMC', 18), ('PART2MAJMC', 18),
('PART1MSCIT', 15), ('PART2MSCIT', 15),
('PART1MSCCS', 14), ('PART2MSCCS', 14),
('PART1MSCES', 16), ('PART2MSCES', 16),
('PART1MCOMAA', 19), ('PART2MCOMAA', 19),
('PART1MCOMBM', 20), ('PART2MCOMBM', 20);

-- Reset students table (for testing)
DELETE FROM students WHERE student_id > 0;
ALTER TABLE students AUTO_INCREMENT = 1;

-- Fix wrong mapping (example)
UPDATE classes
SET course_id = 20
WHERE class_id IN (52, 53);

-- Show all tables
SHOW TABLES;

-- Show records
SELECT * FROM streams;
SELECT * FROM courses;
SELECT * FROM classes;
SELECT * FROM students;
SELECT * FROM eligibility;

-- Get all students with course info
SELECT student_id, name, roll_no, admission_year, course_id
FROM students
ORDER BY student_id;

-- Join students with eligibility
SELECT s.student_id, s.name, s.roll_no, s.class_id,
       COALESCE(e.is_eligible, 0) AS is_eligible
FROM students s
LEFT JOIN eligibility e ON s.student_id = e.student_id
ORDER BY s.class_id;

-- So your friends only need to:

-- 1. Run Step 1 & 2 to create DB + tables.

-- 2. Run Step 3 to insert master data (streams, courses, classes).

-- 3. Use Step 4 only when they want to reset/fix.

-- 4. Use Step 5 to test and see results.

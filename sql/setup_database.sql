-- Create database
CREATE DATABASE IF NOT EXISTS sies_tes;
USE sies_tes;

-- Courses
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL
);

-- Classes
CREATE TABLE IF NOT EXISTS classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Students
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    admission_year INT NOT NULL,
    class_id INT,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);


-- Students Eligibility 
CREATE TABLE eligibility (
    student_id INT PRIMARY KEY,
    is_eligible BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);


-- Optional: Insert some mock data
-- INSERT INTO courses (course_name) VALUES ('BscIT');

-- INSERT INTO classes (class_name, course_id)
-- VALUES 
--     ('FYIT', 56),
--     ('SYIT', 57),
--     ('TYIT', 58);

-- INSERT INTO students (name, roll_no, password, admission_year, class_id) VALUES ('jane', 'r2', 'this', 2023, 52);
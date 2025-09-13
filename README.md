# SIES-TES (Teacher Evaluation System)

A web-based Teacher Evaluation System (TES) for SIES, allowing students to submit feedback for teachers and enabling admin management of courses, classes, and feedback eligibility.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Folder Structure](#folder-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

SIES-TES is designed to collect student feedback on teachers and modules. The system ensures:

- Student registration and login.
- Admin panel to manage courses, classes, and teacher feedback eligibility.
- Dynamic generation of classes and courses.
- Secure storage of feedback in MySQL database.

## Features

### Student Side
- Registration with Name, Roll Number, Password, Admission Year.
- Login to access feedback forms.
- Dynamic selection of courses and classes.
- Submit feedback for teachers.

### Admin Side
- Login to Admin Dashboard.
- Manage courses, classes, and teachers.
- Control student feedback eligibility.
- View feedback reports.
- Export feedback data for analysis.

## Technology Stack

- **Backend:** FastAPI  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** MySQL  
- **Async Database Integration:** `databases` library  
- **Server:** Uvicorn  

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sies-tes.git
   cd sies-tes

2. Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Install dependencies:

pip install -r requirements.txt

4. Set up the MySQL database:

Create a database named sies_tes.

Run the provided SQL scripts to create tables (students, courses, classes, teachers, feedback, etc.)

5. Configure database connection in main.py or config file:

DATABASE_URL = "mysql+aiomysql://username:password@localhost/sies_tes"

-- Usage

1. Start the FastAPI server:

uvicorn main:app --reload


2. Open the application in your browser:

http://127.0.0.1:8000

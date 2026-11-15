
import sqlite3
from config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:

        connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL,
            branch TEXT NOT NULL,
            semester INTEGER NOT NULL,
            section TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            admission_year INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        connection.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            marks_obtained REAL NOT NULL,
            max_marks REAL NOT NULL DEFAULT 100,
            exam_type TEXT NOT NULL,
            semester INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(student_id)
            REFERENCES students(id) ON DELETE CASCADE
        )
        """)

        connection.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            attendance_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('Present','Absent')),
            FOREIGN KEY(student_id)
            REFERENCES students(id) ON DELETE CASCADE
        )
        """)

        connection.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS unique_student_attendance
        ON attendance(student_id, subject, attendance_date)
        """)

    print("Database initialized successfully!")


def get_student_count():
    with get_connection() as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]


def get_marks_count():
    with get_connection() as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM marks"
        ).fetchone()[0]


def get_attendance_count():
    with get_connection() as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM attendance"
        ).fetchone()[0]

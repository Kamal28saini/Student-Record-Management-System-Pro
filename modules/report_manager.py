
import csv
from config import BASE_DIR
from database.db import get_connection


def export_students_csv(filename="students_report.csv"):
    path = BASE_DIR / filename

    with get_connection() as connection:
        rows = connection.execute("""
        SELECT id, name, roll_number, course, branch,
               semester, section, email, phone, admission_year
        FROM students ORDER BY name
        """).fetchall()

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID", "Name", "Roll Number", "Course", "Branch",
            "Semester", "Section", "Email", "Phone", "Admission Year"
        ])

        writer.writerows([tuple(row) for row in rows])

    return path


def export_marks_csv(filename="marks_report.csv"):
    path = BASE_DIR / filename

    with get_connection() as connection:
        rows = connection.execute("""
        SELECT students.name, students.roll_number,
               marks.subject, marks.marks_obtained,
               marks.max_marks, marks.exam_type, marks.semester
        FROM marks
        JOIN students ON marks.student_id=students.id
        ORDER BY students.name
        """).fetchall()

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Student", "Roll Number", "Subject",
            "Obtained Marks", "Maximum Marks",
            "Exam Type", "Semester"
        ])

        writer.writerows([tuple(row) for row in rows])

    return path


def export_attendance_csv(filename="attendance_report.csv"):
    path = BASE_DIR / filename

    with get_connection() as connection:
        rows = connection.execute("""
        SELECT students.name, students.roll_number,
               attendance.subject, attendance.attendance_date,
               attendance.status
        FROM attendance
        JOIN students ON attendance.student_id=students.id
        ORDER BY attendance.attendance_date DESC
        """).fetchall()

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Student", "Roll Number", "Subject",
            "Date", "Status"
        ])

        writer.writerows([tuple(row) for row in rows])

    return path

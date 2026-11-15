
from database.db import get_connection


def validate_student(name, roll_number, course, branch,
                    semester, section):
    if not name.strip():
        raise ValueError("Student name is required.")

    if not roll_number.strip():
        raise ValueError("Roll number is required.")

    if not course.strip():
        raise ValueError("Course is required.")

    if not branch.strip():
        raise ValueError("Branch is required.")

    if not section.strip():
        raise ValueError("Section is required.")

    semester = int(semester)

    if not 1 <= semester <= 12:
        raise ValueError("Semester must be between 1 and 12.")

    return semester


def add_student(name, roll_number, course, branch,
                semester, section, email="", phone="",
                admission_year=2026):

    semester = validate_student(
        name, roll_number, course, branch, semester, section
    )

    with get_connection() as connection:
        cursor = connection.execute("""
        INSERT INTO students
        (name, roll_number, course, branch, semester,
         section, email, phone, admission_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name.strip(),
            roll_number.strip().upper(),
            course.strip(),
            branch.strip(),
            semester,
            section.strip(),
            email.strip(),
            phone.strip(),
            int(admission_year)
        ))

        return cursor.lastrowid


def get_all_students():
    with get_connection() as connection:
        return connection.execute("""
        SELECT * FROM students ORDER BY id DESC
        """).fetchall()


def get_student_by_id(student_id):
    with get_connection() as connection:
        return connection.execute("""
        SELECT * FROM students WHERE id = ?
        """, (student_id,)).fetchone()


def search_students(keyword):
    keyword = f"%{keyword.strip()}%"

    with get_connection() as connection:
        return connection.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR roll_number LIKE ?
        OR course LIKE ?
        OR branch LIKE ?
        ORDER BY id DESC
        """, (keyword, keyword, keyword, keyword)).fetchall()


def update_student(student_id, name, roll_number,
                   course, branch, semester, section,
                   email="", phone="", admission_year=2026):

    semester = validate_student(
        name, roll_number, course, branch, semester, section
    )

    with get_connection() as connection:
        cursor = connection.execute("""
        UPDATE students
        SET name=?, roll_number=?, course=?, branch=?,
            semester=?, section=?, email=?, phone=?,
            admission_year=?
        WHERE id=?
        """, (
            name.strip(),
            roll_number.strip().upper(),
            course.strip(),
            branch.strip(),
            semester,
            section.strip(),
            email.strip(),
            phone.strip(),
            int(admission_year),
            student_id
        ))

        return cursor.rowcount > 0


def delete_student(student_id):
    with get_connection() as connection:
        cursor = connection.execute("""
        DELETE FROM students WHERE id=?
        """, (student_id,))

        return cursor.rowcount > 0

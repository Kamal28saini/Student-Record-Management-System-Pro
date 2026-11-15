
from database.db import get_connection


def add_marks(student_id, subject, marks_obtained,
              max_marks=100, exam_type="Mid Term", semester=1):

    marks_obtained = float(marks_obtained)
    max_marks = float(max_marks)
    semester = int(semester)

    if not subject.strip():
        raise ValueError("Subject is required.")

    if max_marks <= 0:
        raise ValueError("Maximum marks must be greater than zero.")

    if not 0 <= marks_obtained <= max_marks:
        raise ValueError("Marks must be within the valid range.")

    with get_connection() as connection:
        cursor = connection.execute("""
        INSERT INTO marks
        (student_id, subject, marks_obtained,
         max_marks, exam_type, semester)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student_id, subject.strip(), marks_obtained,
            max_marks, exam_type, semester
        ))

        return cursor.lastrowid


def get_all_marks():
    with get_connection() as connection:
        return connection.execute("""
        SELECT marks.*, students.name, students.roll_number
        FROM marks
        JOIN students ON marks.student_id = students.id
        ORDER BY marks.id DESC
        """).fetchall()


def get_marks_by_student(student_id):
    with get_connection() as connection:
        return connection.execute("""
        SELECT * FROM marks
        WHERE student_id=?
        ORDER BY id DESC
        """, (student_id,)).fetchall()


def delete_marks(mark_id):
    with get_connection() as connection:
        cursor = connection.execute("""
        DELETE FROM marks WHERE id=?
        """, (mark_id,))

        return cursor.rowcount > 0


def calculate_percentage(student_id, semester):
    with get_connection() as connection:
        result = connection.execute("""
        SELECT SUM(marks_obtained), SUM(max_marks)
        FROM marks
        WHERE student_id=? AND semester=?
        """, (student_id, semester)).fetchone()

    obtained, maximum = result

    if not maximum:
        return 0.0

    return round(obtained / maximum * 100, 2)


from datetime import date
from database.db import get_connection


def mark_attendance(student_id, subject,
                    attendance_date=None, status="Present"):

    if not subject.strip():
        raise ValueError("Subject is required.")

    if status not in ("Present", "Absent"):
        raise ValueError("Status must be Present or Absent.")

    if attendance_date is None:
        attendance_date = date.today().isoformat()

    with get_connection() as connection:
        cursor = connection.execute("""
        INSERT INTO attendance
        (student_id, subject, attendance_date, status)
        VALUES (?, ?, ?, ?)
        """, (
            student_id, subject.strip(), attendance_date, status
        ))

        return cursor.lastrowid


def get_all_attendance():
    with get_connection() as connection:
        return connection.execute("""
        SELECT attendance.*, students.name, students.roll_number
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        ORDER BY attendance_date DESC
        """).fetchall()


def get_attendance_by_student(student_id):
    with get_connection() as connection:
        return connection.execute("""
        SELECT * FROM attendance
        WHERE student_id=?
        ORDER BY attendance_date DESC
        """, (student_id,)).fetchall()


def delete_attendance(attendance_id):
    with get_connection() as connection:
        cursor = connection.execute("""
        DELETE FROM attendance WHERE id=?
        """, (attendance_id,))

        return cursor.rowcount > 0


def calculate_attendance_percentage(student_id, subject=None):
    with get_connection() as connection:
        if subject:
            result = connection.execute("""
            SELECT
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END),
            COUNT(*)
            FROM attendance
            WHERE student_id=? AND subject=?
            """, (student_id, subject)).fetchone()
        else:
            result = connection.execute("""
            SELECT
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END),
            COUNT(*)
            FROM attendance
            WHERE student_id=?
            """, (student_id,)).fetchone()

    present, total = result

    if not total:
        return 0.0

    return round(present / total * 100, 2)

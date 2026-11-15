
import unittest

from database.db import initialize_database
from modules.student_manager import (
    add_student,
    get_all_students,
    search_students,
    get_student_by_id,
    delete_student
)


class StudentManagerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def test_add_student(self):
        roll = "TEST001"

        try:
            student_id = add_student(
                "Test Student",
                roll,
                "B.Tech",
                "AI & DS",
                3,
                "A",
                "test@example.com",
                "9999999999",
                2026
            )

            student = get_student_by_id(student_id)

            self.assertIsNotNone(student)
            self.assertEqual(student["roll_number"], roll)

        finally:
            from database.db import get_connection

            with get_connection() as connection:
                connection.execute(
                    "DELETE FROM students WHERE roll_number=?",
                    (roll,)
                )

    def test_search_student(self):
        results = search_students("TEST")
        self.assertIsInstance(results, list)

    def test_get_all_students(self):
        students = get_all_students()
        self.assertIsInstance(students, list)

    def test_delete_student(self):
        student_id = add_student(
            "Delete Test",
            "DELETE001",
            "B.Tech",
            "AI & DS",
            1,
            "A",
            "",
            "",
            2026
        )

        result = delete_student(student_id)

        self.assertTrue(result)
        self.assertIsNone(get_student_by_id(student_id))


if __name__ == "__main__":
    unittest.main()

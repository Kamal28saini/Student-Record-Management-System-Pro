
import tkinter as tk
from tkinter import ttk, messagebox

from modules.student_manager import (
    add_student,
    update_student,
    get_student_by_id
)


class StudentForm(tk.Toplevel):

    def __init__(self, parent, refresh_callback, student_id=None):
        super().__init__(parent)

        self.refresh_callback = refresh_callback
        self.student_id = student_id

        self.title("Student Registration")
        self.geometry("500x650")
        self.resizable(False, False)

        self.entries = {}

        fields = [
            ("Name", "name"),
            ("Roll Number", "roll_number"),
            ("Course", "course"),
            ("Branch", "branch"),
            ("Semester", "semester"),
            ("Section", "section"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Admission Year", "admission_year")
        ]

        ttk.Label(
            self,
            text="Student Registration",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        form = ttk.Frame(self)
        form.pack(fill="both", padx=25)

        for label, key in fields:
            ttk.Label(form, text=label).pack(anchor="w", pady=(8, 2))

            entry = ttk.Entry(form, width=45)
            entry.pack(fill="x")

            self.entries[key] = entry

        self.entries["semester"].insert(0, "1")
        self.entries["section"].insert(0, "A")
        self.entries["admission_year"].insert(0, "2026")

        if student_id:
            self.load_student(student_id)

        ttk.Button(
            self,
            text="Save Student",
            command=self.save_student
        ).pack(pady=25)

    def load_student(self, student_id):
        student = get_student_by_id(student_id)

        if student:
            for key in self.entries:
                self.entries[key].insert(0, str(student[key] or ""))

    def save_student(self):
        data = {
            key: entry.get().strip()
            for key, entry in self.entries.items()
        }

        try:
            if self.student_id:
                update_student(
                    self.student_id,
                    data["name"],
                    data["roll_number"],
                    data["course"],
                    data["branch"],
                    data["semester"],
                    data["section"],
                    data["email"],
                    data["phone"],
                    data["admission_year"]
                )
            else:
                add_student(
                    data["name"],
                    data["roll_number"],
                    data["course"],
                    data["branch"],
                    data["semester"],
                    data["section"],
                    data["email"],
                    data["phone"],
                    data["admission_year"]
                )

            messagebox.showinfo(
                "Success",
                "Student record saved successfully!"
            )

            self.refresh_callback()
            self.destroy()

        except Exception as error:
            messagebox.showerror("Error", str(error))

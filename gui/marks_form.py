
import tkinter as tk
from tkinter import ttk, messagebox

from modules.student_manager import get_all_students
from modules.marks_manager import add_marks


class MarksForm(tk.Toplevel):

    def __init__(self, parent, refresh_callback):
        super().__init__(parent)

        self.refresh_callback = refresh_callback

        self.title("Marks Management")
        self.geometry("450x500")
        self.resizable(False, False)

        ttk.Label(
            self,
            text="Add Student Marks",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        form = ttk.Frame(self)
        form.pack(fill="both", padx=30)

        ttk.Label(form, text="Student").pack(anchor="w")

        students = get_all_students()
        self.student_map = {
            f"{s['roll_number']} - {s['name']}": s["id"]
            for s in students
        }

        self.student_var = tk.StringVar()

        ttk.Combobox(
            form,
            textvariable=self.student_var,
            values=list(self.student_map.keys()),
            state="readonly"
        ).pack(fill="x", pady=5)

        self.subject = self.create_field(form, "Subject")
        self.obtained = self.create_field(form, "Marks Obtained")
        self.maximum = self.create_field(form, "Maximum Marks")
        self.exam_type = self.create_field(form, "Exam Type")
        self.semester = self.create_field(form, "Semester")

        self.maximum.insert(0, "100")
        self.exam_type.insert(0, "Mid Term")
        self.semester.insert(0, "1")

        ttk.Button(
            self,
            text="Save Marks",
            command=self.save_marks
        ).pack(pady=25)

    @staticmethod
    def create_field(parent, label):
        ttk.Label(parent, text=label).pack(anchor="w", pady=(8, 2))
        entry = ttk.Entry(parent)
        entry.pack(fill="x")
        return entry

    def save_marks(self):
        student = self.student_var.get()

        if student not in self.student_map:
            messagebox.showerror("Error", "Select a student.")
            return

        try:
            add_marks(
                self.student_map[student],
                self.subject.get(),
                self.obtained.get(),
                self.maximum.get(),
                self.exam_type.get(),
                self.semester.get()
            )

            messagebox.showinfo("Success", "Marks saved!")
            self.refresh_callback()
            self.destroy()

        except Exception as error:
            messagebox.showerror("Error", str(error))


import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from modules.student_manager import get_all_students
from modules.attendance_manager import mark_attendance


class AttendanceForm(tk.Toplevel):

    def __init__(self, parent, refresh_callback):
        super().__init__(parent)

        self.refresh_callback = refresh_callback

        self.title("Attendance Management")
        self.geometry("450x450")
        self.resizable(False, False)

        ttk.Label(
            self,
            text="Mark Attendance",
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
        self.attendance_date = self.create_field(
            form, "Date (YYYY-MM-DD)"
        )
        self.attendance_date.insert(0, date.today().isoformat())

        ttk.Label(form, text="Status").pack(anchor="w", pady=(8, 2))

        self.status = tk.StringVar(value="Present")

        ttk.Combobox(
            form,
            textvariable=self.status,
            values=["Present", "Absent"],
            state="readonly"
        ).pack(fill="x")

        ttk.Button(
            self,
            text="Save Attendance",
            command=self.save_attendance
        ).pack(pady=25)

    @staticmethod
    def create_field(parent, label):
        ttk.Label(parent, text=label).pack(anchor="w", pady=(8, 2))
        entry = ttk.Entry(parent)
        entry.pack(fill="x")
        return entry

    def save_attendance(self):
        student = self.student_var.get()

        if student not in self.student_map:
            messagebox.showerror("Error", "Select a student.")
            return

        try:
            mark_attendance(
                self.student_map[student],
                self.subject.get(),
                self.attendance_date.get(),
                self.status.get()
            )

            messagebox.showinfo("Success", "Attendance saved!")
            self.refresh_callback()
            self.destroy()

        except Exception as error:
            messagebox.showerror("Error", str(error))

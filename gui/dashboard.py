
import tkinter as tk
from tkinter import ttk, messagebox

from database.db import (
    get_student_count,
    get_marks_count,
    get_attendance_count
)

from modules.student_manager import (
    get_all_students,
    search_students,
    delete_student
)

from modules.report_manager import (
    export_students_csv,
    export_marks_csv,
    export_attendance_csv
)

from gui.student_form import StudentForm
from gui.marks_form import MarksForm
from gui.attendance_form import AttendanceForm


class Dashboard:

    def __init__(self, root):
        self.root = root

        self.root.title("Student Record Management System Pro")
        self.root.geometry("1350x800")
        self.root.minsize(1100, 650)
        self.root.configure(bg="#F4F7FB")

        self.setup_style()
        self.setup_sidebar()
        self.setup_main_area()
        self.refresh_dashboard()

    # ================= STYLE =================

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#1E293B",
            rowheight=38,
            font=("Arial", 11),
            fieldbackground="white",
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#E8EEF7",
            foreground="#1E293B",
            font=("Arial", 11, "bold"),
            padding=10,
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#1E40AF")]
        )

    # ================= SIDEBAR =================

    def setup_sidebar(self):
        self.sidebar = tk.Frame(
            self.root,
            bg="#14213D",
            width=240
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="SRMS PRO",
            bg="#14213D",
            fg="white",
            font=("Arial", 23, "bold")
        ).pack(pady=(35, 5))

        tk.Label(
            self.sidebar,
            text="Student Management",
            bg="#14213D",
            fg="#94A3B8",
            font=("Arial", 10)
        ).pack(pady=(0, 35))

        self.sidebar_button("Dashboard", self.refresh_dashboard)
        self.sidebar_button("Add Student", self.add_student)
        self.sidebar_button("Manage Marks", self.add_marks)
        self.sidebar_button("Attendance", self.add_attendance)

        tk.Frame(
            self.sidebar,
            bg="#334155",
            height=1
        ).pack(fill="x", padx=20, pady=20)

        self.sidebar_button("Export Students", self.export_students)
        self.sidebar_button("Export Marks", self.export_marks)
        self.sidebar_button("Export Attendance", self.export_attendance)

        tk.Label(
            self.sidebar,
            text="Version 1.0.0",
            bg="#14213D",
            fg="#64748B",
            font=("Arial", 9)
        ).pack(side="bottom", pady=20)

    def sidebar_button(self, text, command):
        button = tk.Label(
            self.sidebar,
            text="   " + text,
            bg="#14213D",
            fg="#FFFFFF",
            font=("Arial", 12),
            anchor="w",
            padx=20,
            pady=14,
            cursor="hand2"
        )

        button.pack(fill="x", padx=10, pady=3)

        button.bind(
            "<Button-1>",
            lambda event: command()
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(
                bg="#263B65",
                fg="#FFFFFF"
            )
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(
                bg="#14213D",
                fg="#FFFFFF"
            )
        )

    # ================= MAIN AREA =================

    def setup_main_area(self):
        self.main = tk.Frame(
            self.root,
            bg="#F4F7FB"
        )

        self.main.pack(
            side="left",
            fill="both",
            expand=True
        )

        header = tk.Frame(
            self.main,
            bg="#F4F7FB"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        tk.Label(
            header,
            text="Dashboard Overview",
            bg="#F4F7FB",
            fg="#172554",
            font=("Arial", 25, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Manage students, marks and attendance records",
            bg="#F4F7FB",
            fg="#64748B",
            font=("Arial", 12)
        ).pack(anchor="w", pady=5)

        self.setup_statistics()
        self.setup_toolbar()
        self.setup_search()
        self.setup_table()

    # ================= STATISTICS =================

    def setup_statistics(self):
        cards = tk.Frame(
            self.main,
            bg="#F4F7FB"
        )

        cards.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.student_label = self.create_card(
            cards, "TOTAL STUDENTS", "0", "#2563EB"
        )

        self.marks_label = self.create_card(
            cards, "MARKS RECORDS", "0", "#059669"
        )

        self.attendance_label = self.create_card(
            cards, "ATTENDANCE RECORDS", "0", "#EA580C"
        )

    @staticmethod
    def create_card(parent, title, value, accent):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        card.pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        tk.Frame(
            card,
            bg=accent,
            height=5
        ).pack(fill="x")

        tk.Label(
            card,
            text=title,
            bg="white",
            fg="#64748B",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 5))

        value_label = tk.Label(
            card,
            text=value,
            bg="white",
            fg=accent,
            font=("Arial", 27, "bold")
        )

        value_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        return value_label

    # ================= TOOLBAR =================

    def setup_toolbar(self):
        toolbar = tk.Frame(
            self.main,
            bg="#F4F7FB"
        )

        toolbar.pack(
            fill="x",
            padx=30,
            pady=15
        )

        self.modern_button(
            toolbar,
            "+ Add Student",
            self.add_student,
            "#2563EB"
        )

        self.modern_button(
            toolbar,
            "Update Student",
            self.update_student,
            "#475569"
        )

        self.modern_button(
            toolbar,
            "Delete Student",
            self.delete_selected,
            "#DC2626"
        )

        self.modern_button(
            toolbar,
            "Refresh",
            self.refresh_dashboard,
            "#64748B"
        )

    @staticmethod
    def modern_button(parent, text, command, color):
        button = tk.Label(
            parent,
            text=text,
            bg=color,
            fg="#FFFFFF",
            font=("Arial", 10, "bold"),
            padx=16,
            pady=11,
            cursor="hand2"
        )

        button.pack(side="left", padx=5)

        button.bind(
            "<Button-1>",
            lambda event: command()
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(
                bg="#1E293B",
                fg="#FFFFFF"
            )
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(
                bg=color,
                fg="#FFFFFF"
            )
        )

        return button

    # ================= SEARCH =================

    def setup_search(self):
        frame = tk.Frame(
            self.main,
            bg="#F4F7FB"
        )

        frame.pack(
            fill="x",
            padx=35,
            pady=(5, 15)
        )

        tk.Label(
            frame,
            text="Student Records",
            bg="#F4F7FB",
            fg="#172554",
            font=("Arial", 17, "bold")
        ).pack(side="left")

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            frame,
            textvariable=self.search_var,
            font=("Arial", 12),
            relief="solid",
            bd=1,
            width=28,
            bg="white",
            fg="#1E293B",
            insertbackground="#1E293B"
        )

        search_entry.pack(
            side="right",
            ipady=8,
            padx=5
        )

        search_entry.insert(
            0,
            "Search students..."
        )

        search_entry.bind(
            "<FocusIn>",
            lambda event: self.clear_placeholder(search_entry)
        )

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.search_records()
        )

        tk.Label(
            frame,
            text="Search:",
            bg="#F4F7FB",
            fg="#475569",
            font=("Arial", 11)
        ).pack(
            side="right",
            padx=5
        )

    def clear_placeholder(self, entry):
        if entry.get() == "Search students...":
            entry.delete(0, "end")

    def search_records(self):
        keyword = self.search_var.get()

        if keyword == "Search students...":
            self.load_students()
            return

        self.load_students(search_students(keyword))

    # ================= TABLE =================

    def setup_table(self):
        frame = tk.Frame(
            self.main,
            bg="white",
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        columns = (
            "id", "name", "roll", "course",
            "branch", "semester", "section",
            "email", "phone"
        )

        self.tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Student Name",
            "roll": "Roll Number",
            "course": "Course",
            "branch": "Branch",
            "semester": "Semester",
            "section": "Section",
            "email": "Email",
            "phone": "Phone"
        }

        widths = {
            "id": 50,
            "name": 160,
            "roll": 110,
            "course": 100,
            "branch": 130,
            "semester": 80,
            "section": 70,
            "email": 180,
            "phone": 110
        }

        for column in columns:
            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self.update_student()
        )

    # ================= DATA =================

    def refresh_dashboard(self):
        self.student_label.config(
            text=str(get_student_count())
        )

        self.marks_label.config(
            text=str(get_marks_count())
        )

        self.attendance_label.config(
            text=str(get_attendance_count())
        )

        self.load_students()

    def load_students(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if records is None:
            records = get_all_students()

        for student in records:
            self.tree.insert(
                "",
                "end",
                values=(
                    student["id"],
                    student["name"],
                    student["roll_number"],
                    student["course"],
                    student["branch"],
                    student["semester"],
                    student["section"],
                    student["email"],
                    student["phone"]
                )
            )

    def get_selected_student_id(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection",
                "Please select a student first."
            )
            return None

        values = self.tree.item(
            selected[0], "values"
        )

        return int(values[0])

    # ================= ACTIONS =================

    def add_student(self):
        StudentForm(
            self.root,
            self.refresh_dashboard
        )

    def update_student(self):
        student_id = self.get_selected_student_id()

        if student_id:
            StudentForm(
                self.root,
                self.refresh_dashboard,
                student_id
            )

    def delete_selected(self):
        student_id = self.get_selected_student_id()

        if not student_id:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this student and all associated records?"
        )

        if confirm:
            try:
                delete_student(student_id)

                messagebox.showinfo(
                    "Success",
                    "Student deleted successfully."
                )

                self.refresh_dashboard()

            except Exception as error:
                messagebox.showerror(
                    "Error",
                    str(error)
                )

    def add_marks(self):
        if get_student_count() == 0:
            messagebox.showwarning(
                "Warning",
                "Add a student first."
            )
            return

        MarksForm(
            self.root,
            self.refresh_dashboard
        )

    def add_attendance(self):
        if get_student_count() == 0:
            messagebox.showwarning(
                "Warning",
                "Add a student first."
            )
            return

        AttendanceForm(
            self.root,
            self.refresh_dashboard
        )

    # ================= EXPORT =================

    def export_students(self):
        self.export_report(export_students_csv)

    def export_marks(self):
        self.export_report(export_marks_csv)

    def export_attendance(self):
        self.export_report(export_attendance_csv)

    @staticmethod
    def export_report(function):
        try:
            path = function()

            messagebox.showinfo(
                "Export Successful",
                f"Report saved successfully:\n{path}"
            )

        except Exception as error:
            messagebox.showerror(
                "Export Error", str(error)
            )

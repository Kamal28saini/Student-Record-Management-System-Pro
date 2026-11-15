
import tkinter as tk
from tkinter import messagebox

from database.db import initialize_database
from gui.dashboard import Dashboard


def main():
    initialize_database()

    root = tk.Tk()

    try:
        Dashboard(root)
        root.mainloop()

    except Exception as error:
        messagebox.showerror(
            "Application Error",
            str(error)
        )


if __name__ == "__main__":
    main()

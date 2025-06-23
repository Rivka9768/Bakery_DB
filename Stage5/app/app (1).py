import tkinter as tk
from tkinter import messagebox
import subprocess

# Import the reports screen class
from reports_screen import BakeryReportsScreen  # Assuming the file is named paste.py
from proc_screen import ProduceApp  # Assuming the file is named produce_screen.py
# פונקציות מדומות לפתיחת מסכים אחרים (נשנה בהמשך)
from employee_screen import EmployeeApp  # ✅ import the class
from baked_goods_screen import BakedGoodsApp  # ✅ import the class

def open_employee_screen():
    """Open the employee management screen"""
    try:
        EmployeeApp()
    except Exception as e:
        messagebox.showerror("שגיאה", f"לא ניתן לפתוח את מסך ניהול עובדים: {str(e)}")

def open_baked_goods_screen():
    """Open the baked goods management screen"""
    try:
        BakedGoodsApp()
    except Exception as e:
        messagebox.showerror("שגיאה", f"לא ניתן לפתוח את מסך ניהול מוצרי מאפה: {str(e)}")

def open_shifts_screen():
    ProduceApp() # ✅ open the employee management screen

def open_reports_screen():
    """Open the reports screen"""
    try:
        # Create a new window for the reports screen
        reports_window = tk.Toplevel(root)
        reports_app = BakeryReportsScreen(reports_window)
    except Exception as e:
        messagebox.showerror("שגיאה", f"לא ניתן לפתוח את מסך הדוחות: {str(e)}")

def exit_app():
    root.destroy()

# יצירת חלון ראשי
root = tk.Tk()
root.title("מערכת ניהול מאפייה")
root.geometry("400x450")
root.configure(bg="#f4f4f4")

# כותרת
title = tk.Label(root, text="ברוכים הבאים למערכת הניהול", font=("Arial", 16), bg="#f4f4f4")
title.pack(pady=20)

# כפתורים
btn_employees = tk.Button(root, text="ניהול עובדים", width=25, height=2, command=open_employee_screen)
btn_employees.pack(pady=10)

btn_baked_goods = tk.Button(root, text="ניהול מוצרי מאפה", width=25, height=2, command=open_baked_goods_screen)
btn_baked_goods.pack(pady=10)

btn_shifts = tk.Button(root, text="ניהול פסי ייצור", width=25, height=2, command=open_shifts_screen)
btn_shifts.pack(pady=10)

btn_reports = tk.Button(root, text="דוחות ושאילתות", width=25, height=2, command=open_reports_screen)
btn_reports.pack(pady=10)

btn_exit = tk.Button(root, text="יציאה", width=25, height=2, bg="#d9534f", fg="white", command=exit_app)
btn_exit.pack(pady=30)

# הצגת המסך
root.mainloop()
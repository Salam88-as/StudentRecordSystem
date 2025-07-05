import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

DATA_FILE = "students.csv"
USERNAME = "Salam"
PASSWORD = "123"
students = []
next_id = 1

# ----------- File Handling -----------
def load_data():
    global next_id
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header if present
            for row in reader:
                if len(row) == 11:  # 11 columns (ID + 7 subjects + Percentage + Grade)
                    sid, name, vp, ai, ailab, ma, cn, cnlab, tbr, perc, grade = row
                    students.append((int(sid), name, float(vp), float(ai), float(ailab), float(ma), float(cn), float(cnlab), float(tbr), float(perc), grade))
                    next_id = max(next_id, int(sid) + 1)

def save_data():
    with open(DATA_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "VP", "AI", "AI Lab", "MAD", "CN", "CN Lab", "TBR", "Percentage", "Grade"])
        for s in students:
            writer.writerow(s)

# ----------- Grading -----------
def calculate_grade(percentage):
    if percentage >= 90:
        return 'A'
    elif percentage >= 75:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

# ----------- GUI Windows -----------

def add_student_window():
    window = tk.Toplevel(root)
    window.title("Add Student")
    window.geometry("420x480")
    window.configure(bg="#f9f9f9")

    labels = ["Student ID:", "Full Name:", "Visual Programming:", "Artificial Intelligence:",
              "AI Lab:", "Mobile Applications:", "Computer Network:", "CN Lab:", "Technical Business Report:"]
    entries = []

    for i, text in enumerate(labels):
        tk.Label(window, text=text, font=("Arial", 12, "bold"), bg="#f9f9f9").grid(row=i, column=0, pady=5, padx=10, sticky="e")
        entry = tk.Entry(window, font=("Arial", 12))
        entry.grid(row=i, column=1, pady=5, padx=10)
        entries.append(entry)

    entries[0].insert(0, str(next_id))  # Suggest next ID

    def submit():
        try:
            sid = int(entries[0].get())
            vp = float(entries[2].get())
            ai = float(entries[3].get())
            ailab = float(entries[4].get())
            ma = float(entries[5].get())
            cn = float(entries[6].get())
            cnlab = float(entries[7].get())
            tbr = float(entries[8].get())
            # Check valid marks 0-100
            if not all(0 <= mark <= 100 for mark in [vp, ai, ailab, ma, cn, cnlab, tbr]):
                raise ValueError("Marks must be between 0 and 100")
            # Check unique positive ID
            if sid < 1 or any(s[0] == sid for s in students):
                raise ValueError("ID already exists or invalid")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        name = entries[1].get().strip()
        if not name:
            messagebox.showerror("Invalid Input", "Name cannot be empty")
            return

        total = vp + ai + ailab + ma + cn + cnlab + tbr
        perc = round(total / 7, 2)
        grade = calculate_grade(perc)

        students.append((sid, name, vp, ai, ailab, ma, cn, cnlab, tbr, perc, grade))
        global next_id
        next_id = max(next_id, sid + 1)
        save_data()
        update_tree()
        messagebox.showinfo("Success", f"Student {name} added with {perc}% and Grade {grade}")
        window.destroy()

    tk.Button(window, text="Submit", command=submit, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=18).grid(row=9, column=0, columnspan=2, pady=20)

def search_student_window():
    window = tk.Toplevel(root)
    window.title("Search Student")
    window.geometry("400x300")
    window.configure(bg="#f9f9f9")

    tk.Label(window, text="Enter Student ID:", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=15)
    entry = tk.Entry(window, font=("Arial", 12))
    entry.pack(pady=10)

    result = tk.Label(window, text="", font=("Arial", 12), bg="#f9f9f9", wraplength=350)
    result.pack(pady=10)

    def search():
        sid = entry.get()
        if not sid.isdigit():
            messagebox.showerror("Error", "Enter a valid ID")
            return
        sid = int(sid)
        for s in students:
            if s[0] == sid:
                result.config(text=(
                    f"Name: {s[1]}\n"
                    f"VP: {s[2]}, AI: {s[3]}, AI Lab: {s[4]}\n"
                    f"MAD: {s[5]}, CN: {s[6]}, CN Lab: {s[7]}\n"
                    f"TBR: {s[8]}\n"
                    f"Percentage: {s[9]}%, Grade: {s[10]}"
                ))
                return
        result.config(text="Student Not Found")

    tk.Button(window, text="Search", command=search, bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=18).pack(pady=15)

def delete_student_window():
    window = tk.Toplevel(root)
    window.title("Delete Student")
    window.geometry("350x200")
    window.configure(bg="#f9f9f9")

    tk.Label(window, text="Enter Student ID:", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=15)
    entry = tk.Entry(window, font=("Arial", 12))
    entry.pack(pady=10)

    def delete():
        sid = entry.get()
        if not sid.isdigit():
            messagebox.showerror("Error", "Invalid ID")
            return
        sid = int(sid)
        for s in students:
            if s[0] == sid:
                students.remove(s)
                save_data()
                update_tree()
                messagebox.showinfo("Deleted", f"Student with ID {sid} removed")
                window.destroy()
                return
        messagebox.showerror("Not Found", "No student with this ID")

    tk.Button(window, text="Delete", command=delete, bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=18).pack(pady=15)

def count_students_window():
    total = len(students)
    messagebox.showinfo("Total Students", f"Total number of students: {total}")

def update_tree():
    for item in tree.get_children():
        tree.delete(item)
    for s in students:
        tree.insert('', tk.END, values=s)

# ----------- Main Window -----------
def main_window():
    global root, tree
    root = tk.Tk()
    root.title("🎓 Student Record System")
    root.geometry("1020x600")
    root.configure(bg="#f5f5f5")

    frame = tk.Frame(root, bg="#fff", bd=2, relief="solid")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    sidebar = tk.Frame(frame, bg="#1a237e", width=270)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="Student Record\nSystem", font=("Arial", 16, "bold"), fg="#fff", bg="#1a237e", justify="center").pack(pady=25)
    btn_params = {"font": ("Arial", 13), "fg": "#fff", "bg": "#1a237e", "bd": 0, "width": 20, "pady": 10}
    tk.Button(sidebar, text="➕ Add Student", command=add_student_window, **btn_params).pack(pady=5)
    tk.Button(sidebar, text="🔍 Search", command=search_student_window, **btn_params).pack(pady=5)
    tk.Button(sidebar, text="❌ Delete", command=delete_student_window, **btn_params).pack(pady=5)
    tk.Button(sidebar, text="🔢 Count", command=count_students_window, **btn_params).pack(pady=5)
    tk.Button(sidebar, text="🚪 Exit", command=root.destroy, **btn_params).pack(pady=5)
    tk.Button(sidebar, text="📤 Export to Excel", font=("Arial", 13), fg="#fff", bg="#1a237e", bd=0, width=20, pady=10, command=export_to_excel).pack(pady=5)

    content = tk.Frame(frame, bg="#fff")
    content.pack(side="right", fill="both", expand=True, padx=10)

    tk.Label(content, text="Student Record System", font=("Arial", 22, "bold"), fg="#1a237e").pack(pady=12)
    tree = ttk.Treeview(content, columns=("ID", "Name", "VP", "AI", "AI Lab", "MAD", "CN", "CN Lab", "TBR", "Percentage", "Grade"), show='headings')
    tree.pack(fill="both", expand=True)

    for col in ("ID", "Name", "VP", "AI", "AI Lab", "MAD", "CN", "CN Lab", "TBR", "Percentage", "Grade"):
        tree.heading(col, text=col)
        tree.column(col, width=110 if col == "Name" else 80)

    update_tree()

    root.mainloop()

# ----------- Login Window -----------

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if username == USERNAME and password == PASSWORD:
        login_win.destroy()
        load_data()
        main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password", icon="warning")

login_win = tk.Tk()
login_win.title("Login Portal")
login_win.geometry("420x350")
login_win.configure(bg="#2c3e50")

# Stylish title
tk.Label(login_win, text="Student Record System", font=("Helvetica", 22, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=25)

frame = tk.Frame(login_win, bg="#34495e", padx=25, pady=25)
frame.pack(expand=True, padx=20, pady=10)

tk.Label(frame, text="Username:", font=("Arial", 14, "bold"), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, pady=15, sticky="e")
username_entry = tk.Entry(frame, font=("Arial", 14), width=25, bg="#ecf0f1", bd=0)
username_entry.grid(row=0, column=1, pady=15, padx=10)

tk.Label(frame, text="Password:", font=("Arial", 14, "bold"), bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, pady=15, sticky="e")
password_entry = tk.Entry(frame, show="*", font=("Arial", 14), width=25, bg="#ecf0f1", bd=0)
password_entry.grid(row=1, column=1, pady=15, padx=10)

login_btn = tk.Button(frame, text="Login", command=login, font=("Arial", 14, "bold"), bg="#27ae60", fg="white", width=18, bd=0)
login_btn.grid(row=2, column=0, columnspan=2, pady=25)

login_win.mainloop()

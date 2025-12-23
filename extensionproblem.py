import tkinter as tk
from tkinter import simpledialog, messagebox

STUDENT_FILE = 'Assessment 1 - Skills Portfolio\\A1 - Resources\\studentMarks.txt'

# Load and save students
def load_students():
    students = []
    try:
        with open(STUDENT_FILE, "r") as f:
            total = int(f.readline())
            for line in f:
                parts = line.strip().split(",")
                s = {"id": int(parts[0]), "name": parts[1],
                     "marks": [int(parts[2]), int(parts[3]), int(parts[4])],
                     "exam": int(parts[5])}
                students.append(s)
    except:
        pass
    return students

def save_students(students):
    try:
        with open(STUDENT_FILE, "w") as f:
            f.write(str(len(students)) + "\n")
            for s in students:
                line = f"{s['id']},{s['name']},{s['marks'][0]},{s['marks'][1]},{s['marks'][2]},{s['exam']}\n"
                f.write(line)
    except:
        messagebox.showerror("Error", "Could not save file!")

# Helper functions
def total_marks(s):
    return sum(s['marks']) + s['exam']

def percentage(s):
    return round(total_marks(s)/160*100, 2)

def grade(s):
    p = percentage(s)
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"

# Main App
class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("950x600")
        self.students = load_students()
        self.root.configure(bg="#cecece")
        self.menu()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def menu(self):
        self.clear()
        tk.Label(self.root, text="Student Manager", font=("Arial", 28, "bold"),
                 fg="white", bg="#1C1C1C", pady=20).pack(fill="x")
        btn_frame = tk.Frame(self.root, bg="#cecece", pady=30)
        btn_frame.pack()
        tk.Button(btn_frame, text="1. View All Students", width=30, bg="#1C1C1C", fg="white",
                  command=self.view_all).pack(pady=5)
        tk.Button(btn_frame, text="2. View One Student", width=30, bg="#1C1C1C", fg="white",
                  command=self.view_one).pack(pady=5)
        tk.Button(btn_frame, text="3. Highest Total", width=30, bg="#1C1C1C", fg="white",
                  command=self.view_highest).pack(pady=5)
        tk.Button(btn_frame, text="4. Lowest Total", width=30, bg="#1C1C1C", fg="white",
                  command=self.view_lowest).pack(pady=5)
        tk.Button(btn_frame, text="5. Sort Students", width=30, bg="#1C1C1C", fg="white",
                  command=self.sort_students).pack(pady=5)
        tk.Button(btn_frame, text="6. Add Student", width=30, bg="#1C1C1C", fg="white",
                  command=self.add_student).pack(pady=5)
        tk.Button(btn_frame, text="7. Delete Student", width=30, bg="#1C1C1C", fg="white",
                  command=self.delete_student).pack(pady=5)
        tk.Button(btn_frame, text="8. Update Student", width=30, bg="#1C1C1C", fg="white",
                  command=self.update_student).pack(pady=5)
        tk.Button(btn_frame, text="Exit", width=30, bg="#1C1C1C", fg="white", command=self.root.quit).pack(pady=10)

    # Grid display with mouse-wheel scroll
    def show_students(self, title, students_list):
        self.clear()
        tk.Label(self.root, text=title, font=("Arial", 22, "bold"),
                 bg="#1C1C1C", fg="white", pady=10).pack(fill="x")

        canvas_frame = tk.Frame(self.root, bg="#cecece")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        canvas = tk.Canvas(canvas_frame, bg="#cecece", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        frame = tk.Frame(canvas, bg="#cecece")
        canvas.create_window((0,0), window=frame, anchor="nw")

        # Mouse-wheel scrolling
        def scroll(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", scroll)

        cols = 3
        for i, s in enumerate(students_list):
            row = i // cols
            col = i % cols
            card = tk.Frame(frame, bg="#cecece", bd=2, relief="groove", padx=10, pady=8)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            tk.Label(card, text=f"Name: {s['name']}", font=("Arial", 14, "bold")).pack(fill="x")
            tk.Label(card, text=f"ID: {s['id']}", font=("Arial", 12)).pack(fill="x")
            tk.Label(card, text=f"Coursework: {sum(s['marks'])}/60", font=("Arial", 12)).pack(fill="x")
            tk.Label(card, text=f"Exam: {s['exam']}/100", font=("Arial", 12)).pack(fill="x")
            tk.Label(card, text=f"Percentage: {percentage(s)}%", font=("Arial", 12)).pack(fill="x")
            tk.Label(card, text=f"Grade: {grade(s)}", font=("Arial", 12, "bold")).pack(fill="x")

        for col in range(cols):
            frame.grid_columnconfigure(col, weight=1)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Summary at bottom
        if title=="All Students" and students_list:
            total_s = len(students_list)
            avg = round(sum(percentage(s) for s in students_list)/total_s, 2)
            summary = tk.Frame(self.root, bg="#cecece", pady=10)
            summary.pack(fill="x")
            tk.Label(summary, text=f"Total Students: {total_s}", font=("Arial", 14, "bold"), bg="#cecece").pack()
            tk.Label(summary, text=f"Average Percentage: {avg}%", font=("Arial", 14, "bold"), bg="#cecece").pack()

        tk.Button(self.root, text="Back to Menu", bg="#1C1C1C", fg="white",
                  command=self.menu).pack(pady=10)

    def find_student(self, prompt):
        val = simpledialog.askstring("Find Student", prompt)
        if not val: return None
        if val.isdigit():
            s = next((x for x in self.students if x['id']==int(val)), None)
        else:
            s = next((x for x in self.students if val.lower() in x['name'].lower()), None)
        if not s: messagebox.showerror("Error","Student not found")
        return s

    # Menu actions
    def view_all(self): self.show_students("All Students", self.students)
    def view_one(self):
        s = self.find_student("Enter ID or Name:")
        if s: self.show_students("Student Record", [s])
    def view_highest(self):
        if self.students: self.show_students("Highest Total", [max(self.students, key=total_marks)])
    def view_lowest(self):
        if self.students: self.show_students("Lowest Total", [min(self.students, key=total_marks)])

    def sort_students(self):
        choice = simpledialog.askstring("Sort","asc or desc?")
        if choice=="asc": self.students.sort(key=total_marks)
        elif choice=="desc": self.students.sort(key=total_marks, reverse=True)
        else: messagebox.showerror("Error","Invalid choice"); return
        self.show_students(f"Sorted ({choice})", self.students)

    def add_student(self):
        try:
            sid=int(simpledialog.askstring("Add","ID:"))
            name=simpledialog.askstring("Add","Name:")
            m1=int(simpledialog.askstring("Add","CW1:"))
            m2=int(simpledialog.askstring("Add","CW2:"))
            m3=int(simpledialog.askstring("Add","CW3:"))
            exam=int(simpledialog.askstring("Add","Exam:"))
            self.students.append({"id":sid,"name":name,"marks":[m1,m2,m3],"exam":exam})
            save_students(self.students)
            messagebox.showinfo("Success","Student added")
        except: messagebox.showerror("Error","Invalid input")

    def delete_student(self):
        s=self.find_student("ID or Name to delete:")
        if s:
            self.students.remove(s)
            save_students(self.students)
            messagebox.showinfo("Deleted","Student removed")
            self.view_all()

    def update_student(self):
        s=self.find_student("ID or Name to update:")
        if not s: return
        choice=simpledialog.askstring("Update","Field to update: ID, Name, CW1, CW2, CW3, Exam")
        if not choice: return
        try:
            if choice.lower()=="id": s['id']=int(simpledialog.askstring("Update","New ID:"))
            elif choice.lower()=="name": s['name']=simpledialog.askstring("Update","New Name:")
            elif choice.lower()=="cw1": s['marks'][0]=int(simpledialog.askstring("Update","New CW1:"))
            elif choice.lower()=="cw2": s['marks'][1]=int(simpledialog.askstring("Update","New CW2:"))
            elif choice.lower()=="cw3": s['marks'][2]=int(simpledialog.askstring("Update","New CW3:"))
            elif choice.lower()=="exam": s['exam']=int(simpledialog.askstring("Update","New Exam:"))
            else: messagebox.showerror("Error","Invalid field"); return
            save_students(self.students)
            messagebox.showinfo("Updated","Student updated")
            self.view_all()
        except: messagebox.showerror("Error","Invalid input")

# Run App
root = tk.Tk()
app = StudentManager(root)
root.mainloop()

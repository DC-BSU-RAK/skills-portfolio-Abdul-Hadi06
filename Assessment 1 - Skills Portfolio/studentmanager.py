import tkinter as tk
from tkinter import messagebox, simpledialog

# Student data file
STUDENT_FILE = 'Assessment 1 - Skills Portfolio\\A1 - Resources\\studentMarks.txt'

# Load students from file
def load_students(file_path):
    students = []
    try:
        with open(file_path, "r") as f:
            total = int(f.readline().strip())
            for line in f:
                parts = line.strip().split(",")
                student = {
                    "id": int(parts[0]),
                    "name": parts[1],
                    "marks": list(map(int, parts[2:5])),
                    "exam": int(parts[5])
                }
                students.append(student)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file:\n{e}")
    return students

# Helper functions
def calculate_total(student):
    return sum(student["marks"]) + student["exam"]

def calculate_percentage(student):
    return round((calculate_total(student)/160)*100, 2)

def calculate_grade(student):
    p = calculate_percentage(student)
    if p >= 70:
        return "A"
    elif p >= 60:
        return "B"
    elif p >= 50:
        return "C"
    elif p >= 40:
        return "D"
    else:
        return "F"

# Main App
class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("950x600")
        self.students = load_students(STUDENT_FILE)
        self.main_menu()
        self.root.configure(bg="#cecece")

    # Main Menu
    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Student Manager", font=("Arial", 28, "bold"),
                 fg="white", bg="#1C1C1C", pady=20).pack(fill="x")

        btn_frame = tk.Frame(self.root, bg="#cecece", pady=30)
        btn_frame.pack()

        self.add_button(btn_frame, "View All Student Records", self.view_all)
        self.add_button(btn_frame, "View Individual Student Record", self.view_one)
        self.add_button(btn_frame, "Student with Highest Total", self.view_highest)
        self.add_button(btn_frame, "Student with Lowest Total", self.view_lowest)
        self.add_button(btn_frame, "Exit", self.root.quit)

    def add_button(self, parent, text, command):
        b = tk.Button(parent, text=text, font=("Arial", 15), width=30,
                      bg="#1C1C1C", fg="white", command=command)
        b.pack(pady=10)

    # Clear all widgets
    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()

    # Display students in rows
    def display_students(self, title, students_list):
        self.clear_window()

        tk.Label(self.root, text=title, font=("Arial", 22, "bold"), bg="#1C1C1C", fg="white", pady=10).pack(fill="x")

    # Canvas to allow scrolling with mouse
        canvas_f = tk.Frame(self.root, bg="#cecece")
        canvas_f.pack(fill="both", expand=True, padx=10, pady=(0,10))

        canvas = tk.Canvas(canvas_f, bg="#cecece", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas, bg="#cecece")
        canvas.create_window((0,0), window=frame, anchor="nw")

    # Simple mouse wheel scrolling
        def scroll(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", scroll)

    # Put student cards in grid
        cols = 3
        for i, s in enumerate(students_list):
            r = i // cols
            c = i % cols
            card = tk.Frame(frame, bg="#cecece", bd=2, relief="groove", padx=10, pady=8)
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

            tk.Label(card, text=f"Name: {s['name']}", font=("Arial", 14, "bold")).pack(fill="x")
            tk.Label(card, text=f"ID: {s['id']}", font=("Arial", 12)).pack(fill="x")
            tk.Label(card, text=f"Coursework: {sum(s['marks'])}/60", font=("Arial", 12)).pack(fill="x")
            tk.Label(card, text=f"Exam: {s['exam']}/100", font=("Arial", 12)).pack(fill="x")
            tk.Label(card, text=f"Percentage: {calculate_percentage(s)}%", font=("Arial", 12)).pack(fill="x")
            tk.Label(card, text=f"Grade: {calculate_grade(s)}", font=("Arial", 12, "bold")).pack(fill="x")

    # Make columns expand evenly
        for col in range(cols):
            frame.grid_columnconfigure(col, weight=1)

    # Update scroll region
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # Summary section (inside the function!)
        if title == "All Students" and students_list:
            total_students = len(students_list)
            avg_percentage = round(sum(calculate_percentage(s) for s in students_list)/total_students, 2)
            summary_frame = tk.Frame(self.root, bg="#cecece", pady=10)
            summary_frame.pack(fill="x")
            tk.Label(summary_frame, text=f"Total Students: {total_students}", font=("Arial", 14, "bold"), bg="#cecece").pack()
            tk.Label(summary_frame, text=f"Average Percentage: {avg_percentage}%", font=("Arial", 14, "bold"), bg="#cecece").pack()

    # Back button centered at bottom
        bottom = tk.Frame(self.root, bg="#cecece")
        bottom.pack(fill="x", pady=10)
        tk.Button(bottom, text="Back to Menu", font=("Arial", 12),
                  bg="#1C1C1C", fg="white",
                  command=self.main_menu).pack()

    # Menu actions
    def view_all(self):
        self.display_students("All Students", self.students)

    # Updated view_one function
    def view_one(self):
    # Ask user for input (can be ID or name)
        user_input = simpledialog.askstring("Select Student", "Enter Student Number or Name:")
        if user_input is None:
            return

    # Try to interpret input as student ID
        student = None
        if user_input.isdigit():
            sid = int(user_input)
            student = next((x for x in self.students if x['id'] == sid), None)
        else:
    # Search by name (case-insensitive)
            matches = [x for x in self.students if user_input.lower() in x['name'].lower()]
            if len(matches) == 1:
                student = matches[0]
            elif len(matches) > 1:
                messagebox.showinfo("Multiple Matches", f"Multiple students found for '{user_input}'. Please enter full name or ID.")
                return

        if student:
            self.display_students("Student Record", [student])
        else:
            messagebox.showerror("Error", f"No student found matching '{user_input}'")

    def view_highest(self):
        if self.students:
            top = max(self.students, key=calculate_total)
            self.display_students("Highest Scoring Student", [top])

    def view_lowest(self):
        if self.students:
            low = min(self.students, key=calculate_total)
            self.display_students("Lowest Scoring Student", [low])

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
    
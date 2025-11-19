import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime

ACCOUNTS_FILE = 'accounts.txt'

# Ensure accounts file exists
if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, 'w') as f:
        f.write("")

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tool")
        self.root.geometry('720x540')

        self.current_user = None
        self.expenses = []  # list of (category, amount)

        # Frames
        self.login_frame = tk.Frame(root, padx=12, pady=12)
        self.create_frame = tk.Frame(root, padx=12, pady=12)
        self.budget_frame = tk.Frame(root, padx=12, pady=12)

        self.build_login_frame()
        self.build_create_frame()
        self.build_budget_frame()

        self.show_frame(self.login_frame)

    # ACCOUNT FILE HANDLING
    def load_accounts(self):
        accounts = {}
        if not os.path.exists(ACCOUNTS_FILE):
            return accounts
        with open(ACCOUNTS_FILE, 'r') as f:
            lines = [line.strip() for line in f.readlines()]

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith('username:'):
                try:
                    username = line.split(':', 1)[1].strip()
                    pw_line = lines[i+1] if i+1 < len(lines) else ''
                    if pw_line.startswith('password:'):
                        password = pw_line.split(':', 1)[1].strip()
                        accounts[username] = password
                        i += 2
                        # skip potential blank line
                        if i < len(lines) and lines[i] == '':
                            i += 1
                        continue
                except Exception:
                    pass
            i += 1
        return accounts

    def save_account(self, username, password):
        with open(ACCOUNTS_FILE, 'a') as f:
            f.write(f"username: {username}\npassword: {password}\n\n")

    def budgets_filename(self, username):
        return f"budgets_{username}.txt"

    #FRAME SWITCHER
    def show_frame(self, frame):
        for f in (self.login_frame, self.create_frame, self.budget_frame):
            f.pack_forget()
        frame.pack(fill='both', expand=True)

    #LOGIN SCREEN
    def build_login_frame(self):
        f = self.login_frame
        tk.Label(f, text="Login", font=(None, 16)).pack(pady=(0,8))

        form = tk.Frame(f)
        form.pack()

        tk.Label(form, text="Username:").grid(row=0, column=0, sticky='e', padx=6, pady=4)
        self.login_user = tk.Entry(form)
        self.login_user.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(form, text="Password:").grid(row=1, column=0, sticky='e', padx=6, pady=4)
        self.login_pass = tk.Entry(form, show='*')
        self.login_pass.grid(row=1, column=1, padx=6, pady=4)

        btn_frame = tk.Frame(f)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Login", width=14, command=self.attempt_login, bg="#b3e6b3").grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Create Account", width=14, command=lambda: self.show_frame(self.create_frame), bg="#b3d9ff").grid(row=0, column=1, padx=6)

    def attempt_login(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()

        accounts = self.load_accounts()

        if username in accounts and accounts[username] == password:
            self.current_user = username
            self.expenses = []
            self.income_var.set("")
            self.update_expenses_listbox()
            self.user_label.config(text=f"User: {username}")
            messagebox.showinfo("Success", "Login successful!")
            self.show_frame(self.budget_frame)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    #CREATE ACCOUNT SCREEN
    def build_create_frame(self):
        f = self.create_frame
        tk.Label(f, text="Create Account", font=(None, 16)).pack(pady=(0,8))

        form = tk.Frame(f)
        form.pack()

        tk.Label(form, text="Username:").grid(row=0, column=0, sticky='e', padx=6, pady=4)
        self.new_user = tk.Entry(form)
        self.new_user.grid(row=0, column=1, padx=6, pady=4)

        tk.Label(form, text="Password:").grid(row=1, column=0, sticky='e', padx=6, pady=4)
        self.new_pass = tk.Entry(form, show='*')
        self.new_pass.grid(row=1, column=1, padx=6, pady=4)

        tk.Label(form, text="Confirm Password:").grid(row=2, column=0, sticky='e', padx=6, pady=4)
        self.new_pass2 = tk.Entry(form, show='*')
        self.new_pass2.grid(row=2, column=1, padx=6, pady=4)

        btn_frame = tk.Frame(f)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Create", width=14, command=self.create_account, bg="#b3d9ff").grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Back", width=14, command=lambda: self.show_frame(self.login_frame), bg="#f2b3b3").grid(row=0, column=1, padx=6)

    def create_account(self):
        user = self.new_user.get().strip()
        p1 = self.new_pass.get().strip()
        p2 = self.new_pass2.get().strip()

        if not user or not p1:
            messagebox.showerror("Error", "Fill all fields")
            return
        if p1 != p2:
            messagebox.showerror("Error", "Passwords do not match")
            return

        accounts = self.load_accounts()
        if user in accounts:
            messagebox.showerror("Error", "Username already exists")
            return

        self.save_account(user, p1)
        messagebox.showinfo("Success", "Account created!")
        # clear fields
        self.new_user.delete(0, 'end')
        self.new_pass.delete(0, 'end')
        self.new_pass2.delete(0, 'end')
        self.show_frame(self.login_frame)

    #BUDGET SCREEN
    def build_budget_frame(self):
        f = self.budget_frame

        top = tk.Frame(f)
        top.pack(fill='x')
        self.user_label = tk.Label(top, text="User:")
        self.user_label.pack(side='left', padx=6)
        tk.Button(top, text="Logout", command=self.logout, bg="#ffd9b3").pack(side='right', padx=6)

        main = tk.Frame(f, bg="#f0f4ff")
        main.pack(fill='both', expand=True)

        left = tk.Frame(main, bg="#d6e0ff", padx=8, pady=8)
        left.pack(side='left', fill='y', padx=6, pady=6)

        right = tk.Frame(main, bg="#eef3ff", padx=8, pady=8)
        right.pack(side='left', fill='both', expand=True, padx=6, pady=6)

        tk.Label(left, text="Income:").pack(anchor='w')
        self.income_var = tk.StringVar()
        tk.Entry(left, textvariable=self.income_var).pack(fill='x', pady=(0,6))

        #Fixed Categories
        tk.Label(left, text="Expense Categories:").pack(anchor='w', pady=(6,4))

        self.fixed_categories = {
            "Groceries": tk.StringVar(),
            "Car": tk.StringVar(),
            "Rent": tk.StringVar(),
            "Utilities": tk.StringVar(),
            "Other": tk.StringVar()
        }

        for cat, var in self.fixed_categories.items():
            row = tk.Frame(left, bg=left['bg'])
            row.pack(fill='x', pady=2)
            tk.Label(row, text=f"{cat}:", width=10, anchor='w', bg=left['bg']).pack(side='left')
            tk.Entry(row, textvariable=var).pack(side='left', fill='x', expand=True)

        tk.Button(left, text="Update Expenses", command=self.load_fixed_expenses, bg="#b3c7ff").pack(fill='x', pady=6)
        tk.Button(left, text="Reset Categories", command=self.reset_categories, bg="#ffb3b3").pack(fill='x', pady=2)

        tk.Button(left, text="Calculate Remaining", command=self.calculate_remaining, bg="#b3e6b3").pack(fill='x', pady=6)
        tk.Button(left, text="Save Budget to File", command=self.save_budget_to_file, bg="#d9d9ff").pack(fill='x')
        tk.Button(left, text="Show Pie Chart", command=self.show_pie_chart, bg="#ffd9b3").pack(fill='x', pady=4)

        tk.Label(right, text="Expenses:", bg=right['bg']).pack(anchor='w')
        self.exp_listbox = tk.Listbox(right)
        self.exp_listbox.pack(fill='both', expand=True, pady=(4,6))

        self.result_label = tk.Label(right, text="Remaining:", bg=right['bg'])
        self.result_label.pack(anchor='w')

    #EXPENSE HANDLING
    def load_fixed_expenses(self):
        self.expenses = []
        for cat, var in self.fixed_categories.items():
            val = var.get().strip()
            if val:
                try:
                    amt = float(val)
                    if amt < 0:
                        raise ValueError("negative")
                    self.expenses.append((cat, amt))
                except Exception:
                    messagebox.showerror("Error", f"Invalid amount for {cat}")
                    return
        self.update_expenses_listbox()

    def reset_categories(self):
        for var in self.fixed_categories.values():
            var.set("")
        self.expenses = []
        self.update_expenses_listbox()

    def update_expenses_listbox(self):
        self.exp_listbox.delete(0, 'end')
        for c, a in self.expenses:
            self.exp_listbox.insert('end', f"{c}: ${a:.2f}")

    def remove_selected(self):
        sel = self.exp_listbox.curselection()
        if not sel:
            return
        del self.expenses[sel[0]]
        self.update_expenses_listbox()

    #CALCULATING
    def calculate_remaining(self):
        try:
            income = float(self.income_var.get()) if self.income_var.get().strip() else 0.0
        except Exception:
            messagebox.showerror("Error", "Invalid income")
            return
        total = sum(v for _, v in self.expenses)
        rem = income - total
        self.result_label.config(text=f"Remaining: ${rem:.2f} (Income: ${income:.2f} - Expenses: ${total:.2f})")
        return rem

    #SAVING BUDGET TO TEXT FILE
    def save_budget_to_file(self):
        if not self.current_user:
            messagebox.showerror("Error", "You must be logged in to save budgets")
            return

        try:
            income = float(self.income_var.get()) if self.income_var.get().strip() else 0.0
        except Exception:
            messagebox.showerror("Error", "Invalid income")
            return

        total = sum(v for _, v in self.expenses)
        rem = income - total

        fn = self.budgets_filename(self.current_user)
        with open(fn, 'a') as f:
            f.write(f"timestamp: {datetime.now()}\n")
            f.write(f"income: {income}\n")
            for c, a in self.expenses:
                f.write(f"{c}: {a}\n")
            f.write(f"Remaining: {rem}\n---\n")

        messagebox.showinfo("Saved", f"Saved to {fn}")

    #PIE CHART
    def show_pie_chart(self):
        if not self.expenses:
            messagebox.showerror("Error", "No expenses to show")
            return

        labels = [c for c, _ in self.expenses]
        sizes = [a for _, a in self.expenses]
        total = sum(sizes)
        if total == 0:
            messagebox.showerror("Error", "Expenses total is zero")
            return

        # Create a simple pie
        top = tk.Toplevel(self.root)
        top.title("Expense Pie Chart")
        canvas_size = 420
        canvas = tk.Canvas(top, width=canvas_size, height=canvas_size, bg='white')
        canvas.pack(fill='both', expand=True)

        x0, y0, x1, y1 = 10, 10, canvas_size-10, canvas_size-10
        start_angle = 0
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#f0b3ff']
        for i, (lbl, val) in enumerate(zip(labels, sizes)):
            extent = (val/total) * 360
            color = colors[i % len(colors)]
            canvas.create_arc(x0, y0, x1, y1, start=start_angle, extent=extent, fill=color, outline='white')
            # label position (Where it's placed)
            mid_angle = (start_angle + extent/2) * 3.14159 / 180.0
            rx = (x0 + x1)/2 + (canvas_size/3) * 0.6 * tk.cos(mid_angle) if hasattr(tk, 'cos') else (x0 + x1)/2
            ry = (y0 + y1)/2 + (canvas_size/3) * 0.6 * tk.sin(mid_angle) if hasattr(tk, 'sin') else (y0 + y1)/2
            
            start_angle += extent

        # Legend on the right
        legend_y = 20
        for i, (lbl, val) in enumerate(zip(labels, sizes)):
            color = colors[i % len(colors)]
            percent = val/total * 100
            canvas.create_rectangle(canvas_size-180, legend_y, canvas_size-160, legend_y+12, fill=color, outline='')
            canvas.create_text(canvas_size-150, legend_y+6, anchor='w', text=f"{lbl}: ${val:.2f} ({percent:.1f}%)")
            legend_y += 20

    #LOGOUT
    def logout(self):
        self.current_user = None
        self.expenses = []
        self.income_var.set("")
        self.update_expenses_listbox()
        self.show_frame(self.login_frame)


if __name__ == '__main__':
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
    
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta

from file_manager import FileManager
from user import Member, Librarian
from book import Book
from loan import Loan


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library System")
        self.current_user = None

        # Load data
        self.users = FileManager.load_users("users.csv")
        self.books = FileManager.load_books("books.csv")
        self.loans = FileManager.load_loans("loans.csv")

        self.login_screen()

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            for user in self.users:
                if user.username == username and user.password == password:
                    self.current_user = user
                    if user.role == "member":
                        self.member_dashboard()
                    else:
                        self.librarian_dashboard()
                    return
            messagebox.showerror("Login Failed", "Invalid credentials.")

        tk.Button(self.root, text="Login", command=login).pack()

    def member_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.current_user.username} (Member)", font=('Arial', 14)).pack(pady=10)

        tk.Button(self.root, text="Search Books", command=self.search_books).pack(pady=5)
        tk.Button(self.root, text="Borrow Book", command=self.borrow_book).pack(pady=5)
        tk.Button(self.root, text="Extend Loan", command=self.extend_loan).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=20)

    def librarian_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome, {self.current_user.username} (Librarian)", font=('Arial', 14)).pack(pady=10)

        tk.Button(self.root, text="Add Book", command=self.add_book).pack(pady=5)
        tk.Button(self.root, text="View Loans", command=self.view_loans).pack(pady=5)
        tk.Button(self.root, text="Create User", command=self.create_user).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=20)

    def search_books(self):
        self.clear_screen()
        tk.Label(self.root, text="Available Books:", font=('Arial', 12)).pack()

        for book in self.books:
            if book.is_available:
                tk.Label(self.root, text=f"{book.book_id} - {book.title} by {book.author}").pack()

        tk.Button(self.root, text="Back", command=self.member_dashboard).pack(pady=10)

    def borrow_book(self):
        book_id = simpledialog.askstring("Borrow Book", "Enter Book ID:")
        if book_id:
            # check if user already borrowed 4 books
            user_loans = [l for l in self.loans if l.username == self.current_user.username]
            if len(user_loans) >= 4:
                messagebox.showerror("Limit Reached", "You can't borrow more than 4 books.")
                return

            for book in self.books:
                if book.book_id == book_id and book.is_available:
                    loan_date = datetime.today().strftime("%Y-%m-%d")
                    due_date = (datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")
                    new_loan = Loan(self.current_user.username, book.book_id, loan_date, due_date)
                    self.loans.append(new_loan)
                    book.mark_as_borrowed()
                    FileManager.save_loans("loans.csv", self.loans)
                    FileManager.save_books("books.csv", self.books)
                    messagebox.showinfo("Success", "Book borrowed successfully.")
                    return
            messagebox.showerror("Unavailable", "Book not available or ID invalid.")

    def extend_loan(self):
        book_id = simpledialog.askstring("Extend Loan", "Enter Book ID:")
        for loan in self.loans:
            if loan.book_id == book_id and loan.username == self.current_user.username:
                if loan.extended:
                    messagebox.showerror("Error", "Loan already extended once.")
                else:
                    loan.extend_due_date()
                    FileManager.save_loans("loans.csv", self.loans)
                    messagebox.showinfo("Success", "Loan extended by 7 days.")
                return
        messagebox.showerror("Not Found", "No such loan found.")

    def add_book(self):
        title = simpledialog.askstring("Add Book", "Enter Title:")
        author = simpledialog.askstring("Add Book", "Enter Author:")
        if title and author:
            new_id = str(100 + len(self.books) + 1)
            new_book = Book(new_id, title, author, True)
            self.books.append(new_book)
            FileManager.save_books("books.csv", self.books)
            messagebox.showinfo("Success", "Book added.")

    def view_loans(self):
        self.clear_screen()
        tk.Label(self.root, text="All Active Loans:", font=('Arial', 12)).pack()
        for loan in self.loans:
            tk.Label(self.root, text=f"{loan.username} → Book {loan.book_id} → Due: {loan.due_date}").pack()
        tk.Button(self.root, text="Back", command=self.librarian_dashboard).pack(pady=10)

    def create_user(self):
        username = simpledialog.askstring("Create User", "Username:")
        password = simpledialog.askstring("Create User", "Password:")
        role = simpledialog.askstring("Create User", "Role (member/librarian):")
        if username and password and role in ["member", "librarian"]:
            with open("users.csv", "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([username, password, role])
            self.users = FileManager.load_users("users.csv")
            messagebox.showinfo("Success", "User created.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

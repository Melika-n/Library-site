import csv
from book import Book
from user import Member, Librarian
from loan import Loan

class FileManager:
    @staticmethod
    def load_users(file_path):
        users = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                username, password, role = row
                if role == "member":
                    users.append(Member(username, password))
                elif role == "librarian":
                    users.append(Librarian(username, password))
        return users

    @staticmethod
    def load_books(file_path):
        books = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                book_id, title, author, is_available = row
                books.append(Book(book_id, title, author, is_available == "yes"))
        return books

    @staticmethod
    def load_loans(file_path):
        loans = []
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                username, book_id, loan_date, due_date, extended = row
                loans.append(Loan(username, book_id, loan_date, due_date, extended == "yes"))
        return loans

    @staticmethod
    def save_loans(file_path, loans):
        with open(file_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for loan in loans:
                writer.writerow([loan.username, loan.book_id, loan.loan_date, loan.due_date, "yes" if loan.extended else "no"])

    @staticmethod
    def save_books(file_path, books):
        with open(file_path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for book in books:
                writer.writerow([book.book_id, book.title, book.author, "yes" if book.is_available else "no"])

Library Management Software 

Features:
- Member login: borrow and extend books (max 4)
- Librarian login: add books, view loans, create users

How to Run:
1. Make sure all .py files and CSV files are in the same folder.
2. Run main.py
3. Use the login info below:
   - Member: mina / 123
   - Librarian: ali / admin

File Structure:
- users.csv: username,password,role
- books.csv: book_id,title,author,is_available
- loans.csv: username,book_id,loan_date,due_date,extended

Developed using:
- Python 3
- Tkinter
- OOP principles
- CSV file handling

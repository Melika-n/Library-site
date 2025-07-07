import time

class Loan:
    def __init__(self, username, book_id, loan_date, due_date, extended="no"):
        self.username = username
        self.book_id = book_id
        self.loan_date = loan_date  # به صورت رشته مثل "2025-06-01"
        self.due_date = due_date    # به صورت رشته مثل "2025-06-08"
        self.extended = extended    # "no" یا "yes"

    def extend_due_date(self):
        if self.extended == "no":
            # تبدیل تاریخ به ساختار زمان (time struct)
            due_struct = time.strptime(self.due_date, "%Y-%m-%d")
            due_seconds = time.mktime(due_struct)

            # اضافه کردن 7 روز (7*24*60*60 ثانیه)
            new_due_seconds = due_seconds + (7 * 24 * 60 * 60)

            # تبدیل دوباره به رشته تاریخ
            new_due_struct = time.localtime(new_due_seconds)
            self.due_date = time.strftime("%Y-%m-%d", new_due_struct)

            self.extended = "yes"


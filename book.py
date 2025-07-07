class Book:
    def __init__(self, book_id, title, author, is_available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = is_available  # boolean

# متد mark_as_borrowed وقتی کتاب امانت داده می‌شود، آن را غیرقابل امانت می‌کند
    def mark_as_borrowed(self):
        self.is_available = False

# متد mark_as_returned وقتی کتاب پس داده می‌شود، آن را دوباره قابل امانت می‌کند
    def mark_as_returned(self):
        self.is_available = True

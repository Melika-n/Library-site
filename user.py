class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class Member(User):
    def __init__(self, username, password):
        super().__init__(username, password, role="member")
        # عضو فقط می‌تواند ۴ کتاب به امانت بگیرد
        self.max_loans = 4     


class Librarian(User):
    def __init__(self, username, password):
        super().__init__(username, password, role="librarian")

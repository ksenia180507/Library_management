class Member: #stores data about members

    def __init__(self, member_id, name, password):
        self.member_id = member_id
        self.name = name
        self.password = password

        #creating a list for borrowed books by a new user
        self.borrowed_books = []

    def can_borrow(self):
        """User cannot borrow more than 4 books at a time"""
        return len(self.borrowed_books) < 4

    def book_tracking(self, book_id, is_borrowing: bool):
        """Adds to a member id of a book which was borrowed and removes it when returned"""
        if is_borrowing:
            if book_id not in self.borrowed_books: #to prevent double booking of the same book
                self.borrowed_books.append(book_id)
        else:
            if book_id in self.borrowed_books:
                self.borrowed_books.remove(book_id)

    def __str__(self):
        s = "=============Member=============\n"
        s += f"ID: {self.member_id}\n"
        s += f"Books borrowed: {len(self.borrowed_books)}\n"
        s += "================================\n"
        return s


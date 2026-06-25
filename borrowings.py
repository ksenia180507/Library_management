class Borrowings:
    def __init__(self, borrowing_id, member_id, book_id):
        self.borrowing_id = borrowing_id
        self.member_id = member_id
        self.book_id = book_id

        #new borrowing is always active
        self.status = "active"

    def close_borrowing(self):
        """Changes the status of a book to a closed"""
        self.status = "closed"


    def match(self, member_id, book_id):
        """Checks the match between member book and whether it is active or not"""
        return (self.member_id == member_id and self.book_id == book_id and self.status == "active")

    def __str__(self):
        b = "\n=============Borrowing=============\n"
        b += (f"ID:{self.borrowing_id}\n"
              f"Member id: {self.member_id}\n"
              f"Book ID: {self.book_id}\n "
              f"Status: {self.status}\n"
              f"==================================")
        return b
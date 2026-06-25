from borrowings import Borrowings

class Library: #main class

    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.books = [] #list of books in a library
        self.borrowings = [] #list of borrowings in a library


    def add_book(self, books):
        """Adds books to a system"""
        for book_o in books:
            self.books.append(book_o)
            print(f"Book '{book_o.title}' successfully added.")

    def find_book(self, query, search_type):
        """Function finds a book puts it in an empty list and then displays it, if the list remains empty it means that no books are found"""
        found_books = [] #empty list
        for b in self.books:
            if b.matches(query, search_type):
                found_books.append(b)

        return found_books

    def find_book_id(self, book_id):
        """Function finds a book according to its id"""
        for b in self.books:
            if b.book_id == book_id:
                return b
        return None

    def borrow_book(self, book_id, member, all_libraries, borrowing_id):
        """Finds a book, checks book availability, allocates the book to a member, change the status and stock"""
        book = self.find_book_id(book_id)

        if book is None:
            return

        #If the book is out of stock in the library which was chosen by user then it shows available options in other libraries
        if book.quantity == 0:
            for library in all_libraries:
                for b in library.books:
                    if b.title.lower() == book.title.lower() and b.quantity > 0:
                        print(f"Book' {book.title}' is out of stock in '{self.name}'.")
                        print(
                            f"But it is in stock in '{library.name}' the address: {library.address} (Available: {b.quantity})")
                        return
            print(f"{book.title} is not available in any Libraries")
            return

        if not member.can_borrow():
            print("Sorry 1 member cannot borrow more than 4 books")
            return

        book.change_stock(-1)
        member.book_tracking(book_id, is_borrowing=True)

        new_borrowing = Borrowings(borrowing_id, member.member_id, book_id)

        self.borrowings.append(new_borrowing)

        print(f"Message: Book '{book.title}' successfully borrowed by {member.name}!")
        return


    def return_book(self, member, title, author):
        """Finds book, removes the book from a member, makes the book available, changes status and a stock"""
        book = None

        for b in self.books:
            if (b.title.lower() == title.lower() and b.author.lower() == author.lower()):
                book = b
                break

        #Checks whether  a book exist
        if book is None:
            print("Book is not found")
            return

        #create variable
        active_borrowing = None
        #matching the member and book id and saving active borrowing to close it later
        for b in self.borrowings:
            if b.match(member.member_id, book.book_id):
                active_borrowing = b
                break


        if active_borrowing is None:
            print(f"No active borrowings.")
            return

        #deactivating the borrowing, adding the book back to stock
        active_borrowing.close_borrowing()

        book.change_stock(1)

        member.book_tracking(book.book_id, is_borrowing=False)

        print(f" Book '{book.title}' is successfully returned by {member.name}!")

    def __str__(self):
        return (f"Library: {self.name}\n"
                f"Address: {self.address}\n"
                f"Books in catalogue: {len(self.books)}\n"
                f"Borrowing records: {len(self.borrowings)}")
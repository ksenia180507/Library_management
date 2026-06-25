class Book: #stores data about a book
    def __init__(self, book_id, title, genre, author, availability, quantity):
        self.book_id = book_id
        self.title = title
        self.genre = genre
        self.author = author
        self.quantity = quantity #stock of a book
        self.availability = availability

    def change_stock(self, amount):
        """Checks the quantity and changes it according to the amount(-1 when borrowed, +1 when returned, +n when librarian adds books)"""
        self.quantity += amount #amount --> change in quantity
        if self.quantity == 0:
            self.availability = False
        else:
            self.availability = True

    def matches(self, query, search_type):
        """Matches the user input and existing data"""
        if search_type.strip() == "title" and query.lower().strip() in self.title.lower():
            return True
        elif search_type.strip() == "author" and query.lower().strip() in self.author.lower():
            return True
        elif search_type.strip() == "genre" and query.lower().strip() in self.genre.lower():
            return True
        return False

    def __str__(self):
        status = "Available" if self.availability else "Not available"
        return f"ID: {self.book_id}\nTitle and author: {self.title} by {self.author}\nAvailability: {self.quantity} books are {status.lower()}"

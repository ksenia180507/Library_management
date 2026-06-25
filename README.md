# Library Management System

## Purpose
This project is an interactive Library Management System and its purpose is to automate library processes, which allows new users to register or existing users to log in the program. All features searching, borrowing, and returning books abilities. The program also has a librarian mode to manage book stock and manually close active borrowing records. 

## Instructions for Installation and Execution
1. Clone the repository to your local machine: 
2. Ensure you have Python 3.x installed on your system.
3. Open a terminal or command prompt and navigate to the project folder.
4. Verify that the sample data files (`books.txt`, `members.txt`, `borrowings.txt`) are in the same directory.
5. Run the application using the command: 
   `python main.py`

## Example Usage
After launching the program, the system loads the text-based database arrays and asks the user to select one of three library branches (e.g., Berliner Stadtbibliothek (librry coice -- 1)). 

The user is then presented with the main menu:
1. Login as a user
2. Register as a new user
3. Login as a librarian
4. Exit the program

**As a User:** You can search for books by title, author, or genre. If a book is out of stock in your current library, the system automatically checks other libraries. You can borrow up to 4 books concurrently. You can also return a book, if you have any active borrowings.
**As a Librarian:** (Password: `Library123`), you can supply new books to the library shelfs and manage or manually close active user borrowing records.

## List of Key Features and Files
* **`main.py`**: The central entry point containing the interactive CLI, menu routing, and file loading/saving functions.
* **`library.py`**: The main aggregate class that manages the list of books and borrowings, processing checkout and return logic.
* **`book.py`**: Contains the `Book` class, managing individual stock quantities and search matching.
* **`member.py`**: Contains the `Member` class, enforcing the 4-book borrowing limit and tracking user histories.
* **`borrowings.py`**: Contains the `Borrowings` class, tracking active and closed transaction states.
* **Data Files**: `books.txt`, `members.txt`, and `borrowings.txt` act as the database for the application.

#Imports of classes
from library import Library
from book import Book
from member import Member
from borrowings import Borrowings

# Saves all the books to book.txt"
def save_books(all_libraries):
    with open("books.txt", "w") as f:
        for lib in all_libraries:
            for b in lib.books:
                f.write(f"{lib.name},{b.book_id},{b.title},{b.genre},"
                        f"{b.author}, {b.availability}, {b.quantity}\n")

#loads books to an array for faster processing
def load_books_to_array(all_libraries):
    #Exception handling, warns if file was not found
    try:
        with open("books.txt", "r") as f:
            for line in f:
                if line:
                    #strip() used to remove spaces in the value
                    data = [item.strip() for item in line.split(",")]
                    library_name = data[0]
                    book = Book(int(data[1]), data[2], data[3], data[4], data[5] == "True", int(data[6]))

                    for lib in all_libraries:
                        if lib.name == library_name:
                            lib.books.append(book)

        total_books = 0
        for lib in all_libraries:
            total_books += len(lib.books)

        print(f"Books loaded to array successfully! Total books loaded: {total_books}")

    except FileNotFoundError:
        print("Books file not found")

#saves members to txt file
def save_members_file(all_members):
    #Saving members to members.txt
    with open("members.txt", "w",) as f:
        for m in all_members:
            f.write(f"{m.member_id},{m.name},{m.password}\n")

#loads members to an array
def load_members_data(all_members):
    # Exception handling, warns if file was not found
    try:
        with open("members.txt", "r") as f:
            for line in f:
                if line:
                    data = [item.strip() for item in line.split(",")]
                    member = Member(int(data[0]), data[1], data[2])

                    all_members.append(member)
        print("Members are loaded")

    except FileNotFoundError:
        print("Member file is not found")
        
#saves borrowings data to txt file
def save_borrowings(all_libraries):
    #Saving borrowing history to borrowings.txt
    with open("borrowings.txt", "w") as f:
        for lib in all_libraries:
            for br in lib.borrowings:
                f.write(f"{lib.name},{br.borrowing_id},{br.member_id},{br.book_id},{br.status}\n")

def load_borrowings_array(all_libraries, all_members):
    # Exception handling, warns if file was not found
    try:
        with open("borrowings.txt", "r") as f:
            for line in f:
                if line:
                    data = [item.strip() for item in line.split(",")]

                    library_name = data[0]

                    borrowing = Borrowings(int(data[1]), int(data[2]), int(data[3]))
                    borrowing.status = data[4]

                    for lib in all_libraries:
                        if lib.name == library_name:
                            lib.borrowings.append(borrowing)

                    if borrowing.status == "active":
                        for m in all_members:
                            if m.member_id == borrowing.member_id:
                                m.book_tracking(borrowing.book_id, is_borrowing=True)

        print("Borrowings are downloaded")

    except FileNotFoundError:
        print("Borrowings' file is not found")

# ID generator for members (just adds +1 to the old id)
def generate_member_id(all_members):
    if len(all_members) == 0:
        return 1
    last_id = all_members[-1].member_id
    return last_id + 1

#users'main menu
def user_main_menu(current_member, current_library, all_libraries):
    while True:

        print("\n============ User menu ============")
        print("Chose the option below:")
        print("1. Find and borrow a book")
        print("2. Return a book ")
        print("3. Back to the beginning")
        print("===================================")

        #Exception handling (in case user input non-integer values)
        try:
            menu_choice = int(input("\nChoose an option: "))
        except ValueError:
            print("Error: please enter a number")
            continue

        # User chooses to find nd borrow a book
        if menu_choice == 1:
            print("============ Searching tab ============")
            search_type = input("Do you want to search a book according to its title, author or genre: ")
            query = input("Enter search: ")
            print("=======================================\n")

            results = current_library.find_book(query, search_type)

            #Filtering only books with more than 0 quantity
            if results:
                results = [b for b in results if b.quantity > 0]

            if results:
                print(f"Found in {current_library.name}:\n")

                counter = 1

                for b in results:
                    print(f"{counter}. {b.title} by {b.author}")
                    counter += 1

                print("0. Back to search")

                try:
                    borrow_choice = int(input("\nWhich book do you want to borrow: "))
                except ValueError:
                    print("Error: please enter a number")
                    continue

                #in case if member decided to go back to searching
                if borrow_choice == 0:
                    continue

                if borrow_choice < 1 or borrow_choice > len(results):
                    print("Invalid choice, try again")

                #book borrowing
                selected_book = results[borrow_choice - 1]
                borrowing_id = (len(current_library.borrowings) + 1)
                current_library.borrow_book(selected_book.book_id, current_member, all_libraries, borrowing_id)

                #saving information about borrowings and books
                save_borrowings(all_libraries)
                save_books(all_libraries)

                break

            else:
                #searching for a book in another libraries
                print(f"\nNo books found in {current_library.name}.")
                print("\nSearching in other libraries...\n")

                book_found = False

                for lib in all_libraries:
                    if lib != current_library:
                        other_results = lib.find_book(query, search_type)

                        if other_results:
                            book_found = True
                            print(f"Found in {lib.name} ({lib.address}):")

                            for b in other_results:
                                print(b)
                if not book_found:
                    print("We don't have this book in any library")

                again = input("\n Search again? (yes/no): ").strip().lower()
                if again == "no":
                    break

        # Users chooses to return a book
        elif menu_choice == 2:
            if not current_member.borrowed_books:
                print("\nYou don't have any active borrowings.")
            else:
                print("============ Booking tab ============")
                title = input("Enter book title: ")
                author = input("Enter author: ")
                current_library.return_book(current_member, title, author)
                print("=====================================")

                save_borrowings(all_libraries)
                save_books(all_libraries)

        # User chooses to go back
        elif menu_choice == 3:
            print("Returning to the main menu...")
            break

        else:
            print("Please choose a number between 1 and 3")

#Main function
def main():

    all_members = []

    #creating libraries
    library_1 = Library("Berliner Stadtbibliothek", "Breite Str. 30-36, 10178 Berlin")
    library_2 = Library("Jacob-und-Wilhelm-Grimm-Zentrum", "Geschwister-Scholl-Straße 1-3, 10117 Berlin")
    library_3 = Library("Staatsbibliothek zu Berlin", "Unter den Linden 8, 10117 Berlin")

    all_libraries = [library_1, library_2, library_3]

    #loading data to arrays for further processing
    load_members_data(all_members)
    load_books_to_array(all_libraries)
    load_borrowings_array(all_libraries, all_members)


    # Chooses the library to set up the correct list of books, borrowings and other details
    print("\n============ Choose the library ============")
    print("Chose the library where this program will be running:")
    print(f"1.{library_1.name}, {library_1.address}")
    print(f"2.{library_2.name}, {library_2.address}")
    print(f"3.{library_3.name}, {library_3.address}")
    print("==========================================")

    while True:
        # Exception handling is done in case of the input of incorrect value
        try:
            lib_choice = int(input("\nEnter the number of the library: "))

            if lib_choice == 1:
                current_library = library_1
                break

            elif lib_choice == 2:
                current_library = library_2
                break

            elif lib_choice == 3:
                current_library = library_3
                break

            else:
                # Checks if the number is in range
                print("Error: check the input number again!")

        except ValueError:
            #Checks if nothing or wrong information was input
            print("Error: please enter the number of a library")

    print(f"\n Library is successfully chosen: {current_library.name}")

    # After library is set up the main menu opens
    while True:
        try:
            menu = ("\n============ Menu ============\n"
                    "1. Login as a user\n"
                    "2. Register as a new user\n"
                    "3. Login as a librarian\n"
                    "4. Exit the program\n"
                    "==============================")
            print(menu)

            choice = int(input("Choose from 1-4: "))

            # Login in an existing user
            if choice == 1:
                print("\n============ Logging in the system ============")
                input_name = input("Enter your name: ")
                input_password = input("Enter your password: ")
                print("=============================================")

                current_member = None

                for m in all_members:
                    if m.name.lower() == input_name.lower().strip() and m.password == input_password.strip():
                        current_member = m
                        break

                if current_member is not None:
                    print(f"\nWelcome {current_member.name}!")
                    user_main_menu(current_member, current_library, all_libraries) #call the main menu function
                else:
                    print(f"Unfortunately user {input_name} is not found or password is incorrect, please try one more time")

            #Sign in a new user
            elif choice == 2:
                print("\n=========Signing in the system============")
                new_input_name = input("Enter your name: ")
                new_input_password = input("Enter your password: ")

                password_exists = False

                #checking if the password is already used for another user (to eliminate the chance of repeated password)
                for m in all_members:
                    if new_input_password == m.password:
                        password_exists = True

                # To ensure that users have different passwords to distinguish them
                if password_exists:
                    print("This password is already occupied")

                else:
                    new_member_id = generate_member_id(all_members)

                    new_member = Member(new_member_id, new_input_name, new_input_password)

                    #saving new member
                    all_members.append(new_member)
                    save_members_file(all_members)

                    print("New user successfully added!")
                    user_main_menu(new_member, current_library, all_libraries) # call the main menu function

            #Librarian choice
            elif choice == 3:
                #Librarian can add new members, add new books, manage borrowings
                print("\n========= Logging in as a librarian in the system ============")
                librarian_password = input("Enter the password: ")

                #Librarian option can only be accessible if password is correct
                if librarian_password == "Library123":
                    print("\n================= Librarian =================")
                    print("1. Add new books\n" # adds a book with its unique id and according to that stock is changed
                          "2. Manage borowings\n" #displays all the information abt borrowings, can cancel or add new one
                          "3. Exit the librarian mode")

                    librarian_input = int(input("Enter the option: "))
                    
                    # Adding new books to the chosen library by the librarian
                    if librarian_input == 1:
                        print("\n============= Add new books =============")

                        try:
                            books_amount = int(input("How many books do u want to add: "))
                            if books_amount <= 0:
                                print("The amount must be at least 1")
                            else:
                                new_books = [] # empty list which later will be added

                                for i in range(1, books_amount+1):
                                    print(f"\n============= Supply of {i} book =============")

                                    book_id = int(input("Book ID:" ))
                                    title = input("Title: ")
                                    genre = input("Genre: ")
                                    author = input("Author: ")
                                    quantity = int(input("Quantity: "))

                                    availability = quantity > 0

                                    new_book = Book(book_id, title, genre, author, availability, quantity)
                                    new_books.append(new_book)

                                current_library.add_book(new_books)
                                save_books(all_libraries)

                        except ValueError:
                            print("Invalid input")

                    # Managing the borrowings of set up library
                    elif librarian_input == 2:
                        print("============= Borrowings =============")

                        borrowings_exist = False
                        active_borrowing_exists = False

                        for borrowing in current_library.borrowings:
                            print(borrowing)
                            borrowings_exist = True
                            if borrowing.status == "active":
                                active_borrowing_exists = True

                        if not borrowings_exist:
                            print("There are no borrowings")

                        elif not active_borrowing_exists:
                            print("All borrowings are already closed.")

                        else:
                            librarian_choice = input("Do you want to close a borrowing manually? (yes/no): ")

                            if librarian_choice.lower() == "yes":
                                # Exception handling if input is incorrect
                                try:
                                    borrowing_id = int(input("Enter borrowing ID: "))

                                    found = False

                                    for borrowing in current_library.borrowings:
                                        if borrowing.borrowing_id == borrowing_id:
                                            borrowing.close_borrowing()
                                            found = True

                                            save_borrowings(all_libraries)

                                            print("borrowing successfully closed.")
                                            break

                                    if not found:
                                        print("Borrowing ID not found.")

                                except ValueError:
                                    print("Invalid borrowing ID input.")
                            else:
                                break
                    else:
                        print("Exiting the librarian mode")
                else:
                    print("Wrong password")

            #Exit the library
            elif choice == 4:
                print("Goodbye!")
                break

            else:
                print("Please choose a number from 1 to 4")

        except ValueError:
            print("Error: please enter the number of an option")

if __name__ == "__main__":
    main()

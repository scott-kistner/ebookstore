 # ====== Importing Libraries ======
import sqlite3


# ====== Functions ======
# ------- Connecting to Database -------
def database_connect():
    try:
        db = sqlite3.connect('./ebookstore.db') 
        cursor = db.cursor()
        return cursor, db
    except sqlite3.Error as e:
        print(f"Error connecting to database due to: {e}")
        db.rollback()
        return None, None


# ------- Creating Table -------
def create_table():
    try:
        cursor, db = database_connect()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS 
                       book(id INTEGER PRIMARY KEY, title TEXT, 
                       author TEXT, qty INTEGER)
                       ''')
        db.commit()
    
    except sqlite3.Error as e:
        print(f"The following error occurred: {e}.")
        db.rollback()
    

# ------- Populating Table -------
def populate_table():
    try:
        cursor, db = database_connect()
        book_catalogue = [(3001, "A Tale of Two Cities", "Charles Dickens", 30), 
                          (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                          (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25), 
                          (3004, "The Lord of the Rings", "J.R.R. Tolkien", 37), 
                          (3005, "Alice in Wonderland", "Lewis Carroll", 12), 
                          (3006, "Fight Club", "Charles Palahniuk", 12), 
                          (3007, "The Three-Body Problem", "Liu Cixin", 25), 
                          (3008, "Poor Things", "Alasdair Gray", 10), 
                          (3009, "Do Androids Dream of Electric Sheep?", "Philip K. Dick", 8),
                          (3010, "The Shining", "Stephen King", 20)]
        
        
        # Code to detect if books from book_catalogue already exist to prevent errors/duplicates.
        for book in book_catalogue:
            book_id = book[0]
            cursor.execute('''SELECT id FROM book WHERE id = ?''', (book_id,))
            existing_record = cursor.fetchone()
            if not existing_record:
                cursor.execute('''INSERT INTO book(id, title, author, qty) VALUES(?,?,?,?)''', book)
        db.commit()


    except sqlite3.Error as e:
        print(f"\nThe following error occurred: {e}.")
        db.rollback()  
    


# ------- Entering a new book -------
def enter_book():
    try:
        cursor, db = database_connect()

        
        # Create new id for book based on the largest id value in database.
        # If not id values exist, it starts at 3001
        cursor.execute('''SELECT MAX(id) FROM book
                       ''')
        max_id = cursor.fetchone()[0]
        new_book_id = max_id + 1 if max_id else 3001


        new_book_title = input("Please enter the title of the book: ").title()
        new_book_author = input("Please enter the author: ").title()
        try:
            new_book_qty = int(input("Please enter the book quantity (qty): "))
            cursor.execute('''
                           INSERT INTO book(id, title, author, qty)
                           VALUES(?, ?, ?, ?)''',
                           (new_book_id, new_book_title, new_book_author, new_book_qty))
            db.commit()
            print(f"\nSuccess! The following has been entered into the eBookstore database:")
            print(f"id:                 {new_book_id}")
            print(f"Title:              {new_book_title}")
            print(f"Author:             {new_book_author}")
            print(f"Qty:                {new_book_qty}")
            print("______________________________________________________________________\n")
        except ValueError:
            print("\nError: Invalid input. Please enter a valid number.\n")
            db.rollback()
    except sqlite3.Error as e:
        print(f"\nThe following error occurred: {e}.")
        db.rollback()


# ------- Updating an existing book -------
def update_book():
    try:
        cursor, db = database_connect()
        print("\n****** Current List of Books ******\n")
        cursor.execute('''
                       SELECT * FROM book
                       ''')
        for row in cursor:
            print(f"{row[0]}: '{row[1]}' by {row[2]} (x {row[3]})")
    
        while True:
            try:
                update_book_option = int(input('''
                                               \nPlease input one of the following options (0-4): 
                                               1. Update book id
                                               2. Update book title
                                               3. Update book author
                                               4. Update book qty
                                               0. Return
                                               : '''))
                

                # ----- Update book id -----
                if update_book_option == 1:
                    try:
                        book_id = int(input("Enter the id of the book you'd like to update: "))
                        new_id = int(input("What would you like to change its id number to: "))
                        cursor.execute('''UPDATE book SET id = ? WHERE id = ?
                                       ''', (new_id, book_id))
                        db.commit()
                        print(f"\nSuccess! {book_id} has been changed to {new_id}.")
                    except sqlite3.Error as e:
                        print(f"\nThe following error occurred: {e}.")
                        db.rollback()

                
                # ----- Update book title -----
                elif update_book_option == 2:
                    try:
                        book_id = int(input("Enter the id of the book you'd like to update: "))
                        new_title = input("What would you like to change its title to: ").title()
                        cursor.execute('''UPDATE book SET title = ? WHERE id = ?
                                       ''', (new_title, book_id))
                        db.commit()
                        print(f"\nSuccess! {book_id}'s title has been updated.")
                    except sqlite3.Error as e:
                        print(f"\nThe following error occurred: {e}.")
                        db.rollback()
                
                
                # ----- Update book author -----
                elif update_book_option == 3:
                    try:
                        book_id = int(input("Enter the id of the book you'd like to update: "))
                        new_author = input("What would you like to change its author to: ").title()
                        cursor.execute('''UPDATE book SET author = ? WHERE id = ?
                                       ''', (new_author, book_id))
                        db.commit()
                        print(f"\nSuccess! {book_id}'s author has been updated.")
                    except sqlite3.Error as e:
                        print(f"\nThe following error occurred: {e}.")
                        db.rollback()
                
                
                # ----- Update book qty -----
                elif update_book_option == 4:
                    try:
                        book_id = int(input("Enter the id of the book you'd like to update: "))
                        new_qty = int(input("What would you like to change its qty to: "))
                        cursor.execute('''UPDATE book SET qty = ? WHERE id = ?
                                       ''', (new_qty, book_id))
                        db.commit()
                        print(f"\nSuccess! {book_id}'s qty has been updated.")
                    except sqlite3.Error as e:
                        print(f"\nThe following error occurred: {e}.")
                        db.rollback()
                

                # ----- Return to previous option menu -----
                elif update_book_option == 0:
                    break
                
                
                else:
                    print("\nOops - incorrect input. Please try again.")

            except ValueError:
                print("\nInvalid input. Please enter a relevant number.")
                
    except sqlite3.Error as e:
        print(f"The following error occurred: {e}.")
        db.rollback()

    
# ------- Deleting an existing book -------
def delete_book():
    try:
        cursor, db = database_connect()
        cursor.execute(''' SELECT * FROM book''')
        print("\n****** Current List of Books ******\n")
        for row in cursor:
            print(f"{row[0]}: '{row[1]}' by {row[2]} (x {row[3]})")
        print("______________________________________________________________________")
        delete_book_id = int(input("\nEnter the id of the book you'd like to delete: "))
        cursor.execute('''SELECT * FROM book WHERE id = ?''', (delete_book_id,))
        existing_book = cursor.fetchone()
        if existing_book:
            cursor.execute('''DELETE FROM book where id =?''', (delete_book_id,))
            db.commit()
            print(f"\nSuccess! {delete_book_id} has been deleted from database.\n")
        else:
            print("\nError: No book with that id exists in database.\n")
    except sqlite3.Error as e:
        print(f"\nThe following error occurred: {e}.")
        db.rollback()


# ------- Searching for an existing book -------
def search_book():
    try:
        cursor, db = database_connect()
        find_book_title = input("\nPlease enter the title of the book you'd like to find: ").title()
        cursor.execute('''SELECT id, title, author, qty FROM book WHERE title = ?
                       ''', (find_book_title,))
        returned_book = cursor.fetchone()
        if returned_book:
            print("\nSuccess! Please find relevant information for the book below:")
            print(f"id:                 {returned_book[0]}")
            print(f"Title:              {returned_book[1]}")
            print(f"Author:             {returned_book[2]}")
            print(f"Qty:                {returned_book[3]}")
            print("______________________________________________________________________\n")
        else:
            print("\nBook not found.\n")
    except sqlite3.Error as e:
        print(f"The following error occurred: {e}.")
        db.rollback()


 # ====== Main ======
print("\n***** Welcome to the eBookstore Programme *****\n")
create_table()
populate_table()


# Menu options for the user -------
while True:
    try:
        menu = int(input('''From the following options, please choose what you'd like to do (0-4):
                         1. Enter book
                         2. Update book
                         3. Delete book
                         4. Search books
                         0. Exit
                         : '''))
        if menu == 1:
            enter_book()
        
        elif menu == 2:
            update_book()
        
        elif menu == 3:
            delete_book()
        
        elif menu == 4:
            search_book()
        
        elif menu == 0:
            print(f'\n***** Goodbye! Thank you for using your friendly neighbourhood, eBookstore Programme! *****')
            break
        
        else:
            print("\nOops - incorrect input. Please try again.\n")

    except Exception as e:
        print(f"The following error occurred: {e}.")
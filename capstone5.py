# DS T39 Capstone Project 5
# Keith Rochfort
# KR22090004774

# import modules and libraries
import os
from datetime import datetime, date
import sqlite3

# Create a program that can be used by a bookstore clerk. The program should allow the clerk to:
    # ○ add new books to the database
    # ○ update book information
    # ○ delete books from the database
    # ○ search the database to find a specific book.
    
    
# NOTES:
# Create the database named ebookstore
# Create the table with the given Columns
# Create a menu as follows: 
'''
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit

'''
# Create a function for quickly adding titles manually
# 1. ENTER BOOK
# TO add new books to the database: 
    # create a function which takes user input and saves the title, author and quantity as a list item
    # run the INSERT INTO books function to insert the book with autoincremented id value
# 2. UPDATE BOOK
    # When selected it will show the current books, including id
    # The user enters the id they want to update, or use the enumerate function if it works.
    # Ensure a correct entry is selected by specifying the index, with the max and min being the length of the db.
    # Ask the user what they want to change, saving these as variables.
    # Run the UPDATE books, SET column by id, and WHERE by the condition specified.
    # Show the changes made and show the new current db.

# 3. DELETE BOOK

# 4. SEARCH BOOK
 

    
# Create the database
db = sqlite3.connect('data/ebookstore')

# set the cursor function
cursor = db.cursor()

# Create a table called ebooks
try: 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            Title TEXT,
            Author TEXT,
            Quantity INT    
        )     
        ''')
    db.commit()

# Global functions
    # Populate the table with the given books using the function below
    # I have change Qty to Quantity to make it obvious what it is
    def initial_books(id, title, author, qty):
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO books (id, Title, Author, Quantity)
            VALUES(?,?,?,?)
            ''', (id, title, author, qty))
        db.commit()
        
    # Function to use in the add_book function
    def insert_book(book):
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO books (Title, Author, Quantity)
            VALUES(?,?,?)
            ''', (book))
        db.commit()
    # End of insert_book() function

    # Function to show all books in the current table
    # The books get saved in book_list for global use
    book_list = []
    def show_all_books():
        cursor = db.cursor()
        all_books = cursor.execute('''
            SELECT *
            FROM books           
            ''')
        all_books_var = all_books.fetchall()
        # Save the books to a list of dictionaries when fetching all
        for book in all_books_var:
            for i in book:
                curr_book = {}
                curr_book['id'] = book[0]
                curr_book['Title'] = book[1]
                curr_book['Author'] = book[2]
                curr_book['Quantity'] = book[3]
            book_list.append(curr_book)
        # Show the books on one line
        for b in book_list:
            print(b)
    # End of show_all_books() function

    # Menu Option 1: Add a book
    # Create a function to add the books; the ids should auto-increment after adding the first 5, as given
    def add_book():
        book = []
        # The id will autoincrement, so no need to ask for that
        print('You have chosen to add a book.')
        title = input('Enter the book title: ').strip().title()
        book.append(title)     
        # ask for the author
        author = input("Enter the book's author: ").strip().title()
        book.append(author)  
        # ask for the quantity
        while True:
            try:
                quantity = int(input('Enter the quantity: '))
                book.append(quantity)
                break
            except ValueError:
                print('Enter numbers only')          
        # Show what was entered:
        print(f'''You entered:
            book title: {title}
            book author: {author}
            quantity: {quantity}
              ''')          
        # add the book title to the books table using the insert_book function      
        insert_book(book)
    # End of  # Menu Option 1: Add a book
    

    # Menu Option 2: Update the books
    # First show the books to choose from:
    def update_book():
        print('\nYou have chosen to UPDATE a book.')
        print('Here are the books in the database:')
        show_all_books()
        book_ids = [b['id'] for b in book_list]
        # print(book_ids)
        # ask the user for the book id, ensuring it is a valid option
        id_selected = None
        while id_selected not in book_ids:
            try:
                id_selected = int(input("Enter the 'id' of the book to be updated: "))  
            except ValueError:
                print('Enter a valid id number.')
                continue
            # Save full details of selected book by id    
            book_selected = None
            for bk in book_list:
                if bk['id'] == id_selected:
                    book_selected = bk
                    break     
        # Ask the user what is to be updated:
        print(f'\nYou selected: \n\t{book_selected}')
        print('''What do you want to update?      
        1. Title
        2. Author
        3. Quantity
        ''')
        choice = None
        while choice not in range(1,4):
            try:
                choice = int(input(" Enter 1, 2 or 3: "))
                if choice not in range(1,4):
                    print("Not a valid selection.")  
            except ValueError:
                print('Enter a valid number.')
                continue
        # Give options for the selections 1, 2, or 3
        if choice == 1: # Title
            new_title = input('Enter the revised Title:  ')
            # Run the UPDATE SQL function to change the title
            cursor.execute('''
        UPDATE books
            SET Title = ?
            WHERE id = ?
        ''', (new_title, id_selected,))
            db.commit() # commit the changes
        elif choice == 2: # Author
            new_author = input('Enter the revised Author:  ')
            cursor.execute('''
        UPDATE books
            SET Author = ?
            WHERE id = ?
        ''', (new_author, id_selected,))
            db.commit() # commit the changes
        elif choice == 3: # Quantity
            new_quantity = int(input('Enter the new quantity: '))
            cursor.execute('''
        UPDATE books
            SET Quantity = ?
            WHERE id = ?
        ''', (new_quantity, id_selected,))
            db.commit() # commit the changes
        # Show the updates
        print('\nThe book has been updated.')
    # End of Menu option2: Update books function
    
    # Menu Option 3: Delete a book
    # Use some of the starting code from Option2 (Update)
    # First show the books to choose from:
    def delete_book():
        print('\nYou have chosen to DELETE a book.')
        print('Here are the books in the database:')
        show_all_books()
        book_ids = [b['id'] for b in book_list]
        # print(book_ids)
        # ask the user for the book id, ensuring it is a valid option
        id_selected = None
        while id_selected not in book_ids:
            try:
                id_selected = int(input("Enter the 'id' of the book to be Deleted: "))
            except ValueError:
                print('Enter a valid id number.')
                continue
            # Save full details of selected book by id    
            book_selected = None
            for bk in book_list:
                if bk['id'] == id_selected:
                    book_selected = bk
                    break    
            print(f'\nYou selected: \n\t{book_selected}')
            print('Are you sure you want to delete this book?')
            delete_y_n = input("Enter 'yes' or 'no': ").lower()
            while True:
                if delete_y_n == 'yes':
                    print('The book you selected has been deleted.')
                    cursor.execute('''
                DELETE FROM books
                    WHERE id = ?
                    ''', (id_selected,))
                    db.commit()
                    break
                elif delete_y_n == 'no':
                    break
                else:
                    print('Not a valid selection.')
                    delete_y_n = input("Enter 'yes' or 'no': ").lower()         
    # End of Menu Option 3: Delete a book      
    
    
    # Menu Option 4: Search Books by Title or Author using the LIKE function
    def search_books():
        print('\nSearch by title or author, including partial terms.')
        search_term = input('\nEnter your search term and hit Enter (leave blank to show all books): ')
        # return any like results
        cursor.execute('''
        SELECT *
            FROM books
            WHERE Title LIKE ? 
            OR Author LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%' ))
        matches = cursor.fetchall()
        print('Here are your results (id, Title, Author, Quantity):')
        for match in matches:
            print('\t', match)
    # End Menu Option 4: Search Books by Title or Author using the LIKE function    
                     
            
    # Initialise the db with soiime entries
    # add the first 5 books given using the initial_books() function, plus some of my own choices
    initial_books(3001, 'A Tale of Two Cities', 'Charles Dickens', 30)
    initial_books(3002, "Harry Potter and the Philosopher's Stone", 'J.K.Rowling', 40)
    initial_books(3003, 'The Lion, the Witch and the Wardrobe ', 'C.S.Lewis', 25)
    initial_books(3004, 'The Lord of the Rings', 'J.R.R Tolkein', 37)
    initial_books(3005, 'Alice in Wonderland', 'Lewis Carroll', 52)            
    initial_books(3006, 'Percy Jackson and the Battle of the Labyrinth', 'Rick Riordan ', 28)            
    initial_books(3007, 'The Return of the King', 'J.R.R Tolkein', 67)            
    initial_books(3008, 'The Stand', 'Stephen King', 7)            
          
          
    # Create the menu options:  
    while True:
        
        try:
            menu = int(input('''\nSelect one of the following options by entering the number:
        1. Enter book
        2. Update book
        3. Delete book
        4. Search books
        0. Exit        
            : '''))   
        except ValueError:
            print('Not a valid option. Enter 1, 2, 3, 4, or 0.') 
            continue
        
        if menu == 1: # Enter Book
            add_book()
        elif menu == 2: # Update Book
            update_book()
        elif menu == 3: # Delete Book
            delete_book()
        elif menu == 4: # Search Books
            search_books()
        elif menu == 0:
            print('Goodbye!')
            exit()
        else: # invalid option
            print('Invalid option. Try again.')
        
            

# catch the exception and rollback if any errors
except Exception as e:
    db.rollback()

finally:        
    # drop the table so the file can re-run without errors
    cursor.execute('''DROP TABLE books''')
    print('\nbooks table deleted')
    db.close()


# End of code

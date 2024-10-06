import mysql.connector
from mysql.connector import Error
from datetime import date


def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            database='library_management', 
            user='root',  # Replace with your MySQL username
            password='P@ssw0rd'  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection  # Return the connection object if successful
    except Error as e:
        print(f"Error: {e}")
        return None
    
def add_book(title, author, year, genre, quantity):
    connection = connect_to_db()  # Establish database connection
    if connection:
        cursor = connection.cursor()  # Create a cursor to execute queries
        query = """INSERT INTO Books (Title, Author, PublishedYear, Genre, Quantity) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (title, author, year, genre, quantity)  # Values to insert
        cursor.execute(query, values)  # Execute the SQL query
        connection.commit()  # Commit the changes to the database
        print(f"Book '{title}' added successfully.")
        connection.close()  # Close the connection

def register_user(name, email, user_type):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO Users (Name, Email, UserType) 
                   VALUES (%s, %s, %s)"""
        values = (name, email, user_type)
        cursor.execute(query, values)
        connection.commit()
        print(f"User '{name}' registered successfully.")
        connection.close()

def issue_book(book_id, user_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()

        # Check if the book is available (i.e., Quantity > 0)
        cursor.execute("SELECT Quantity FROM Books WHERE BookID = %s", (book_id,))
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            issue_date = date.today()  # Get today's date
            # Insert the transaction
            cursor.execute("""INSERT INTO Transactions (BookID, UserID, IssueDate, Status) 
                              VALUES (%s, %s, %s, 'Issued')""", (book_id, user_id, issue_date))
            # Update the quantity of the book
            cursor.execute("UPDATE Books SET Quantity = Quantity - 1 WHERE BookID = %s", (book_id,))
            connection.commit()
            print(f"Book with ID {book_id} issued to User ID {user_id}.")
        else:
            print("Book is not available.")
        
        connection.close()

def return_book(transaction_id):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        
        # Get the BookID and UserID from the transaction record
        cursor.execute("SELECT BookID, UserID FROM Transactions WHERE TransactionID = %s", (transaction_id,))
        result = cursor.fetchone()
        
        if result:
            book_id, user_id = result
            
            # Update the Transactions table to mark the book as returned
            cursor.execute("UPDATE Transactions SET ReturnDate = %s, Status = 'Returned' WHERE TransactionID = %s",
                           (date.today(), transaction_id))
            # Update the quantity of the book
            cursor.execute

def return_book(transaction_id):
    connection = connect_to_db()  # Connect to the database
    if connection:
        cursor = connection.cursor()
        
        # Get the BookID from the transaction record
        cursor.execute("SELECT BookID FROM Transactions WHERE TransactionID = %s", (transaction_id,))
        result = cursor.fetchone()
        
        if result:
            book_id = result[0]
            
            # Update the Transactions table to mark the book as returned
            cursor.execute("UPDATE Transactions SET ReturnDate = %s, Status = 'Returned' WHERE TransactionID = %s",
                           (date.today(), transaction_id))
            
            # Update the quantity of the book
            cursor.execute("UPDATE Books SET Quantity = Quantity + 1 WHERE BookID = %s", (book_id,))
            connection.commit()  # Commit changes to the database
            print(f"Book with Transaction ID {transaction_id} has been returned.")
        else:
            print("Transaction not found.")
        
        connection.close()

def view_books():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()  # Fetch all rows
        print("Books in the Library:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Year: {book[3]}, Genre: {book[4]}, Quantity: {book[5]}")
        connection.close()

def view_users():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()  # Fetch all rows
        print("Users Registered in the Library System:")
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, User Type: {user[3]}")
        connection.close()


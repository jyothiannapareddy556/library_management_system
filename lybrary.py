import sqlite3
from datetime import date

# Connect to database
conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    quantity INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS issues (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    student_id INTEGER,
    issue_date TEXT,
    return_date TEXT
)
""")

conn.commit()

# Functions
def add_book():
    title = input("Book Title: ")
    author = input("Author: ")
    qty = int(input("Quantity: "))
    cur.execute("INSERT INTO books VALUES (NULL,?,?,?)", (title, author, qty))
    conn.commit()
    print("Book added successfully!")

def view_books():
    cur.execute("SELECT * FROM books")
    for row in cur.fetchall():
        print(row)

def add_student():
    name = input("Student Name: ")
    course = input("Course: ")
    cur.execute("INSERT INTO students VALUES (NULL,?,?)", (name, course))
    conn.commit()
    print("Student added successfully!")

def view_students():
    cur.execute("SELECT * FROM students")
    for row in cur.fetchall():
        print(row)

def issue_book():
    book_id = int(input("Book ID: "))
    student_id = int(input("Student ID: "))

    cur.execute("SELECT quantity FROM books WHERE book_id=?", (book_id,))
    qty = cur.fetchone()

    if qty and qty[0] > 0:
        cur.execute("INSERT INTO issues VALUES (NULL,?,?,?,NULL)",
                    (book_id, student_id, date.today()))
        cur.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id=?", (book_id,))
        conn.commit()
        print("Book issued successfully!")
    else:
        print("Book not available!")

def return_book():
    issue_id = int(input("Issue ID: "))
    cur.execute("SELECT book_id FROM issues WHERE issue_id=?", (issue_id,))
    book = cur.fetchone()

    if book:
        cur.execute("UPDATE issues SET return_date=? WHERE issue_id=?",
                    (date.today(), issue_id))
        cur.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id=?", (book[0],))
        conn.commit()
        print("Book returned successfully!")
    else:
        print("Invalid Issue ID!")

# Menu
while True:
    print("""
--- Library Management System ---
1. Add Book
2. View Books
3. Add Student
4. View Students
5. Issue Book
6. Return Book
7. Exit
""")

    choice = input("Enter choice: ")

    if choice == '1':
        add_book()
    elif choice == '2':
        view_books()
    elif choice == '3':
        add_student()
    elif choice == '4':
        view_students()
    elif choice == '5':
        issue_book()
    elif choice == '6':
        return_book()
    elif choice == '7':
        break
    else:
        print("Invalid choice!")

conn.close()


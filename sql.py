import sqlite3

with sqlite3.connect('blog.db') as connection:
    c = connection.cursor()

    # Create table
    c.execute("""CREATE TABLE posts (title TEXT, post TEXT)""")

    # Enter posts
    c.execute('INSERT INTO posts VALUES("Good", "I\'m good")')
    c.execute('INSERT INTO posts VALUES("Well", "I\'m well")')
    c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent")')
    c.execute('INSERT INTO posts VALUES("Okay", "I\'m ok")')
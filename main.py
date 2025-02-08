import sqlite3
import sqlitedb

def main():
    db = sqlitedb.db()
    db.create_table(
        "test_table",
        [
            "Email VARCHAR(255) NOT NULL",
            "First_Name CHAR(25) NOT NULL",
            "Last_Name CHAR(25)",
            "Score INT"
        ]
    )
    
if __name__ == "__main__":
    main()
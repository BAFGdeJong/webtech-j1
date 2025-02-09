import sqlite3
from sqldb import Db

def main():
    db = Db('test')
    db.create_tables({
        'users':["email VARCHAR(255) NOT NULL UNIQUE","first_name CHAR(25) NOT NULL",],
        'keys': ["key NOT NULL UNIQUE",]
    })
    db.add_user("testtest.com", "tester")
    
if __name__ == "__main__":
    main()
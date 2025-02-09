import sqlite3
from sqldb import Db

def main():
    db = Db('test')
    db.create_tables({
        'test1':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
        'test2':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
        'test3':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
        'test4':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
        'test5':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
        'test6':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
        'test7':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
        'test8':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
        'test9':["Email VARCHAR(255) NOT NULL","First_Name CHAR(25) NOT NULL","Last_Name CHAR(25)","Score INT"],
    })
    
if __name__ == "__main__":
    main()
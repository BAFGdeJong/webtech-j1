import sqlite3

class db:
    def __init__(self):
        self.conn = sqlite3.connect(
            "test.db"
        )
        
    def create_table(self, table_name: str, what: list):
        if not what:
            return
        curs = self.conn.cursor()
        if len(what) > 1:
            what = what.__repr__().replace('[', '').replace(']', '')
        else:
            what = what[0]
        curs.execute(
            f"CREATE TABLE {table_name} ({what});"
        )
        curs.close()
    
    
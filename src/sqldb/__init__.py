import sqlite3
from pathlib import Path

# Need to make class easier to access.
class DbPath():
    def __init__(self, db_name):
        self.path = self._set_path(db_name)
    
    def _set_path(self, database_name):
        if not isinstance(database_name, str):
            raise ValueError("Name must be a string")
        if Path(database_name).suffix != ".db":
            database_name = f"{database_name}.db"
        loc = None
        d = Path(__file__).parent # Needs to be fixed in the futures, directory is location of sqlitedb.py atm.
        full_path = d.joinpath(database_name)
        temp = [d.joinpath("db"), d.joinpath("database")]
        # Check if there is already a db folder or file in current dir.
        for x in d.iterdir():
            if x == full_path \
            or x.is_dir() and x == temp[0] \
            or x.is_dir() and x == temp[1]:
                loc = x
                break
        
        tempi = d.parent.joinpath(database_name)
        temp = [d.parent.joinpath("db"), d.parent.joinpath("database")]
        # Check if there is already a db folder or file in parent dir.
        for x in d.parent.iterdir():
            if x == tempi \
            or x.is_dir() and x == temp[0] \
            or x.is_dir() and x == temp[1]:
                loc = x
                break
            
        if loc:
            if loc.is_dir():
                full_path = loc.joinpath(database_name)
            elif loc.is_file():
                full_path = loc
        else:
            d.parent.joinpath('db').mkdir()
            full_path = d.parent.joinpath('db')
        
        return full_path

class DbConn():
    def __init__(self, path, id):
        self._db_path = path
        self._conn_id = id
        self._connection = sqlite3.connect(path)
        self._available = True
        self._connection_alive = True
    
    def is_available(self):
        return self._available
    
    def is_connection_alive(self):
        return self._connection_alive
    
    def get_cursor(self):
        return self._connection.cursor()
    
    def commit(self):
        self._connection.commit()
    
    def open_connection(self):
        self._available = True
        return self._connection
    
    def close_connection(self):
        self._available = False
    
    def set_id(self, id: int):
        self._conn_id = id
        
    def get_id(self):
        return self._conn_id

    def forcefully_close(self):
        self._available = False
        self._connection.close()
        self._connection_alive = False

class DbPool():
    def __init__(self, path, connection_limit):
        self._path = path
        self._connection_limit = connection_limit
        self._pool = {}
        self._add_to_pool(connection_limit) # id: DbConn
        
    def _add_to_pool(self, amount):
        for x in range(len(self._pool), amount):
            self._pool.update({
                x: DbConn(self._path, x)
            })
    
    def _remove_from_pool(self, amount):
        for x in range(len(self._pool)-1, amount-1, -1):
            temp = self._pool.pop(x)
            temp.forcefully_close()
    
    def _clear_pool(self):
        self._pool.clear()
    
    def get_connection(self):
        for x, y in zip(self._pool.keys(), self._pool.values()):
            if y.is_available:
                return { x: y }
    
    def close_connection(self, connection: dict):
        self._pool.get(list(connection.keys())[0]).close_connection() # Improve later
    
    def set_connection_limit(self, new_limit: int):
        if new_limit == self._connection_limit:
            return
        
        if new_limit > self._connection_limit:
            self._add_to_pool(new_limit)
        else:
            self._remove_from_pool(self, new_limit)
        
        self._connection_limit = new_limit
    
    def reset_pool(self):
        for x in self._pool.values():
            x.forcefully_close()
        self._clear_pool()
        self._add_to_pool(self._connection_limit)

class Db:    
    def __init__(self, database_name: str, connection_limit: int = 100):
        self.pool = DbPool(DbPath(database_name).path, connection_limit)

    def add_user(self, email: str, first_name: str):
        db = self.pool.get_connection()
        conn: DbConn = list(db.values())[0] # Needs to be improved
        curs = conn.get_cursor()
        
        try:
            curs.execute("INSERT INTO users (email, first_name) VALUES (?, ?)", (email, first_name))
        except Exception as e:
            print(e)
        
        curs.close()
        conn.commit()
        self.pool.close_connection(db)

    def create_tables(self, tables_to_create: dict):
        """
        Input:
            tables_to_create: dict = { 'table_name': ['columns_and_constraints'] }
        Ouput:
            void, creates the requested tables in the database.
        """
        for table, what in zip(tables_to_create.keys(), tables_to_create.values()):
            if len(what) > 0:
                self.create_table(table, what)
            else:
                print(f"Error: What to add is not defined, {table}: {what}. Skipping table: {table}.")
    
    def create_table(self, table_name: str, columns_and_constraints: list):
        """
        Input:
            table_name: str = " {name of the table to add} "
            columns_and_constraints: list = [ {Columns of table} ]
        Ouput: 
            void, creates the requested table in the database.
        """
        connection = self.pool.get_connection()
        conn = list(connection.values())[0]
        
        curs = conn.get_cursor()
        
        what = columns_and_constraints.__repr__().replace('[', '').replace(']', '').replace("'", '')
        try:
            curs.execute(f"CREATE TABLE {table_name} ({what})")
        except Exception as e:
            print(f"Error: {e}, while executing: CREATE TABLE {table_name} ({what}) in def create_table")
        curs.close()
        self.pool.close_connection(connection)
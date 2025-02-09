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
        self._conn_id = id
        self._connection = sqlite3.connect(path)
        self._cursors = []
        self._in_use = False
        self._connection_alive = True
    
    def is_available(self):
        return self._in_use
    
    def is_connection_alive(self):
        return self._connection_alive
    
    def get_cursor(self):
        x = self._connection.cursor()
        self._cursors.append(id(x))
        return x
    
    def close_cursor(self, cursor):
        if id(cursor) in self._cursors:
            cursor.close()
        else:
            raise
    
    def set_connection(self, path):
        self._in_use = True
        self.close_connection()
        self._connection = sqlite3.connect(path)
        self._in_use = False
        
    def set_id(self, id: int):
        self._conn_id = id
        
    def get_id(self):
        return self._conn_id

    def forcefully_close(self):
        self._in_use = True
        self._connection.close()
        self._connection_alive = False
        self._in_use = False


class DbPool():
    def __init__(self, path, connection_limit):
        self._path = path
        self._connection_limit = connection_limit
        self._pool = {}
        self._add_to_pool(path, connection_limit)
        
    def _add_to_pool(self, amount):
        for x in range(len(self._pool), amount):
            self._pool.update({
                x: DbConn(self._path, x)
            })
    
    def _remove_from_pool(self, amount):
        for x in range(len(self._pool)-1, amount-1, -1):
            temp = self._pool.pop(x)
            temp.forcefully_close()
    
    def set_connection_limit(self, new_limit: int):
        if new_limit == self._connection_limit:
            return
        
        if new_limit > self._connection_limit:
            self._add_to_pool(new_limit)
        else:
            self._remove_from_pool(self, new_limit)
        
        self._connection_limit = new_limit
            
    

    # def create_connection(self):
    #     try: 
    #         temp = self._add_to_pool()
    #         return {'id': temp, 'connection': self._pool.get(temp)}
    #     except Exception as e:
    #         raise e
    
    # def close_connection(self, connection: dict):
    #     try:
    #         self._remove_from_pool(connection.get('id'))
    #         return
    #     except Exception as e:
    #         raise e
    
    # def _get_id_and_pop(self) -> int:
    #     return (self._poss_ids[-1], self._poss_ids.pop())[0]
    
    # def _return_id_to_list(self, id_to_ret_to_list):
    #     self._poss_ids.append(id_to_ret_to_list)
    
    # def reset_pool(self):
    #     for x in self._pool.values():
    #         x.disconnect()
    #     self._pool.clear()
    #     self._poss_ids = [x for x in reversed(range(self._connection_limit))]

class Db:    
    def __init__(self, database_name: str, connection_limit: int = 100):
        self.pool = DbPool(DbPath(database_name).path, connection_limit)

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
        try:
            connection = self.pool.create_connection()
            conn: DbConn = connection.get('connection')
        except Exception as e:
            raise e
        
        curs = conn.connection.cursor()
        
        what = columns_and_constraints.__repr__().replace('[', '').replace(']', '')
        try:
            curs.execute(f"CREATE TABLE {table_name} ({what})")
        except Exception as e:
            print(f"Error: {e}, while executing: CREATE TABLE {table_name} ({what}) in def create_table")
        curs.close()
        self.pool.close_connection(connection)
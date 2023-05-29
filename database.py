from pyodbc import connect

class DataBase():
    server = 'dbhackathon.database.windows.net'
    database = 'hack'
    username = 'hack'
    password = 'Password23'
    table_name = 'dbo.PRODUTO'
    connection = None

    def __init__(self) -> None:
        self.connection = connect('DRIVER={SQL SERVER};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password, timeout=5)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __del__(self) -> None:
        if self.connection:
            self.connection.close()

    def __exit__(self, exc_type, exc_value, traceback):
        del self

    def query_execute(self, query:str):
        self.cursor.execute(query)
        self.connection.commit()
        return self

    def create_table(self, cols:list):
        cols_str = f'{cols[0]} TEXT PRIMARY KEY, '
        cols_str += ' TEXT, '.join(cols[1:])
        cols_str += ' TEXT'
        query = f'CREATE TABLE {self.table_name} ({cols_str});'
        self.table_exist = True
        return self.query_execute(query)

    def insert(self, cols, values):
        if self.table_exist == False:
            self.create_table(cols)

        cols_str = ', '.join(cols)
        values_str = '"'
        values_str += '", "'.join(values)
        values_str += '"'

        query = f'INSERT INTO {self.table_name} ({cols_str}) VALUES ({values_str})'
        return self.query_execute(query)

    def update(self, cols, values):
        if self.table_exist == False:
            self.create_table(cols)

        if not self.exist(cols[0], values[0]):
            return self.insert(cols, values)

        set_str = ', '.join([f'{col}="{val}"' for col, val in zip(cols, values)])
        query = f'UPDATE {self.table_name} SET {set_str}'
        return self.query_execute(query)

    def exist(self, col, value):
        query = f'SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE {col}="{value}")'
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return True if result == 1 else False

    def select(self, col, value) -> list:
        query = f'SELECT * FROM {self.table_name} WHERE {col}="{value}"'
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_all(self):
        query = f'SELECT * FROM {self.table_name}'
        self.cursor.execute(query)
        return self.cursor.fetchall()
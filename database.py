from pyodbc import connect

class DataBase():
    server = 'dbhackathon.database.windows.net'
    database = 'hack'
    username = 'hack'
    password = 'Password23'
    table_name = 'dbo.PRODUTO'

    def __init__(self) -> None:
        self.connection = connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __del__(self) -> None:
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

class Produto():
    def __init__(self, id:int, nome:str, taxa_de_juros:float, prazo_minimo:int, prazo_maximo:int, valor_minimo:float, valor_maximo:float) -> None:
        self.id = id
        self.nome = nome
        self.taxa_de_juros = taxa_de_juros
        self.prazo_minimo = prazo_minimo
        self.prazo_maximo = prazo_maximo
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo

    def validar_simulacao(self, valor_desejado:float, prazo:int) -> bool:
        if self.valor_maximo is not None and valor_desejado > self.valor_maximo:
            return False
        if self.valor_minimo is not None and valor_desejado < self.valor_minimo:
            return False
        if self.prazo_maximo is not None and valor_desejado > self.prazo_maximo:
            return False
        if self.prazo_minimo is not None and valor_desejado < self.prazo_minimo:
            return False
        return True

    def __str__(self) -> str:
        return f'{self.nome} | Taxa: {self.taxa_de_juros} | Prazo(min-max): {self.prazo_maximo}-{self.prazo_minimo} | Valor(min-max): {self.valor_maximo}-{self.valor_minimo}'

class Lista_Produtos(list):
    def __init__(self) -> None:
        return super().__init__()

    def carregar_produtos_da_db(self):
        self.clear()
        with DataBase() as db:
            rows = db.select_all()
        for row in rows:
            self.append(Produto(*row))

    def __str__(self) -> str:
        txt = ''
        for i in [f'{i} - {produto}\n' for i, produto in enumerate(self)]:
            txt += i
        return txt

if __name__ == '__main__':
    lista = Lista_Produtos()
    lista.carregar_produtos_da_db()
    print(lista)
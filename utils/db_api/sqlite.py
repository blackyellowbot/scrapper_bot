import datetime
import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):

        if not parameters:
            parameters = tuple()

        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        id int NOT NULL,
        Name varchar(255) NOT NULL,
        dates TIMESTAMP ,
        is_user int ,
        worlds varchar(255),
        PRIMARY KEY (id)

        );
        """
        self.execute(sql, commit=True)

    def create_table_worlds(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Worlds(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worldes varchar(255)
        );
        """
        self.execute(sql, commit=True)

    def create_table_allowed_users(self):
        sql = """
           CREATE TABLE IF NOT EXISTS Ausers(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           idn varchar(255)
           );
           """
        self.execute(sql, commit=True)

    def create_table_chats(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat varchar(255)
        );
        """
        self.execute(sql, commit=True)

    def create_table_lanch(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Lanch(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id varchar(255) NOT NULL,
        dates TIMESTAMP ,
        isFree int NOT NULL

        );
        """
        self.execute(sql, commit=True)

    def create_table_coffe(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Coffe(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id varchar(255) NOT NULL,
        dates TIMESTAMP ,
        isFree int NOT NULL

        );
        """
        self.execute(sql, commit=True)

    def add_auser(self, id: int, idn: str):
        sql = "INSERT INTO Ausers(id, idn) VALUES (?,?)"
        parameters = (None, idn)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_ausers(self):
        sql = "SELECT * from Ausers"
        return self.execute(sql, fetchall=True)

    def delete_ausers(self, id: int):
        self.execute("DELETE FROM Ausers WHERE id=?", (id,), commit=True)

    def add_worlds(self, id: int, worldes: str):
        sql = "INSERT INTO Worlds(id, worldes) VALUES (?,?)"
        parameters = (None, worldes)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_worlds(self):
        sql = "SELECT * from Worlds"
        return self.execute(sql, fetchall=True)

    def delete_world(self, ids: int):
        self.execute("DELETE FROM Worlds WHERE id=?", (ids,), commit=True)



    def add_chats(self, id: int, chat: str):
        sql = "INSERT INTO Chats(id, chat) VALUES (?,?)"
        parameters = (None, chat)
        self.execute(sql, parameters=parameters, commit=True)

    def select_all_chats(self):
        sql = "SELECT * from Chats"
        return self.execute(sql, fetchall=True)

    def delete_chats(self, ids: int):
        self.execute("DELETE FROM Chats WHERE id=?", (ids,), commit=True)


    def addLanch(self, id: int, user_id, dates: str, isFree: int):
        sql = "INSERT INTO Lanch(id, user_id, dates, isFree) VALUES (?,?,?,?)"
        parameters = (None, user_id, dates, isFree)
        self.execute(sql, parameters=parameters, commit=True)

    def addCoffe(self, id: int, user_id, dates: str, isFree: int):
        sql = "INSERT INTO Coffe(id, user_id, dates, isFree) VALUES (?,?,?,?)"
        parameters = (None, user_id, dates, isFree)
        self.execute(sql, parameters=parameters, commit=True)

    def update_qr(self, name, id):
        sql = "UPDATE Qrcode SET Name=? WHERE id=?"
        return self.execute(sql, parameters=(name, id), commit=True)

    def select_lanch(self, **kwargs):
        sql = "SELECT * FROM Lanch WHERE "
        sql, parameters = self.format_args(self, sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def select_coffe(self, **kwargs):
        sql = "SELECT * FROM Coffe WHERE "
        sql, parameters = self.format_args(self, sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def add_user(self, id: int, name: str, date: str, is_user: int, worlds: str):
        sql = "INSERT INTO Users(id, Name, dates, is_user, worlds) VALUES (?,?,?,?,?)"
        parameters = (id, name, date, is_user, worlds)
        self.execute(sql, parameters=parameters, commit=True)

    def update_user(self, id: int, name: str, date: str, lanch: int, coffe: int):
        sql = "UPDATE  Users SET  Name=?, dates=?, lanch=?, coffe=? WHERE id=?"
        # parameters = (id, name, date, lanch, coffe)
        return self.execute(sql, parameters=(name, date, lanch, coffe, id), commit=True)
        # self.execute(sql, parameters=parameters, commit=True)

    @staticmethod
    def format_args(self, sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(self, sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def update_launch(self, dates, lanch, id):
        sql = "UPDATE Users SET dates=?, lanch=? WHERE id=?"
        return self.execute(sql, parameters=(dates, lanch, id), commit=True)

    def select_all_users(self):
        sql = "SELECT * from Users"
        return self.execute(sql, fetchall=True)


def logger(statement):
    print('')
    print(f"""
    ___________________________________________
    Execute:
    # {statement}
    ___________________________________________

    """)

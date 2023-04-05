import sqlite3


con = sqlite3.connect('database/data.db')
cursor = con.cursor()


class db():
    def __init__(self, user_id):
        self.user_id = user_id
        try:
            self.__data = self.select_data('users')
            self.hin = int(self.__data[1])
            self.xp = int(self.__data[2])
            self.lvl = int(self.__data[3])
            self.next_xp = int(self.__data[4])
        except:
            self.xp = int
            self.lvl = int

    def new_user(self, table, values):
        cursor.execute(f'INSERT INTO {table} VALUES {values}')
        con.commit()


    def inset_value_to_table(self, table, values):
        cursor.execute(f'INSERT INTO \'{table}\' VALUES ({values})')
        con.commit()

    def select_from_table(self, table):
        cursor.execute(f'SELECT * FROM {table}')
        return cursor.fetchall()

    def select_chats(self, table, chat_id):
        cursor.execute(f'SELECT {chat_id} FROM {table} WHERE chat_id = {chat_id}')
        return cursor.fetchone()

    def is_user(self):
        a = cursor.execute(
            f'SELECT {self.user_id} FROM users WHERE user_id = {self.user_id}')
        if a.fetchall() == []:
            return False
        else:
            return True

    def select_data(self, table):
        cursor.execute(f'SELECT * FROM {table} WHERE user_id = {self.user_id}')
        return cursor.fetchall()[0]

    def select_value(self, value, table):
        cursor.execute(
            f'SELECT {value} FROM \'{table}\' WHERE user_id = {self.user_id}')
        return cursor.fetchone()

    def select_value_from_table(self, value, table):
        cursor.execute(f'SELECT {value} FROM {table}')
        return cursor.fetchone()[0]

    def set_value_from_table(self, name, value, table):
        cursor.execute(f'UPDATE {table} SET {name} = {value}')
        con.commit()

    def set_value(self, name, value, table):
        cursor.execute(
            f'UPDATE {table} SET {name} = {value} WHERE user_id = {self.user_id}')
        con.commit()

    def create_table(self, table, values):
        cursor.execute(f'CREATE TABLE IF NOT EXISTS \'{table}\' ({values})')
        con.commit()

    def delete_table(self, table):
        cursor.execute(f'DROP TABLE IF EXISTS \'{table}\'')
        con.commit()

    def minus_value(self, value, name, table):
        cursor.execute(f'UPDATE {table} SET {name} = {name} - {value} WHERE user_id = {self.user_id}')
        con.commit()

    def plus_value(self, value, name, table):
        cursor.execute(f'UPDATE {table} SET {name} = {name} + {value} WHERE user_id = {self.user_id}')
        con.commit()
    
        

    def is_table(self, table):
        try:
            cursor.execute(f'SELECT * FROM {table}')
            return True
        except:
            return None

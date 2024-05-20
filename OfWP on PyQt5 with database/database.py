import sqlite3


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('users.db')
        self.cursor = self.connection.cursor()

    def registration(self, login, password):
        try:
            sql = 'INSERT INTO logins (login, password) values (?, ?)'
            self.cursor.execute(sql, (str(login), str(password)))
            self.connection.commit()
            return True
        except:
            return False

    def login(self, login, password):
        try:
            sql = "SELECT login, password FROM logins WHERE login = ? AND password = ?"
            data = self.cursor.execute(sql, (login, password)).fetchall()
            if data:
                return True
            else:
                return False

        except Exception as e:
            return e

    def usr_del_programs(self, programs):
        if programs == 'all':
            sql = 'UPDATE user_program SET status = "1" WHERE id BETWEEN ? AND ?'
            self.cursor.execute(sql, (self.rang - 30, self.rang))
            self.connection.commit()
        elif programs == 'reinstall':
            sql = 'UPDATE user_program SET status = "0" WHERE id BETWEEN ? AND ?'
            self.cursor.execute(sql, (self.rang - 30, self.rang))
            self.connection.commit()
        else:
            for app in programs:
                # узнаём id программы:
                sql = 'SELECT id FROM programs WHERE program = ?'
                appid = self.cursor.execute(sql, (app,)).fetchone()[0]
                sql = 'UPDATE user_program SET status = 1 WHERE (id BETWEEN ? AND ?) AND program_id = ?'
                self.cursor.execute(sql, (self.rang - 30, self.rang, appid))
                self.connection.commit()

    def user_log_in(self, username):
        usrid = self.cursor.execute("SELECT id FROM logins WHERE login = ?",
                                    (str(username))).fetchone()[0]
        for i in range(1, 31):
            sql = 'INSERT INTO user_program (user_id, program_id, status) values (?, ?, ?)'
            self.cursor.execute(sql, (usrid, i, 0))
            self.connection.commit()
        self.rang = int(self.cursor.execute(
            "SELECT MAX(`id`) FROM `user_program`").fetchone()[0])

    def close_connection(self):
        self.connection.close()

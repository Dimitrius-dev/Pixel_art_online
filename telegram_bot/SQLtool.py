import psycopg2
from config import host, user, password, db_name


class SQL:
    def __init__(self):
        self.connection = None
        self.error = "error"
        self.ok = "operation completed"

    def my_accounts(self, chat_id):
        msg = self.get(
            "SELECT login FROM users WHERE telegram_id = '" + str(chat_id) + "';"
            , some_answers=True)
        print("msg:", msg, chat_id)
        return msg

    def is_special_login(self, login_):
        msg = self.get(
            "SELECT login FROM users WHERE login = '" + str(login_) + "';"
            , some_answers=False)
        # print("msg:", msg)
        if msg == login_:
            return False
        else:
            return True

    def delete_account_by_login(self, login_):
        msg = self.set(
            "DELETE FROM users " \
            "WHERE login = '" + str(login_) + "';"
        )
        # print("msg:", msg)
        if msg == self.error:
            return False
        else:
            return True

    def is_my_login(self, login_, chat_id):
        msg = self.get(
            "SELECT login FROM users " \
            "WHERE login = '" + str(login_) + "' AND telegram_id = '" + str(chat_id) + "';"
            , some_answers=False)
        print("msg:=", msg, "=")
        if msg == login_:
            return True
        else:
            return False

    def add_account(self, login_, password_, chat_id):
        msg = self.set(
            "INSERT INTO users(login, password, telegram_id) VALUES " \
            "('" + str(login_) + "', '" + str(password_) + "', '" + str(chat_id) + "');"
        )

        if msg == self.error:
            return False
        else:
            return True

    def set(self, sql_msg):
        sql_msg: str

        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            self.connection.autocommit = True

            with self.connection.cursor() as cursor:
                cursor.execute(
                    sql_msg
                )
            return self.ok
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
            return self.error
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                print("[INFO] PostgreSQL connection closed")

    def get(self, sql_msg, some_answers=False):
        sql_msg: str

        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            self.connection.autocommit = True

            with self.connection.cursor() as cursor:
                cursor.execute(
                    sql_msg
                    # "SELECT version();"
                    # "SELECT password FROM users WHERE login = '" + login_ + "';"
                    # "SELECT * FROM users;"
                )

                if not some_answers:
                    return self.parse(cursor)

                msg = ""
                iter = 1
                while True:
                    buf = self.parse(cursor)
                    if buf == "None":
                        if not msg:
                            return "None"
                        return msg
                    msg += str(iter) + ". " + buf + '\n'
                    iter += 1

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
            return self.error
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                # print("[INFO] PostgreSQL connection closed")

    def parse(self, cursor):
        buf = str(cursor.fetchone()) \
            .replace(',', "") \
            .replace('(', "") \
            .replace(')', "") \
            .replace('\'', "")
        return buf

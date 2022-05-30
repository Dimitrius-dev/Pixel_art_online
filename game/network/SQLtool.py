import psycopg2
from config import host_db, user, password, db_name


class SQL:
    def __init__(self):
        self.connection = None

    def is_password(self, login_, password_):

        receiv_passwd = self.get_password(login_)
        print("password: l", receiv_passwd, "l")
        if receiv_passwd == "" or receiv_passwd != password_:
            print("blocked")
            return False
        else:
            print("entering")
            return True

    def get_password(self, login_: str):
        password_ = ""

        try:
            self.connection = psycopg2.connect(
                host=host_db,
                user=user,
                password=password,
                database=db_name
            )
            self.connection.autocommit = True

            with self.connection.cursor() as cursor:
                cursor.execute(
                    # "SELECT version();"
                    "SELECT password FROM users WHERE login = '" + login_ + "';"
                    # "SELECT * FROM users;"
                )

                password_ = str(cursor.fetchone()) \
                    .replace(',', "") \
                    .replace('(', "") \
                    .replace(')', "") \
                    .replace('\'', "") \
                    .replace(' ', "")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
            return password_
        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
                # print("[INFO] PostgreSQL connection closed")
            return password_

    # the cursor for perfoming database operations
    # cursor = connection.cursor()

    # create a new table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE users(
    #             id serial PRIMARY KEY,
    #             first_name varchar(50) NOT NULL,
    #             nick_name varchar(50) NOT NULL);"""
    #     )

    #     # connection.commit()
    #     print("[INFO] Table created successfully")

    # insert data into a table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO users (first_name, nick_name) VALUES
    #         ('Oleg', 'barracuda');"""
    #     )

    #     print("[INFO] Data was succefully inserted")

    # get data from a table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """SELECT nick_name FROM users WHERE first_name = 'Oleg';"""
    #     )

    #     print(cursor.fetchone())

    # delete a table
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """DROP TABLE users;"""
    #     )

    #     print("[INFO] Table was deleted")

import sqlite3


class User:
    def __init__(self, user_id, first_name, username, role):
        self.user_id = user_id
        self.first_name = first_name
        self.username = username
        self.role = role

    @staticmethod
    def does_admin_exist() -> bool:
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM users WHERE role = 'admin'"
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                return result != []

    @staticmethod
    def get_all_admins_ids() -> list:
        ids = []
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT user_id FROM users WHERE role = 'admin' OR role = 'moderator'"
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

            for user in result:
                ids.append(user[0])

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            return ids

    @staticmethod
    def get_all_blocked_ids() -> list:
        ids = []
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT user_id FROM users WHERE role = 'blocked'"
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

            for user in result:
                ids.append(user[0])

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            return ids

    @staticmethod
    def get_from_database_by_id(user_id: int):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM users WHERE user_id = ?"
            data = (user_id,)
            cursor.execute(query, data)

            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            if result != []:
                return User(result[0], result[1], result[2], result[3])
            return None

    @staticmethod
    def get_from_database_by_username(username: str):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM users WHERE username = ?"
            data = (username,)
            cursor.execute(query, data)

            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            if result != []:
                return User(result[0], result[1], result[2], result[3])
            return None

    def add_to_database(self) -> bool:
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "INSERT INTO users (user_id, first_name, username, role) VALUES (?, ?, ?, ?)"
            data = (self.user_id, self.first_name, self.username, self.role)
            cursor.execute(query, data)

            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                return True
            return False

    def delete_from_database(self) -> bool:
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "DELETE FROM users WHERE user_id = ?"
            data = (self.user_id,)

            cursor.execute(query, data)
            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                return True
            return False

    @staticmethod
    def is_user_new(user_id: int) -> bool:
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM users WHERE user_id = ?"
            data = (user_id,)
            cursor.execute(query, data)

            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                return result is None
            return True

    def set_role(self, role: str) -> bool:
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "UPDATE users SET role = ? WHERE user_id = ?"
            data = (role, self.user_id)

            cursor.execute(query, data)
            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                self.role = role
                return True
            return False

    @staticmethod
    def is_admin(user_id: int) -> bool:
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT role FROM users WHERE user_id = ?"
            data = (user_id,)
            cursor.execute(query, data)

            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                return result[0] == "admin"
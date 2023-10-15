import sqlite3


class Ad:
    def __init__(self, title: str, description: str, photo_id: str, created_by: int, topic_id: int, ad_id: str,
                 status: str):
        self.title = title
        self.description = description
        self.photo_id = photo_id
        self.created_by = created_by
        self.topic_id = topic_id
        self.ad_id = ad_id
        self.status = status.lower()

    @staticmethod
    def get_ad_by_id(ad_id: str):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM ads WHERE ad_id = ?"
            data = (ad_id,)
            cursor.execute(query, data)

            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            if result:
                return Ad(
                    title=result[0],
                    description=result[1],
                    photo_id=result[2],
                    created_by=result[3],
                    topic_id=result[4],
                    ad_id=result[5],
                    status=result[6]
                )
            return None

    def add_to_database(self):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "INSERT INTO ads (title, description, photo_id, created_by, topic_id, ad_id, status) VALUES (?, ?, ?, ?, ?, ?, ?)"
            data = (
            self.title, self.description, self.photo_id, self.created_by, self.topic_id, self.ad_id, self.status)
            cursor.execute(query, data)

            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()

    def change_status(self, new_status):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "UPDATE ads SET status = ? WHERE ad_id = ?"
            data = (new_status, self.ad_id)
            cursor.execute(query, data)

            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
                self.status = new_status

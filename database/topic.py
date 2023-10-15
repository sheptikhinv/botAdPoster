import sqlite3


class Topic:
    def __init__(self, topic_id, title, created_by):
        self.topic_id = topic_id
        self.title = title
        self.created_by = created_by

    @staticmethod
    def get_all_topics():
        topics = []
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM topics"
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

            for topic in result:
                topics.append(Topic(topic[0], topic[1], topic[2]))

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            return topics

    @staticmethod
    def get_topic_by_id(topic_id: int):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "SELECT * FROM topics WHERE topic_id = ?"
            data = (topic_id,)
            cursor.execute(query, data)

            result = cursor.fetchone()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()
            if result != []:
                return Topic(result[0], result[1], result[2])
            return None

    def add_to_database(self):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "INSERT INTO topics (topic_id, title, created_by) VALUES (?, ?, ?)"
            data = (self.topic_id, self.title, self.created_by)
            cursor.execute(query, data)

            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()

    def delete_from_database(self):
        try:
            db_connection = sqlite3.connect("database.db")
            cursor = db_connection.cursor()

            query = "DELETE FROM topics WHERE topic_id = ?"
            data = (self.topic_id,)
            cursor.execute(query, data)

            db_connection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print(error)

        finally:
            if db_connection:
                db_connection.close()

import sqlite3


def create_tables():
    db_connection = sqlite3.connect("database.db")
    cursor = db_connection.cursor()

    query = """
            CREATE TABLE if NOT EXISTS users
            (
                user_id    integer not null,
                first_name TEXT    not null,
                username   TEXT,
                role       TEXT    not null
            );
            """
    cursor.execute(query)

    query = """
            CREATE TABLE if NOT EXISTS topics
            (
                topic_id   integer not null,
                title      TEXT    not null,
                created_by INT     not null
            );
            """

    cursor.execute(query)

    query = """
            CREATE TABLE if NOT EXISTS ads
            (
                title       TEXT    not null,
                description TEXT    not null,
                photo_id    TEXT,
                created_by  integer not null,
                topic_id    integer not null,
                ad_id       TEXT    not null,
                status      TEXT    not null
            );
            """

    cursor.execute(query)

    db_connection.commit()
    cursor.close()

    if db_connection:
        db_connection.close()
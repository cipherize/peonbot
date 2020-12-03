import psycopg2

from modules import blizzard
from modules.config import config

conn_params = {
    "host": config.db.host if config.db.host else None,
    "port": config.db.port if config.db.host else None,
    "dbname": config.db.dbname,
    "user": config.db.user,
    "password": config.db.password,
}

conn = psycopg2.connect(**conn_params)


def db_test():
    cur = conn.cursor()
    cur.execute("SELECT CURRENT_TIMESTAMP;")
    return cur.fetchone()


def get_my_characters(user_id: int):
    cur = conn.cursor()
    cur.execute(
        "SELECT char_name, realm_slug FROM characters WHERE user_id = %s;", [user_id]
    )
    return cur.fetchall()


def get_char_owner(char_name: str, realm_slug: str):
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id FROM characters WHERE char_name = %s AND realm_slug = %s;",
        [char_name, realm_slug],
    )
    return cur.fetchone()


def set_char_owner(user_id: int, char_name: str, realm_slug: str):
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO characters VALUES (%s, %s, %s);", [user_id, char_name, realm_slug]
    )
    conn.commit()

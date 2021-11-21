import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connections = create_connection("C:\\Users\dkony\PycharmProjects\pythonProject\sm_app.sqlite")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  password TEXT,
  permission INTEGER
);
"""

create_tests_table = """
CREATE TABLE IF NOT EXISTS tests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  date_of_creation datetime default current_timestamp,
  creator_id INTEGER NOT NULL
);
"""


create_questions_table = """
CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  test_id INTEGER NOT NULL,
  number INTEGER NOT NULL,
  question TEXT NOT NULL,
  type INTEGER NOT NULL,
  answer TEXT,
  FOREIGN KEY (test_id) REFERENCES tests (id)
);
"""


create_variants_table = """
CREATE TABLE IF NOT EXISTS variants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER,
  number INTEGER NOT NULL,
  variant TEXT,
  FOREIGN KEY (question_id) REFERENCES questions (id)
);
"""


create_user_answer_table = """
CREATE TABLE IF NOT EXISTS user_answer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  user_answer TEXT,
  FOREIGN KEY (question_id) REFERENCES questions (id) FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


execute_query(connections, create_users_table)
execute_query(connections, create_tests_table)
execute_query(connections, create_questions_table)
execute_query(connections, create_variants_table)
execute_query(connections, create_user_answer_table)

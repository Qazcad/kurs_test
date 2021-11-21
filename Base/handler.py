import sqlite3
import re


def login(login, passw, signal):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()

    # Проверяем есть ли такой пользователь
    cur.execute(f'SELECT * FROM users WHERE name="{login}";')
    value = cur.fetchall()

    if value != [] and value[0][2] == passw:
        signal.emit('Успешная авторизация!')
        id = value[0][0]
        cur.close()
        con.close()
        return id
    else:
        signal.emit('Проверьте правильность ввода данных!')
        cur.close()
        con.close()
        return -1


def register(login, passw, signal):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()

    cur.execute(f'SELECT * FROM users WHERE name="{login}";')
    value = cur.fetchall()

    if value != []:
        signal.emit('Такой ник уже используется!')
        cur.close()
        con.close()
        return -1

    elif value == []:
        cur.execute(f"INSERT INTO users (name, password) VALUES ('{login}', '{passw}')")
        signal.emit('Вы успешно зарегистрированы!')
        id  = cur.lastrowid
        con.commit()
        cur.close()
        con.close()
        return id


def register_test(test_name, count, user_id, signal):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM tests WHERE name="{test_name}";')
    value = cur.fetchall()

    if value != []:
        signal.emit('Тест с таким названием уже есть!')
        return 0
        cur.close()
        con.close()

    elif value == []:
        cur.execute(f"INSERT INTO tests (name, creator_id) VALUES ('{test_name}', {user_id})")
        signal.emit('Тест успешно создан!')
        id = cur.lastrowid
        con.commit()
        cur.close()
        con.close()
        return id


def give_test_list():
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    t_list = []
    cur.execute('SELECT COUNT(*) FROM tests')
    count = cur.fetchone()[0]
    cur.execute('SELECT name FROM tests')

    for i in range(0, int(count)):
        name = cur.fetchone()[0]
        t_list.append(name)
    return t_list


def register_question(test_id, index, question, answer, type1, signal):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM questions WHERE number={index} AND test_id={test_id};')
    value = cur.fetchall()
    if value == []:
        #cur.execute(f"INSERT INTO questions (test_id, number, question, type, answer) VALUES ({test_id}, {index}, '{question}', {type1}, {answer})")
        sqlite_insert_with_param = f"""INSERT INTO questions
                                (test_id, number, question, type, answer)
                                VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (test_id, index, question, type1, answer)
        cur.execute(sqlite_insert_with_param, data_tuple)
        signal.emit('Вопрос создан!')
        ide = cur.lastrowid
        con.commit()
        cur.close()
        con.close()
        return ide
    elif value != []:
        sqlite_insert_with_param = f"""UPDATE questions
                                            SET
                                              question = ?, 
                                              type = ?, 
                                              answer = ?
                                        WHERE number={index} AND test_id={test_id};"""

        data_tuple = (question, type1, answer)
        cur.execute(sqlite_insert_with_param, data_tuple)
        signal.emit('Вопрос создан!')
        ide = cur.lastrowid
        con.commit()
        cur.close()
        con.close()
        return ide


def register_variant(question_id, index, text):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM variants WHERE number={index} AND question_id={question_id};')
    value = cur.fetchall()
    if value == []:
        # cur.execute(f"INSERT INTO questions (test_id, number, question, type, answer) VALUES ({test_id}, {index}, '{question}', {type1}, {answer})")
        sqlite_insert_with_param = f"""INSERT INTO variants
                                    (question_id, number, variant)
                                    VALUES (?, ?, ?);"""

        data_tuple = (question_id, index, text)
        cur.execute(sqlite_insert_with_param, data_tuple)
        con.commit()
        cur.close()
        con.close()

    elif value != []:
        sqlite_insert_with_param = f"""UPDATE variants
                                            SET
                                              variant = ?
                                        WHERE number={index} AND question_id={question_id};"""

        data_tuple = (text)
        cur.execute(sqlite_insert_with_param, data_tuple)
        con.commit()
        cur.close()
        con.close()


def check_question(test_id, index):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM questions WHERE test_id={test_id} AND number = {index};')
    value = cur.fetchall()

    if value != []:
        cur.execute(f'SELECT * FROM questions WHERE test_id={test_id} AND number = {index};')
        a = cur.fetchone()[0]
        print('Айди вопроса = ' + str(a))
        cur.close()
        con.close()
        return int(a)

    elif value == []:
        cur.close()
        con.close()
        return 0

def give_text_question(test_id, index):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT question FROM questions WHERE test_id={test_id} AND number = {index};')
    check = cur.fetchone()

    value = ""
    if check is not None:
        value = check[0]
    cur.close()
    con.close()
    return value

def give_question_type(test_id, index):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT type FROM questions WHERE test_id={test_id} AND number = {index};')
    value = int(cur.fetchone()[0])
    cur.close()
    con.close()
    return value

def give_question_answer(test_id, index):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT answer FROM questions WHERE test_id={test_id} AND number = {index};')
    value = cur.fetchone()[0]
    parse = value.replace('[', '')
    parse = parse.replace(']', '')
    parse = parse.replace(',', '')
    parse = parse.replace("'", '')
    parse = parse.split()
    cur.close()
    con.close()
    return parse

def give_question_variant(question_id, number):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT variant FROM variants WHERE question_id={question_id} AND number = {number};')
    value = cur.fetchone()[0]
    return value

def check_true_variant(test_id, index, text):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT answer FROM questions WHERE test_id={test_id} AND number = {index};')
    value = cur.fetchone()[0]
    parse = value.replace('[', '')
    parse = parse.replace(']', '')
    parse = parse.replace(',', '')
    parse = parse.replace("'", '')
    parse = parse.split()
    a = len(parse)
    check = False
    for i in range (0, a):
        if text == parse[i]:
            check = True
    con.commit()
    cur.close()
    con.close()
    return check

def questions_count(test_id):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT COUNT(*) FROM questions WHERE test_id={test_id}')
    value = cur.fetchone()[0]
    con.commit()
    cur.close()
    con.close()
    return value

def save_user_answer(user_id, index, text):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM user_answer WHERE user_id={user_id} AND question_id={index};')
    value = cur.fetchall()
    if value == []:
        # cur.execute(f"INSERT INTO questions (test_id, number, question, type, answer) VALUES ({test_id}, {index}, '{question}', {type1}, {answer})")
        sqlite_insert_with_param = f"""INSERT INTO user_answer
                                        (user_id, question_id, user_answer_text)
                                        VALUES (?, ?, ?);"""

        data_tuple = (user_id, index, text)
        cur.execute(sqlite_insert_with_param, data_tuple)
        con.commit()
        cur.close()
        con.close()

    elif value != []:
        print(text)
        sqlite_insert_with_param = f"""UPDATE user_answer
        									SET
        									  user_answer_text = ?
        								WHERE user_id=? AND question_id=?;"""

        data_tuple = (text, user_id, index)
        cur.execute(sqlite_insert_with_param, data_tuple)

        con.commit()
        cur.close()
        con.close()

def give_question_id(test_id, text1):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT id FROM questions WHERE test_id={test_id} AND question="{text1}";')
    value = cur.fetchone()[0]
    con.commit()
    cur.close()
    con.close()
    return int(value)

def give_test_id(text):
    con = sqlite3.connect('Base/sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT id FROM tests WHERE name="{text}";')
    value = cur.fetchone()[0]
    con.commit()
    cur.close()
    con.close()
    return int(value)




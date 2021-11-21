import sqlite3
import json
import re

def give_question_answer(test_id, index):
    con = sqlite3.connect('sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT answer FROM questions WHERE test_id={test_id} AND number = {index};')
    value = cur.fetchone()[0]
    print(value)
    # parse = re.findall('([-+]?\d+)', value)
    parse = value.replace('[', '')
    parse = parse.replace(']', '')
    parse = parse.replace(',', '')
    parse = parse.replace("'", '')
    print(parse)
    parse = parse.split()
    print(parse)
    return parse


def give_text_question(test_id, index):
    con = sqlite3.connect('sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT question FROM questions WHERE test_id={test_id} AND number = {index};')
    check = cur.fetchone()

    value = ""
    if check is not None:
        value = check[0]
    return value

def give_question_type(test_id, index):
    con = sqlite3.connect('sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT type FROM questions WHERE test_id={test_id} AND number = {index};')
    value = cur.fetchone()[0]
    return value

def give_question_variant(question_id, number):
    con = sqlite3.connect('sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT variant FROM variants WHERE question_id={question_id} AND number = {number};')
    value = cur.fetchone()[0]
    return value

def check_true_variant(test_id, index, text):
    con = sqlite3.connect('sm_app.sqlite')
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
    con = sqlite3.connect('sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT COUNT(*) FROM questions WHERE test_id={test_id}')
    value = cur.fetchone()[0]
    con.commit()
    cur.close()
    con.close()
    return value

def give_test_id(text):
    con = sqlite3.connect('sm_app.sqlite')
    cur = con.cursor()
    cur.execute(f'SELECT id FROM tests WHERE name="{text}";')
    value = cur.fetchone()[0]
    con.commit()
    cur.close()
    con.close()
    return int(value)

#text = give_question_answer(44, 1)
text1 = "['q', 'q', '3']"
#mas = json.loads(text1)
#parse = re.findall('([-+]?\d+)', text)
#print(parse[1])

text = give_test_id('Вопросы')
print(text)

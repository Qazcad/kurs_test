from PyQt5 import QtCore, QtGui, QtWidgets
from Base.handler import *

class CheckThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def thr_login(self, name, passw):
        check = login(name, passw, self.mysignal)
        return check

    def thr_register(self, name, passw):
        check = register(name, passw, self.mysignal)
        return check

    def thr_register_test(self, test_name, count, user_id):
        id = register_test(test_name, count, user_id, self.mysignal)
        return id

    def thr_register_question(self, test_id, index, question, type1, answer):
        question_id = register_question(test_id, index, question, answer, type1, self.mysignal)
        return question_id

    def thr_register_variant(self, question_id, index, text):
        register_variant(question_id, index, text)

    def thr_check_question(self, test_id, index):
        check = check_question(test_id, index)
        return check

    def thr_give_text_question(self, test_id, index):
        text = give_text_question(test_id, index)
        return text

    def thr_give_question_type(self, test_id, index):
        type = give_question_type(test_id, index)
        return type

    def thr_give_question_answer(self, test_id, index):
        text = give_question_answer(test_id, index)
        return text

    def thr_give_question_variant(self, question_id, number):
        text = give_question_variant(question_id, number)
        return text

    def thr_check_true_variant(self, test_id, index, text):
        check = check_true_variant(test_id, index, text)
        return check

    def thr_questions_count(self, test_id):
        count = questions_count(test_id)
        return count

    def thr_save_user_answer(self, user_id, index, text):
        save_user_answer(user_id, index, text)

    def thr_give_question_id(self, test_id, text1):
        ide = give_question_id(test_id, text1)
        return ide

    def thr_give_test_id(self, text):
        ide = give_test_id(text)
        return ide
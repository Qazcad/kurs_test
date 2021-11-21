import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from check_db import *
from windows.form import *
from windows.back import *
from windows.test_list import *
from windows.Begin import *
from windows.Question_creator import *
from windows.Do_test import *


class Items:
    user_id = 1
    test_id = 79
    count = 3

help = Items()

class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)



class Interface(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_register.clicked.connect(self.reg)
        self.ui.pushButton_login.clicked.connect(self.auth)
        self.base_line_edit = [self.ui.line_login, self.ui.line_password]

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)


    # Проверка правильности ввода
    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)
        return wrapper


    # Обработчик сигналов
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)


    @check_input
    def auth(self):
        name = self.ui.line_login.text()
        passw = self.ui.line_password.text()
        help.user_id = self.check_db.thr_login(name, passw)
        if help.user_id > 0:
            self.goto("search")


    @check_input
    def reg(self):
        name = self.ui.line_login.text()
        passw = self.ui.line_password.text()
        help.user_id = self.check_db.thr_register(name, passw)
        if help.user_id > 0:
            self.goto("search")


class Back_window(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Back()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.back)

    def back(self):
        self.cams = Interface()
        self.cams.show()
        self.close()


class Test_list(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Test_list()
        self.ui.setupUi(self)

        self.list = self.give_list()

        self.ui.test_list.addItems(self.list)
        self.ui.back.clicked.connect(self.back)
        self.ui.create_test.clicked.connect(self.begin)
        self.ui.begin_test.clicked.connect(self.start_test)

        self.check_db = CheckThread()

    def give_list(self):
        t_list = give_test_list()
        return t_list

    def back(self):
        self.goto("main")

    def begin(self):
        self.goto("begin")

    def start_test(self):
        text = self.ui.test_list.currentText()
        print(text)
        help.test_id = self.check_db.thr_give_test_id(text)
        self.goto('Do')


class Begin(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Begin()
        self.ui.setupUi(self)

        self.m_pages = {}

        self.ui.create.clicked.connect(self.reg)
        self.base_line_edit = [self.ui.test_name, self.ui.test_count]
        self.ui.Back.clicked.connect(self.back)

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)



    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)
        return wrapper


    # Обработчик сигналов
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)

    @check_input
    def reg(self):
        test_name = self.ui.test_name.text()
        count = int(self.ui.test_count.text())
        help.test_id = self.check_db.thr_register_test(test_name, count, help.user_id)
        print(help.test_id)
        help.count = int(self.ui.test_count.text())
        print(help.count)
        if help.test_id > 0:
            self.goto("Question_creator")

    def back(self):
        self.goto("search")

    def go(self):
        help.count = int(self.ui.test_count.text())
        self.goto("Question_creator")


class Question_creator(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Question_creator()
        self.ui.setupUi(self)

        self.q_list = self.counts()


        self.ui.question_number.addItems(self.q_list)
        self.ui.question_number.currentIndexChanged.connect(self.change_question)
        self.ui.change_type.stateChanged.connect(self.change)
        self.ui.save_question.clicked.connect(self.save)
        self.base_box_edit = [self.ui.text_question]
        self.ui.exit.clicked.connect(self.exit)
        #self.ui.question_number.setCurrentIndex(0)

        self.check_db = CheckThread()




    def change_question(self):
        i = self.ui.question_number.currentIndex() + 1
        check = self.check_db.thr_check_question(help.test_id, i)
        if check != 0:
            text1 = self.check_db.thr_give_text_question(help.test_id, i)
            self.ui.text_question.setPlainText(text1)
            question_type = self.check_db.thr_give_question_type(help.test_id, i)
            if question_type == 1:

                self.ui.change_type.setChecked(False)
                """self.ui.answer.setEnabled(True)
                self.ui.change_type.setChecked(False)
                self.ui.variant_1.setEnabled(False)
                self.ui.variant_2.setEnabled(False)
                self.ui.variant_3.setEnabled(False)
                self.ui.variant_4.setEnabled(False)
                self.ui.true_variant_1.setEnabled(False)
                self.ui.true_variant_2.setEnabled(False)
                self.ui.true_variant_3.setEnabled(False)
                self.ui.true_variant_4.setEnabled(False)"""
                self.ui.true_variant_1.setChecked(False)
                self.ui.true_variant_2.setChecked(False)
                self.ui.true_variant_3.setChecked(False)
                self.ui.true_variant_4.setChecked(False)
                self.ui.variant_1.clear()
                self.ui.variant_2.clear()
                self.ui.variant_3.clear()
                self.ui.variant_4.clear()
                text2 = self.check_db.thr_give_question_answer(help.test_id, i)
                text3 = text2[0]
                self.ui.answer.setText(text3)

            elif question_type == 2:
                self.ui.change_type.setChecked(True)
                self.ui.answer.clear()
                """self.ui.change_type.setChecked(True)
                self.ui.answer.setEnabled(False)
                self.ui.variant_1.setEnabled(True)
                self.ui.variant_2.setEnabled(True)
                self.ui.variant_3.setEnabled(True)
                self.ui.variant_4.setEnabled(True)
                self.ui.true_variant_1.setEnabled(True)
                self.ui.true_variant_2.setEnabled(True)
                self.ui.true_variant_3.setEnabled(True)
                self.ui.true_variant_4.setEnabled(True)"""

                text4 = self.check_db.thr_give_question_variant(check,  1)
                self.ui.variant_1.setText(text4)
                check_true = self.check_db.thr_check_true_variant(help.test_id, i, self.ui.variant_1.text())
                if check_true:
                    self.ui.true_variant_1.setChecked(True)
                else:
                    self.ui.true_variant_1.setChecked(False)

                text4 = self.check_db.thr_give_question_variant(check, 2)
                self.ui.variant_2.setText(text4)
                check_true = self.check_db.thr_check_true_variant(help.test_id, i, self.ui.variant_2.text())
                if check_true:
                    self.ui.true_variant_2.setChecked(True)
                else:
                    self.ui.true_variant_2.setChecked(False)

                text4 = self.check_db.thr_give_question_variant(check, 3)
                self.ui.variant_3.setText(text4)
                check_true = self.check_db.thr_check_true_variant(help.test_id, i, self.ui.variant_3.text())
                if check_true:
                    self.ui.true_variant_3.setChecked(True)
                else:
                    self.ui.true_variant_3.setChecked(False)

                text4 = self.check_db.thr_give_question_variant(check, 4)
                self.ui.variant_4.setText(text4)
                check_true = self.check_db.thr_check_true_variant(help.test_id, i, self.ui.variant_4.text())
                if check_true:
                    self.ui.true_variant_4.setChecked(True)
                else:
                    self.ui.true_variant_4.setChecked(False)

        else:
            self.ui.text_question.clear()
            self.ui.answer.clear()
            #self.ui.answer.setEnabled(True)
            self.ui.change_type.setChecked(False)
            self.ui.variant_1.clear()
            #self.ui.variant_1.setEnabled(False)
            self.ui.variant_2.clear()
            #self.ui.variant_2.setEnabled(False)
            #self.ui.variant_3.setEnabled(False)
            self.ui.variant_3.clear()
            #self.ui.variant_4.setEnabled(False)
            self.ui.variant_4.clear()
            self.ui.true_variant_1.setEnabled(False)
            self.ui.true_variant_2.setEnabled(False)
            self.ui.true_variant_3.setEnabled(False)
            self.ui.true_variant_4.setEnabled(False)
            self.ui.true_variant_1.setChecked(False)
            self.ui.true_variant_2.setChecked(False)
            self.ui.true_variant_3.setChecked(False)
            self.ui.true_variant_4.setChecked(False)



    def counts(self):
        count_list = []
        print(help.count)
        b = help.count
        for i in range(1, b + 1):
            a = str(i)
            count_list.append(a)
        print(count_list)
        return count_list



    def change(self):
        check = self.ui.change_type.isChecked()
        print(check)
        if check:
            self.ui.answer.setEnabled(False)
            self.ui.variant_1.setEnabled(True)
            self.ui.variant_2.setEnabled(True)
            self.ui.variant_3.setEnabled(True)
            self.ui.variant_4.setEnabled(True)
            self.ui.true_variant_1.setEnabled(True)
            self.ui.true_variant_2.setEnabled(True)
            self.ui.true_variant_3.setEnabled(True)
            self.ui.true_variant_4.setEnabled(True)
        else:
            self.ui.answer.setEnabled(True)
            self.ui.variant_1.setEnabled(False)
            self.ui.variant_2.setEnabled(False)
            self.ui.variant_3.setEnabled(False)
            self.ui.variant_4.setEnabled(False)
            self.ui.true_variant_1.setEnabled(False)
            self.ui.true_variant_2.setEnabled(False)
            self.ui.true_variant_3.setEnabled(False)
            self.ui.true_variant_4.setEnabled(False)

        """check = self.ui.variant_1.isEnabled()
        if check:
            self.ui.variant_1.setEnabled(False)
            self.ui.variant_2.setEnabled(False)
            self.ui.variant_3.setEnabled(False)
            self.ui.variant_4.setEnabled(False)
            self.ui.true_variant_1.setEnabled(False)
            self.ui.true_variant_2.setEnabled(False)
            self.ui.true_variant_3.setEnabled(False)
            self.ui.true_variant_4.setEnabled(False)
        else:
            self.ui.variant_1.setEnabled(True)
            self.ui.variant_2.setEnabled(True)
            self.ui.variant_3.setEnabled(True)
            self.ui.variant_4.setEnabled(True)
            self.ui.true_variant_1.setEnabled(True)
            self.ui.true_variant_2.setEnabled(True)
            self.ui.true_variant_3.setEnabled(True)
            self.ui.true_variant_4.setEnabled(True)"""


    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_box_edit:
                if len(line_edit.toPlainText()) == 0:
                    return
            funct(self)
        return wrapper


    # Обработчик сигналов
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)

    @check_input
    def save(self):
        index = self.ui.question_number.currentIndex() + 1
        question = self.ui.text_question.toPlainText()
        answer = []
        check_2 = self.ui.answer.isEnabled()
        if check_2:
            answer.append(self.ui.answer.text())
            self.check_db.thr_register_question(help.test_id, index, question, 1, str(answer))
        else:
            check_3 = self.ui.true_variant_1.isChecked()
            if check_3:
                answer.append(self.ui.variant_1.text())
            check_3 = self.ui.true_variant_2.isChecked()
            if check_3:
                answer.append(self.ui.variant_2.text())
            check_3 = self.ui.true_variant_3.isChecked()
            if check_3:
                answer.append(self.ui.variant_3.text())
            check_3 = self.ui.true_variant_4.isChecked()
            if check_3:
                answer.append(self.ui.variant_4.text())
            print(help.test_id)
            print(str(answer))
            question_id = self.check_db.thr_register_question(help.test_id, index, question, 2, str(answer))
            self.check_db.thr_register_variant(question_id, 1, str(self.ui.variant_1.text()))
            self.check_db.thr_register_variant(question_id, 2, str(self.ui.variant_2.text()))
            self.check_db.thr_register_variant(question_id, 3, str(self.ui.variant_3.text()))
            self.check_db.thr_register_variant(question_id, 4, str(self.ui.variant_4.text()))

    def exit(self):
        self.goto("search")


class Do_test(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Do_test()
        self.ui.setupUi(self)

        self.check_db = CheckThread()
        self.q_list = self.counts()

        self.ui.question_count.addItems(self.q_list)
        self.ui.question_count.currentIndexChanged.connect(self.change_question)
        ###self.ui.next.clicked.connect(self.swap)
        self.start()
        self.ui.next.clicked.connect(self.save_answer)
        self.ui.exit.clicked.connect(self.show)
        self.ui.end_test.clicked.connect(self.begin)




    def start(self):
        check = self.check_db.thr_give_text_question(help.test_id, 1)
        if check == "":
            return
        self.ui.question_text.setText(self.check_db.thr_give_text_question(help.test_id, 1))
        check = self.check_db.thr_give_question_type(help.test_id, 1)
        if check == 1:
            self.ui.user_answer.clear()
            self.ui.user_answer.show()
            """text1 = self.check_db.thr_give_question_answer(help.test_id, i)
            self.ui.answer.setText(text1[0])"""
            self.ui.variant_1.clear()
            self.ui.variant_2.clear()
            self.ui.variant_3.clear()
            self.ui.variant_4.clear()
            self.ui.variant_1.hide()
            self.ui.variant_2.hide()
            self.ui.variant_3.hide()
            self.ui.variant_4.hide()
            self.ui.true_1.hide()
            self.ui.true_2.hide()
            self.ui.true_3.hide()
            self.ui.true_4.hide()

        elif check == 2:
            ide = self.check_db.thr_check_question(help.test_id, 1)
            self.ui.user_answer.clear()
            self.ui.user_answer.hide()
            self.ui.variant_1.clear()
            self.ui.variant_2.clear()
            self.ui.variant_3.clear()
            self.ui.variant_4.clear()
            self.ui.variant_1.show()
            self.ui.variant_2.show()
            self.ui.variant_3.show()
            self.ui.variant_4.show()

            text4 = self.check_db.thr_give_question_variant(ide, 1)
            self.ui.variant_1.setText(text4)

            text4 = self.check_db.thr_give_question_variant(ide, 2)
            self.ui.variant_2.setText(text4)

            text4 = self.check_db.thr_give_question_variant(ide, 3)
            self.ui.variant_3.setText(text4)

            text4 = self.check_db.thr_give_question_variant(ide, 4)
            self.ui.variant_4.setText(text4)

            self.ui.true_1.setChecked(False)
            self.ui.true_2.setChecked(False)
            self.ui.true_3.setChecked(False)
            self.ui.true_4.setChecked(False)

            self.ui.true_1.show()
            self.ui.true_2.show()
            self.ui.true_3.show()
            self.ui.true_4.show()


    def counts(self):
        """count_list = []
        print(help.count)
        b = help.count
        for i in range(1, b + 1):
            a = str(i)
            count_list.append(a)
        print(count_list)
        return count_list"""
        count = self.check_db.thr_questions_count(help.test_id)
        count_list = []
        print(count)
        b = count
        for i in range(1, b + 1):
            a = str(i)
            count_list.append(a)
        print(count_list)
        return count_list

    def change_question(self):
        i = self.ui.question_count.currentIndex() + 1
        self.ui.question_text.clear()
        text = self.check_db.thr_give_text_question(help.test_id, i)
        self.ui.question_text.setText(text)
        check = self.check_db.thr_give_question_type(help.test_id, i)
        if check == 1:
            self.ui.user_answer.clear()
            self.ui.user_answer.show()
            """text1 = self.check_db.thr_give_question_answer(help.test_id, i)
            self.ui.answer.setText(text1[0])"""
            self.ui.variant_1.clear()
            self.ui.variant_2.clear()
            self.ui.variant_3.clear()
            self.ui.variant_4.clear()
            self.ui.variant_1.hide()
            self.ui.variant_2.hide()
            self.ui.variant_3.hide()
            self.ui.variant_4.hide()
            self.ui.true_1.hide()
            self.ui.true_2.hide()
            self.ui.true_3.hide()
            self.ui.true_4.hide()

        elif check == 2:
            ide = self.check_db.thr_check_question(help.test_id, i)
            self.ui.user_answer.clear()
            self.ui.user_answer.hide()
            self.ui.variant_1.clear()
            self.ui.variant_2.clear()
            self.ui.variant_3.clear()
            self.ui.variant_4.clear()
            self.ui.variant_1.show()
            self.ui.variant_2.show()
            self.ui.variant_3.show()
            self.ui.variant_4.show()

            text4 = self.check_db.thr_give_question_variant(ide, 1)
            self.ui.variant_1.setText(text4)

            text4 = self.check_db.thr_give_question_variant(ide, 2)
            self.ui.variant_2.setText(text4)

            text4 = self.check_db.thr_give_question_variant(ide, 3)
            self.ui.variant_3.setText(text4)

            text4 = self.check_db.thr_give_question_variant(ide, 4)
            self.ui.variant_4.setText(text4)

            self.ui.true_1.setChecked(False)
            self.ui.true_2.setChecked(False)
            self.ui.true_3.setChecked(False)
            self.ui.true_4.setChecked(False)

            self.ui.true_1.show()
            self.ui.true_2.show()
            self.ui.true_3.show()
            self.ui.true_4.show()

    def save_answer(self):
        i = self.ui.question_count.currentIndex() + 1
        text1 = self.ui.question_text.text()
        ide = self.check_db.thr_give_question_id(help.test_id, text1)
        type1 = self.check_db.thr_give_question_type(help.test_id, i)
        mas = []
        if type1 == 1:
            text = self.ui.user_answer.text()
            if text != '':
                mas.append(text)
                self.check_db.thr_save_user_answer(help.user_id, ide, str(mas))
                print("ok2")
        elif type1 == 2:
            check = self.ui.true_1.isChecked()
            if check:
                text = self.ui.variant_1.text()
                mas.append(text)

            check = self.ui.true_2.isChecked()
            if check:
                text = self.ui.variant_2.text()
                mas.append(text)

            check = self.ui.true_3.isChecked()
            if check:
                text = self.ui.variant_3.text()
                mas.append(text)

            check = self.ui.true_4.isChecked()
            if check:
                text = self.ui.variant_4.text()
                mas.append(text)

            print(str(mas))
            if len(mas) != 0:
                self.check_db.thr_save_user_answer(help.user_id, ide, str(mas))

        print("ok")

    def show(self):
        text = self.ui.question_text.text()
        print(text)
        text = self.ui.user_answer.text()
        print(text)

    def begin(self):
        self.goto("search")













class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(700, 400, 400, 600)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(Interface(), "main")
        self.register(Test_list(), "search")
        self.register(Begin(), "begin")
        self.register(Question_creator(), "Question_creator")
        self.register(Do_test(), "Do")

        self.goto("main")

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        self.register(Interface(), "main")
        self.register(Test_list(), "search")
        self.register(Begin(), "begin")
        self.register(Question_creator(), "Question_creator")
        self.register(Do_test(), "Do")

        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


def change_count(count):
    Question_creator.counts(count)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywin = Window()
    mywin.show()
    sys.exit(app.exec_())


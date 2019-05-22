from main_window import Ui_MainWindow
import sort_station
import recursive_descent
import global_func_val
import sys
import time
import os
import about_program
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QLocale, QTranslator, QLibraryInfo

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = about_program.Ui_Dialog()
        self.ui.setupUi(self)

    def exit(self):
        self.close()


class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Тут сделал более большой шрифт, но можно и уюбрать если что
        tmp = QtGui.QFont(self.ui.lineEdit.font())
        tmp.setPointSize(10)
        self.ui.lineEdit.setFont(tmp)
        self.ui.lineEdit_2.setFont(tmp)
        self.ui.tableWidget.setFont(tmp)

    def translate_button(self):
        start_time_traslate = 0
        end_time_traslate = 0
        global_func_val.input_string = self.ui.lineEdit.text();
        self.ui.textBrowser.setText("")
        self.ui.lineEdit_2.setText("")
        row_count = self.ui.tableWidget.rowCount()
        while (row_count >= 0):
            self.ui.tableWidget.removeRow(row_count)
            row_count -= 1

        if (global_func_val.input_string == ""):
            self.ui.textBrowser.append("Вам необходимо ввести исходное выражение")
        else:
            global_func_val.folding_string = global_func_val.folding(global_func_val.input_string)
            self.ui.textBrowser.append("Упрощаем введенное выражение...")
            self.ui.textBrowser.append("Упрощенное выражение: " +  global_func_val.folding_string)
            global_func_val.infix_string = global_func_val.unary_minus_coding(global_func_val.folding_string)
            self.ui.textBrowser.append("Кодируем унарный минус...")
            self.ui.textBrowser.append("Закодированное выражение: " + global_func_val.infix_string)
            global_func_val.index = 0
            global_func_val.token = ""
            global_func_val.postfix_string = ""
            global_func_val.result_string = ""
            global_func_val.num_brackets = 0
            isOk = global_func_val.string_validation(global_func_val.infix_string)
            if (isOk == None):
                self.ui.textBrowser.append("Переводим в постфиксную запись...")
                global_func_val.index = 0
                global_func_val.token = ""
                global_func_val.postfix_string = ""
                global_func_val.result_string = ""
                global_func_val.num_brackets = 0
                global_func_val.token = global_func_val.get_token(global_func_val.infix_string)
                if (self.ui.radioButton.isChecked()):
                    start_time_traslate = time.time()
                    sort_station.dijkstra_method()
                    end_time_traslate = time.time()
                else:
                    start_time_traslate = time.time()
                    recursive_descent.check_binary_plus_minus()
                    end_time_traslate = time.time()
                self.ui.textBrowser.append("Выражение переведно в постфиксную запись")
                self.ui.textBrowser.append("Для перевода потребовалось: " + str((end_time_traslate - start_time_traslate)*1000000) + " миллисекунд")
                global_func_val.result_string = global_func_val.postfix_string.replace("!", "-")
                self.ui.lineEdit_2.setText(global_func_val.result_string)
            elif (isOk == 0):
                errorMessage = 'Первый токен введен неверно'
                self.ui.textBrowser.append(errorMessage)
            elif (isOk == 1):
                errorMessage = 'Последний токен введен неверно'
                self.ui.textBrowser.append(errorMessage)
            elif (isOk == 2):
                errorMessage =  "Количество '(' не соответсвует количеству ')'"
                self.ui.textBrowser.append(errorMessage)
            elif (isOk == 3):
                errorMessage =  'Неизвестная ошибка'
                self.ui.textBrowser.append(errorMessage)
            else:
                errorMessage = 'После ' + (isOk[0].__str__()) + ' ' + 'с позицей ' + (isOk[1].__str__()) + ' стоит некорректный токен: ' + global_func_val.input_string[0:isOk[1]] + "<font color=\"Red\">" + global_func_val.input_string[isOk[1]:isOk[2]] + "</font>" + global_func_val.input_string[isOk[2]:len(global_func_val.input_string)]
                self.ui.textBrowser.append(errorMessage)

    def exit_button(self):
        sys.exit(app.exec())

    def find_value_button(self):
        if (global_func_val.postfix_string == ""):
            self.ui.textBrowser.setText("")
            self.ui.textBrowser.append("Введите исходное выражение и переведите его в постфиксную форму")
        else:
            row_count = self.ui.tableWidget.rowCount()
            while (row_count >= 0):
                self.ui.tableWidget.removeRow(row_count)
                row_count -= 1
            self.ui.textBrowser.append("Находим значение выражения...")

            start_time_find_value = 0
            end_time_find_value = 0
            row = 0
            stack = []
            global_func_val.index = 0
            tmp_token = global_func_val.get_token(global_func_val.postfix_string)

            start_time_find_value = time.time()

            while tmp_token!= None:
                if global_func_val.isNum(tmp_token):
                    stack.append(tmp_token)
                    data = []
                    data.append(QtWidgets.QTableWidgetItem(tmp_token))
                    data[0].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem("поместить в вершину стека"))
                    data[1].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem(
                        stack.__str__().replace("'", "").replace(",", "   ").replace("[", "").replace("]", "")))
                    data[2].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.insertRow(row)
                    for i in range(3):
                        self.ui.tableWidget.setItem(row, i, data[i])
                    row += 1
                elif (tmp_token == "!"):
                    tmp_val_1 = stack.pop()
                    tmp_val_1 = round((float(tmp_val_1) * -1),4)
                    stack.append(tmp_val_1)
                    data = []
                    data.append(QtWidgets.QTableWidgetItem("-"))
                    data[0].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem("сменить знак первого операнда в вершине стека"))
                    data[1].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem(
                        stack.__str__().replace("'", "").replace(",", "   ").replace("[", "").replace("]", "")))
                    data[2].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.insertRow(row)
                    for i in range(3):
                        self.ui.tableWidget.setItem(row, i, data[i])
                    row += 1
                elif (tmp_token == "+"):
                    tmp_val_2 = stack.pop()
                    tmp_val_1 = stack.pop()
                    stack.append(round((float(tmp_val_1) + float(tmp_val_2)), 4))
                    data = []
                    data.append(QtWidgets.QTableWidgetItem(tmp_token))
                    data[0].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem("сложение двух первых операндов в вершине стека"))
                    data[1].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem(
                        stack.__str__().replace("'", "").replace(",", "   ").replace("[", "").replace("]", "")))
                    data[2].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.insertRow(row)
                    for i in range(3):
                        self.ui.tableWidget.setItem(row, i, data[i])
                    row += 1
                elif (tmp_token == "-"):
                    tmp_val_2 = stack.pop()
                    tmp_val_1 = stack.pop()
                    stack.append(round((float(tmp_val_1) - float(tmp_val_2)), 4))
                    data = []
                    data.append(QtWidgets.QTableWidgetItem(tmp_token))
                    data[0].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem("вычитание двух первых операндов в вершине стека"))
                    data[1].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem(
                        stack.__str__().replace("'", "").replace(",", "   ").replace("[", "").replace("]", "")))
                    data[2].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.insertRow(row)
                    for i in range(3):
                        self.ui.tableWidget.setItem(row, i, data[i])
                    row += 1
                elif (tmp_token == "*"):
                    tmp_val_2 = stack.pop()
                    tmp_val_1 = stack.pop()
                    stack.append(round((float(tmp_val_1) * float(tmp_val_2)), 4))
                    data = []
                    data.append(QtWidgets.QTableWidgetItem(tmp_token))
                    data[0].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem("умножение двух первых операндов в вершине стека"))
                    data[1].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem(
                        stack.__str__().replace("'", "").replace(",", "   ").replace("[", "").replace("]", "")))
                    data[2].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.insertRow(row)
                    for i in range(3):
                        self.ui.tableWidget.setItem(row, i, data[i])
                    row += 1
                elif (tmp_token == "/"):
                    tmp_val_2 = stack.pop()
                    tmp_val_1 = stack.pop()
                    stack.append(round((float(tmp_val_1) / float(tmp_val_2)), 4))
                    data = []
                    data.append(QtWidgets.QTableWidgetItem(tmp_token))
                    data[0].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem("деление двух первых операндов в вершине стека"))
                    data[1].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    data.append(QtWidgets.QTableWidgetItem(
                        stack.__str__().replace("'", "").replace(",", "   ").replace("[", "").replace("]", "")))
                    data[2].setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.ui.tableWidget.insertRow(row)
                    for i in range(3):
                        self.ui.tableWidget.setItem(row, i, data[i])
                    row += 1
                tmp_token = global_func_val.get_token(global_func_val.postfix_string)

            end_time_find_value = time.time()

            self.ui.textBrowser.append("Значение выражения = " + str(stack.pop()))
            self.ui.textBrowser.append("Для решения потребовалось: " + str((end_time_find_value - start_time_find_value) * 1000) + " миллисекунд")

    def info(self):
        self.dialog = Dialog()
        self.dialog.exec_()

    def help(self):
        try:
            os.startfile(r'help.chm')
        except Exception:
            self.ui.textBrowser.setText("Файл справки не был найден")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()

    sys.exit(app.exec())
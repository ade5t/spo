from main_window import Ui_MainWindow
import sort_station
import recursive_descent
import global_func_val
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def translate_button(self):
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
                    sort_station.dijkstra_method()
                else:
                    recursive_descent.check_binary_plus_minus()
                self.ui.textBrowser.append("Выражение переведно в постфиксную запись")
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
        stack = []
        row_count = self.ui.tableWidget.rowCount()
        while (row_count >= 0):
            self.ui.tableWidget.removeRow(row_count)
            row_count -= 1
#             сюда вычисление postfix_string через get_token и стек.



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()

    sys.exit(app.exec())
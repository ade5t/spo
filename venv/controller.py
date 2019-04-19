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
        if (global_func_val.input_string == ""):
            self.ui.textBrowser.append("Вам необходимо ввести исходное выражение")
        else:
            global_func_val.folding_string = global_func_val.folding(global_func_val.input_string)
            self.ui.textBrowser.append("Упрощаем введенное выражение...")
            self.ui.textBrowser.append("Упрощенное выражение: " +  global_func_val.folding_string)
            global_func_val.infix_string = global_func_val.unary_minus_coding(global_func_val.folding_string)
            self.ui.textBrowser.append("Кодируем унарный минус...")
            self.ui.textBrowser.append("Закодированное выражение: " + global_func_val.infix_string)
            isOk = global_func_val.string_validation(global_func_val.infix_string)
            if (isOk == None):
                self.ui.textBrowser.append("Переводим в постфиксную запись...")
                global_func_val.index = 0
                global_func_val.token = ""
                global_func_val.num_brackets = 0
                global_func_val.token = global_func_val.get_token()
                if (self.ui.radioButton.isChecked()):
                    sort_station.dijkstra_method()
                else:
                    recursive_descent.check_binary_plus_minus()
                global_func_val.result_string = global_func_val.postfix_string.replace("!", "-")
                self.ui.lineEdit_2.setText(global_func_val.result_string)
            else:

                self.ui.textBrowser.append("Ошибка(")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()

    sys.exit(app.exec())
import global_func_val
# Преобразование выражения из инфиксной записи в постфиксную
# методом рекурсивного спуска. Унарный минус записывается как в
# скобках, так и без них. Изначально производится сворачивание
# знаков "минус", а также замена унарного минуса на "!"

# Функция, проверяющая бинарные "+", "-"
# Вход -
# Выход -
def check_binary_plus_minus():
    check_binary_mul_div()
    while (global_func_val.token == "+" or global_func_val.token == "-"):
        tmp_token = global_func_val.token
        global_func_val.token = global_func_val.get_token()
        check_binary_mul_div()
        global_func_val.postfix_string += tmp_token + " "

# Функция, проверяющая бинарные "*", "/"
# Вход -
# Выход -
def check_binary_mul_div():
    check_unary_minus()
    while (global_func_val.token == "*" or global_func_val.token == "/"):
        tmp_token = global_func_val.token
        global_func_val.token = global_func_val.get_token()
        check_unary_minus()
        global_func_val.postfix_string += tmp_token + " "

# Функция, проверяющая унарный "-"
# Вход -
# Выход -
def check_unary_minus():
    check_brackets()
    while (global_func_val.token == "!"):
        tmp_token = global_func_val.token
        global_func_val.token = global_func_val.get_token()
        check_brackets()
        global_func_val.postfix_string += tmp_token + " "

# Функция, проверяющая "(", ")"
# Вход -/
# Выход -
def check_brackets():
    if (global_func_val.token == "("):
        global_func_val.token = global_func_val.get_token()
        check_binary_plus_minus()
        if (global_func_val.token != ")"):
            print("Неизвестная ошибка со скобками")
        else:
            global_func_val.token = global_func_val.get_token()
    else:
        check_number()

# Функция, проверяющая числа
# Вход -
# Выход -
def check_number():
    if global_func_val.isNum(global_func_val.token):
        global_func_val.postfix_string += global_func_val.token + " "
        global_func_val.token = global_func_val.get_token()

# if __name__ == '__main__':
#     global_func_val.input_string = input()
#     if (global_func_val.input_string == ""):
#         print("Строка пуста")
#     else:
#         global_func_val.folding_string = global_func_val.folding(global_func_val.input_string)
#         global_func_val.infix_string = global_func_val.unary_minus_coding(global_func_val.folding_string)
#         isOk = global_func_val.string_validation(global_func_val.infix_string)
#         if (isOk == None):
#             global_func_val.index = 0
#             global_func_val.token = ""
#             global_func_val.num_brackets = 0
#             global_func_val.token = global_func_val.get_token()
#             check_binary_plus_minus()
#             global_func_val.result_string = global_func_val.postfix_string.replace("!", "-")
#             print(global_func_val.postfix_string)
#         else:
#             print(isOk)
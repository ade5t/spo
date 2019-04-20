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
        global_func_val.token = global_func_val.get_token(global_func_val.infix_string)
        check_binary_mul_div()
        global_func_val.postfix_string += tmp_token + " "

# Функция, проверяющая бинарные "*", "/"
# Вход -
# Выход -
def check_binary_mul_div():
    check_unary_minus()
    while (global_func_val.token == "*" or global_func_val.token == "/"):
        tmp_token = global_func_val.token
        global_func_val.token = global_func_val.get_token(global_func_val.infix_string)
        check_unary_minus()
        global_func_val.postfix_string += tmp_token + " "

# Функция, проверяющая унарный "-"
# Вход -
# Выход -
def check_unary_minus():
    check_brackets()
    while (global_func_val.token == "!"):
        tmp_token = global_func_val.token
        global_func_val.token = global_func_val.get_token(global_func_val.infix_string)
        check_brackets()
        global_func_val.postfix_string += tmp_token + " "

# Функция, проверяющая "(", ")"
# Вход -/
# Выход -
def check_brackets():
    if (global_func_val.token == "("):
        global_func_val.token = global_func_val.get_token(global_func_val.infix_string)
        check_binary_plus_minus()
        if (global_func_val.token != ")"):
            print("Неизвестная ошибка со скобками")
        else:
            global_func_val.token = global_func_val.get_token(global_func_val.infix_string)
    else:
        check_number()

# Функция, проверяющая числа
# Вход -
# Выход -
def check_number():
    if global_func_val.isNum(global_func_val.token):
        global_func_val.postfix_string += global_func_val.token + " "
        global_func_val.token = global_func_val.get_token(global_func_val.infix_string)

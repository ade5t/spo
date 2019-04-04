import global_variables
# Преобразование выражения из инфиксной записи в постфиксную
# методом рекурсивного спуска. Унарный минус записывается как в
# скобках, так и без них. Изначально производится сворачивание
# знаков "минус", а также замена унарного минуса на "!"

# Функция, проверяющая является ли подстрока вещественным числом
# Вход - подстрока, содержащая предположительно число
# Выход - true - подстрока содержит вещественное число, иначе false
def isNum(str):
    index = 0
    point = False
    num1 = False
    num2 = False
    while index < len(str):
         if point:
             if str[index].isnumeric():
                 num2 = True
                 index += 1
             else:
                 return False
         else:
             if str[index].isnumeric():
                 num1 = True
                 index += 1
             else:
                 if (str[index] == "."):
                    point = True
                    index += 1
                 else:
                     return False
    if ((num1 and not point) or (num1 and point and num2)):
        return True
    else:
        return False

# Функция, которая сворачивает группу последовательных знаков "-"
# Вход - исходная строка в инфиксной форме
# Выход - свернутая строка в инфиксной форме
def folding(str):
    index = 0
    prev_index = 0
    while index < len(str):
        tmp_str = ""
        num_min = 0
        if (str[index] == "-"):
            prev_index = index
            while (index < len(str) and str[index] == "-"):
                num_min +=1
                index +=1
            if (num_min % 2 == 0 and num_min > 1):
                tmp_str += str[0: prev_index]
                if (len(tmp_str) > 0 and ((tmp_str[len(tmp_str)-1]).isnumeric() or tmp_str[len(tmp_str)-1] == ")")): tmp_str += "+"
                tmp_str += str[index: len(str)]
                str = tmp_str
                index = prev_index
            else:
                tmp_str += str[0: prev_index]
                tmp_str += "-"
                tmp_str += str[index: len(str)]
                str = tmp_str
                index = prev_index
        index += 1
    return str


# Функция, которая заменяет унарный минус символом "!", чтобы унарный
# и бинарный минус кодировались различным образом
# У унарного минуса после сворачивания справа всегда число либо "(", а слева
# всегда НЕ число
# Вход - свернутая строка в инфиксной форме
# Выход - свернутая строка в инфиксной форме с закодированным унарным минусом
def unary_minus_coding(str):
    index = len(str)-1
    while index >= 0:
        tmp_str = ""
        if (str[index] == "-" and (str[index+1] == "(" or (str[index+1]).isnumeric()) and (index == 0 or not (str[index-1]).isnumeric())):
            tmp_str += str[0: index]
            tmp_str += "!"
            tmp_str += str[index+1: len(str)]
            str = tmp_str
        index -= 1
    return str

# Фукнция, считывающая очередную лексему для анализа
# Вход -
# Выход - лексема: либо число, либо знак операции
def get_token():
    tmp_str = ""
    if (global_variables.index < len(global_variables.infix_string)):
        if (global_variables.infix_string[global_variables.index] == "+"):
            global_variables.index += 1
            return global_variables.infix_string[global_variables.index-1]
        elif (global_variables.infix_string[global_variables.index] == "-"):
            global_variables.index += 1
            return global_variables.infix_string[global_variables.index-1]
        elif (global_variables.infix_string[global_variables.index] == "*"):
            global_variables.index += 1
            return global_variables.infix_string[global_variables.index-1]
        elif (global_variables.infix_string[global_variables.index] == "/"):
            global_variables.index += 1
            return global_variables.infix_string[global_variables.index-1]
        elif (global_variables.infix_string[global_variables.index] == "("):
            global_variables.index += 1
            return global_variables.infix_string[global_variables.index-1]
        elif (global_variables.infix_string[global_variables.index] == ")"):
            global_variables.index += 1
            return global_variables.infix_string[global_variables.index-1]
        elif (global_variables.infix_string[global_variables.index] == "!"):
            global_variables.index += 1
            return global_variables.infix_string[global_variables.index-1]
        else:
            while (global_variables.index < len(global_variables.infix_string) and not (global_variables.infix_string[global_variables.index] in global_variables.math_op)):
                tmp_str += global_variables.infix_string[global_variables.index]
                global_variables.index += 1
            return tmp_str

# Функция, проверяющая бинарные "+", "-"
# Вход -
# Выход -
def check_binary_plus_minus():
    check_binary_mul_div()
    while (global_variables.token == "+" or global_variables.token == "-"):
        tmp_token = global_variables.token
        global_variables.token = get_token()
        check_binary_mul_div()
        global_variables.postfix_string += tmp_token

# Функция, проверяющая бинарные "*", "/"
# Вход -
# Выход -
def check_binary_mul_div():
    check_unary_minus()
    while (global_variables.token == "*" or global_variables.token == "/"):
        tmp_token = global_variables.token
        global_variables.token = get_token()
        check_unary_minus()
        global_variables.postfix_string += tmp_token

# Функция, проверяющая унарный "-"
# Вход -
# Выход -
def check_unary_minus():
    check_brackets()
    while (global_variables.token == "!"):
        tmp_token = global_variables.token
        global_variables.token = get_token()
        check_brackets()
        global_variables.postfix_string += tmp_token

# Функция, проверяющая "(", ")"
# Вход -
# Выход -
def check_brackets():
    if (global_variables.token == "("):
        global_variables.num_brackets += 1
        global_variables.token = get_token()
        check_binary_plus_minus()
        if (global_variables.token != ")"):
            print("В скобках дичь")
        else:
            global_variables.num_brackets -= 1
            global_variables.token = get_token()
            if (global_variables.num_brackets == 0 and global_variables.token == ")"):
                print("В скобках дичь")
    else:
        check_number()

# Функция, проверяющая числа
# Вход -
# Выход -
def check_number():
    if isNum(global_variables.token):
        global_variables.postfix_string += global_variables.token
        global_variables.token = get_token()

if __name__ == '__main__':
    #Временная дичь для проверки
    global_variables.input_string = input()
    global_variables.folding_string = folding(global_variables.input_string)
    global_variables.infix_string = unary_minus_coding(global_variables.folding_string)
    global_variables.token = get_token()
    check_binary_plus_minus()
    print(global_variables.postfix_string)
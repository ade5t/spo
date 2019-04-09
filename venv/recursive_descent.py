import global_variables
# Преобразование выражения из инфиксной записи в постфиксную
# методом рекурсивного спуска. Унарный минус записывается как в
# скобках, так и без них. Изначально производится сворачивание
# знаков "минус", а также замена унарного минуса на "!"

# Функция проверки свернутой и закодированной инфиксной строки
# на правильность
# Вход - свернутая и закодированная инфиксная строка
# Выход - строка с причиной ошибки или пустая строка
def string_validation(str):
    state = ""
    prev_position = 0
    tmp_num_brackets = 0
    tmp_math_op = {'+', '-', '*', '/'}
    if (not str[0] in {'(', '!'} and not str[0].isnumeric()):
        return "Первый токен введен неверно"
    if (str[len(str)-1] != ")" and not str[len(str)-1].isnumeric()):
        return "Последний токен введен неверно"
    elif(str[len(str)-1] == ")"):
        tmp_num_brackets -= 1
    state = get_token()
    tmp_token = get_token()
    while (tmp_token != None):
        if (state == "!"):
            if (tmp_token == "(" or isNum(tmp_token)):
                prev_position = global_variables.index
                state = tmp_token
                tmp_token = get_token()
            else:
                return ' '.join(i.__str__() for i in ('После' ' - ' 'с позицей ', prev_position, ' стоит некорректный токен'))
        elif (state == "("):
            if (tmp_token == "(" or tmp_token == "!" or isNum(tmp_token)):
                prev_position = global_variables.index
                state = tmp_token
                tmp_token = get_token()
                tmp_num_brackets += 1
            else:
                return ' '.join(i.__str__() for i in ('После' ' ( ' 'с позицей ', prev_position, ' стоит некорректный токен'))
        elif (state == ")"):
            if (tmp_token == ")" or tmp_token in tmp_math_op):
                prev_position = global_variables.index
                state = tmp_token
                tmp_token = get_token()
                tmp_num_brackets -= 1
            else:
                return ' '.join(i.__str__() for i in ('После' ' ) ' 'с позицей ', prev_position, ' стоит некорректный токен'))
        elif (state in tmp_math_op):
            if (tmp_token == "(" or tmp_token == "!" or isNum(tmp_token)):
                prev_position = global_variables.index
                state = tmp_token
                tmp_token = get_token()
            else:
                return ' '.join(i.__str__() for i in ('После', state, 'с позицей ', prev_position, ' стоит некорректный токен'))
        elif (isNum(state)):
            if (tmp_token in tmp_math_op or tmp_token == ")"):
                prev_position = global_variables.index
                state = tmp_token
                tmp_token = get_token()
            else:
                return ' '.join(i.__str__() for i in ('После', state, 'с позицей ', prev_position, ' стоит некорректный токен'))
        else:
            return 'Неизвестная ошибка'
    if (tmp_num_brackets != 0):
        return "Количество '(' не соответсвует количеству ')'"

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
# всегда НЕ число.
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
# Вход -/
# Выход -
def check_brackets():
    if (global_variables.token == "("):
        global_variables.token = get_token()
        check_binary_plus_minus()
        if (global_variables.token != ")"):
            print("В скобках дичь рекурсия")
        else:
            global_variables.token = get_token()
    else:
        check_number()

# Функция, проверяющая числа
# Вход -
# Выход -
def check_number():
    if isNum(global_variables.token):
        global_variables.postfix_string += global_variables.token
        global_variables.token = get_token()
    else:
        if (global_variables.token != "!" and global_variables.token != "(" and global_variables.index == len(global_variables.infix_string)):
            print("В первом токене дичь рекурсия")
        elif (len(global_variables.token) > 1):
            print("В операнде дичь рекурсия")

if __name__ == '__main__':
    #Временная дичь для проверки
    global_variables.input_string = input()
    if (global_variables.input_string == ""):
        print("Строка пуста")
    else:
        global_variables.folding_string = folding(global_variables.input_string)
        global_variables.infix_string = unary_minus_coding(global_variables.folding_string)
        isOk = string_validation(global_variables.infix_string)
        if ( isOk == ""):
            global_variables.token = get_token()
            check_binary_plus_minus()
            global_variables.result_string = global_variables.postfix_string.replace("!", "-")
            print(global_variables.postfix_string)
        else:
            print(isOk)

    # Это реализация стека для следущего способа
    # kek = []
    # kek.append(0)
    # kek.append(1)
    # kek.append(2)
    # print(kek)
    # print("вытащил ", kek.pop())
    # print(kek)
    # print("вытащил ", kek.pop())
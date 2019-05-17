# Глобальные переменные
math_op = {'+', '-', '*', '/', '(', ')', '!'}
index = 0
token = ""
input_string = ""
folding_string = ""
infix_string = ""
postfix_string = ""
result_string = ""
num_brackets = 0

# Функция проверки свернутой и закодированной инфиксной строки
# на правильность
# Вход - свернутая и закодированная инфиксная строка
# Выход - строка с причиной ошибки или пустая строка
def string_validation(str):
    global index

    state = ""
    prev_position = 0
    tmp_num_brackets = 0
    tmp_math_op = {'+', '-', '*', '/'}
    if (not str[0] in {'(', '!'} and not str[0].isnumeric()):
        return 0
    elif (str[len(str)-1] != ")" and not str[len(str)-1].isnumeric()):
        return 1
    elif(str[len(str)-1] == ")"):
        tmp_num_brackets -= 1

    state = get_token(infix_string)
    tmp_token = get_token(infix_string)
    while (tmp_token != None):
        if (state == "!"):
            if (tmp_token == "(" or isNum(tmp_token)):
                prev_position = index
                state = tmp_token
                tmp_token = get_token(infix_string)
            else:
                if (prev_position == 0):
                    tmp_str = str[prev_position: prev_position + 2]
                    tmp_pos_error_1 = input_string.find(tmp_str.replace("!", "-"), prev_position, len(input_string))
                else:
                    tmp_str = str[prev_position - 1: prev_position + 2]
                    tmp_pos_error_1 = input_string.find(tmp_str.replace("!", "-"), prev_position - 1, len(input_string))
                index = tmp_pos_error_1
                tmp_str = get_token(input_string)
                tmp_str = get_token(input_string)
                tmp_pos_error_2 = index
                return (state.replace("!", "-"), tmp_pos_error_1, tmp_pos_error_2)
        elif (state == "("):
            if (tmp_token == "(" or tmp_token == "!" or isNum(tmp_token)):
                prev_position = index
                state = tmp_token
                tmp_token = get_token(infix_string)
                tmp_num_brackets += 1
            else:
                tmp_str = str[prev_position - 1: prev_position + 2]
                tmp_pos_error_1 = input_string.find(tmp_str.replace("!", "-"), prev_position - 1, len(input_string))
                index = tmp_pos_error_1
                tmp_str = get_token(input_string)
                tmp_str = get_token(input_string)
                tmp_pos_error_2 = index
                return (state.replace("!", "-"), tmp_pos_error_1, tmp_pos_error_2)
        elif (state == ")"):
            if (tmp_token == ")" or tmp_token in tmp_math_op):
                prev_position = index
                state = tmp_token
                tmp_token = get_token(infix_string)
                tmp_num_brackets -= 1
            else:
                tmp_str = str[prev_position - 1: prev_position + 2]
                tmp_pos_error_1 = input_string.find(tmp_str.replace("!", "-"), prev_position - 1, len(input_string))
                index = tmp_pos_error_1
                tmp_str = get_token(input_string)
                tmp_str = get_token(input_string)
                tmp_pos_error_2 = index
                return (state.replace("!", "-"), tmp_pos_error_1, tmp_pos_error_2)
        elif (state in tmp_math_op):
            if (tmp_token == "(" or tmp_token == "!" or isNum(tmp_token)):
                prev_position = index
                state = tmp_token
                tmp_token = get_token(infix_string)
            else:
                tmp_str = str[prev_position - 1: prev_position + 2]
                tmp_pos_error_1 = input_string.find(tmp_str.replace("!", "-"), prev_position - 1, len(input_string))
                index = tmp_pos_error_1
                tmp_str = get_token(input_string)
                tmp_str = get_token(input_string)
                tmp_pos_error_2 = index
                return (state.replace("!", "-"), tmp_pos_error_1, tmp_pos_error_2)
        elif (isNum(state)):
            if (tmp_token in tmp_math_op or tmp_token == ")"):
                prev_position = index
                state = tmp_token
                tmp_token = get_token(infix_string)
            else:
                tmp_str = str[prev_position - 1: prev_position + 2]
                tmp_pos_error_1 = input_string.find(tmp_str.replace("!", "-"), prev_position - 1, len(input_string))
                index = tmp_pos_error_1
                tmp_str = get_token(input_string)
                tmp_str = get_token(input_string)
                tmp_pos_error_2 = index
                return (state.replace("!", "-"), tmp_pos_error_1, tmp_pos_error_2)
        else:
            return 3
    if (tmp_num_brackets != 0):
        return 2

# Функция, проверяющая является ли подстрока вещественным числом
# Вход - подстрока, содержащая предположительно число
# Выход - true - подстрока содержит вещественное число, иначе false
def isNum(str):
    tmp_index = 0
    point = False
    num1 = False
    num2 = False

    while tmp_index < len(str):
         if point:
             if str[tmp_index].isnumeric():
                 num2 = True
                 tmp_index += 1
             else:
                 return False
         else:
             if str[tmp_index].isnumeric():
                 num1 = True
                 tmp_index += 1
             else:
                 if (str[tmp_index] == "."):
                    point = True
                    tmp_index += 1
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
    tmp_index = 0
    prev_tmp_index = 0
    while tmp_index < len(str):
        tmp_str = ""
        num_min = 0
        if (str[tmp_index] == "-"):
            prev_tmp_index = tmp_index
            while (tmp_index < len(str) and str[tmp_index] == "-"):
                num_min +=1
                tmp_index +=1
            if (num_min % 2 == 0 and num_min > 1):
                tmp_str += str[0: prev_tmp_index]
                if (len(tmp_str) > 0 and ((tmp_str[len(tmp_str)-1]).isnumeric() or tmp_str[len(tmp_str)-1] == ")")): tmp_str += "+"
                tmp_str += str[tmp_index: len(str)]
                str = tmp_str
                tmp_index = prev_tmp_index
            else:
                tmp_str += str[0: prev_tmp_index]
                tmp_str += "-"
                tmp_str += str[tmp_index: len(str)]
                str = tmp_str
                tmp_index = prev_tmp_index
        tmp_index += 1
    return str

# Функция, которая заменяет унарный минус символом "!", чтобы унарный
# и бинарный минус кодировались различным образом
# У унарного минуса после сворачивания справа всегда число либо "(", а слева
# всегда НЕ число.
# Вход - свернутая строка в инфиксной форме
# Выход - свернутая строка в инфиксной форме с закодированным унарным минусом
def unary_minus_coding(str):
    if (not str[len(str)-1] == "-"):
        tmp_index = len(str)-1
        while tmp_index >= 0:
            tmp_str = ""
            # (str[tmp_index] == "-" and (str[tmp_index + 1] == "(" or (str[tmp_index + 1]).isnumeric()) and (tmp_index == 0 or not (str[tmp_index - 1]).isnumeric())):
            if ((str[tmp_index] == "-") and ((tmp_index == 0 and str[tmp_index+1].isnumeric()) or (str[tmp_index+1] == "(") or (str[tmp_index+1].isnumeric() and not str[tmp_index-1].isnumeric() and str[tmp_index-1] != ")"))):
                tmp_str += str[0: tmp_index]
                tmp_str += "!"
                tmp_str += str[tmp_index+1: len(str)]
                str = tmp_str
            tmp_index -= 1
    return str

# Фукнция, считывающая очередную лексему для анализа
# Вход -
# Выход - лексема: либо число, либо знак операции
def get_token(str):
    global math_op
    global infix_string
    global index

    tmp_str = ""
    if (index < len(str)):
        if (str[index] == "+"):
            index += 1
            return str[index-1]
        elif (str[index] == "-"):
            index += 1
            return str[index-1]
        elif (str[index] == "*"):
            index += 1
            return str[index-1]
        elif (str[index] == "/"):
            index += 1
            return str[index-1]
        elif (str[index] == "("):
            index += 1
            return str[index-1]
        elif (str[index] == ")"):
            index += 1
            return str[index-1]
        elif (str[index] == "!"):
            index += 1
            return str[index-1]
        else:
            while (index < len(str) and not (str[index] in math_op) and str[index] != " "):
                tmp_str += str[index]
                index += 1
            if (index < len(str) and str[index] == " "):
                index += 1
            return tmp_str
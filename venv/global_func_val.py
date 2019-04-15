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
        return "Первый токен введен неверно"
    elif (str[len(str)-1] != ")" and not str[len(str)-1].isnumeric()):
        return "Последний токен введен неверно"
    elif(str[len(str)-1] == ")"):
        tmp_num_brackets -= 1

    state = get_token()
    tmp_token = get_token()
    while (tmp_token != None):
        if (state == "!"):
            if (tmp_token == "(" or isNum(tmp_token)):
                prev_position = index
                state = tmp_token
                tmp_token = get_token()
            else:
                return ' '.join(i.__str__() for i in ('После' ' - ' 'с позицей ', prev_position, ' стоит некорректный токен'))
        elif (state == "("):
            if (tmp_token == "(" or tmp_token == "!" or isNum(tmp_token)):
                prev_position = index
                state = tmp_token
                tmp_token = get_token()
                tmp_num_brackets += 1
            else:
                return ' '.join(i.__str__() for i in ('После' ' ( ' 'с позицей ', prev_position, ' стоит некорректный токен'))
        elif (state == ")"):
            if (tmp_token == ")" or tmp_token in tmp_math_op):
                prev_position = index
                state = tmp_token
                tmp_token = get_token()
                tmp_num_brackets -= 1
            else:
                return ' '.join(i.__str__() for i in ('После' ' ) ' 'с позицей ', prev_position, ' стоит некорректный токен'))
        elif (state in tmp_math_op):
            if (tmp_token == "(" or tmp_token == "!" or isNum(tmp_token)):
                prev_position = index
                state = tmp_token
                tmp_token = get_token()
            else:
                return ' '.join(i.__str__() for i in ('После', state, 'с позицей ', prev_position, ' стоит некорректный токен'))
        elif (isNum(state)):
            if (tmp_token in tmp_math_op or tmp_token == ")"):
                prev_position = index
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
    tmp_index = len(str)-1
    while tmp_index >= 0:
        tmp_str = ""
        if (str[tmp_index] == "-" and (str[tmp_index+1] == "(" or (str[tmp_index+1]).isnumeric()) and (tmp_index == 0 or not (str[tmp_index-1]).isnumeric())):
            tmp_str += str[0: tmp_index]
            tmp_str += "!"
            tmp_str += str[tmp_index+1: len(str)]
            str = tmp_str
        tmp_index -= 1
    return str

# Фукнция, считывающая очередную лексему для анализа
# Вход -
# Выход - лексема: либо число, либо знак операции
def get_token():
    global math_op
    global infix_string
    global index

    tmp_str = ""
    if (index < len(infix_string)):
        if (infix_string[index] == "+"):
            index += 1
            return infix_string[index-1]
        elif (infix_string[index] == "-"):
            index += 1
            return infix_string[index-1]
        elif (infix_string[index] == "*"):
            index += 1
            return infix_string[index-1]
        elif (infix_string[index] == "/"):
            index += 1
            return infix_string[index-1]
        elif (infix_string[index] == "("):
            index += 1
            return infix_string[index-1]
        elif (infix_string[index] == ")"):
            index += 1
            return infix_string[index-1]
        elif (infix_string[index] == "!"):
            index += 1
            return infix_string[index-1]
        else:
            while (index < len(infix_string) and not (infix_string[index] in math_op)):
                tmp_str += infix_string[index]
                index += 1
            return tmp_str
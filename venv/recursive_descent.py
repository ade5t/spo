# Преобразование выражения из инфиксной записи в постфиксную
# методом рекурсивного спуска. Унарный минус записывается как в
# скобках, так и без них. Изначально производится сворачивание
# знаков "минус", а также замена унарного минуса на "!"

# Глобальные переменные
math_op = {'+', '-', '*', '/', '(', ')', '!'}
index = 0
token = ""
input_string = ""
folding_string = ""
infix_string = ""
postfix_string = ""
result = ""
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

# Функция, проверяющая бинарные "+", "-"
# Вход -
# Выход -
def check_binary_plus_minus():
    global token
    global postfix_string

    check_binary_mul_div()
    while (token == "+" or token == "-"):
        tmp_token = token
        token = get_token()
        check_binary_mul_div()
        postfix_string += tmp_token

# Функция, проверяющая бинарные "*", "/"
# Вход -
# Выход -
def check_binary_mul_div():
    global token
    global postfix_string

    check_unary_minus()
    while (token == "*" or token == "/"):
        tmp_token = token
        token = get_token()
        check_unary_minus()
        postfix_string += tmp_token

# Функция, проверяющая унарный "-"
# Вход -
# Выход -
def check_unary_minus():
    global token
    global postfix_string

    check_brackets()
    while (token == "!"):
        tmp_token = token
        token = get_token()
        check_brackets()
        postfix_string += tmp_token

# Функция, проверяющая "(", ")"
# Вход -/
# Выход -
def check_brackets():
    global token

    if (token == "("):
        token = get_token()
        check_binary_plus_minus()
        if (token != ")"):
            print("В скобках дичь рекурсия")
        else:
            token = get_token()
    else:
        check_number()

# Функция, проверяющая числа
# Вход -
# Выход -
def check_number():
    global token
    global postfix_string
    global infix_string
    global index

    if isNum(token):
        postfix_string += token
        token = get_token()
    else:
        if (token != "!" and token != "(" and index == len(infix_string)):
            print("В первом токене дичь рекурсия")
        elif (len(token) > 1):
            print("В операнде дичь рекурсия")

if __name__ == '__main__':
    input_string = input()
    if (input_string == ""):
        print("Строка пуста")
    else:
        folding_string = folding(input_string)
        infix_string = unary_minus_coding(folding_string)
        isOk = string_validation(infix_string)
        if (isOk == None):
            index = 0
            token = ""
            num_brackets = 0
            token = get_token()
            check_binary_plus_minus()
            result_string = postfix_string.replace("!", "-")
            print(postfix_string)
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
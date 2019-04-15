import global_func_val

#Глобальные переменные
stack = []

def kek():
    global stack
    while global_func_val.token != None:
        if (global_func_val.isNum(global_func_val.token)):
            global_func_val.postfix_string += global_func_val.token + " "
        elif (global_func_val.token == "!"):
            if (len(stack) == 0):
                stack.append(global_func_val.token)
            else:
                tmp_token = stack.pop()
                if (tmp_token != "!"):
                    stack.append(tmp_token)
                    stack.append(global_func_val.token)
                else:
                    while (tmp_token == "!"):
                        global_func_val.postfix_string += tmp_token + " "
                        tmp_token = stack.pop()
                    stack.append(tmp_token)
                    stack.append(global_func_val.token)
        elif(global_func_val.token == "*" or global_func_val.token == "/"):
            if (len(stack) == 0):
                stack.append(global_func_val.token)
            else:
                tmp_token = stack.pop()
                if (tmp_token == "+" or tmp_token == "-" or tmp_token == "("):
                    stack.append(tmp_token)
                    stack.append(global_func_val.token)
                else:
                    while (tmp_token == "!" or tmp_token == "*" or tmp_token == "/"):
                        global_func_val.postfix_string += tmp_token + " "
                        tmp_token = stack.pop()
                    stack.append(tmp_token)
                    stack.append(global_func_val.token)


        global_func_val.token = global_func_val.get_token()

    while (len(stack) != 0):
        global_func_val.postfix_string += stack.pop() + " "


if __name__ == '__main__':
    global_func_val.input_string = input()
    if (global_func_val.input_string == ""):
        print("Строка пуста")
    else:
        global_func_val.folding_string = global_func_val.folding(global_func_val.input_string)
        global_func_val.infix_string = global_func_val.unary_minus_coding(global_func_val.folding_string)
        isOk = global_func_val.string_validation(global_func_val.infix_string)
        if (isOk == None):
            global_func_val.index = 0
            global_func_val.token = ""
            global_func_val.num_brackets = 0
            global_func_val.token = global_func_val.get_token()

            kek()

            global_func_val.result_string = global_func_val.postfix_string.replace("!", "-")
            print(global_func_val.postfix_string)
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
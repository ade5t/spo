import sort_station
import recursive_descent
import global_func_val
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
            recursive_descent.check_binary_plus_minus()
            global_func_val.result_string = global_func_val.postfix_string.replace("!", "-")
            print("Рекурсивный спуск:" + global_func_val.postfix_string)

            global_func_val.index = 0
            global_func_val.token = ""
            global_func_val.postfix_string = ""
            global_func_val.result_string = ""
            global_func_val.num_brackets = 0
            global_func_val.token = global_func_val.get_token()
            sort_station.dijkstra_method()
            global_func_val.result_string = global_func_val.postfix_string.replace("!", "-")
            print("Сортировочная ста:" + global_func_val.postfix_string)
        else:
            print(isOk)
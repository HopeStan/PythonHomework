from final_task.operate import OPERATIONS, DICT_Math, DICT_Const, DICT_All
from final_task.split import is_number, parse_to_list


def infix_to_postfix(parsed_exp):
    stack = []
    postfix_list = []
    for element in parsed_exp:
        if (element in OPERATIONS) or (element in DICT_Math):
            if element == '(':
                stack.append(element)
            elif element == ')':
                while stack and stack[-1] != '(':
                    postfix_list.append(stack.pop())
                if stack:
                    stack.pop()
            else:
                if DICT_All[element].associativity != 1:
                    while stack and DICT_All[element].priority < DICT_All[stack[-1]].priority:
                        postfix_list.append(stack.pop())
                else:
                    while stack and DICT_All[element].priority <= DICT_All[stack[-1]].priority:
                        postfix_list.append(stack.pop())
                stack.append(element)
        elif element in DICT_Const:
            postfix_list.append(element)
        elif is_number(element):
            postfix_list.append(element)
        else:
            raise ValueError(f'ERROR: name {element} is not defined')
    while stack:
        postfix_list.append(stack.pop())
    return postfix_list


def calculate(exp):
    stack = []
    parsed_exp = parse_to_list(exp)
    polish = infix_to_postfix(parsed_exp)
    if all((element in OPERATIONS) for element in polish):
        raise ValueError('ERROR:not valid input')
    for element in polish:
        if element in DICT_All:
            if element in DICT_Math and len(polish) == 1:
                stack.append(DICT_Math[element].func())
            elif element in DICT_Math:
                variable_1 = stack.pop()
                if type(variable_1) is list:
                    res = DICT_Math[element].func(*variable_1)
                else:
                    res = DICT_Math[element].func(*[variable_1])
                stack.append(res)
            elif element in DICT_Const:
                stack.append(DICT_Const[element].func)
            elif not DICT_All[element].is_binary:
                variable_1 = stack.pop()
                stack.append(DICT_All[element].func(variable_1))
            else:
                try:
                    variable_2, variable_1 = stack.pop(), stack.pop()
                    stack.append(DICT_All[element].func(variable_1, variable_2))
                except Exception as e:
                    raise ValueError(f'ERROR: binary operation is a calculation that combines two elements {e}')
        else:
            stack.append(float(element))
    return stack[0]



import argparse
import importlib
import operator
import re


class Operator:
    def __init__(self, name, priority, associativity, is_binary, func):
        self.name = name
        self.priority = priority
        self.associativity = associativity
        self.is_binary = is_binary
        self.func = func


class Function:
    def __init__(self, name, priority, associativity, is_binary, func):
        self.name = name
        self.priority = priority
        self.associativity = associativity
        self.is_binary = is_binary
        self.func = func


class Constant:
    def __init__(self, name, priority, associativity, is_binary, func):
        self.name = name
        self.priority = priority
        self.associativity = associativity
        self.is_binary = is_binary
        self.func = func


class FunctionDict:
    functions_dict = {}
    constants_dict = {}

    def __init__(self):
        self.parse_math()
        self.functions_dict["abs"] = Function(object, 7, 1, True, abs)
        self.functions_dict["round"] = Function(object, 7, 1, True, round)

    def parse_math(self):
        for module in ['math']:
            attr = importlib.import_module(module)
            for element in vars(attr):
                if element[0:2] != '__':
                    if isinstance(vars(attr)[element], (int, float, complex)):
                        self.constants_dict[element] = Constant(element, 7, 1, True, vars(attr)[element])
                    else:
                        self.functions_dict[element] = Function(element, 7, 1, True, vars(attr)[element])


def all_dict(dict_math, dict_const, operations):
    dict_all = dict_math.copy()
    dict_all.update(dict_const)
    dict_all.update(operations)
    return dict_all


OPERATIONS = {
    '^': Operator('^', 5, 2, True, operator.pow),
    '*': Operator('*', 4, 1, True, operator.mul),
    '//': Operator('//', 4, 1, True, operator.floordiv),
    '/': Operator('/', 4, 1, True, operator.truediv),
    '%': Operator('%', 4, 1, True, operator.mod),
    '<=': Operator('<=', 2, 1, True, operator.le),
    '>=': Operator('>=', 2, 1, True, operator.ge),
    '+': Operator('+', 3, 1, True, operator.add),
    '-': Operator('-', 3, 1, True, operator.sub),
    '<': Operator('<', 2, 1, True, operator.lt),
    ">": Operator('>', 2, 1, True, operator.gt),
    "==": Operator('==', 1, 1, True, operator.eq),
    '!=': Operator('!=', 1, 1, True, operator.ne),
    '(': Operator('(', 0, 1, False, None),
    ')': Operator(')', 0, 1, False, None),
    ',': Operator(',', 1, 1, True, lambda x, y: [x, y]),
    'unarym': Operator('unarym', 6, 1, False, lambda x: -x),
    'unaryp': Operator('unaryp', 6, 1, False, lambda x: x),
}

DICT_Math = FunctionDict().functions_dict
DICT_Const = FunctionDict().constants_dict
DICT_All = all_dict(DICT_Math, DICT_Const, OPERATIONS)
LIST_OF_OP = list(OPERATIONS.keys())


def is_number(s):
    """ Returns True if string is a number. """
    return s.replace('.', '', 1).isdigit()


def good_parentheses(parsed_exp) -> int:
    count = 0
    for element in parsed_exp:
        if element == "(":
            count += 1
        if element == ")":
            count -= 1
    return count


def split_by_prefix(inp_string, prefixes):
    regex = re.compile('|'.join(map(re.escape, prefixes)))
    while True:
        match = regex.match(inp_string)
        if not match:
            break
        end = match.end()
        yield inp_string[:end]
        inp_string = inp_string[end:]
    if inp_string:
        yield inp_string


def pre_validate(inp):
    """Need to apply pre-validation of some errors before parsing"""
    if not inp:
        raise ValueError('ERROR: Formula should be not empty string!')
    if '..' in inp or re.search(r'\.\d+\.', inp):
        raise ValueError('ERROR: Number can not contain more than one delimiter "." !')
    if re.search(r'/\s+/|<\s+=|>\s+=|=\s+=|!\s+=', inp):
        raise ValueError('ERROR: space is not allowed in operators: //, <=, >=, ==, !=.')
    if re.search(r'(\d\s+\d)|(\d\.\s+\d)', inp):
        raise ValueError('ERROR: space is not allowed between digits!')


def validate_parsed_list(parsed_exp: list):
    """Validation of various errors before polish sorting"""
    if parsed_exp[-1] in ['-', '+', '*', '/', '//', '%', '^', '<', '<=', '>', '>=', '==', '!=', ".", ","]:
        raise ValueError('ERROR: Operator at the end of the formula: "{}" '.format(parsed_exp[-1]))
    if parsed_exp[0] in ['*', '/', '//', '%', '^', '<', '<=', '>', '>=', '==', '!=']:
        raise ValueError('ERROR: Formula can not start with binary operator "{}"'.format(parsed_exp[0]))
    if good_parentheses(parsed_exp) != 0:
        raise ValueError('ERROR: Wrong number of opened or closed parentheses in formula!')


def parse_to_list(inp):
    """String splitting by operators and operands using regular expressions"""
    pre_validate(inp)
    prefixes = LIST_OF_OP
    str_list = re.findall(r'(?:\d+\.\d+)|(?:\d+\.?)|[a-zA-Z\d]+|\s*\W{,2}', inp)
    new_str = []
    for item in str_list:
        if item in LIST_OF_OP:
            new_str.append(item)
        else:
            new_str.extend(split_by_prefix(item, prefixes))
    parsed_exp = [element.strip(' ') for element in new_str]
    validate_parsed_list(parsed_exp)
    parsed_exp = [element for element in parsed_exp if element != '']
    for index, element in enumerate(parsed_exp):
        if element == ".":
            parsed_exp[index] = "0{}{}".format(parsed_exp.pop(index), parsed_exp[index])
    return find_unary_signs(parsed_exp)


def find_unary_signs(parsed_exp):
    for index, element in enumerate(parsed_exp):
        while True:
            if (parsed_exp[index] == '-' and parsed_exp[index + 1] == '-') or \
                    (parsed_exp[index] == '+' and parsed_exp[index + 1] == '+'):
                parsed_exp.pop(index), parsed_exp.pop(index), parsed_exp.insert(index, '+')
            elif (parsed_exp[index] == '+' and parsed_exp[index + 1] == '-') or \
                    (parsed_exp[index] == '-' and parsed_exp[index + 1] == '+'):
                parsed_exp.pop(index), parsed_exp.pop(index), parsed_exp.insert(index, '-')
            elif parsed_exp[0] == '-' and (is_number(parsed_exp[1]) or
                                           parsed_exp[1] == '(' or
                                           parsed_exp[1] in DICT_Math or
                                           parsed_exp[1] in DICT_Const):
                parsed_exp.pop(index), parsed_exp.insert(index, 'unarym')
            elif parsed_exp[0] == '+' and (is_number(parsed_exp[1]) or
                                           parsed_exp[1] == '(' or
                                           parsed_exp[1] in DICT_Math or
                                           parsed_exp[1] in DICT_Const):
                parsed_exp.pop(index), parsed_exp.insert(index, 'unaryp')
            elif (parsed_exp[index] in ['(', '*', '/', '//', '%', '^', '<', '<=', '>', '>=', '==', '!=', ',']) and \
                    (parsed_exp[index + 1] == '-') and (parsed_exp[index + 2] in DICT_Math or
                                                        parsed_exp[index + 2] in DICT_Const or
                                                        is_number(parsed_exp[index + 2])):
                parsed_exp.pop(index + 1), parsed_exp.insert(index + 1, 'unarym')
            elif (parsed_exp[index] in ['(', '*', '/', '//', '%', '^', '<', '<=', '>', '>=', '==', '!=', ',']) and \
                    (parsed_exp[index + 1] == '+') and (parsed_exp[index + 2] in DICT_Math or
                                                        parsed_exp[index + 2] in DICT_Const or
                                                        is_number(parsed_exp[index + 2])):
                parsed_exp.pop(index + 1), parsed_exp.insert(index + 1, 'unaryp')
            else:
                index += 1
            if index < len(parsed_exp) - 1:
                continue
            else:
                break
    return parsed_exp


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


def calcul(exp):
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


def main():
    parser = argparse.ArgumentParser(description="Pure-python command-line calculator.")
    parser.add_argument("EXPRESSION", help="Please, enter an expression for calculating", type=str)
    args = parser.parse_args()
    result = args.EXPRESSION
    try:
        print(calcul(result))
    except Exception as e:
        print(f'ERROR: {e}')


if __name__ == '__main__':
    main()

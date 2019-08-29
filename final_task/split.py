import re
from final_task.operator import LIST_OF_OP, DICT_Math, DICT_Const


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
    str_list = re.findall(r'(?:\d+\.\d+)|(?:\d+\.?)|[a-zA-Z\d]+|\W+', inp)
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

import importlib
import operator


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

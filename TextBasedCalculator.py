import re
from enum import Enum

class UnaryOperators(Enum):
    ADD = 1
    SUB = 2

UnaryOperatorsRegexMap = {'\+\+':UnaryOperators.ADD,
                          '\-\-':UnaryOperators.SUB}

class MathBaseOperators(Enum):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4

# elements order has logical influence
BinaryOperatorsMap = {'+':MathBaseOperators.ADD,
                      '-':MathBaseOperators.SUB,
                      '*':MathBaseOperators.MUL,
                      '/':MathBaseOperators.DIV}

#Signs: Plus or Minus
SignMap = {'+':MathBaseOperators.ADD,
           '-':MathBaseOperators.SUB}

VAR_REGEX = r'([\w]*[A-Za-z]+[\w]*)'  # [0-9a-zA-Z_]*[A-Za-z]+[0-9a-zA-Z_]* (var can't be digits only)

def is_int(num):
    #Checks if a num is a number using regex, This could be extended to support floats
    p = r'^[-+]?(\d)+$'  # possible positivity sign followed by digits
    if re.match(p, num):
        return True
    return False

class Evaluator:
    def __init__(self):
        self.variables = {}

    def evaluate(self, expressions):
        """
        evaluate a series of expressions separated by newlines
        :param expressions: a series of expressions
        :return: a one line summary of the variables
        """
        if not expressions:
            return None
        if type(expressions) is not str:
            raise ValueError("expressions should be of type str not "+str(type(expressions)))

        for expression in expressions.strip().split('\n'):
            self.evaluate_line(expression)

        res = self.vars_to_string()
        self.clear_variables()
        return res

    def evaluate_line(self, expression):
        """
        Evaluates a single expression into self.variables
        """
        if not expression:
            return None
        expression = "".join(expression.split())
        expression = self.replace_assignment_shortcuts(expression)
        if '=' not in expression:
            raise SyntaxError("expression should have an assignment char ")

        key, expression = expression.split('=', 1)  # Currently assume we have one '=' in the expression
        if not re.search('^'+VAR_REGEX+'$', key):
            raise SyntaxError("var must contain at least one letter and be constructed of alphanumeric chars only. "+key+" is invalid")

        self.variables[key] = self.compute(expression)

    def compute(self, expression):
        """
        Computes the arithmetic part of the expression
        """
        if not expression:
            return None
        if is_int(expression):
            return int(expression)

        expression = self.resolve_brackets(expression)              # Brackets first
        expression = self.resolve_unary_operators(expression)       # Unary operators second (ex. a)
        expression = self.resolve_concatenated_signs(expression)    # concatenated signs third (ex. 4--5 is 4+5)
        return int(self.compute_basic_expression(expression))            # basic +-/* computation are last

    def replace_assignment_shortcuts(self, expression):
        """
        Replaces assignment shortcuts such as '+=' with their full syntax
        Example: x+=10-5 will become x=x+(10-5)
        """
        op_rgx = r'(([\+\-\*\/])=)+'
        p = re.compile(VAR_REGEX + ' *' + op_rgx)

        idx = 0
        new_exp = ""
        for m in p.finditer(expression):
            var = m.group(1)
            op = m.group(3)
            new_exp += expression[idx:m.start(2)] + "=" + var + op + '('
            idx = m.end(2)

        if new_exp == "":
            return expression

        cnt_brackets = len(p.findall(expression))
        new_exp += expression[idx:] + ")" * cnt_brackets
        return new_exp

    def resolve_brackets(self, expression):
        """
        Computes the brackets if exists using recursion
        :param expression: a mathematical expression that may contain brackets
        :return: mathematical expression after the brackets were computed
        """
        while '(' in expression:
            lft_idx = expression.rfind('(')
            rgt_idx = expression.find(')', lft_idx)
            if rgt_idx == -1:
                raise SyntaxError("No matching closing bracket for opening bracket at:" + str(lft_idx))
            val = self.compute(expression[lft_idx + 1:rgt_idx])  # Brackets inner expression
            expression = expression[:lft_idx] + str(val) + expression[rgt_idx + 1:]  # Concatenate result value
        return expression

    def resolve_unary_operators(self, expression):
        """
        Computes and assign the value of unary operations
        example: i++ or i--
        :param expression: mathematical expression that may consist of unary operations
        :return: a mathematical expression after unary operations are resolved
        """
        for op in UnaryOperatorsRegexMap:
            for p in [VAR_REGEX + op, op + VAR_REGEX]:
                idx = 0
                new_exp = ""
                for m in re.compile(p).finditer(expression):  # re.compile compiles the pattern given to a regex object
                    var = m.group(1)
                    if var not in self.variables:
                        raise ValueError("variable " + var + " referenced before assignment")

                    if p == (VAR_REGEX + op):  # Assign value before operator
                        new_exp += expression[idx:m.start()] + str(self.variables[var])

                    if UnaryOperatorsRegexMap[op] == UnaryOperators.ADD:
                        self.variables[var] += 1
                    elif UnaryOperatorsRegexMap[op] == UnaryOperators.SUB:
                        self.variables[var] -= 1
                    else:
                        raise ValueError('Operator ' + op + ' not implemented')

                    if p == (op + VAR_REGEX):  # Assign value after operator
                        new_exp += expression[idx:m.start()] + str(self.variables[var])

                    idx = m.end()

                if idx != 0:  # Reset
                    expression = new_exp + expression[idx:]

        return expression

    @staticmethod
    def resolve_concatenated_signs(expression):
        """
        Aggregates segments of plus and minus signs that are concatenated
        :param expression: a mathematical expression that may contain segments of concatenated plus/minus signs
        :return: mathematical expression with aggregated plus/minus signs
        """
        p = '['+''.join(SignMap)+']{2,}'  # Two or more concatenated signs
        idx = 0
        new_exp = ""
        for m in re.compile(p).finditer(expression):
            if m.group().count('-') % 2 == 0:
                aggregated_sign = '+'
            else:
                aggregated_sign = '-'

            new_exp += expression[idx:m.start()] + aggregated_sign
            idx = m.end()

        if idx == 0:
            return expression
        new_exp += expression[idx:]
        return new_exp

    def compute_basic_expression(self, expression):
        """
        Computes the value of an expression that contains only basic +-*/ binary operators
        :param expression: contains no brackets, '=' or unary operators. only binary arithmetic operators
        :return: the result of the basic expression according to arithmetic rules
        """
        if is_int(expression):
            return int(expression)

        p = r'((?<![\*\/])(?!^))\{}'
        """
        p is a regex pattern that finds all the plus/minus signs that should be splitted except::
        1. a lookbehind for MUL and DIV operations followed by POSITIVE or NEGATIVE sign
        2. a lookahead for a POSITIVE or NEGATIVE sign at prefix
        Example: in x=-1-2*-3*-4-5, -1, -3 and -4 should not be splitted at '-'
        """
        res = None
        for op in BinaryOperatorsMap:
            if op in expression:
                if op in SignMap:  # TODO:Use positive and negative constants
                    sub_expressions = re.compile(p.format(op)).split(expression)
                    sub_expressions = list(filter(None, sub_expressions))
                    if len(sub_expressions) == 1:
                        continue  # There was no need to split, we continue
                else:
                    sub_expressions = expression.split(op)

                for sub_exp in sub_expressions:
                    val = self.compute_basic_expression(sub_exp)
                    if res is None:
                        res = val
                    elif BinaryOperatorsMap[op] == MathBaseOperators.ADD:
                        res += val
                    elif BinaryOperatorsMap[op] == MathBaseOperators.SUB:
                        res -= val
                    elif BinaryOperatorsMap[op] == MathBaseOperators.MUL:
                        res *= val
                    elif BinaryOperatorsMap[op] == MathBaseOperators.DIV:
                        if val == 0:
                            raise ArithmeticError("Division by zero is forbidden")
                        res /= val
                    else:
                        raise ValueError('Operator ' + op + ' not implemented')
                return res

        if expression in self.variables:
            return self.variables[expression]
        raise SyntaxError("Unresolved expression:" + expression)

    def vars_to_string(self):
        if not self.variables:
            print("No variables found.")
            return

        res = "("
        for idx, (key, value) in enumerate(self.variables.items()):
            if idx > 0:
                res += ","
            res += str(key) + "=" + str(value)
        res += ")"

        return res

    def clear_variables(self):
        self.variables.clear()

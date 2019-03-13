from utilities import *
import re


#  TODO: What happens if you divied by zero?


class ExpressionCalculator:
    def __init__(self):
        self.variables = {}
        self.binary_operators = ['+', '-', '/', '*']  # elements order have a logic influence
        self.unary_operators = ['\+\+', '\-\-']  # TODO: dont forget the r is for raw string representation

    def evaluate(self, expressions):
        # TODO: What happens if expressions is None/empty/int and not str?
        for expression in expressions.split('\n'):
            self.evaluate_single(expression)
        return self.variables

    def evaluate_single(self, expression):
        expression = self.replace_assignment_shortcuts(expression)
        #  TODO: Handle cases where expression is i++ or i+=j+=1(This is party treated)
        key, expression = expression.split('=', 1)  # Currently assume we have one '=' in the expression
        self.variables[key] = self.compute(expression)

    def compute(self, expression):
        if is_int(expression):
            return int(expression)
        # TODO: check if expression is blank maybe? maybe expression is '()'
        # Priority 2 -> compute inner brackets
        # TODO: export '(' to an enum or something parallel to left_bracket
        # TODO: test the case in which the expression has ')' but not '('
        expression = self.resolve_brackets(expression)

        # Priority 3 -> compute unary operators
        expression = self.resolve_unary_operations(expression)

        # #Priority 4 -> compute concatd +- signs
        expression = self.resolve_concatenated_signs(expression)

        # Pririty 5 -> compute binary operators
        res = self.compute_without_brackets(expression)

        return res

    @staticmethod
    def replace_assignment_shortcuts(expression):
        """
        Replaces assignment shortcuts such as '+=' with their full syntax
        Example: x+=10-5 will become x=x+(10-5)
        """
        var_name_rgx = r'(\w*[A-Za-z]+\w*)'
        op_rgx = r'(([\+\-\*\/])=)+'
        p = re.compile(var_name_rgx + ' *' + op_rgx)

        idx = 0  # TODO:This is duplicate code, I can surely export it to an external function
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
        :param expression: mathematical expression that may contains brackets
        :return: mathematical expression after the brackets were computed
        """
        while '(' in expression:
            lft_idx = expression.rfind('(')
            rgt_idx = expression.find(')', lft_idx)
            if rgt_idx == -1:
                print("No matching closing bracket for the one at:"+str(lft_idx))
                return None
            val = self.compute(expression[lft_idx + 1:rgt_idx])  # Brackets inner expression
            if val is None:
                return None
            expression = expression[:lft_idx] + str(val) + expression[rgt_idx + 1:]  # Concatenate result value

        return expression

    def resolve_unary_operations(self, expression):
        last_index = 0
        modified_expression = ""
        for unary_operand in self.unary_operators:
            # TODO: Change this condition, somevariables may contains numbers such as tmp2
            p = re.compile(r'[a-zA-Z]+' + unary_operand)  # TODO: Get an inner-depth understanding of how this works
            for m in p.finditer(expression):
                var = expression[m.start():m.end() - 2]  # Reducing the -- or ++ #TODO: This might not be best practice
                if var not in self.variables:
                    print(
                        var + " assigned before assertion")  # Double check that this is the correct syntex you want to use for the message
                    return None
                modified_expression += (expression[last_index:m.start()] + str(self.variables[var]))
                last_index = m.end()
                if unary_operand == '\+\+':  # TODO: Definetly not best practice
                    self.variables[var] += 1
                elif unary_operand == '\-\-':
                    self.variables[var] -= 1
                else:
                    print('not suppose to arrive here')

            if last_index != 0:  # Reset
                expression = modified_expression + expression[last_index:]
                last_index = 0
                modified_expression = ""

            p = re.compile(
                r'' + unary_operand + '[a-zA-Z]+')  # TODO: Get an inner-depth understanding of how this works
            for m in p.finditer(expression):
                var = expression[m.start() + 2:m.end()]  # Reducing the -- or ++  #TODO: This might not be best practice
                if var not in self.variables:
                    print(
                        var + " assigned before assertion")  # Double check that this is the correct syntex you want to use for the message
                    return None

                if unary_operand == '\+\+':  # TODO: Definetly not best practice, replace with an enum
                    self.variables[var] += 1
                elif unary_operand == '\-\-':
                    self.variables[var] -= 1
                else:
                    print('not suppose to arrive here')
                modified_expression += (expression[last_index:m.start()] + str(self.variables[var]))
                last_index = m.end()

            if last_index != 0:  # Reset
                expression = modified_expression + expression[last_index + 1:]
                last_index = 0
                modified_expression = ""

        return expression

    def resolve_concatenated_signs(self, expression):
        p = re.compile('[+-]{2,}')
        last_index = 0
        modified_expression = ""
        for m in p.finditer(expression):
            if m.group().count('-') % 2 == 0:
                aggregated_sign = '+'
            else:
                aggregated_sign = '-'

            modified_expression += (expression[last_index:m.start()] + aggregated_sign)
            last_index = m.end()

        if last_index == 0:
            return expression

        modified_expression += expression[last_index:]
        return modified_expression

    # Returns a value, it can manipulate the value
    def compute_without_brackets(self, expression):
        if is_int(expression):
            return int(expression)
        special_slice_regex = '((?<!\*)(?!^))\\{}'
        res = None
        # Instead of iterating through all operators we can send as a parameter the ones that were left, its a complexity-memory tradeoff
        for operator in self.binary_operators:
            if operator in expression:
                if operator in ['-',
                                '+']:  # This is a special case due to the affect that the minus sign has before numbers
                    sub_expressions = re.compile(special_slice_regex.format(operator)).split(expression)
                    sub_expressions = list(filter(None, sub_expressions))
                    if len(
                            sub_expressions) == 1:  # There was no real need to split, If this is too complex we can remove it
                        continue
                else:
                    sub_expressions = expression.split(
                        operator)  # The problem is with the split here. if I could do a split based on regex it would be great

                for item in sub_expressions:
                    item = self.compute_without_brackets(item)
                    if not item:  # Unresolved expression (item) - Bubble the error upwards
                        return None
                    elif not res:
                        res = item
                    elif operator == '+':
                        res += item
                    elif operator == '-':
                        res -= item
                    elif operator == '*':
                        res *= item
                    elif operator == '/':
                        res /= item
                    else:
                        print("Exception, not suppose to arrive here")

                return res

        if expression in self.variables:
            return self.variables[expression]

        # TODO: Replace with an exception?
        print("Unresolved expression:" + expression)
        return None


myExpression = ExpressionCalculator()
res = myExpression.evaluate("i=0\n"
                            "j=++i\n"
                            "x=i+++5\n"
                            "y=5+3*10\n"
                            "i+=y")

print_variables(res)

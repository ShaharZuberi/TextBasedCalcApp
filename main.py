import re
#TODO: Go over the naming convention
#TODO: What happens if you divied by zero?

class ExpressionCalculator:
    def __init__(self):
        self.single_line_expressions = []
        self.vars = {}
        self.binary_operators = ['+', '-', '/', '*']  # elements order have a logic influence
        self.unary_operators = ['\+\+', '\-\-']  #TODO: dont forget the r is for raw string representation

    def evaluate(self, expression_series):
        self.single_line_expressions = expression_series.split('\n')

        for expression in self.single_line_expressions:
            self.parse_expression(expression)

        self.print_variables(self.vars)

    #  TODO: parse is not the right term for what it does
    def parse_expression(self, expression):
        res=expression.split('=') #  TODO: Handle cases where expression is i++ or i+=j+=1
        key = res[0]
        exp = res[1]
        self.vars[key] = self.compute(exp)

    def compute(self, expression):
        #TODO: check if this if condition is necessery in both compute and compute_without_brackets
        if self.is_int(expression):
            return int(expression)
        #TODO: check if expression is blank maybe? maybe expression is '()'

        #Priority 1 -> compute inner brackets
        #TODO: export '(' to an enum or something parallel to left_bracket
        #TODO: test the case in which the expression has ')' but not '('
        expression = self.resolve_inner_brackets(expression)

        #Priority 2 -> compute unary operators
        expression = self.resolve_unary_operations(expression)

        # #Priority 3 -> compute concatd +- signs
        expression = self.resolve_concatenated_signs(expression)

        #Pririty 4 -> compute binary operators
        res = self.compute_without_brackets(expression)

        return res

    def resolve_inner_brackets(self, expression):
        while '(' in expression:
            lft_idx = expression.rfind('(')
            rgt_idx = expression.find(')',lft_idx)
            res = self.compute(expression[lft_idx+1:rgt_idx]) #Without brackets
            expression = expression[:lft_idx]+str(res)+expression[rgt_idx+1:]

        return expression

    def resolve_unary_operations(self, expression):
        last_index = 0
        modified_expression = ""
        for unary_operand in self.unary_operators:
            p = re.compile(r'[a-zA-Z]+' + unary_operand)  # TODO: Get an inner-depth understanding of how this works
            for m in p.finditer(expression):
                var = expression[m.start():m.end() - 2]  # Reducing the -- or ++ #TODO: This might not be best practice
                if var not in self.vars:
                    print(
                        var + " assigned before assertion")  # Double check that this is the correct syntex you want to use for the message
                    return None
                modified_expression += (expression[last_index:m.start()] + str(self.vars[var]))
                last_index = m.end()
                if unary_operand == '\+\+':  # TODO: Definetly not best practice
                    self.vars[var] += 1
                elif unary_operand == '\-\-':
                    self.vars[var] -= 1
                else:
                    print('not suppose to arrive here')

            if last_index != 0:  # Reset
                expression = modified_expression + expression[last_index + 1:]
                last_index = 0
                modified_expression = ""

            p = re.compile(
                r'' + unary_operand + '[a-zA-Z]+')  # TODO: Get an inner-depth understanding of how this works
            for m in p.finditer(expression):
                var = expression[m.start() + 2:m.end()]  # Reducing the -- or ++  #TODO: This might not be best practice
                if var not in self.vars:
                    print(
                        var + " assigned before assertion")  # Double check that this is the correct syntex you want to use for the message
                    return None

                if unary_operand == '\+\+':  # TODO: Definetly not best practice, replace with an enum
                    self.vars[var] += 1
                elif unary_operand == '\-\-':
                    self.vars[var] -= 1
                else:
                    print('not suppose to arrive here')
                modified_expression += (expression[last_index:m.start()] + str(self.vars[var]))
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

            modified_expression+=(expression[last_index:m.start()]+aggregated_sign)
            last_index=m.end()

        if last_index == 0:
            return expression

        modified_expression += expression[last_index:]
        return modified_expression

    #Returns a value, it can manipulate the value
    def compute_without_brackets(self, expression):
        if self.is_int(expression):
            return int(expression)

        res = None
        #Instead of iterating through all operators we can send as a parameter the ones that were left, its a complexity-memory tradeoff
        for operator in self.binary_operators:
            if operator in expression:
                if operator in ['-', '+']: #This is a special case due to the affect that the minus sign has before numbers
                    sub_expressions = re.compile('((?<!\*)(?!^))\\{}'.format(operator)).split(expression)
                    sub_expressions = list(filter(None, sub_expressions))
                    if len(sub_expressions) == 1:  #There was no real need to split, If this is too complex we can remove it
                        continue
                else:
                    sub_expressions = expression.split(operator) #The problem is with the split here. if I could do a split based on regex it would be great

                for item in sub_expressions:
                    item = self.compute_without_brackets(item)
                    if not item: #Unresolved expression (item) - Bubble the error upwards
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

        if expression in self.vars:
            return self.vars[expression]

        #TODO: Replace with an exception?
        print("Unresolved expression:"+expression)
        return None

    #TODO: This may be further improved
    @staticmethod
    def print_variables(varDict):
        print("(", end="")
        for idx, key in enumerate(varDict):
            if idx > 0:
                print(",", end="")
            print(str(key) + "=" + str(varDict[key]), end="")
        print(")")

    @staticmethod  #TODO: we can export this to outside of the class
    def is_int(num):
        #We can use exceptions but they are expensive so we would prefere to use as a workflow. instead we can use regular expressions
        if re.match(r'^[-+]?(\d)+$',num):
            return True
        return False

MyExpression = ExpressionCalculator()
MyExpression.evaluate("a=-5-5")
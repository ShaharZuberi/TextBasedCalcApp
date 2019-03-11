#TODO: Go over the naming convention

class ExpressionCalculator:
    def __init__(self):
        self.single_line_expressions = []
        self.vars={}
        self.operators = ['+', '-', '/', '*']  # elements order have a logic influence

    def evaluate(self, expression_series):
        self.single_line_expressions = expression_series.split('\n')

        for expression in self.single_line_expressions:
            self.parse_expression(expression)

        #  TODO: Export this to an outer function and add ','
        print("(",end="")
        for idx,key in enumerate(self.vars):
            if idx > 0: print(",",end="")
            print(str(key)+"="+str(self.vars[key]),end="")
        print(")")

    #  TODO: parse is not the right term for what it does
    def parse_expression(self, expression):
        res=expression.split('=') #  TODO: Handle cases where expression is i++ or i+=j+=1
        key = res[0]
        exp = res[1]
        self.vars[key] = self.compute(exp)

    def compute(self, expression):
        #TODO: export is digit to an outside function, maybe in the future we would like to implement is digit for float numbers as well
        #TODO: check if this if condition is necessery in both compute and compute_without_brackets
        if expression.isdigit():
            return int(expression)
        #TODO: check if expression is blank maybe? maybe expression is '()'

        #TODO: export '(' to an enum or something parallel to left_bracket
        #TODO: test the case in which the expression has ')' but not '('
        while '(' in expression:
            lft_idx = expression.rfind('(')
            rgt_idx = expression.find(')',lft_idx)
            res = self.compute(expression[lft_idx+1:rgt_idx]) #Without brackets
            expression = expression[:lft_idx]+str(res)+expression[rgt_idx+1:]

        return self.compute_without_brackets(expression)
    #TODO: Check what happens if I get a series of numbers with spaces, what then?
    #Returns a value, it can manipulate the value
    def compute_without_brackets(self, expression):
        if expression.isdigit():
            return int(expression)

        res = None
        #Instead of iterating through all operators we can send as a parameter the ones that were left, its a complexity-memory tradeoff
        for operator in self.operators:
            if operator in expression:
                sub_expressions = expression.split(operator)

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


MyExpression = ExpressionCalculator()
MyExpression.evaluate("i=5 4 4 5\nx=(1+(2+1)*3)*3")
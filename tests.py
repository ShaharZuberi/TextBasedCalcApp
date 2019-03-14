import unittest
import CalcEvaluator #TODO: Rename to TextBasedCalc or something like that

evaluator = CalcEvaluator.CalcEvaluator()


class TestMethods(unittest.TestCase):
    def test_given_example(self):
        self.assertEqual(evaluator.evaluate("i=0\n"
                                            "j=++i\n"
                                            "x=i+++5\n"
                                            "y=5+3*10\n"
                                            "i+=y"), '(i=37,j=1,x=6,y=35)')

    def test_base_arithmetic(self):
        self.assertEqual(evaluator.evaluate("a=5+5+5*2/10-3"), '(a=8)')

    def test_unary_operators(self):
        self.assertEqual(evaluator.evaluate("a=1\n"
                                            "b=++a\n"
                                            "c=a++\n"
                                            "d=b+++1\n"
                                            "e=++d+1"), '(a=3,b=3,c=2,d=4,e=5)')

    def test_brackets(self):
        self.assertEqual(evaluator.evaluate("a=(1+2)*(3+4)\n"
                                            "b=(a+a)*a+a/2-1\n"
                                            "c=(2*(2*(2)))*2"), '(a=21,b=891,c=16)')

    def test_concatenated_signs(self):
        self.assertEqual(evaluator.evaluate("a=4\n"
                                            "b = -----5\n"
                                            "c=-2--3\n"
                                            "d=-3+-+-+-2\n"
                                            "e=-10000\n"), '(a=4,b=-5,c=1,d=-5,e=-10000)')

    def test_assignment_shortcuts(self):
        self.assertEqual(evaluator.evaluate("a=0\n"
                                            "b=0\n"
                                            "c=2\n"
                                            "d=100\n"
                                            "a += 4*3\n"
                                            "b -= 2\n"
                                            "c*=20*c\n"
                                            "d/=-5"), '(a=12,b=-2,c=80,d=-20)')

    def test_mixed_complex_scenarios(self):
        #TODO: Complete this
        print("...")
        # self.assertEqual(evaluator.evaluate("a=\n"
        #                                     "b=0\n"
        #                                     "c=2\n"
        #                                     "d=100\n"
        #                                     "a += 4*3\n"
        #                                     "b -= 2\n"
        #                                     "c*=20*c\n"
        #                                     "d/=-5"), '(a=12,b=-2,c=80,d=-20)')

    def test_blank_inputs(self):
        self.assertEqual(evaluator.evaluate(""), None)
        self.assertEqual(evaluator.evaluate("   "), None)
        self.assertEqual(evaluator.evaluate("   \n"
                                            "x=4+6"), '(x=10)')

    def test_value_errors(self):
        #Parameter passed is not of type str
        self.assertRaises(ValueError, evaluator.evaluate, 1)
        self.assertRaises(ValueError, evaluator.evaluate, 1.2)

        #variable referenced before assignment
        self.assertRaises(ValueError, evaluator.evaluate, "x=a++")

    def test_syntax_errors(self):
        #Brackets
        self.assertRaises(SyntaxError, evaluator.evaluate, "x=(")
        self.assertRaises(SyntaxError, evaluator.evaluate, "x=((4342)")
        self.assertRaises(SyntaxError, evaluator.evaluate, "x=(4342))")
        self.assertRaises(SyntaxError, evaluator.evaluate, "x=4342)")
        self.assertRaises(SyntaxError, evaluator.evaluate, "x=)4342(")

        #No assignment char
        self.assertRaises(SyntaxError, evaluator.evaluate, "i++")

        #Var is not valid
        self.assertRaises(SyntaxError, evaluator.evaluate, "3=4")
        self.assertRaises(SyntaxError, evaluator.evaluate, "i+3=4")

    def test_arithmetic_error(self):
        self.assertRaises(ArithmeticError, evaluator.evaluate, "x=1/0")

    #TODO: Test for x=a, its a syntax error and not a value one

if __name__ == '__main__':
    unittest.main()

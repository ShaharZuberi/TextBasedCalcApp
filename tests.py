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
        #TODO
        # self.assertEqual(evaluator.evaluate("a=\n"
        #                                     "b=0\n"
        #                                     "c=2\n"
        #                                     "d=100\n"
        #                                     "a += 4*3\n"
        #                                     "b -= 2\n"
        #                                     "c*=20*c\n"
        #                                     "d/=-5"), '(a=12,b=-2,c=80,d=-20)')


    # def advanced_tests(self):
    #     self.assertEqual(evaluator.evaluate(""))

    # def syntax_error_tests(self):
    #     self.assertEqual(evaluator.evaluate(""))
    #
    # def value_error_tests(self):
    #     self.assertEqual(evaluator.evaluate(""))
    #
    # def arithmetic_error_tests(self):
    #     self.assertEqual(evaluator.evaluate(""))

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()

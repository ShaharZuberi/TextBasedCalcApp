import unittest
import CalcEvaluator

evaluator = CalcEvaluator.CalcEvaluator()

class TestMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual(evaluator.evaluate("i=0\n"
                                            "j=++i\n"
                                            "x=i+++5\n"
                                            "y=5+3*10\n"
                                            "i+=y"), '(i=37,j=1,x=6,y=35)')

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

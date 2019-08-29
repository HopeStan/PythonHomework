import unittest
import math
from final_task.pycalc.pycalc import parse_to_list, split_by_prefix, calcul, infix_to_postfix


class PycalcTests(unittest.TestCase):
    def test_split_by_prefix(self):
        s = '>=+-'
        self.assertEqual(list(split_by_prefix(s, ['+', '-', '>=', '<=', '!=', '=='])), ['>=', '+', '-'])

    def test_parse_to_list(self):
        s = '5+63/3*79'
        self.assertEqual(parse_to_list(s), ['5', '+', '63', '/', '3', '*', '79'])
        s = '10>=1'
        self.assertEqual(parse_to_list(s), ['10', '>=', '1'])
        s = 'sin(10)'
        self.assertEqual(parse_to_list(s), ['sin', '(', '10', ')'])
        s = 'log10(100)'
        self.assertEqual(parse_to_list(s), ['log10', '(', '100', ')'])
        s = '5+sin(10+5)-10^3'
        self.assertEqual(parse_to_list(s), ['5', '+', 'sin', '(', '10', '+', '5', ')', '-', '10', '^', '3'])

    def test_functions(self):
        self.assertEqual(calcul('sin(1)'), math.sin(1))
        self.assertEqual(calcul('cos(sin(exp(12)))'), math.cos(math.sin(math.exp(12))))
        self.assertEqual(calcul('hypot(3, 6)'), math.hypot(3, 6))
        self.assertEqual(calcul('atan2(log10(123), expm1(4))'), math.atan2(math.log10(123), math.expm1(4)))

    def test_errors(self):
        self.assertRaises(Exception, calcul, '')
        self.assertRaises(Exception, calcul, '((')
        self.assertRaises(Exception, calcul, '==log(11)')
        self.assertRaises(Exception, calcul, '1+21*((3+2)')
        self.assertRaises(Exception, calcul, '>11')
        self.assertRaises(Exception, calcul, 'log(e)/0')
        self.assertRaises(Exception, calcul, '1+13/14 7')
        self.assertRaises(Exception, calcul, '123.123.4')
        self.assertRaises(Exception, calcul, '12.3+.123.5')
        self.assertRaises(Exception, calcul, 'abr(1)')
        self.assertRaises(Exception, calcul, 'pow(2, 3, 4)')

    def test_infix_to_postfix(self):
        s = '101+51^21-sin(10)'
        self.assertEqual(infix_to_postfix(parse_to_list(s)), ['101', '51', '21', '^', '+', '10', 'sin', '-'])
        s = '(21.0^(pi/pi+e/e+21.0^0.0))'
        self.assertEqual(infix_to_postfix(parse_to_list(s)), ['21.0', 'pi', 'pi', '/', 'e', 'e', '/', '+', '21.0',
                                                              '0.0', '^', '+', '^'])
        s = '5+10-60^2'
        self.assertEqual(infix_to_postfix(parse_to_list(s)), ['5', '10', '+', '60', '2', '^', '-'])


if __name__ == '__main__':
    unittest.main()

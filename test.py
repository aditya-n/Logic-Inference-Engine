from unittest import TestCase
import homework3

class TestInference(TestCase):
    def test_getInputs(self):
        homework3.queries = ['R(John, Joe)']
        homework3.sentences = ['~G(x) | H(x)',
                                '~H(x) | F(x)',
                                'R(x, y)']
        self.assertEqual(False, homework3.resolveByImplication('R(x,y)'))
        self.assertEqual(False, homework3.resolveByOrElimination('R(x,y)'))
        self.assertEqual(True, homework3.resolveIfLiteralPresent('R(Yot,Joe)'))
        self.assertEqual({'x': 'John', 't': 'Missy'}, homework3.getUnifierDict('Rat(John,y,Missy)', 'Rat(x,z,t)'));
        pass

    def test_unification(self):
        homework3.getInputs(homework3.queries, homework3.sentences, 'input.txt')
        homework3.resolveByImplication('Criminal(West)')
        b = homework3.getUnifierDict('Criminal(x)', 'Criminal(West)')
        a = homework3.resolveIfLiteralPresent('Criminal(x)')
        pass
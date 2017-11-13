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
        self.assertEqual({'x': 'John', 't': 'Missy'}, homework3.getUnifierDict('Rat(x,z,t)', 'Rat(John,y,Missy)'));
        pass

    def test_unification(self):
        homework3.queries, homework3.sentences = [], []
        homework3.getInputs(homework3.queries, homework3.sentences, 'input.txt')
        e = homework3.resolve('Missile(x)')
        d = homework3.resolveByImplication('Weapon(y)')
        b = homework3.getUnifierDict('Criminal(x)', 'Criminal(x)')
        a = homework3.resolve('Sells(West,M2,Nono)')
        pass
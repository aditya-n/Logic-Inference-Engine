from unittest import TestCase
import homework3

class TestInference(TestCase):
    def test_getInputs(self):
        homework3.queries = ['R(John, Joe)']
        homework3.sentences = ['~G(x) | H(x)',
                                '~H(x) | F(x)',
                                'R(x, y)']
        self.assertEqual(False, homework3.resolveByImplication('R(x,y)'))
        self.assertEqual(False, homework3.resolveByOrEliminationForKB('R(x,y)'))
        self.assertEqual(True, homework3.resolveIfLiteralPresent('R(Yot,Joe)'))
        self.assertEqual({'x': 'John', 't': 'Missy'}, homework3.getUnifierDict('Rat(John,y,Missy)', 'Rat(x,z,t)'));
        self.assertEqual({'x': 'John', 't': 'Missy'}, homework3.getUnifierDict('Rat(x,z,t)', 'Rat(John,y,Missy)'));
        pass

    def test_unification(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'input.txt')
        e = homework3.resolve('Missile(x)')
        d = homework3.resolveByImplication('Weapon(y)')
        b = homework3.getUnifierDict('Sells(West,x,Nono)', 'Sells(West,M2,Nono)')
        a1 = homework3.applyTransitiveOperation({'x':'y'}, {'y':'West'})
        a11 = homework3.resolveByOrElimination('Sells(x,y,z)', '~Missile(x) | ~Owns(Nono,x) | Sells(West,x,Nono)');
        a2 = homework3.resolveByOrEliminationForKB('Sells(x,y,z)')
        a3 = homework3.resolve('Weapon(y)')
        a34 = homework3.resolveByOrElimination('Sells(West,M1,z)', '~Missile(x) | ~Owns(Nono,x) | Sells(West,x,Nono)');
        a4 = homework3.resolveByOrEliminationForKB('Criminal(West)')
        pass
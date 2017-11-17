from unittest import TestCase
import homework3

class TestInference(TestCase):
    def test_getInputs(self):
        homework3.queries = ['R(John, Joe)']
        homework3.KB_sentences = ['~G(x) | H(x)',
                                '~H(x) | F(x)',
                                'R(x, y)']
        self.assertEqual(False, homework3.resolveByOrEliminationForKB('R(x,y)'))
        self.assertNotEqual(False, homework3.resolveIfLiteralPresent('R(Yot,Joe)'))
        self.assertEqual({'John':'x', 'y':'z', 'Missy':'t'}, homework3.getUnifierDict('Rat(John,y,Missy)', 'Rat(x,z,t)'));
        self.assertEqual({'x':'John', 'y':'z', 't':'Missy'}, homework3.getUnifierDict('Rat(x,y,t)', 'Rat(John,z,Missy)'));
        pass

    def test_unification(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'test3.txt')
        e = homework3.resolve('Missile(x)')
        b = homework3.getUnifierDict('Sells(West,x,Nono)', 'Sells(West,M2,Nono)')
        a1 = homework3.applyTransitiveOperation({'x':'y'}, {'y':'West'})
        a11 = homework3.resolveByOrElimination('Sells(x,y,z)', '~Missile(x) | ~Owns(Nono,x) | Sells(West,x,Nono)');
        a2 = homework3.resolveByOrEliminationForKB('Sells(x,y,z)')
        a3 = homework3.resolve('Weapon(y)')
        a34 = homework3.resolveByOrElimination('Sells(West,M1,z)', '~Missile(x) | ~Owns(Nono,x) | Sells(West,x,Nono)');
        self.assertNotEqual(False, homework3.resolve('Criminal(West)'));
        pass

    def test_unification(self):
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'test2.txt')
        a = homework3.apply_unifiers('Ancestor(x,z)', {'x': 'Liz', 'z': 'Joe'})
        b = homework3.resolveByOrElimination('Parent(Liz,y)', '~Mother(x,y) | Parent(x,y)')
        self.assertNotEqual(False, homework3.resolve('Ancestor(Liz,Billy)'));
        self.assertEqual(False, homework3.resolve('Ancestor(Liz,Joe)'));
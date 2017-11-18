from unittest import TestCase
import homework3

class TestInference(TestCase):
    def test_0(self):
        homework3.queries = ['R(John, Joe)']
        homework3.KB_sentences = ['~G(x) | H(x)',
                                '~H(x) | F(x)',
                                'R(x, y)']
        self.assertEqual(False, homework3.resolveByOrEliminationForKB('R(x,y)', set()))
        self.assertNotEqual(False, homework3.resolveIfLiteralPresent('R(Yot,Joe)'))
        self.assertEqual({'John':'x', 'y':'z', 'Missy':'t'}, homework3.getUnifierDict('Rat(John,y,Missy)', 'Rat(x,z,t)'));
        self.assertEqual({'x':'John', 'y':'z', 't':'Missy'}, homework3.getUnifierDict('Rat(x,y,t)', 'Rat(John,z,Missy)'));
        pass

    def test_3(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'test3.txt')
        self.assertNotEqual(False, homework3.resolve('Criminal(West)', set()));
        pass

    def test_2(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'test2.txt')
        a = homework3.apply_unifiers('Ancestor(x,z)', {'x': 'Liz', 'z': 'Joe'})

        self.assertNotEqual(False, homework3.resolve('Ancestor(Liz,Billy)', set()));
        self.assertEqual(False, homework3.resolve('Ancestor(Liz,Joe)', set()));

    def test_1(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'test1.txt')

        a = homework3.resolveIfLiteralPresent('B(John,y)');
        a = homework3.resolveIfLiteralPresent('D(Joe,y)');

        a = homework3.resolve('B(John,x)', set());
        a = homework3.resolve('C(John,Joe)', set());
        a = homework3.resolve('A(John)', set());

        self.assertEqual(False, homework3.resolve('F(Joe)', set()));
        self.assertNotEqual(False, homework3.resolve('H(John)', set()));
        self.assertNotEqual(False, homework3.resolve('~H(Alice)', set()));
        self.assertEqual(False, homework3.resolve('~H(John)', set()));
        self.assertEqual(False, homework3.resolve('G(Joe)', set()));
        self.assertNotEqual(False, homework3.resolve('G(Tom)', set()));


    def test_4(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'test4.txt')
        self.assertEqual(False, homework3.resolve('Kills(Curiosity,Tuna)', set()));

    def test_5(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'test5.txt')
        self.assertNotEqual(False, homework3.resolve('L(Tony,Snow)', set()));

    def test_dropbox(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'input.txt')
        self.assertNotEqual(False, homework3.resolve('B(John)', set()));
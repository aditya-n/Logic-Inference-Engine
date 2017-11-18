from unittest import TestCase
import homework3, os

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
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'tests/input3.txt')
        self.assertNotEqual(False, homework3.resolve('Criminal(West)', set()));
        pass

    def test_2(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'tests/input2.txt')
        a = homework3.apply_unifiers('Ancestor(x,z)', {'x': 'Liz', 'z': 'Joe'})

        self.assertNotEqual(False, homework3.resolve('Ancestor(Liz,Billy)', set()));
        self.assertEqual(False, homework3.resolve('Ancestor(Liz,Joe)', set()));

    def test_1(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'tests/input1.txt')

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
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'tests/input12.txt')
        a = homework3.resolve('Animal(Tuna)', set());
        a = homework3.resolve('AnimalLover(Jack)', set());
        a = homework3.resolve('~Kills(Jack,Tuna)', set());
        self.assertNotEqual(False, homework3.resolve('Kills(Curiosity,Tuna)', set()));

    def test_5(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'tests/input13.txt')
        self.assertNotEqual(False, homework3.resolve('L(Tony,Snow)', set()));

    def test_input(self):
        homework3.queries, homework3.KB_sentences = [], []
        homework3.getInputs(homework3.queries, homework3.KB_sentences, 'input.txt')
        a = homework3.resolve('B(Ada)', set());
        pass

    def test_dropbox(self):
        for i in range(1,15):
            homework3.queries, homework3.KB_sentences = [], []
            homework3.getInputs(homework3.queries, homework3.KB_sentences, os.path.join('tests', 'input' + str(i) + '.txt'))
            with open(os.path.join('tests', 'output' + str(i) + '.txt'), 'r') as output_file:
                lines = output_file.readlines()
                j = 0
                for output_line in lines:
                    result = homework3.resultInCorrectOutputFormat(homework3.queries[j])
                    self.assertEqual(output_line.strip('\n'), result)
                    j += 1
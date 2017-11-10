from unittest import TestCase
import homework3

class TestInference(TestCase):
    def test_getInputs(self):
        homework3.getInputs(homework3.queries, homework3.sentences, 'input.txt')
        self.assertEqual(1, len(homework3.queries))
        self.assertEqual(8, len(homework3.sentences))
        self.assertEqual(False, homework3.resolveByImplication('R(x)'))
        self.assertEqual(False, homework3.resolveByOrElimination('R(x)'))
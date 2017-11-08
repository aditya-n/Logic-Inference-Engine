from unittest import TestCase
import homework3

class TestInference(TestCase):
    def test_getInputs(self):
        homework3.getInputs()
        self.assertEqual(6, len(homework3.queries))
        self.assertEqual(14, len(homework3.sentences))
        self.assertEqual('~W', homework3.negation('W'))
        self.assertEqual('W', homework3.negation('~W'))
import unittest

class TestAdd(unittest.TestCase):

    def test_details(self):
        self.assertEqual(add(3, 4), 7)
        self.assertEqual(add(-1, 1), 0)

import functions as fa

fa.getDetails()

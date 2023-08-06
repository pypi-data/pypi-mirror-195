from unittest import TestCase
from src.eon4dice import dice


class Test(TestCase):
    def test_roll(self):
        test_strings = [
            '5T6+2',
            '1T6',
            '1t100',
            '2T6+0'
        ]
        for test in test_strings:
            assert(dice.roll(test) > 0)

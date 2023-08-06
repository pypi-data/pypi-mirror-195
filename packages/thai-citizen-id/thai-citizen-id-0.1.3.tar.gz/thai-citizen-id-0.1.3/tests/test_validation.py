import unittest
from thai_citizen_id import validate


class TestThaiCitizenIdValidation(unittest.TestCase):

    def test_validation_valid(self):
        self.assertEqual(validate("4854701245289"), True)
        self.assertEqual(validate("1654254291038"), True)
        self.assertEqual(validate("4221843650658"), True)
        self.assertEqual(validate("5132666814025"), True)
        self.assertEqual(validate("7651971135811"), True)
        self.assertEqual(validate("1170847908779"), True)

    def test_validation_invalid_type(self):
        self.assertEqual(validate(4854701245289), False)
        self.assertEqual(validate(4854701245289.0), False)
        self.assertEqual(validate("48547012s5289"), False)
        self.assertEqual(validate("485470125289 "), False)
        self.assertEqual(validate("485470125282a"), False)

    def test_validation_invalid_len(self):
        self.assertEqual(validate("48547012452892"), False)
        self.assertEqual(validate("485470124528"), False)


def main():
    unittest.main()


if __name__ == '__main__':
    main()

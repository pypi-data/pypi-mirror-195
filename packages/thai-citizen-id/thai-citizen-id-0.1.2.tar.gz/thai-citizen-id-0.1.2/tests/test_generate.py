import unittest
from thai_citizen_id import generate, validate
import random


class TestThaiCitizenIdGenerate(unittest.TestCase):

    def test_generate_without_seed(self):
        list_citizen: list[int] = []
        for _ in range(30):
            list_citizen.append(generate())
        self.assertEqual(checkUniqueList(list_citizen), True)
        self.assertEqual(checkValidAllList(list_citizen), True)

    def test_generate_with_seed(self):
        seed = random.randint(0, 1000000000)
        list_citizen: list[int] = []
        for _ in range(30):
            list_citizen.append(generate(seed))
        self.assertEqual(checkUniqueList(list_citizen), False)
        self.assertEqual(checkValidAllList(list_citizen), True)


def checkUniqueList(list_data: list[str]) -> bool:
    set_data = set(list_data)
    return len(list_data) == len(set_data)


def checkValidAllList(list_data: list[str]) -> bool:
    for i in list_data:
        if not validate(i):
            return False
    return True


def main():
    unittest.main()


if __name__ == '__main__':
    main()

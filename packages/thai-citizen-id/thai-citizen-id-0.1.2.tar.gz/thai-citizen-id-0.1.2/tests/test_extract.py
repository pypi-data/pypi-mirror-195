import unittest
from thai_citizen_id import extract


class TestThaiCitizenIdExtract(unittest.TestCase):

    def test_extract(self):
        self.assertEqual(extract("1234567890121"), {
                         'person_type': 'คนที่เกิดและมีสัญชาติไทยและได้แจ้งเกิดภายในกำหนดเวลา', 'born_address': 'Not found', 'first_order': 67890, 'second_order': 12})
        self.assertEqual(extract("2660835443125"), {
                         'person_type': 'คนที่เกิดและมีสัญชาติไทยได้แจ้งเกิดเกินกำหนดเวลา', 'born_address': 'ทับคล้อ', 'first_order': 35443, 'second_order': 12})
        self.assertEqual(extract("6270997890131"), {
                         'person_type': 'ผู้ที่เข้าเมืองโดยไม่ชอบด้วยกฎหมาย และผู้ที่เข้าเมืองโดยชอบด้วยกฎหมายแต่อยู่ในลักษณะชั่วคราว', 'born_address': 'วังสมบูรณ์', 'first_order': 97890, 'second_order': 13})

    def test_extract_invalid_citizen_id(self):
        with self.assertRaises(ValueError) as err:
            extract("23131")
        the_exception = err.exception
        self.assertEqual(the_exception.__str__(), 'Citizen ID is not valid')

        with self.assertRaises(ValueError) as err:
            extract("23131dasdaasdada")
        the_exception = err.exception
        self.assertEqual(the_exception.__str__(), 'Citizen ID is not valid')

        with self.assertRaises(ValueError) as err:
            extract("1234567890120")
        the_exception = err.exception
        self.assertEqual(the_exception.__str__(), 'Citizen ID is not valid')


def main():
    unittest.main()


if __name__ == '__main__':
    main()

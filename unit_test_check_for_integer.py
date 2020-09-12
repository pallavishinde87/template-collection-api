import unittest


def checkInteger(val):
    return True if int(val) else False


class CheckStringToIntegerValue(unittest.TestCase):
    def test_check_string_to_integer(self):
        self.assertTrue(checkInteger('123a'))


if __name__ == '__main__':
    unittest.main()

import unittest

from jtwcalive.parser.parser import Parser


class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = Parser("../outputs/jtwc_2023073109.txt")

    def test_init(self):
        with self.assertRaises(FileNotFoundError):
            Parser("not_exist.txt")

    def test_parse(self):
        f = Parser("C:\Users\Shengbin Jia\git\jtwc_alive\jtwcalive\outputs\jtwc_2023073109.txt")
        tc = f.parse()

        self.assertEqual(tc.src, "test")
        self.assertEqual(tc.typhoon_id, "06W")
import unittest

from jtwcalive.parser.parser import Parser


class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = Parser("../outputs/jwtc_2023073109.txt")

    def test_init(self):
        with self.assertRaises(FileNotFoundError):
            Parser("not_exist.txt")

    def test_parse(self):
        self.c.parse()
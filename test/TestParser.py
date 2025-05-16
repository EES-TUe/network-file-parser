import unittest
from NetworFileParser.GnfParser import GnfParser

class Test(unittest.TestCase):

    def setUp(self):
        self.gnf_parser = GnfParser("Alliander_Arch1_Net1_anoniem_2023_Q2.gnf")

    def test_gnf_parser(self):
        self.gnf_parser.parse_file()
        self.gnf_parser.write_all_data_frames()

if __name__ == '__main__':
    unittest.main()
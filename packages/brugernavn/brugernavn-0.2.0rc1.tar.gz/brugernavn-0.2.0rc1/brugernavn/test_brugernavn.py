import unittest
from brugernavn import Brugernavn


class BrugernavnTest(unittest.TestCase):
    def setUp(self):
        self.brugernavn = Brugernavn("username", "ressources/tests.json")

    def testSearchQuiet(self):
        brugernavn = self.brugernavn
        brugernavn.search_quiet()

    def testSearchLoud(self):
        brugernavn = self.brugernavn
        brugernavn.search_loud()


if __name__ == "__main__":
    unittest.main()

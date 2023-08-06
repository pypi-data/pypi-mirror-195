#import .brugernavn
from .brugernavn import Brugernavn

class Tests():
    def __init__(self):
        self.brugernavn = Brugernavn("username", "ressources/tests.json")
    def test_search_quiet(self):
        brugernavn = self.brugernavn
        brugernavn.search_quiet()
    def test_search_loud(self):
        brugernavn = self.brugernavn
        brugernavn.search_loud()

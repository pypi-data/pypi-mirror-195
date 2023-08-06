import typer
from brugernavn import Brugernavn


def search(username: str):
    brugernavn = Brugernavn(username)
    brugernavn.search_loud()


if __name__ == "__main__":
    typer.run(search)

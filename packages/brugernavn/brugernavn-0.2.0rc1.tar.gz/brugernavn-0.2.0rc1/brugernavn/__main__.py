from pathlib import Path
import typer
from enum import Enum

from brugernavn import Brugernavn

app = typer.Typer()


class ShowOptions(str, Enum):
    all = "all"
    error = "error"
    available = "available"
    unavailable = "unavailable"


@app.command()
def search(
    username: str,
    show: ShowOptions = ShowOptions.all,
    use_list: Path = typer.Option(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        default=f"{Path(__file__).parent.resolve()}/ressources/data.json",
    ),
    check_only: str = "None",
):
    brugernavn = Brugernavn(username)
    if check_only == "None":
        brugernavn.search_loud(show)
    else:
        brugernavn.search_loud_only(check_only, show)


if __name__ == "__main__":
    app()

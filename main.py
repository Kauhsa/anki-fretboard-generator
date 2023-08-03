import typer
import random
from pathlib import Path

from typing import Optional
from typing_extensions import Annotated
from notes import get_note_by_id
from generate_anki import generate_anki_deck


app = typer.Typer(add_completion=False)


def note_list(value: str) -> list[str]:
    return [get_note_by_id(x) for x in value.split(",")]


def positive_float_list(value: str) -> list[float]:
    def convert(x: str) -> float:
        val = float(x)
        if val <= 0:
            raise ValueError("Width must be greater than 0.")
        return val

    return [convert(x) for x in value.split(",")]


@app.command()
def generate_deck(
    name: Annotated[str, typer.Option()],
    output_path: Annotated[Path, typer.Option()],
    deck_id: Annotated[Optional[int], typer.Option()] = None,
    tuning: Annotated[str, typer.Option(parser=note_list)] = "E,A,D,G,B,E",
    widths: Annotated[
        str, typer.Option(parser=positive_float_list)
    ] = "3,2.5,2,1.5,1,1",
    frets: Annotated[int, typer.Option()] = 21,
):
    if len(tuning) != len(widths):
        raise ValueError("Tuning and widths must have the same length.")

    if frets <= 0:
        raise ValueError("Frets must be greater than 0.")

    id = id if deck_id else random.randrange(1 << 30, 1 << 31)

    generate_anki_deck(
        id=id,
        name=name,
        tuning=tuning,
        widths=widths,
        frets=frets,
        output_path=output_path,
    )


if __name__ == "__main__":
    app()

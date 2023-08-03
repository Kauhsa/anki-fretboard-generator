import genanki
import tempfile
from pathlib import Path
from notes import Note, add_semitones
from generate_fretboard import generate_fretboard_svg, Position


def generate_anki_deck(
    id: int,
    name: str,
    tuning: list[Note],
    widths: list[float],
    frets: int,
    output_path: str,
):
    fretboard_model = genanki.Model(
        model_id=id + 1,
        name="Fretboard",
        fields=[
            {"name": "String"},
            {"name": "Fret"},
            {"name": "Note"},
            {"name": "Image"},
        ],
        templates=[
            {
                "name": "Fretboard Card",
                "qfmt": "{{Image}}",
                "afmt": '{{FrontSide}}<h1 style="text-align: center;">{{Note}}</h1>',
            },
        ],
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        deck = genanki.Deck(id, name)
        media_files = []

        for string_number, string_note in enumerate(tuning):
            for fret_number in range(frets):
                image = generate_fretboard_svg(
                    fret_count=frets,
                    string_widths=widths,
                    highlight_position=Position(fret=fret_number, string=string_number),
                )

                filename = f"{string_number}-{fret_number}.svg"
                full_path = Path(tmpdir, filename)
                with open(full_path, "w") as f:
                    f.write(image)
                media_files.append(full_path)

                image_definition = f"""<img src="{filename}">"""
                fret_note = add_semitones(string_note, fret_number)
                note = genanki.Note(
                    model=fretboard_model,
                    guid=genanki.guid_for(fret_number, string_number, fret_note),
                    fields=[
                        str(string_number),
                        str(fret_number),
                        fret_note.label(),
                        image_definition,
                    ],
                )
                deck.add_note(note)

        package = genanki.Package(deck)
        package.media_files = media_files
        package.write_to_file(output_path)

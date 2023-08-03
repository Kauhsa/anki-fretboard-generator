class Note:
    def __init__(self, ids: set[str], names: list[str]):
        self.ids = ids
        self.names = names

    def label(self):
        return "/".join(self.names)

    def __str__(self):
        return self.label()

    def __repr__(self) -> str:
        return f"Note({str(self)})"

    def matches_id(self, id: str) -> bool:
        return id in self.ids


notes = [
    Note({"C"}, ["C"]),
    Note({"C#", "Db"}, ["C♯", "D♭"]),
    Note({"D"}, ["D"]),
    Note({"D#", "Eb"}, ["D♯", "E♭"]),
    Note({"E"}, ["E"]),
    Note({"F"}, ["F"]),
    Note({"F#", "Gb"}, ["F♯", "G♭"]),
    Note({"G"}, ["G"]),
    Note({"G#", "Ab"}, ["G♯", "A♭"]),
    Note({"A"}, ["A"]),
    Note({"A#", "Bb"}, ["A♯", "B♭"]),
    Note({"B"}, ["B"]),
]


def get_note_by_id(id: str) -> Note:
    for note in notes:
        if note.matches_id(id):
            return note
    raise ValueError(f"Note with id '{id}' not found.")


def add_semitones(note: Note, semitones: int) -> Note:
    note = get_note_by_id(next(iter(note.ids)))
    index = notes.index(note)
    return notes[(index + semitones) % len(notes)]

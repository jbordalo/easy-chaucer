from typing import List
from note import Note
import re

class Line:
    def __init__(self, text: str):
        self.text = text
        self.notes = []

    def add_notes(self, notes: List[Note]):
        self.notes += notes

    def get_text(self) -> str:
        return self.text

    def set_text(self, line: str):
        self.text = line

    def has_notes(self) -> bool:
        return self.notes != []

    def get_notes(self) -> List[Note]:
        return self.notes[::-1]

    def __str__(self) -> str:
        return f"{repr(self.text)} ; {', '.join([str(note) for note in self.get_notes()])} "


def is_verse(line):
    return not re.match(r'^\d+[\.:]?.*', line)


# pre-condition: not is_verse
def is_simple_note(line):
    assert not is_verse(line)
    try:
        int(line.split(maxsplit=1)[0])
        return True
    except ValueError:
        return False


def is_multiline_note(line):
    try:
        start, end = line.split(maxsplit=1)[0].split('-')
        int(start)
        int(end)
        return True
    except Exception:
        return False


def is_special(line_text: str) -> bool:
    # account for 2 and 4 space tabs
    return len(line_text) > len(line_text.lstrip())

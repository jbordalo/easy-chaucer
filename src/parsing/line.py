from typing import List
from note import Note


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

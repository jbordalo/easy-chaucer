class Note:
    def __init__(self, span: str, note_text: str):
        self.span = span
        self.note_text = note_text

    def get_span(self):
        return self.span

    def get_note_text(self):
        return self.note_text

    def __str__(self) -> str:
        return f"{self.span}: {self.note_text}"

from typing import List, Dict
import re
from create_html_lines import construct_lines_with_notes
from line import Line
from note import Note

NOTE_TAG = "NOTE: "


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


def expand_note(verse: str, full_note: str):
    # Grab the number and position of each note
    colon_position = full_note.rfind(":")
    if colon_position == -1:
        return []

    # All on the right is surely the note
    note_text = full_note[colon_position+1:].strip()

    new_line = full_note[:colon_position].strip()
    word_by_word = new_line.split()

    # Assume the first word will always be part of it
    span = [word_by_word.pop()]

    while " ".join([word_by_word[-1]] + span).lower() in verse.lower():
        span.insert(0, word_by_word.pop())

    span_text = " ".join(span)

    note_span = span_text

    span_idx = full_note.find(span_text)

    nxt = full_note[:span_idx]

    return [Note(note_span, note_text)] + expand_note(verse, nxt)


def parse_multiline_notes(lines: List[Line], line: str, colon_position: int, start: int, end: int):
    # All on the right is surely the note
    note_text = line[colon_position + 1:].strip()

    new_line = line[:colon_position].strip()
    word_by_word = new_line.split()[1:]
    span = [word_by_word.pop()]

    while " ".join([word_by_word[-1]] + span).lower() in lines[end-1].get_text().lower():
        span.insert(0, word_by_word.pop())

    # TODO I'm not sure why this has no conditionals

    lines[end-1].add_notes([Note(" ".join(span), note_text)])

    lines[start-1].add_notes([Note(" ".join(word_by_word), note_text)])


def get_multiline_range(start_str: str, end_str: str):
    start = int(start_str)
    end = int(end_str)

    # For cases such as: '1025-29'
    if end < start:
        end = int(start_str[:-2] + end_str)

    return start - chapter_initial_line + 1, end - chapter_initial_line + 1


def is_special(line: str):
    return line.startswith("\t")


if __name__ == '__main__':
    lines: List[Line] = []

    chapter = "knights-tale"
    chapter_initial_line = 859

    with open(f'raw_{chapter}.txt', 'r') as f:
        """
            A line can be a normal line, a special line (incipit, explicit), a simple note, a multiline note
        """
        for line in f:
            if is_verse(line):
                lines.append(Line(line))
            elif is_simple_note(line):
                note_number = int(line.split(maxsplit=1)[0])
                note_number = note_number - chapter_initial_line + 1
                exp_notes = expand_note(lines[note_number-1].get_text(), line)

                lines[note_number - 1].add_notes(exp_notes)
            elif is_multiline_note(line):
                start_str, end_str = line.split(maxsplit=1)[0].split('-')
                start, end = get_multiline_range(start_str, end_str)

                colon_position = line.find(":")

                if start == end - 1 and colon_position != -1:
                    parse_multiline_notes(
                        lines, line, colon_position, start=start, end=end)
                else:
                    lines[end-1].add_notes(
                        [Note("", line.split(maxsplit=1)[1].strip())]
                    )
            else:
                # Unexpected behavior
                print("Couldn't find type of line for line:")
                print(line)

    with open(f'new_{chapter}.txt', 'w') as lines_file, open(f'new_{chapter}_notes.txt', 'w') as notes_file:
        for line_number, line in enumerate(lines):
            lines_file.write(line.get_text())

            for note in line.get_notes():
                if not note.get_span():
                    out = f"{line_number + 1} {note.get_note_text()}"
                    notes_file.write(out)
                else:
                    out = f"{line_number + 1} {note}"
                    notes_file.write(out)

                notes_file.write("\n")

    lines_html = construct_lines_with_notes(lines)

    with open(f'new_{chapter}_html.txt', 'w') as f:
        for line in lines_html:
            f.write(line.get_text())

from typing import List, Tuple, Dict
import re
from create_html_lines import construct_lines_with_notes
from line import Line, is_special, is_verse, is_simple_note, is_multiline_note
from note import Note

NOTE_TAG = "NOTE: "


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

    lines[end-1].add_notes([Note(" ".join(span), note_text)])

    lines[start-1].add_notes([Note(" ".join(word_by_word), note_text)])


def get_multiline_range(start_str: str, end_str: str):
    start = int(start_str)
    end = int(end_str)

    # For cases such as: '1025-29'
    if end < start:
        end = int(start_str[:-2] + end_str)

    return start - chapter_initial_line + 1, end - chapter_initial_line + 1


def parse_special_line(special_lines: Dict[str, Tuple[Line, int]], line: str, line_index: int):
    if line.lstrip().startswith(NOTE_TAG):
        # Assuming these notes are single notes
        span, note_text = line.replace(NOTE_TAG, "").split(":")

        assert span.strip() in special_lines

        special_lines[span.strip()][0].add_notes(
            [Note(span, note_text.strip())])
    else:
        special_lines[line.strip()] = (Line(line), line_index)


def insert_special_lines(lines: List[Line], special_lines: Dict[str, Tuple[Line, int]]):
    # Insert sort, but leverages the order of insertion of the map to order consecutive special lines correctly
    # Python guarantees that iteration order is the same as insertion order
    ordered_special_lines = []
    for line, idx in special_lines.values():
        insert_idx = 0
        for _, e_idx in ordered_special_lines:
            if e_idx > idx:
                insert_idx += 1

        ordered_special_lines.insert(insert_idx, (line, idx))

    for line, idx in ordered_special_lines:
        lines.insert(idx, line)


if __name__ == '__main__':
    lines: List[Line] = []
    special_lines: Dict[str, Tuple[Line, int]] = {}

    chapter = "knights-tale"
    chapter_initial_line = 859

    with open(f'raw_{chapter}.txt', 'r') as f:
        """
            A line can be a normal line, a special line (incipit, explicit), a simple note, a multiline note
        """
        for line in f:
            if is_special(line):
                parse_special_line(special_lines, line, len(lines))
            elif is_verse(line):
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

    insert_special_lines(lines, special_lines)

    with open(f'{chapter}.txt', 'w') as lines_file, open(f'{chapter}_notes.txt', 'w') as notes_file:
        line_number = 1
        for line in lines:
            lines_file.write(line.get_text())

            for note in line.get_notes():
                if is_special(note.get_span()):
                    notes_file.write(str(note))
                else:
                    out = f"{line_number} {note}"
                    notes_file.write(out)

                notes_file.write("\n")

            if not is_special(line.get_text()):
                line_number += 1

    lines_html = construct_lines_with_notes(lines)

    with open(f'{chapter}_html.txt', 'w') as f:
        for line in lines_html:
            f.write(line.get_text())

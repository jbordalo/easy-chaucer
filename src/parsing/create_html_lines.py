from typing import Tuple, List, Dict
import re
import html

lines = []


def split_number_and_note(line: str) -> Tuple[int, str]:
    return re.match(r'^(\d+)\s*(.*)', line).groups()


def transform_line(line: str, span: str, note_text: str) -> str:
    if not span:
        new_line = f"<dfn data-note=\"{note_text}\">{line}</dfn>\n"
    else:
        found_span = re.search(
            rf'(?:\b|\s)({re.escape(span)})(?:\b|\s|$)', line, re.IGNORECASE)

        if not found_span:
            print(span)
            print(re.escape(span))
            print(line)
            print("ERROR:", line)
            exit(1)

        start = found_span.start(1)
        end = found_span.end(1)
        new_line = line[:start] + \
            f"<dfn data-note=\"{html.escape(note_text)}\">{span}</dfn>" + \
            line[end:]

    return new_line


def construct_lines_with_notes(lines: List[str], notes: List[str]):
    lines_html = lines.copy()

    for note in notes:
        note_number, note_text = split_number_and_note(note)

        colon_position = note_text.find(":")
        if colon_position != -1:
            span, note_text = note_text.split(":")
        else:
            span = ""

        note_number = int(note_number)

        new_line = transform_line(
            lines_html[note_number-1], span.strip(), note_text.strip())
        lines_html[note_number-1] = new_line

    return lines_html

from typing import Tuple, List
import re
import html

from line import Line


def split_number_and_note(line: str) -> Tuple[int, str]:
    return re.match(r'^(\d+)\s*(.*)', line).groups()


def transform_line(line: Line, span: str, note_text: str) -> str:
    if not span:
        new_line = f"<dfn data-note=\"{note_text}\">{line.get_text()}</dfn>\n"
    else:
        found_span = re.search(
            rf'(?:\b|\s)({re.escape(span)})(?:\b|\s|$)', line.get_text(), re.IGNORECASE)

        if not found_span:
            print(span)
            print(re.escape(span))
            print(line)
            print("ERROR:", line)
            exit(1)

        start = found_span.start(1)
        end = found_span.end(1)
        new_line = line.get_text()[:start] + \
            f"<dfn data-note=\"{html.escape(note_text)}\">{span}</dfn>" + \
            line.get_text()[end:]

    line.set_text(new_line)


def construct_lines_with_notes(lines: List[Line]) -> List[Line]:
    lines_html = lines.copy()

    for line in lines_html:
        if not line.has_notes():
            continue

        for note in line.get_notes():
            transform_line(
                line, note.get_span(), note.get_note_text()
            )

    return lines_html

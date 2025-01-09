import re
import html

files = {
    "General Prologue": ["prologue.txt", "prologue_notes.txt"]
}

lines = []


def split_number_and_note(line):
    return re.match(r'^(\d+)\s*(.*)', line).groups()


def transform_line(line, span, note_text):
    if not span:
        new_line = f"<dfn data-note=\"{note_text}\">{line}</dfn>\n"
    else:
        found_span = re.search(rf'(?:\b|\s)({re.escape(span)})(?:\b|\s|$)', line, re.IGNORECASE)

        if not found_span:
            print(span)
            print(re.escape(span))
            print(line)
            print("ERROR:", line)
            exit(1)

        start = found_span.start(1)
        end = start + len(span)
        new_line = line[:start] + f"<dfn data-note=\"{html.escape(note_text)}\">{span}</dfn>" + line[end:]

        print(line, start, end, new_line, span, sep=";")

    return new_line


def load_lines(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def construct_lines_with_notes(filename, lines):
    with open(filename, 'r') as f:
        for note in f:
            note_number, note = split_number_and_note(note)

            colon_position = note.find(":")
            if colon_position != -1:
                span, note_text = note.split(":")
            else:
                span = ""
                note_text = note

            note_number = int(note_number)

            new_line = transform_line(lines[note_number-1], span.strip(), note_text.strip())
            lines[note_number-1] = new_line


def get_page_lines(page):
    lines = load_lines(f"db/{files[page][0]}")

    construct_lines_with_notes(f"db/{files[page][1]}", lines)

    return lines

if __name__ == '__main__':
    lines = load_lines('prologue.txt')

    construct_lines_with_notes('prologue_notes.txt', lines)

    with open('trash.txt', 'w') as f:
        for line in lines:
            f.write(line)
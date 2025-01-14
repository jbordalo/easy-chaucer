import re
import html

metadata = {
    "general-prologue": {
        "title": "General Prologue",
        "incipit": "Here bygynneth the Book of the Tales of Caunterbury.",
        "file_root_name": "prologue"
    },
    "knights-tale": {
        "title": "Knight's Tale",
        "incipit": "Heere bigynneth the Knyghtes Tale.",
        "file_root_name": "knights-tale"
    },
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
        end = found_span.end(1)
        new_line = line[:start] + f"<dfn data-note=\"{html.escape(note_text)}\">{span}</dfn>" + line[end:]

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


def get_chapter_info(chapter):
    lines = load_lines(f"db/{metadata[chapter]['file_root_name']}.txt")

    construct_lines_with_notes(f"db/{metadata[chapter]['file_root_name']}_notes.txt", lines)

    title = metadata[chapter]["title"]
    incipit = metadata[chapter]["incipit"]

    return (title, incipit, lines)

if __name__ == '__main__':
    chapter = "knights-tale"
    lines = load_lines(f'{chapter}.txt')

    construct_lines_with_notes(f'{chapter}_notes.txt', lines)

    with open('trash.txt', 'w') as f:
        for line in lines:
            f.write(line)
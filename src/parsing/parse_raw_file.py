import re


def is_verse(line):
    return not re.match(r'^\d+[\.:]?.*', line)


#pre-condition: not is_verse
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


def expand_note(verse: str, line: str):
    note = {
        "span": "",
        "note_text": ""
    }

    # Grab the number and position of each note
    colon_position = line.rfind(":")
    if colon_position == -1:
        return []

    # All on the right is surely the note
    note["note_text"] = line[colon_position+1:].strip()

    new_line = line[:colon_position].strip()
    word_by_word = new_line.split()

    # Assume the first word will always be part of it
    span = [word_by_word.pop()]

    while " ".join([word_by_word[-1]] + span).lower() in verse.lower():
        span.insert(0, word_by_word.pop())

    span_text = " ".join(span)

    note["span"] = span_text

    span_idx = line.find(span_text)

    nxt = line[:span_idx]

    return [note] + expand_note(verse, nxt)


def parse_multiline_notes(line, colon_position, start, end):
    # All on the right is surely the note
    note_text = line[colon_position + 1:].strip()

    new_line = line[:colon_position].strip()
    word_by_word = new_line.split()[1:]
    span = [word_by_word.pop()]

    while " ".join([word_by_word[-1]] + span).lower() in lines[end-1].lower():
        span.insert(0, word_by_word.pop())
    notes[end].append({
        "span": " ".join(span),
        "note_text": note_text
    })

    if not start in notes:
        notes[start] = []

    notes[start].append({
        "span": " ".join(word_by_word),
        "note_text": note_text
    })

lines = []
notes: dict = {}


def get_multiline_range(start_str: str, end_str: str):
    start = int(start_str)
    end = int(end_str)

    # For cases such as: '1025-29'
    if end < start:
        end = int(start_str[:-2] + end_str)

    return start - offset + 1, end - offset + 1


if __name__ == '__main__':
    chapter="knights-tale"
    offset=859

    with open(f'raw_{chapter}.txt', 'r') as f:
        """
        Line can be a normal line, a simple note, a multiline note
        """
        for line in f:
            if is_verse(line):
                lines.append(line)
            elif is_simple_note(line):
                note_number = int(line.split(maxsplit=1)[0])
                note_number = note_number - offset + 1
                exp_notes = expand_note(lines[note_number-1], line)
                if not note_number in notes:
                    notes[note_number] = []
                notes[note_number] += exp_notes[::-1]
            elif is_multiline_note(line):
                start_str, end_str = line.split(maxsplit=1)[0].split('-')
                start, end = get_multiline_range(start_str, end_str)

                colon_position = line.find(":")
                if not end in notes:
                    notes[end] = []

                if start == end-1 and colon_position != -1:
                    parse_multiline_notes(line, colon_position, start=start, end=end)
                else:
                    notes[end].append({
                        "span": "",
                        "note_text": line.split(maxsplit=1)[1].strip()
                    })     
            else:
                # Unexpected behavior
                print("Couldn't find type of line for line:")
                print(line)

    with open(f'{chapter}.txt', 'w') as f:
        for line in lines:
            f.write(line)

    with open(f'{chapter}_notes.txt', 'w') as f:
        for note_number in notes.keys():
            for note in notes.get(note_number):
                if not note['span']:
                    f.write(f"{note_number} {note['note_text']}")
                else:
                    f.write(f"{note_number} {note['span']}: {note['note_text']}")
                f.write("\n")
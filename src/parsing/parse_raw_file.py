import re

def is_verse(line):
    return not re.match(r'^\d+[\.:]?.*', line)


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


def parse_multiline_notes(line, colon_position):
        # All on the right is surely the note
    note_text = line[colon_position+1:].strip()

    new_line = line[:colon_position].strip()
    word_by_word = new_line.split()[1:]
    endingspan = " ".join(word_by_word[-2:])
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

with open('raw_prologue.txt', 'r') as f:
    """
        For normal notes you might have ellipsis, which will make the algorithm fail
        For multiline notes
        If n-n+1 interpret the whole thing as 1, likely split at Upper case word, since new verse
        If no note found (no colon), it's an explanation, add it to the first verse
    """

    for line in f:
        if is_verse(line):
            lines.append(line)
        else:
            try:
                note_number = int(line.split(maxsplit=1)[0])
                exp_notes = expand_note(lines[note_number-1], line)
                if not note_number in notes:
                    notes[note_number] = []
                notes[note_number] += exp_notes[::-1]
            except ValueError:
                # In this case, the note is multiline
                start_str, end_str = line.split(maxsplit=1)[0].split('-')
                start = int(start_str)
                end = int(end_str)
                if end < start:
                    end = int(start_str[:-2] + end_str)

                colon_position = line.find(":")

                if not end in notes:
                    notes[end] = []

                # If n-n+1 interpret the whole thing as 1, likely split at Upper case word, since new verse
                if start == end-1 and colon_position != -1:
                    parse_multiline_notes(line, colon_position)
                else:
                    notes[end].append({
                        "span":"",
                        "note_text": line.split(maxsplit=1)[1].strip()
                    })
            except IndexError:
                print(line)
                exit(0)
               

             

with open('prologue.txt', 'w') as f:
    for line in lines:
        f.write(line)

with open('prologue_notes.txt', 'w') as f:
    for note_number in notes.keys():
        for note in notes.get(note_number):
            if not note['span']:
                f.write(f"{note_number} {note['note_text']}")
            else:
                f.write(f"{note_number} {note['span']}: {note['note_text']}")
            f.write("\n")
import re


def is_verse(line):
    return not re.match(r'^\d+[\.:]?.*', line)


def expand_note(verse, line):
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

    while " ".join([word_by_word[-1]] + span) in verse:
        span.insert(0, word_by_word.pop())

    span_text = " ".join(span)

    note["span"] = span_text

    span_idx = line.find(span_text)

    nxt = line[:span_idx]

    return [note] + expand_note(verse, nxt)


lines = []
notes: dict = {}

with open('raw_prologue.txt', 'r') as f:
    for line in f:
        if is_verse(line):
            lines.append(line)
        else:
            try:
                note_number = int(line.split(maxsplit=1)[0])
                exp_notes = expand_note(lines[note_number], line)
                notes[note_number] = exp_notes
            except ValueError:
                # In this case, the note is multiline
                # TODO
                pass

with open('prologue.txt', 'w') as f:
    for line in lines:
        f.write(line)

with open('prologue_notes.txt', 'w') as f:
    for note_number in notes.keys():
        for note in notes.get(note_number):
            f.write(f"{note_number} {note['span']}: {note['note_text']}")
            f.write("\n")
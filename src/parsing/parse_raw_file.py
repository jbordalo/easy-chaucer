import re

"""
TODO:
Parse notes in a special way, you can't use the upper case function with multiline notes
A line of notes ends when another starts (with digits)
A line of notes may have multiple notes. I'll assume they are separated by ":" 
"""


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
    for i, line in enumerate(f):
        if is_verse(line):
            lines.append(line)
        else:
            note_number = int(line.split(maxsplit=1)[0])
            exp_notes = expand_note(lines[note_number - 1], line)
            notes[i] = exp_notes

with open('prologue.txt', 'w') as f:
    for i, line in enumerate(lines):
        f.write(line)
        f.write("\n")

with open('prologue_notes.txt', 'w') as f:
    for i, line in enumerate(notes):
        f.write(line)
        f.write("\n")
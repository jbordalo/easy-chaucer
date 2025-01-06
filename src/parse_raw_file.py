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
    notes = []

    # Find all matches of words in the verse and line
    verse_words = re.findall(r'\b\w+\b', verse)
    line_words = re.findall(r'\b\w+\b', line)
    
    matches = set(verse_words) & set(line_words)  # Find common words
    
    # For each match found, find the note associated with the match
    for match in matches:
        # Find the span (the start of the note)
        note_start = line.find(match)
        
        # Extract everything from the colon (:) to the next match (or end of line)
        note_text = line[note_start:].split(":")[1].strip()
        
        # Add note info to the notes list
        notes.append({
            "verse": verse.split(maxsplit=1)[0],  # Grab verse number
            "span": match,  # Matched word/phrase
            "text": note_text  # Extracted note text after the colon
        })
    
    return notes


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
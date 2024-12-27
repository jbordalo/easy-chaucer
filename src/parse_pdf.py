import pytesseract
from pdf2image import convert_from_path
import re

"""
TODO:
Parse notes in a special way, you can't use the upper case function with multiline notes
A line of notes ends when another starts (with digits)
"""

def fn(line):
    return line != ""

def is_verse(line):
    return not re.match(r'^\d+[\.:]?.*', line)

def reconstruct(lines):
    new_lines = []

    for l in lines:
        if not l[0].islower():
            new_lines.append(l)
        else:
            new_lines[-1] += ' ' + l

    return new_lines

pages = convert_from_path("canterbury_tales.pdf", last_page=1)

cropped_pages=[]

for i, page in enumerate(pages):
    width, height = page.size
    cropped_page = page.crop((0, 150, width, height))
    cropped_pages.append(cropped_page)

lines = []

for page in cropped_pages:
    page_text = pytesseract.image_to_string(page)

    lines = page_text.split("\n")
    lines = list(filter(fn, lines))

    # Manual clean up
    lines = lines[6:]

    lines = reconstruct(lines)
    lines = list(filter(is_verse, lines))


with open('text.txt', 'w') as f:
    for i, line in enumerate(lines):
        f.write(str(i+1))
        f.write(' ')
        f.write(line)
        f.write("\n")
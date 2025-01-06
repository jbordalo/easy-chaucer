import pytesseract
from pdf2image import convert_from_path
import re

"""
TODO:
Parse notes in a special way, you can't use the upper case function with multiline notes
A line of notes ends when another starts (with digits)
A line of notes may have multiple notes. I'll assume they are separated by ":" 
"""

def line_filter(line):
    return line != ""

def reconstruct(lines):
    new_lines = []

    for l in lines:
        if not l[0].islower():
            new_lines.append(l)
        else:
            new_lines[-1] += ' ' + l

    return new_lines

pages = convert_from_path("canterbury_tales.pdf", last_page=14)

cropped_pages = []

for i, page in enumerate(pages):
    width, height = page.size
    cropped_page = page.crop((0, 150, width, height))
    cropped_pages.append(cropped_page)

lines = []

for page in cropped_pages:
    page_text = pytesseract.image_to_string(page)

    l = page_text.split("\n")
    l = list(filter(line_filter, l))

    l = reconstruct(l)
    lines.extend(l)

with open('raw_prologue.txt', 'w') as f:
    for i, line in enumerate(lines):
        f.write(line)
        f.write("\n")
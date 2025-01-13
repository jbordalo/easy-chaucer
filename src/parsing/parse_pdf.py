import pytesseract
from pdf2image import convert_from_path
import re

chapter_ranges = {
    "prologue" : (0, 14),
    "knights-tale" : (15, 44),
    "millers-prologue" : (44, 45),
    "millers-tale" : (46, 55),
    "reeves-prologue": (55, 56),
    "reeves-tale": (56, 62),
    "cooks-prologue": (62, 63),
    "cooks-tale": (63, 64)
}

def line_filter(line):
    return line.strip() != ""


def remove_trailing_number(s):
    return re.sub(r' \d+$', '', s)

def reconstruct(lines):
    new_lines = []

    for l in lines:
        if not l[0].islower():
            new_lines.append(l)
        else:
            try:
                new_lines[-1] += ' ' + l
            except IndexError:
                continue

    return new_lines

parsed_chapter= "knights-tale"
page_range = chapter_ranges[parsed_chapter]
pages = convert_from_path("canterbury_tales.pdf", first_page=page_range[0], last_page=page_range[1])

cropped_pages = []

for i, page in enumerate(pages):
    width, height = page.size
    cropped_page = page.crop((0, 150, width, height - 150))
    cropped_pages.append(cropped_page)

lines = []

for page in cropped_pages:
    page_text = pytesseract.image_to_string(page)

    l = page_text.split("\n")
    l = list(filter(line_filter, l))
    l = list(map(remove_trailing_number, l))
    l = reconstruct(l)
    lines.extend(l)

with open(f'raw_{parsed_chapter}.txt', 'w') as f:
    for i, line in enumerate(lines):
        f.write(line)
        f.write("\n")
metadata = {
    "general-prologue": {
        "title": "General Prologue",
        "incipit": "Here bygynneth the Book of the Tales of Caunterbury.",
        "file_root_name": "prologue",
        "initial_line": 1
    },
    "knights-tale": {
        "title": "Knight's Tale",
        "incipit": "Heere bigynneth the Knyghtes Tale.",
        "file_root_name": "knights-tale",
        "initial_line": 859
    },
}


def get_chapter_info(chapter):
    with open(f"loadable/{metadata[chapter]['file_root_name']}_html.txt") as f:
        lines = f.readlines()

    title = metadata[chapter]["title"]
    incipit = metadata[chapter]["incipit"]

    return (title, incipit, lines)


if __name__ == '__main__':
    chapter = "knights-tale"
    title, _, lines = get_chapter_info(chapter)

    with open(f"temp_{title}.txt", 'w') as f:
        for line in lines:
            f.write(line)

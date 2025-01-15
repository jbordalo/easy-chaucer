metadata = {
    "general-prologue": {
        "title": "General Prologue",
        "file_root_name": "prologue",
        "initial_line": 1
    },
    "knights-tale": {
        "title": "Knight's Tale",
        "file_root_name": "knights-tale",
        "initial_line": 859
    },
}


# def tag_lines(lines):
#     return [{"line": line, "is_special": } for line in lines]


def get_chapter_info(chapter):
    with open(f"loadable/{metadata[chapter]['file_root_name']}_html.txt") as f:
        lines = f.readlines()

    # tagged_lines = tag_lines(lines)

    title = metadata[chapter]["title"]
    initial_line = metadata[chapter]["initial_line"]

    return (title, initial_line, lines)


if __name__ == '__main__':
    chapter = "knights-tale"
    title, _, lines = get_chapter_info(chapter)

    with open(f"temp_{title}.txt", 'w') as f:
        for line in lines:
            f.write(line)

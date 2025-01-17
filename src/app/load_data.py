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
    "millers-prologue": {
        "title": "Miller's Prologue",
        "file_root_name": "millers-prologue",
        "initial_line": 3109
    },
    "millers-tale": {
        "title": "Miller's Tale",
        "file_root_name": "millers-tale",
        "initial_line": 3187
    },
    "reeves-prologue": {
        "title": "Reeve's Prologue",
        "file_root_name": "reeves-prologue",
        "initial_line": 3855
    },"reeves-tale": {
        "title": "Reeve's Tale",
        "file_root_name": "reeves-tale",
        "initial_line": 3921
    },
    "cooks-prologue": {
        "title": "Cook's Prologue",
        "file_root_name": "cooks-prologue",
        "initial_line": 4325
    },"cooks-tale": {
        "title": "Cook's Tale",
        "file_root_name": "cooks-tale",
        "initial_line": 4365
    },
}


def get_chapter_info(chapter):
    with open(f"loadable/{metadata[chapter]['file_root_name']}_html.txt") as f:
        lines = f.readlines()

    title = metadata[chapter]["title"]
    initial_line = metadata[chapter]["initial_line"]

    return (title, initial_line, lines)


if __name__ == '__main__':
    chapter = "knights-tale"
    title, _, lines = get_chapter_info(chapter)

    with open(f"temp_{title}.txt", 'w') as f:
        for line in lines:
            f.write(line)

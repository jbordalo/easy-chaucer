import sys
from flask import Flask, render_template

from load_data import get_chapter_info

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<page_name>')
def page(page_name):
    try:
        title, initial_line, lines = get_chapter_info(chapter=page_name, root_dir=ROOT_DIR)
        return render_template('page.html', title=title, initial_line=initial_line, lines=lines)
    except KeyError:
        return "Page not found", 404
    except FileNotFoundError:
        print("Could not load the correspondent file")
        return "We're still working on that one", 500
    except Exception as e:
        print(f"Unexpected error: {type(e)} {e}")
        return "An unexpected error occurred", 500


if __name__ == '__main__':
    if len(sys.argv) < 2:
        ROOT_DIR = 'app/static/data'
    else:
        ROOT_DIR = sys.argv[1]

    host="0.0.0.0"
    port=5000

    print(f"Config: {{host={host}, port={port}, root_dir={ROOT_DIR}}}")

    app.run(host=host, port=port)

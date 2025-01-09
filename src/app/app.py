from flask import Flask, render_template

from load_data import get_page_lines

current_page="General Prologue"

app = Flask(__name__)

@app.route('/')
def home():
    lines = get_page_lines(current_page)
    return render_template('index.html', lines=lines)

if __name__ == '__main__':
    app.run(debug=True)

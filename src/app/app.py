from flask import Flask, render_template

app = Flask(__name__)

lines = [
    "Whan that Aprill with <dfn data-note=\"its\">his</dfn> shoures soote",
    "The <dfn data-note=\"dryness\">droghte</dfn> of March hath perced to the roote",
    "And bathed every veyne in swich licour",
    "Of which vertu engendred is the flour;",
    "Whan Zephirus eek with his sweete breeth",
    "Inspired hath in every holt and heeth",
]

@app.route('/')
def home():
    return render_template('index.html', lines=lines)

if __name__ == '__main__':
    app.run(debug=True)

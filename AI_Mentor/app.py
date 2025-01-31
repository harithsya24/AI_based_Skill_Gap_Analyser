from flask import Flask, render_template
from mentor import mentor_bp 

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

app.register_blueprint(mentor_bp, url_prefix="/mentor")

@app.route("/")
def index():
    return render_template("mentor.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from sqla_wrapper import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy("sqlite:///db.sqlite")
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)

db.create_all()

@app.route("/")
def index():
    messages = db.query(Message).all()
    return render_template("index.html", messages=messages)

@app.route("/add-message", methods=["POST"])
def add_message():
    name = request.form.get("name")
    text = request.form.get("message")

    #print(f"{name} wrote: {message}")

    message = Message(author=name, text=text)
    db.session.add(message)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
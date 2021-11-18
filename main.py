from flask import Flask, render_template, request, redirect, url_for
from sqla_wrapper import SQLAlchemy
import os
from sqlalchemy_pagination import paginate


app = Flask(__name__)

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)

db.create_all()

@app.route("/")
def index():
    page = request.args.get("page")
    if not page:
        page = 1

    messages_query = db.query(Message)
    messages = paginate(messages_query, page=int(page), page_size=5)

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
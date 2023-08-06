from flask import render_template


def index(*args, **kwargs):
    return render_template("index.html")

from flask import Blueprint, render_template
layout = Blueprint('layout', __name__)

@layout.route("/")
def index():
    return render_template("index.html")

@layout.route("/docs")
def docs():
    return render_template("docs.html")
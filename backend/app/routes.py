from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def hello():
    return "Hello from Flask!"

@main_bp.route("/demo")
def next():
    return "this is the next Page"
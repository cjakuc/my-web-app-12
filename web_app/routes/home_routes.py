
# web_app/routes/home_routes.py

from flask import Blueprint

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def hello():
    print("VISITED THE HELLO PAGE")
    return "Hello World!"

@home_routes.route("/about")
def about():
    print("VISITED THE ABOUT PAGE")
    return "About Me!"

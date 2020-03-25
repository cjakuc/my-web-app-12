# web_app/routes/stats_routes.py

from flask import Blueprint, request, jsonify, render_template
from sklearn.datasets import load_iris # just to have some data to use when predicting

from web_app.classifier import load_model

stats_routes = Blueprint("stats_routes", __name__)

@stats_routes.route("/iris")
def iris():
    model = load_model()
    X, y = load_iris(return_X_y=True) # just to have some data to use when predicting
    result = model.predict(X[:2, :])
    return str(result)
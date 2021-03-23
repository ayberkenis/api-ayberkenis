from flask import Blueprint, jsonify, render_template, request
from data import aeapi
api = aeapi.Earthquake()

earthquake = Blueprint('earthquake', __name__, url_prefix="/earthquake")

@earthquake.route("/all")
def all_earthquakes():
    return jsonify(api.get_earthquakes())

@earthquake.route("/latest")
def latest_earthquake():
    return jsonify(api.get_earthquakes()[0])

@earthquake.route("/")
def index_earthquake():
    data = api.get_earthquakes()
    return render_template("earthquake.html", data=data)

@earthquake.route("/q")
def query_earthquake():
    data = api.get_earthquakes()
    query = request.args.to_dict()
    results = []
    print(query.items())
    for item in data:
        if all((key, value) in item.items() for key, value in query.items()):
            results.append(item)
            return jsonify(results)
        else:
            return jsonify({"Error": "Please specify your query parameters and values in full format. Visit: https://api.ayberkenis.online/docs for more detail."})


from flask import Blueprint, jsonify, request, render_template
from data import aeapi
api = aeapi.Exchange()
exchange = Blueprint('exchange', __name__, url_prefix="/exchange")

@exchange.route("/all")
def all_exchanges():
    return jsonify(api.get_exchanges())

@exchange.route("/<code>")
def code_exchanges(code):
    print(api.get_exchanges())
    code = api.get_exchanges()[code]
    return jsonify(code)

@exchange.route("/<args>")
def q_exchanges(args):
    if args in request.args:
        code = str(request.args[args])
        results = []
        for d in api.get_exchanges():
            if code.lower() in api.get_exchanges()[d][args].lower():
                results.append(api.get_exchanges()[d])
        return results

@exchange.route("/")
def index_exchanges():
    data = api.get_exchanges()
    return render_template("exchange.html", data=data)

@exchange.route("/q")
def query_earthquake():
    data = api.get_exchanges()
    query = request.args.to_dict()
    results = {}
    print(data.items())

    for key_a, item in data.items():
        if all((key, value) in item.items() for key, value in query.items()):
            results[key_a] = item
            return jsonify(results)
    else:
        return jsonify({"Error": "Please specify your query parameters and values in full format. Visit: https://api.ayberkenis.online/docs for more detail."})


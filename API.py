from flask import Flask, blueprints
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from modules import earthquake, exchange, layout


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = False
app.config["JSON_AS_ASCII"] = False


limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per hour", "50 per minute"])

with app.app_context():
    app.register_blueprint(earthquake.earthquake)
    app.register_blueprint(exchange.exchange)
    app.register_blueprint(layout.layout)


if __name__ == "__main__":
    app.run(debug=True)
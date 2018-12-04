from decimal import Decimal

from flask import Flask, jsonify, request

app = Flask(__name__)


RATES = {"CZK": Decimal("25.5")}


def convert(amount, currency):
    try:
        rate = RATES[currency]
        return str(Decimal(amount) / rate)
    except KeyError:
        raise NoExchangeRateError


@app.route("/to_eur")
def to_eur():
    currency = request.args["currency"]
    amount = request.args["amount"]
    return jsonify({"result": convert(amount, currency)})


class NoExchangeRateError(Exception):
    status_code = 400


@app.errorhandler(NoExchangeRateError)
def handle_no_rate(error):
    response = jsonify({"detail": "No such rate"})
    response.status_code = error.status_code
    return response

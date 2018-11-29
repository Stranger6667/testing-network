from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://127.0.0.1:5432/test"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from .models import db

    db.init_app(app)

    return app

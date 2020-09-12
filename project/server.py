from app.main import create_app, db
import os
from flask_sqlalchemy import SQLAlchemy
from app.main.models import *
from flask_migrate import Migrate


app = create_app("development")
migrate = Migrate(app, db)


@app.route("/")
def home():
    return "Home Shoppers"


if __name__ == "__main__":
    app.run()
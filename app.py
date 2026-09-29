from flask import Flask
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db
from routes.users import users_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

csrf = CSRFProtect(app)

app.register_blueprint(users_bp)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
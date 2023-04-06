from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)
mail = Mail(app)
app.config.from_object(Config)
app.jinja_options['extensions'] = ['jinja2_humanize_extension.HumanizeExtension']
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
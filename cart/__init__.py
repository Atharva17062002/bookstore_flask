from app import create_app
from settings import settings
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db_url = settings.cart_database_uri
app = create_app(db_url)

db = SQLAlchemy()
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)
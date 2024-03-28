from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app(db_url, mode='debug'):
    """
    Create and configure the Flask app.

    Description:
    This function creates a Flask application instance and configures it based on the specified mode.

    Parameters:
    mode (str): The mode in which the application should run (default is 'debug').

    Return:
    app (Flask): The configured Flask application instance.
    """

    app = Flask(__name__)

    if mode == 'debug':
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['DEBUG'] = True  

    if mode == 'test':
        app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///test.sqlite3"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['TESTING'] = True

    return app

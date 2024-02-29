from flask import Flask
from flask_mail import Mail

mail = Mail()

class Development:
    """
    Development environment configuration.

    Description:
    Configuration settings for the development environment.

    Parameters:
    None

    Return:
    None
    """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Testing:
    """
    Testing environment configuration.

    Description:
    Configuration settings for the testing environment.

    Parameters:
    None

    Return:
    None
    """
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production:
    """
    Production environment configuration.

    Description:
    Configuration settings for the production environment.

    Parameters:
    None

    Return:
    None
    """
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config_mode = {
    'debug': Development,
    'testing': Testing,
    'prod': Production
}

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
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config.from_object(config_mode[mode])
    return app

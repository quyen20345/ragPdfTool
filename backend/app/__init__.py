from flask import Flask
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

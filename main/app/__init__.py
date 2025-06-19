from flask import Flask
from app.routes import home_bp, auth_bp, profile_bp, askpdf_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(home_bp) # Route '/' will be handled by home_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')  # All routes in auth_bp will be prefixed with '/auth'
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(askpdf_bp, url_prefix='/rag')
    
    return app

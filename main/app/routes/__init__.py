from .home import home_bp
from .auth import auth_bp
from .profile import profile_bp
from .askpdf import askpdf_bp

__all__ = ["home_bp", "auth_bp", "profile_bp", "askpdf_bp"] # list all modules can import from app.routes 
from flask import Blueprint, render_template

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/<user>")
def profile(user):
    user_name = user
    return render_template("profile.html", user=user_name) #f"Profile Page {user_name}"
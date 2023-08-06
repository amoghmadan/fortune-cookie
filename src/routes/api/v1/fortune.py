from flask import Blueprint

from views.fortune import CookieView

fortune = Blueprint("fortune", __name__)
fortune.add_url_rule("/cookie", view_func=CookieView.as_view("cookie"))

from flask import Flask

from routes import urlpatterns
from utils import db, ma
from views.root import index
import settings


def get_wsgi_application():
    app = Flask(__name__, template_folder=settings.TEMPLATES_DIR)
    app.config.update(
        DEBUG=settings.DEBUG,
        SQLALCHEMY_DATABASE_URI=settings.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=settings.SQLALCHEMY_TRACK_MODIFICATIONS,
    )
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        db.create_all()
    for path, blueprint in urlpatterns:
        app.register_blueprint(blueprint, url_prefix=path)
    app.add_url_rule("/", view_func=index)
    return app


application = get_wsgi_application()

if __name__ == "__main__":
    application.run()

from flask import Blueprint

from routes.api.v1.fortune import fortune

urlpatterns = [
    ("/fortune", fortune),
]

v1 = Blueprint("v1", __name__)
for path, blueprint in urlpatterns:
    v1.register_blueprint(blueprint, url_prefix=path)

__all__ = ["v1"]

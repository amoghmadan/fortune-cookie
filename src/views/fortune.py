from base64 import b64encode
from http import HTTPStatus
from random import choices

from flask import jsonify, request, views
from marshmallow import ValidationError

from schemas import IdentifierSchema
import settings


class CookieView(views.MethodView):
    """Cookie View"""

    schema_class = IdentifierSchema

    def post(self, *args, **kwargs):
        schema = self.schema_class()
        try:
            validated_data = schema.load(request.json)
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST
        try:
            files = [_ for _ in settings.COOKIE_DIR.iterdir() if _.is_file()]
            cookie = choices(files)[0]
        except IndexError:
            return jsonify({"detail": "No Cookie Found"}), HTTPStatus.NOT_FOUND
        with open(cookie, "rb") as c:
            encoded = b64encode(c.read())
        base64string = f"data:image/{cookie.suffix[1:]};base64,{encoded.decode()}"
        data = {"encoded": base64string, **validated_data}
        return jsonify(schema.dump(data)), HTTPStatus.CREATED

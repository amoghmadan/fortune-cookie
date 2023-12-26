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

    def options(self, *args, **kwargs):
        schema = self.schema_class()
        data = {
            "name": "Fortune Cookie - Generate",
            "description": "Randomly get a new fortune cookie.",
            "renders": ["application/json"],
            "parses": ["application/json"],
            "actions": {
                "POST": {
                    "name": {
                        "type": "string",
                        "required": True,
                        "read_only": False,
                        "label": "Name",
                    },
                    "language": {
                        "type": "string",
                        "required": True,
                        "read_only": False,
                        "label": "Language",
                        "choices": [
                            {"display_name": display_name, "value": value}
                            for value, display_name in zip(
                                schema.fields["language"].validate.choices,
                                schema.fields["language"].validate.labels,
                            )
                        ],
                    },
                    "encoded": {
                        "type": "string",
                        "required": False,
                        "read_only": True,
                        "label": "Encoded",
                    },
                }
            },
        }
        return jsonify(data), HTTPStatus.OK

    def post(self, *args, **kwargs):
        schema = self.schema_class()
        try:
            validated_data = schema.load(request.json)
            language_dir = settings.COOKIE_DIR / validated_data["language"]
            files = [_ for _ in language_dir.iterdir() if _.is_file()]
            cookie = choices(files)[0]
        except IndexError:
            return jsonify({"detail": "No Cookie Found"}), HTTPStatus.NOT_FOUND
        except ValidationError as e:
            return jsonify(e.messages), HTTPStatus.BAD_REQUEST

        with open(cookie, "rb") as c:
            encoded = b64encode(c.read())

        base64string = f"data:image/{cookie.suffix[1:]};base64,{encoded.decode()}"
        data = {"encoded": base64string, **validated_data}
        return jsonify(schema.dump(data)), HTTPStatus.CREATED

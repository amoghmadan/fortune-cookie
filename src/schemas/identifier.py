from marshmallow import fields, validate

from utils import ma
import settings


class IdentifierSchema(ma.Schema):
    """Identifier Schema"""

    LANGUAGE_CHOICES = [
        (_.name, _.name.title()) for _ in settings.COOKIE_DIR.iterdir() if _.is_dir()
    ]

    name = fields.Str(required=True)
    language = fields.Str(
        required=True,
        validate=validate.OneOf(
            choices=[i for i, _ in LANGUAGE_CHOICES],
            labels=[i for _, i in LANGUAGE_CHOICES],
        ),
    )
    encoded = fields.Str(dump_only=True)

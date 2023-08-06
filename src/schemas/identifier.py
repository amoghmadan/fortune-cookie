from marshmallow import fields

from utils import ma


class IdentifierSchema(ma.Schema):
    """Identifier Schema"""

    name = fields.Str(required=True)
    encoded = fields.Str(dump_only=True)

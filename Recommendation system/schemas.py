import marshmallow as ma
from bson import ObjectId


class Nested(ma.fields.Nested):
    """A nested field that deserializes from bson.ObjectId string and serializes to nested object"""
    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        return ObjectId(value)

class Authentification_Schema(ma.Schema):
    login = ma.fields.String()
    first_password = ma.fields.String()
    second_password = ma.fields.String()

class Authors_Schema(ma.Schema):
    image_url = ma.fields.String()
    name = ma.fields.String()
    surname = ma.fields.String()
    patronymic = ma.fields.String()
    date_born = ma.fields.Date()
    date_death = ma.fields.Date()
    biography = ma.fields.String()
    #compositions = ma.fields.String()

class Composition_Schema(ma.Schema):
    image_url = ma.fields.String()
    name = ma.fields.String()
    date = ma.fields.Date()
    author = Nested("Authors_Schema")




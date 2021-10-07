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

class Author_Schema(ma.Schema):
    image_url = ma.fields.String()
    name = ma.fields.String()
    surname = ma.fields.String()
    patronymic = ma.fields.String()
    date_born = ma.fields.Date()
    date_death = ma.fields.Date()
    biography = ma.fields.String()
    #composition = ma.fields.String()

class Composition_Schema(ma.Schema):
    image_url = ma.fields.String()
    name = ma.fields.String()
    date = ma.fields.Date()
    author = Nested("Author_Schema")

class System_Schema(ma.Schema):
    composition = Nested("Composition_Schema")
    summary = ma.fields.String()
    main_problem = ma.fields.String()
    description_problem = ma.fields.String()
    url_link = ma.fields.String()

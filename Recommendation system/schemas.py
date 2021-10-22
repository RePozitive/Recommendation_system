import marshmallow as ma
from bson import ObjectId
from marshmallow import  validate
from mongoengine import fields


class Nested(ma.fields.Nested):
    """A nested field that deserializes from bson.ObjectId string and serializes to nested object"""
    def _deserialize(self, value, attr, data, partial=None, **kwargs):
        return ObjectId(value)

class User_Schema(ma.Schema):
    role = ma.fields.String(validate=validate.OneOf(["admin", "user"]))
    login = ma.fields.String(validate=validate.Length(min=3, max=30))
    first_password = ma.fields.String()
    second_password = ma.fields.String()

class AuthorFIO_Schema(ma.Schema):
    name = ma.fields.String(validate=validate.Length(min=2, max=30))
    surname = ma.fields.String(validate=validate.Length(min=2, max=30))
    patronymic = ma.fields.String(validate=validate.Length(min=2, max=30))

class Author_Schema(AuthorFIO_Schema):
    image_url = ma.fields.String()
    date_born = ma.fields.Date()
    date_death = ma.fields.Date()
    biography = ma.fields.String()
    composition = Nested("CompositionName_Schema")

class CompositionName_Schema(ma.Schema):
    name = ma.fields.String(validate=validate.Length(min=1, max=100))

class Composition_Schema(CompositionName_Schema):
    image_url = ma.fields.String()
    date = ma.fields.Date()
    author = Nested("AuthorFIO_Schema")

class Service_Schema(ma.Schema):
    composition = Nested("CompositionName_Schema")
    author = Nested("AuthorFIO_Schema")
    summary = ma.fields.String()
    main_problem = ma.fields.String()
    description_problem = ma.fields.String()
    url_link = ma.fields.String()

class Service_Key_Value(Service_Schema):
    key_problem = ma.fields.List(ma.fields.String())
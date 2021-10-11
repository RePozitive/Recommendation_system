from typing_extensions import IntVar
from flask import Flask, request, abort, jsonify
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required

from models import Author, Composition, Authentification
from schemas import Author_Schema, Composition_Schema, Authentification_Schema
from settings import Config
from exceptions import InvalidUsage

author_schema = Author_Schema()
composition_schema = Composition_Schema()
authentification_schema = Authentification_Schema()

def creat_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db = MongoEngine(app)
    jwt = JWTManager(app)
    register_routes(app)
    register_errorhandlers(app)
    if __name__ == "__main__":
        app.run()
    return app  

def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response
    app.errorhandler(InvalidUsage)(errorhandler)

def register_routes(app):

    @app.route("/registration", methods=["POST"])
    def registration():
        if not request.is_json:
            raise InvalidUsage.RegistrationError()

        registration_text = request.get_json()
        registration_data = authentification_schema.load(registration_text)
        user = Authentification.objects(login=registration_data["login"]).first()

        if user != None:
            raise InvalidUsage.UserAlreadyRegistered()

        password_hash = generate_password_hash(registration_data["first_password"])

        if check_password_hash(password_hash, registration_data["second_password"]) == False:
            raise InvalidUsage.ErrorPasswords()
        
        new_user = Authentification(login = registration_data["login"], first_password = password_hash, second_password = password_hash)
        new_user.save()
        return {"message": "User successfuly created"}, 201

    @app.route("/authorization", methods=["POST"])
    def authorisation():
        if not request.is_json:
            raise InvalidUsage.AuthorisationError()
        
        authorization_text = request.get_json()
        authorization_data = authentification_schema.load(authorization_text)
        user = Authentification.objects(login=authorization_data["login"]).first()

        if user == None or check_password_hash(user["first_password"], authorization_data["first_password"]) == False:
            raise InvalidUsage.ErrorLoginOrPassword()

        token = create_access_token(identity=user["login"])
        return {"access token": token}, 200

    @app.route("/creat_author", methods=["POST"])
    def creat_author():
        author_text = request.get_json()
        author_data = author_schema.load(author_text)
        authors = Author(**author_data)
        authors.save()
        return {"id": str(authors.id)}, 201

    @app.route("/creat_composition", methods=["POST"])
    def creat_composition():
        composition_text = request.get_json()
        composition_data = composition_schema.load(composition_text)
        composition_author = Author.objects(id = composition_data["author"]).first()
        if composition_author == None:
            raise InvalidUsage.AuthorIsAbsent()
        composition = Composition(**composition_data)
        composition.save()
        return {"id": str(composition.id)}, 201

    @app.route("/authors", methods=["GET"])
    def authors():  
        authors = Author.objects.all()
        return {"Authors": [author_schema.dump(i) for i in authors]}, 200

    @app.route("/compositions", methods=["GET"])
    def compositions():
        composition = Composition.objects.all()
        return {"Compositions": [composition_schema.dump(i) for i in composition]}, 200

    @app.route("/author/<id>", methods=["GET"])                             
    def author(id):
        author = Author.objects(id = id).first()
        if author == None:
            raise InvalidUsage.AuthorIsAbsent()
        return author_schema.dump(author), 200

    @app.route("/composition/<id>", methods=["GET"])                        
    def composition(id):
        composition = Composition.objects(id = id).first()
        if composition == None:
            raise InvalidUsage.CompositionIsAbsent()
        return composition_schema.dump(composition), 200

    @app.route("/update_author/<id>", methods=["PUT"])
    def update_author(id):
        update_text = request.get_json()
        update_data = author_schema.load(update_text)
        author_composition = Composition.objects(id = update_data["composition"]).first()
        if author_composition == None:
            raise InvalidUsage.CompositionIsAbsent()
        author = Author.objects(id = id).update_one(upsert=False, **update_data)
        if not author:
            raise InvalidUsage.AuthorIsAbsent()
        return {"message": "Successfully update author"}, 200

    @app.route("/update_composition/<id>", methods=["PUT"])
    def update_composition(id):
        update_text = request.get_json()
        update_data = composition_schema.load(update_text)
        composition_author = Author.objects(id = update_data["author"]).first()
        if composition_author == None:
            raise InvalidUsage.AuthorIsAbsent()
        composition = Composition.objects(id = id).update_one(upsert=False, **update_data)
        if not composition:
            raise InvalidUsage.CompositionIsAbsent()
        return {"message": "Successfully update composition"}, 200

creat_app()
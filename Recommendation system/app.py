from flask import Flask, request, abort, jsonify
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_manager, jwt_required, current_user

from models import Author, Composition, User, Service
from schemas import Author_Schema, Composition_Schema, User_Schema, Service_Schema, Service_Key_Value
from settings import Config
from exceptions import InvalidUsage


author_schema = Author_Schema()
composition_schema = Composition_Schema()
user_schema = User_Schema()
service_schema = Service_Schema()
key_problem = Service_Key_Value()

def creat_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db = MongoEngine(app)
    jwt = JWTManager(app)
    register_routes(app)
    register_errorhandlers(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user_name):
        return user_name

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.objects(login=identity).first()

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

    @app.route("/registration_user", methods=["POST"])
    def registration():
        if not request.is_json:
            raise InvalidUsage.RegistrationError()

        registration_text = request.get_json()
        registration_data = user_schema.load(registration_text)
        user_name = User.objects(login=registration_data["login"]).first()
        user_first_password = User.objects(first_password = registration_data["first_password"]).first()
        user_second_password = User.objects(second_password = registration_data["second_password"]).first()

        if user_name != None:
            raise InvalidUsage.UserAlreadyRegistered()

        if not user_first_password or user_second_password: 
            raise InvalidUsage.TheLackOfPasswords()

        password_hash = generate_password_hash(registration_data["first_password"])

        if check_password_hash(password_hash, registration_data["second_password"]) == False:
            raise InvalidUsage.ErrorPasswords()
        
        new_user = User(role="user", login = registration_data["login"], first_password = password_hash, second_password = password_hash)
        new_user.save()
        return {"message": "User successfuly created"}, 201

    @app.route("/authorization_user", methods=["POST"])
    def authorisation():
        if not request.is_json:
            raise InvalidUsage.AuthorisationError()

        authorization_text = request.get_json()
        authorization_data = user_schema.load(authorization_text)
        user = User.objects(login=authorization_data["login"]).first()

        if user == None or check_password_hash(user["first_password"], authorization_data["first_password"]) == False:
            raise InvalidUsage.ErrorLoginOrPassword()

        token = create_access_token(identity=user["login"])
        return {"access token": token}, 201

    @app.route("/creat_author", methods=["POST"])
    @jwt_required()
    def creat_author():
        if current_user.role == 'admin' or 'SuperAdmin':
            author_text = request.get_json()
            author_data = author_schema.load(author_text)
            authors = Author(**author_data)
            authors.save()
            return {"id": str(authors.id)}, 201
        else:
            raise InvalidUsage.AccessAdmin()

    @app.route("/creat_composition", methods=["POST"])
    def creat_composition():
        if current_user.role == 'admin' or 'SuperAdmin':
            composition_text = request.get_json()
            composition_data = composition_schema.load(composition_text)
            composition_author = Author.objects(id = composition_data["author"]).first()
            if composition_author == None:
                raise InvalidUsage.AuthorIsAbsent()
            composition = Composition(**composition_data)
            composition.save()
            return {"id": str(composition.id)}, 201
        else:
            raise InvalidUsage.AccessAdmin()

    @app.route("/creat_service", methods=["POST"])
    @jwt_required()
    def creat_main_object():
        if current_user.role == "admin" or "SuperAdmin":
            object_text = request.get_json()
            object_data = key_problem.load(object_text)

            object_author = Author.objects(id = object_data["author"]).first()
            if object_author == None:
                raise InvalidUsage.AuthorIsAbsent()

            object_composition = Composition.objects(id = object_data["composition"]).first()
            if object_composition == None:
                raise InvalidUsage.CompositionIsAbsent()

            creat_object = Service(**object_data)
            creat_object.save()
            return {"id": str(creat_object.id)}, 201
        else:
            raise InvalidUsage.AccessAdmin()

    @app.route("/authors", methods=["GET"])
    @jwt_required()
    def authors(): 
        if current_user.role == 'user' or 'admin' or 'SuperAdmin': 
            authors = Author.objects.all()
            return {"Authors": [author_schema.dump(i) for i in authors]}, 200
        else:
            raise InvalidUsage.AccessUser()

    @app.route("/compositions", methods=["GET"])
    @jwt_required()
    def compositions():
        if current_user.role == 'user' or 'admin' or 'SuperAdmin':
            composition = Composition.objects.all()
            return {"Compositions": [composition_schema.dump(i) for i in composition]}, 200
        else:
            raise InvalidUsage.AccessUser()

    @app.route("/author/<id>", methods=["GET"])
    @jwt_required()                             
    def author(id):
        if current_user.role == 'user' or 'admin' or 'SuperAdmin':
            author = Author.objects(id = id).first()
            if author == None:
                raise InvalidUsage.AuthorIsAbsent()
            return author_schema.dump(author), 200
        else:
            raise InvalidUsage.AccessUser()

    @app.route("/composition/<id>", methods=["GET"])
    @jwt_required()                        
    def composition(id):
        if current_user.role == 'user' or 'admin' or 'SuperAdmin':
            composition = Composition.objects(id = id).first()
            if composition == None:
                raise InvalidUsage.CompositionIsAbsent()
            return composition_schema.dump(composition), 200
        else:
            raise InvalidUsage.AccessUser()

    @app.route("/service/key_problem=<key>", methods=["GET"])
    @jwt_required()
    def all_objects(key):
        if current_user.role == 'user' or 'admin' or 'SuperAdmin':
            key_object = Service.objects(key_problem = key).all()
            if len(key_object) == 0:
                raise InvalidUsage.ProblemIsAbsent()
            return {"objects": [service_schema.dump(i) for i in key_object]}
        else:
            raise InvalidUsage.AccessUser() 

    @app.route("/service/key_problem=<key>/<id>")
    @jwt_required()
    def main_object(key, id):
        if current_user.role == 'user' or 'admin' or 'SuperAdmin':
            key_object = Service.objects(key_problem = key, id = id).first()
            if key_object == None:
                raise InvalidUsage.ServiceIsAbsent()
            return service_schema.dump(key_object), 200
        else:
            raise InvalidUsage.AccessUser()

    @app.route("/update_user/<id>", methods=["PUT"])
    @jwt_required()
    def update_user(id):
        if current_user.role == 'SuperAdmin':
            update_text = request.get_json()
            update_data = user_schema.load(update_text)

            user = User.objects(id = id).update_one(upsert=False, **update_data)

            if user == None:
                raise InvalidUsage.UserIsAbsent()
            return {"message": "Successfully update User!"}
        else:
            raise InvalidUsage.AccessSuperAdmin()

    @app.route("/update_author/<id>", methods=["PUT"])
    @jwt_required()
    def update_author(id):
        if current_user.role == 'admin' or 'SuperAdmin':
            update_text = request.get_json()
            update_data = author_schema.load(update_text)
            author_composition = Composition.objects(id = update_data["composition"]).first()
            if author_composition == None:
                raise InvalidUsage.CompositionIsAbsent()
            author = Author.objects(id = id).update_one(upsert=False, **update_data)
            if not author:
                raise InvalidUsage.AuthorIsAbsent()
            return {"message": "Successfully update author"}, 201
        else:
            raise InvalidUsage.AccessAdmin()

    @app.route("/update_composition/<id>", methods=["PUT"])
    @jwt_required()
    def update_composition(id):
        if current_user.role == 'admin' or 'SuperAdmin':
            update_text = request.get_json()
            update_data = composition_schema.load(update_text)
            composition_author = Author.objects(id = update_data["author"]).first()
            if composition_author == None:
                raise InvalidUsage.AuthorIsAbsent()
            composition = Composition.objects(id = id).update_one(upsert=False, **update_data)
            if not composition:
                raise InvalidUsage.CompositionIsAbsent()
            return {"message": "Successfully update composition"}, 201
        else:
            raise InvalidUsage.AccessAdmin()

    @app.route("/delete_author/<id>", methods=["DELETE"])
    @jwt_required()
    def delete_author(id):
        if current_user.role == 'admin' or 'SuperAdmin':
            delete = Author.objects(id = id).delete()
            if not delete:
                raise InvalidUsage.AuthorIsAbsent()
            return {"message": "Successfully delete author"}, 201
        else:
            raise InvalidUsage.AccessAdmin()

    @app.route("/delete_composition/<id>", methods=["DELETE"])
    @jwt_required()
    def delete_composition(id):
        if current_user.role == 'admin' or 'SuperAdmin':
            delete = Composition.objects(id = id).delete()
            if not delete:
                raise InvalidUsage.CompositionIsAbsent()
            return {"message": "Successfully delete composition"}, 201
        else:
            raise InvalidUsage.AccessAdmin()

    @app.route("/delete_user/<id>", methods=["DELETE"])
    @jwt_required()
    def delete_user(id):
        if current_user.role == "SuperAdmin":
            delete = User.objects(id = id).delete()
            if not delete:
                raise InvalidUsage.UserIsAbsent()
            return {"message": "Successfully delete user"}
        else:
            raise InvalidUsage.AccessSuperAdmin()

creat_app()
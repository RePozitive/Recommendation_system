from flask import jsonify


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}

Error_Absent_Author = template(["This author is not in database"], code=404)
Error_Absent_Composition = template(["This composition is not in database"], code=404)
User_Already_Registered = template(["This login already exists"], code=422)
Error_Passwords = template(["Passwords don't match"], code=404)
Error_Login_or_Password = template(["Passwords don't match"], code=400)
Registration_Error = template(["Registration is not found"], code=404)
Authorisation_Error = template(["Authorisation is not found"], code=404)

class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def AuthorIsAbsent(cls):
        return cls(**Error_Absent_Author)

    @classmethod
    def CompositionIsAbsent(cls):
        return cls(**Error_Absent_Composition)

    @classmethod
    def UserAlreadyRegistered(cls):
        return cls(**User_Already_Registered)

    @classmethod
    def ErrorPasswords(cls):
        return cls(**Error_Passwords)

    @classmethod
    def ErrorLoginOrPassword(cls):
        return cls(**Error_Login_or_Password)

    @classmethod
    def RegistrationError(cls):
        return cls(**Registration_Error)
    
    @classmethod
    def AuthorisationError(cls):
        return cls(**Authorisation_Error)
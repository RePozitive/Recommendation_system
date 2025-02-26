from flask import jsonify

def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}

Error_Absent_Author = template(["This author does not exist"], code=404)
Error_Absent_Composition = template(["This composition does not exist"], code=404)
Error_Absent_User = template(["This user does not exist"], code=404)
Error_Absent_Problem = template(["This problem does not exist in compositions"], code=404)
Error_Absent_Service = template(["The service does not exit"], code=404)
Error_Role = template(["This role was entered incorrectly"], code=404)                          # временно не используется
Error_Passwords = template(["Passwords don't match"], code=401)
Error_Login_or_Password = template(["Login or Password entered incorrectly"], code=401)
User_Already_Registered = template(["This login already exists"], code=422)
Registration_Error = template(["Registration is not found"], code=401)
Authorisation_Error = template(["Authorisation is not found"], code=401)
Privilege_Admin = template(["You don't have rights to this section"], code=403)
Privilege_User = template(["To get access, you need to register"], code=403)
Privilege_SuperAdmin = template(["You don't have rights to this section"], code=403)
Lack_of_password = template(["Enter your password when registering"], code=401)
Lack_of_login = template(["Enter your login when registering"], code=401)

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

    @classmethod
    def AccessAdmin(cls):
        return cls(**Privilege_Admin)

    @classmethod
    def AccessUser(cls):
        return cls(**Privilege_User)

    @classmethod
    def UserIsAbsent(cls):
        return cls(**Error_Absent_User)

    @classmethod
    def IncorrectlyRole(cls):
        return cls(**Error_Role)

    @classmethod
    def AccessSuperAdmin(cls):
        return cls(**Privilege_SuperAdmin)

    @classmethod
    def TheLackOfPasswords(cls):
        return cls(**Lack_of_password)

    @classmethod
    def TheLackOfLogin(cls):
        return cls(**Lack_of_login)

    @classmethod
    def ProblemIsAbsent(cls):
        return cls(**Error_Absent_Problem)

    @classmethod
    def ServiceIsAbsent(cls):
        return cls(**Error_Absent_Service)

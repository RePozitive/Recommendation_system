import mongoengine as me


class Authentification(me.Document):
    login = me.StringField(min_length=3, max_length=30)
    first_password = me.StringField(min_length=5)
    second_password = me.StringField(min_length=5)

class Authors(me.Document):
    image_url = me.StringField()
    name = me.StringField(min_length=2, max_length=30)
    surname = me.StringField(min_length=2, max_length=30)
    patronymic = me.StringField(min_length=2, max_length=30)               # отчество
    date_born = me.DateField()
    date_death = me.DateField()
    biography = me.StringField()
    #books = me.ReferenceField(Composition)
    
class Composition(me.Document):                                            # произведение 
    image_url = me.StringField()
    name = me.StringField(min_length=1, max_length=100)
    date = me.DateField()                                                  # дата написания
    author = me.ReferenceField("Authors")                                  # ФИО автора из класса Author 


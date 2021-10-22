import mongoengine as me


class User(me.Document):
    role = me.StringField()
    login = me.StringField(min_length=3, max_length=30)
    first_password = me.StringField(min_length=5)
    second_password = me.StringField(min_length=5)

class Author(me.Document):
    image_url = me.StringField()
    name = me.StringField(min_length=2, max_length=30)
    surname = me.StringField(min_length=2, max_length=30)
    patronymic = me.StringField(min_length=2, max_length=30)              # Отчество
    date_born = me.DateField()
    date_death = me.DateField()
    biography = me.StringField()
    composition = me.ReferenceField("Composition")
    
class Composition(me.Document):                                           # Произведение 
    image_url = me.StringField()
    name = me.StringField(min_length=1, max_length=100)
    date = me.DateField()                                                 # Дата написания
    author = me.ReferenceField("Author")                                  # ФИО автора из класса Author 

class Service(me.Document):
    composition = me.ReferenceField("Composition")
    author = me.ReferenceField("Author")
    summary = me.StringField()                                            # Краткое содержание
    main_problem = me.StringField()                                       # Основные проблемы произведения
    key_problem = me.ListField(me.StringField())                          # Ключевой атрибут для поиска произведения по его "проблеме"
    description_problem = me.StringField()                                # Описание проблемы
    url_link = me.StringField()                                           # Ссылка на источник c литературой
    
class AbsentAuthorInBd(Exception):
    ''' 
        Исключение возникает в момент отсутствия искомого объекта в коллекции Author.
        Атрибуты:
            author_id — id автора
            message — объяснение ошибки.
    '''

    def __init__(self, author_id, message = "This author is not in database"):
        self.author_id = author_id
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'{self.author_id} -> {self.message}'

class AbsentCompositionInBd(Exception):
    '''
        Исключение возникает в момент отсутствия искомого объекта в коллекции Composition.
        Атрибуты:
            composition_id — id композиции
            message — объяснение ошибки.
    '''
    def __init__(self, composition_id, message = "This composition is not in database"):
        self.composition_id = composition_id
        self.message = message
        super().__init__(self.message)

        def __str__(self):
            return f'{self.composition_id} -> {self.message}'
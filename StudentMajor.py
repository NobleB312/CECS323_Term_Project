from mongoengine import *
import datetime
from Major import Major

class StudentMajor(EmbeddedDocument):

    # string implementation
    #major = StringField(db_field='major', max_length=20, required=True)
    major = ReferenceField(Major, required=True)
    declarationDate = DateTimeField(db_field='declaration_date', required=True)
    
    # FIXME: THIS MIGHT BREAK;
    meta = {
        'indexes': [
            {'unique': True, 'fields': ['major'], 'name': 'studentmajors_uk_1'}
        ]
    }

    def __init__(self, major: str, declarationDate: datetime, *args, **values):

        super().__init__(*args, **values)
        self.major = major
        self.declarationDate = declarationDate

    def __str__(self):
        return f'Student Major: Major: {self.major.majorName} on {self.declarationDate}'

    def get_major(self):
        return self.major

    def __eq__(self, other):
        return self.get_major().majorName == other.get_major().majorName
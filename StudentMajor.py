from mongoengine import *
from datetime import datetime
from Major import Major


class StudentMajor(EmbeddedDocument):

    major = ReferenceField(Major, required=True)
    declarationDate = DateTimeField(db_field='declaration_date', required=True)

    '''
    No student attributes were passed in for validation. We're just using an entire Student object
    As a reference to the specific student. 
    '''
    student = ReferenceField('Student', required=True)

    # Clean method allows for declarationDate validation
    def clean(self):
        if self.declarationDate > datetime.now():
            raise ValidationError("Declaration date cannot be in the future")

    meta = {'collection': 'student_majors',
            'indexes': [
                {'unique': True, 'fields': ['student', 'majorName'], 'name': 'student_majors_uk_01'}
                        ]
            }

    def __init__(self, major, declarationDate, student, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.major = major
        self.declarationDate = declarationDate
        self.student = student

    def __str__(self):
        return f'Student Major: Major: {self.major.majorName} on {self.declarationDate}'

    def get_major(self):
        return self.major

    def __eq__(self, other):
        return self.get_major().majorName == other.major.majorName

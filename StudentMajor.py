from mongoengine import *
from datetime import datetime
from Major import Major

class StudentMajor(EmbeddedDocument):

    major = ReferenceField(Major, required=True)
    declarationDate = DateTimeField(db_field='declaration_date', required=True)

    '''
    No student attributes were passed in for validaiton. We're just using an entire Student object
    As a reference to the specific student. 
    '''
    student = ReferenceField('Student', required=True)


    # Clean method allows for declarationDate validation
    def clean(self):
        if self.declarationDate > datetime.now():
            raise ValidationError("Declaration date cannot be in the future")

    meta = {'collection': 'student_majors',
            'indexes': [
                {'unique': True, 'fields': ['student', 'majorName'], 'name': 'studentmajors_uk_1'}
                        ]
            }

    def __init__(self, major: Major, declarationDate: datetime, *args, **values):

        super().__init__(*args, **values)
        self.major = major
        self.declarationDate = declarationDate

    def __str__(self):
        return f'Student Major: Major: {self.major.majorName} on {self.declarationDate}'

    def get_major(self):
        return self.major

    def __eq__(self, other):
        return self.major == other.major.majorName

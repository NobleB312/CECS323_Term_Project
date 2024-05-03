from mongoengine import *
from datetime import datetime
from StudentMajor import StudentMajor

class Student(Document):
    """"""
    firstName = StringField(db_field='first_name', max_length=40, required=True)
    lastName = StringField(db_field='last_name', max_length=40, required=True)
    eMail = StringField(db_field='email', max_length=100, required=True)
    studentMajor = EmbeddedDocumentListField(StudentMajor,db_field='student_major')
    

    enrollments = ListField(ReferenceField('Enrollment'))
     

    meta = {'collection': 'students',
            'indexes': [
                {'unique': True, 'fields': ['lastName', 'firstName'], 'name': 'students_uk_1'},
                {'unique': True, 'fields': ['eMail'], 'name': 'students_uk_2'}
                ]}


    def __init__(self, firstName: str, lastName: str, eMail: str, *args, **values):

        super().__init__(*args,**values)
        self.firstName = firstName
        self.lastName = lastName
        self.eMail = eMail

    def __str__(self):
        results = f'Student: {self.lastName}, {self.firstName} Email: {self.eMail}'
        for declaredmajor in self.studentMajor:
            results += '\n\t' + f"declared Major: {declaredmajor.major} on {declaredmajor.declarationDate}"
        return results

    def add_major(self, new_major: StudentMajor):

        if self.studentMajor:
            # adding constraints:
            # student cannot declare major they previously declared.
            # student can declare the same major at different time intervals; the assumption is that they dropped the major and returned, which realistically, is a very small chance of occurring multiple times.
            current_major = self.studentMajor[-1]
            if current_major == new_major:
                raise ValueError('Student is already in that major.')
            if current_major.declarationDate >= new_major.declarationDate:
                raise ValueError('The major cannot be declared before the latest major declared.')
            if new_major.declarationDate > datetime.utcnow():
                raise ValueError('The major cannot be declared in the future.')
            self.studentMajor.append(new_major)
        else:
            self.studentMajor = [new_major]
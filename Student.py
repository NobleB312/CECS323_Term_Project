from mongoengine import *
from datetime import datetime
from StudentMajor import StudentMajor

class Student(Document):
    """"""
    firstName = StringField(db_field='first_name', max_length=40, required=True)
    lastName = StringField(db_field='last_name', max_length=40, required=True)
    eMail = StringField(db_field='email', max_length=100, required=True)
    studentMajors = EmbeddedDocumentListField(StudentMajor, db_field='student_major')
    

    enrollments = ListField(ReferenceField('Enrollment'))
     

    meta = {'collection': 'students',
            'indexes': [
                {'unique': True, 'fields': ['lastName', 'firstName'], 'name': 'students_uk_01'},
                {'unique': True, 'fields': ['eMail'], 'name': 'students_uk_02'}
                ]}


    def __init__(self, firstName: str, lastName: str, eMail: str, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.firstName = firstName
        self.lastName = lastName
        self.eMail = eMail

    def __str__(self):
        results = f'Student: {self.lastName}, {self.firstName}'
        for declared_major in self.studentMajors:
            results += '\n\t' + f"declared Major: {declared_major.major} on {declared_major.declarationDate}"
        return results

    def add_major(self, major):
        if not self.studentMajors:
            self.studentMajors = [major]
            return

        for existing_major in self.studentMajors:
            if major == existing_major:
                raise Exception('Major is already declared.')

        self.studentMajors.append(major)

    def remove_major(self, major):
        for existing_major in self.studentMajors:
            if major == existing_major:
                self.studentMajors.remove(existing_major)
                return
        # if it reaches the end and doesn't remove, throw an exception
        raise Exception('Major was never declared.')

    def enroll_in_section(self, enrollment):
        if not self.enrollments:
            self.enrollments = [enrollment]
            return

        for already_enrolled_student in self.enrollments:
            if enrollment == already_enrolled_student:
                raise Exception('Student is already enrolled in this section.')

        self.enrollments.append(enrollment)

    def unenroll_in_section(self, enrollment):
        for already_enrolled_student in self.enrollments:
            if enrollment == already_enrolled_student:
                self.enrollments.remove(already_enrolled_student)
                return
        # if it reaches the end and doesn't remove, throw an exception
        raise Exception('Student is not Enrolled in this section.')

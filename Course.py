import mongoengine
from mongoengine import *
from Department import Department


class Course(Document):
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=700, required=True)
    courseName = StringField(db_field='course_name', required=True)
    courseDescription = StringField(db_field='course_description', required=True)
    courseUnits = IntField(db_field='course_units', min_value=1, max_value=5, required=True)

    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.CASCADE)
    departmentName = StringField(db_field='department_name')

    sections = ListField(ReferenceField('Section'))

    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['departmentName', 'courseNumber'], 'name': 'courses_uk_01'},
                {'unique': True, 'fields': ['departmentName', 'courseName'], 'name': 'courses_uk_02'}
            ]}

    def clean(self):
        self.departmentName = self.department.departmentName

    def __init__(self, department, courseNumber, courseName, courseDescription, courseUnits, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.courseDescription = courseDescription
        self.courseUnits = courseUnits

    def __str__(self):
        return f'Department: {self.department.departmentName}\n'\
            f'Course Name: {self.courseName}\n'\
            f'Course Number: {self.courseNumber}\n'\
            f'Course Units: {self.courseUnits}\n'\
            f'Course Description: {self.courseDescription}'

    '''
       Add and delete functions for sections, since Section is a child of Course and has a reference
       list within the Course object
       '''

    def add_section(self, section):
        if not self.sections:
            self.sections = [section]
            return

        for existingSections in self.sections:
            if section == existingSections:
                raise Exception('Section already exists.')

        self.sections.append(section)

    def remove_section(self, section):
        for existingSection in self.sections:
            if section == existingSection:
                self.sections.remove(existingSection)
                return

        raise Exception('Section does not exist')


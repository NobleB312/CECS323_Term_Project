import mongoengine
from mongoengine import *
from Department import Department

'''
c. Course

    c. Course
        i. {departmentAbbreviation, courseNumber} – Note that you can use
        departmentName instead of departmentAbbreviation if you choose to "migrate"
        that into Course.
        ii. {departmentAbbreviation, courseName}

    i. units must be no less than 1 and no greater than 5.
    ii. courseNumber must be >= 100 and < 700
'''
class Course(Document):
    courseNumber = IntField(db_field='course_number', min_value=100, max_value=700, required=True)
    courseName = StringField(db_field='course_name', required=True)
    courseDescription = StringField(db_field='course_description', required=True)
    courseUnits = IntField(db_field='course_units', min_value=1, max_value=5, required=True)

    department = ReferenceField(Department, required=True, reverse_delete_rule=mongoengine.CASCADE)

    sections = ListField(ReferenceField('Section'))

    meta = {'collection': 'courses',
            'indexes':[
                {'unique': True, 'fields': ['department.departmentName', 'courseNumber'], 'name': 'courses_uk_01'},
                {'unique': True, 'fields': ['department.departmentName', 'courseName'], 'name': 'courses_uk_01'}
            ]}

    def __init__(self, department, courseNumber, courseName, courseDescription, courseUnits, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.courseDescription = courseDescription
        self.courseUnits = courseUnits


    def __str__(self):
        return f'{self.department} Department\n'\
            f'Course Name: {self.courseName}\n'\
            f'Course Number: {self.courseNumber}\n'\
            f'Course Units: {self.courseUnits}\n'\
            f'Course Description: {self.courseDescription}'

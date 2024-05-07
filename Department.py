from mongoengine import *
from DepartmentBuilding import DepartmentBuilding


class Department(Document):
    departmentName = StringField(db_field='department_name', required=True)
    departmentAbbreviation = StringField(db_field='department_abbreviation', max_length=6, required=True)
    departmentChairName = StringField(db_field='department_chair_name', max_length=80, required=True)
    departmentBuilding = EnumField(DepartmentBuilding, db_field='department_building', required=True)
    departmentOffice = IntField(db_field='department_office', required=True)
    departmentDescription = StringField(db_field='department_description', max_length=80, required=True)

    majors = ListField(ReferenceField('Major'))
    courses = ListField(ReferenceField('Course'))

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['departmentName'], 'name': 'departments_uk_01'},
                {'unique': True, 'fields': ['departmentAbbreviation'], 'name': 'departments_uk_02'},
                {'unique': True, 'fields': ['departmentChairName'], 'name': 'departments_uk_03'},
                {'unique': True, 'fields': ['departmentBuilding', 'departmentOffice'], 'name': 'departments_uk_04'}
            ]}

    def __init__(self, departmentName, departmentAbbreviation, departmentChairName, departmentBuilding, departmentOffice,
                 departmentDescription, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.departmentName = departmentName
        self.departmentAbbreviation = departmentAbbreviation
        self.departmentChairName = departmentChairName
        self.departmentBuilding = departmentBuilding
        self.departmentOffice = departmentOffice
        self.departmentDescription = departmentDescription

    def __str__(self):
        return f'{self.departmentName} ({self.departmentAbbreviation}) Department \n'\
            f'Department Chair: {self.departmentChairName}\n'\
            f'Department Building: {self.departmentBuilding.name}\n'\
            f'Department Office: {self.departmentOffice}\n'\
            f'Department Description: {self.departmentDescription}'

    '''
    Add and delete functions for courses, since Course is a child of Department and has a reference
    list within the Department object
    '''
    def add_course(self, course):
        if not self.courses:
            self.courses = [course]
            return

        for existingCourse in self.courses:
            if course == existingCourse:
                raise Exception('Course already exists.')

        self.courses.append(course)

    def remove_course(self, course):
        for existingCourse in self.courses:
            if course == existingCourse:
                self.courses.remove(existingCourse)
                return

        raise Exception('Course does not exist')

    '''
    Add and delete functions for majors, since Major is a child of Department and has a reference
    list within the Department object
    '''

    def add_major(self, major):
        if not self.majors:
            self.majors = [major]
            return

        for existingMajor in self.majors:
            if major == existingMajor:
                raise Exception('Major already exists.')

        self.majors.append(major)

    def remove_major(self, major):
        for existingMajor in self.majors:
            if major == existingMajor:
                self.majors.remove(existingMajor)
                return

        raise Exception('Major does not exist')

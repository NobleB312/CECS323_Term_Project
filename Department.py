from mongoengine import *
from DepartmentBuilding import DepartmentBuilding
'''
Constrtaints

{name}
ii. {abbreviation}
iii. {chairName}
iv. {building, office}

Abbreviation must be six characters or less.
    ii. chairName must be 80 characters or less.
    iii. building name must be 10 characters or less.
        1. It was pointed out to me that the IN constraint that I have on building
           (see below) means that you do not have to worry about the length of the
           building name getting out of hand.
    iv. description must be 80 characters or less.
    v. Building IN ('ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR','VEC')
'''
class Department(Document):
    departmentName = StringField(db_field='department_name', required=True)
    departmentAbbreviation = EnumField(DepartmentBuilding, db_field='department_abbreviation', max_length=6, required=True)
    departmentChairName = StringField(db_field='department_chair_name', max_length=80, required=True)
    departmentBuilding = StringField(db_field='department_building', max_length = 10, required=True)
    departmentOffice = StringField(db_field='department_office', required=True)
    departmentDescription = StringField(db_field='department_description', max_length=80, required=True)
    #TODO Add majors and courses connections

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['departmentName'], 'name': 'departments_uk_01'},
                {'unique': True, 'fields': ['departmentAbbreviation'], 'name': 'departments_uk_02'},
                {'unique': True, 'fields': ['departmentChairName'], 'name': 'departments_uk_03'},
                {'unique': True, 'fields': ['departmentBuilding', 'departmentOffice'], 'name': 'departments_uk_04'}
            ]}


    def __init__(self, departmentName, departmentAbbreviation, departmentChairName, departmentBuilding, departmentOffice,
                 departmentDescription):
        self.departmentName = departmentName
        self.departmentAbbreviation = departmentAbbreviation
        self.departmentChairName = departmentChairName
        self.departmentBuilding = departmentBuilding
        self.departmentOffice = departmentOffice
        self.departmentDescription = departmentDescription


    def __str__(self):
        return f'{self.departmentName} ({self.departmentAbbreviation}) Department \n'\
            f'Department Chair: {self.departmentChairName}\n'\
            f'Department Building: {self.departmentBuilding}\n'\
            f'Department Office: {self.departmentOffice}\n'\
            f'Department Description: {self.departmentDescription}'
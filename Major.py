from mongoengine import *
from datetime import datetime
from Department import Department

class Major(Document):
    """
    
    """
    majorName = StringField(db_field='major_name',max_length=20,required=True)
    majorDescription = StringField(db_field='major_description',max_length=800,required=True)
    
    ## FIXME: reference to Department ##
    department = ReferenceField(Department, required=True, reverse_delete_rule=CASCADE)

    meta = {'collection': 'majors',
            'indexes': [
                {'unique': True, 'fields': ['majorName'], 'name': 'majors_uk_01'}
             ]}

    def __init__(self, majorName: str, majorDescription: str, *args, **values):
        super().__init__(*args, **values)
        self.majorName = majorName
        self.majorDescription = majorDescription

    def __str__(self):
        return f'Major: {self.majorName}: {self.majorDescription}'


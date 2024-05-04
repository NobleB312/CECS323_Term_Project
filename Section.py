import mongoengine
from mongoengine import *
from Course import Course
from Semester import Semester
from DepartmentBuilding import DepartmentBuilding
from Schedule import Schedule
from datetime import datetime

class Section(Document):
    sectionNumber = IntField(db_field='section_number', required=True)
    semester = EnumField(Semester, db_field='semester', required=True)
    sectionYear = IntField(db_field='section_year', required=True)
    building = EnumField(DepartmentBuilding, db_field='building', required=True)
    room = IntField(db_field='room', min_value=1, max_value=999, required=True)
    schedule = EnumField(Schedule, db_field='schedule', required=True)
    startTime = DateTimeField(db_field='start_time', required=True)
    instructor = StringField(db_field='instructor', required=True)

    course = ReferenceField(Course, required=True, reverse_delete_rule=mongoengine.CASCADE)

    enrollments = ListField(ReferenceField('Enrollment'))

    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['course', 'sectionNumber', 'semester', 'sectionYear'], 'name': 'sections_uk_01'},
                {'unique': True, 'fields': ['semester', 'sectionYear', 'building', 'room', 'schedule', 'startTime'], 'name': 'sections_uk_02'},
                {'unique': True, 'fields': ['semester', 'sectionYear', 'schedule', 'startTime', 'instructor'], 'name': 'sections_uk_03'}
            ]}

    def clean(self):
        time_conversion: datetime = self.startTime
        hours = time_conversion.hour
        minutes = time_conversion.minute
        # Logic: before 8am OR after 8pm OR after 7:30pm. We extracted hours and minutes, so we need two cases for 7:30.
        if hours < 8 or hours >= 20 or (hours == 19 and minutes > 30):
            raise ValidationError("Start time must be between 8am and 7:30pm")


    def __init__(self, course, sectionNumber, semester, sectionYear, building, room, schedule, startTime, instructor,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = course
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor

    def __str__(self):
        return "Section:\n"\
               f"  Course - {self.course.department.departmentAbbreviation} {self.course.courseNumber}\n" \
               f"  Section Number - {self.sectionNumber}\n" \
               f"  Semester - {self.semester}\n" \
               f"  Year - {self.sectionYear}\n" \
               f"  Building - {self.building}\n" \
               f"  Room - {self.room}\n" \
               f"  Schedule - {self.schedule}\n" \
               f"  Start Time - {self.startTime}\n" \
               f"  Instructor - {self.instructor}"


    def enroll_student(self, enrollment):
        if not self.enrollments:
            self.enrollments = [enrollment]
            return

        for already_enrolled_student in self.enrollments:
            if enrollment == already_enrolled_student:
                raise Exception('Student is already enrolled in this section.')

        self.enrollments.append(enrollment)

    def unenroll_student(self, enrollment):
        for already_enrolled_student in self.enrollments:
            if enrollment == already_enrolled_student:
                self.enrollments.remove(already_enrolled_student)
                return
        # if it reaches the end and doesn't remove, throw an exception
        raise Exception('Student is not Enrolled in this section.')

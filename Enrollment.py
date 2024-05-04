import mongoengine
from mongoengine import *

from DepartmentBuilding import DepartmentBuilding
from Section import Section
from Semester import Semester
from Student import Student
from EnrollmentDetails import EnrollmentDetails


class Enrollment(Document):
    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.CASCADE)
    section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.CASCADE)

    semester = EnumField(Semester, db_field='semester')
    sectionYear = IntField(db_field='section_year')
    departmentAbbreviation = StringField(db_field='department_abbreviation')
    courseNumber = IntField(db_field='course_number')

    # DESIGN CHANGE - enrollmentDetails must be non-nullable due to complete inheritance for minSatisfactory and P/NP
    enrollmentDetails = EmbeddedDocumentField(EnrollmentDetails, db_field='enrollment_details', required=True)

    '''
    SINGLE TABLE LOGIC
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    incomplete recovery plan and letter grade: Incomplete disjoint. Since these are issued at the end of a student
    being enrolled in a course, errors should be thrown if one is already set to a value and the other is attempting
    to be added.
    
    minimum satisfactory grade and pass fail application date: Complete disjoint. Since a student is able to change 
    their status to and from pass/fail until the two week deadline, one option should delete the instance of the other. 
    '''

    # Add the add methods for enrollment details
    def add_inc_recovery_plan(self, recovery_plan):
        # disjoint from letter grade
        if self.enrollmentDetails.letterGrade:
            raise ValidationError('Letter grade already received. Enrollment cannot be marked as incomplete.')
        self.enrollmentDetails.incRecoveryPlan = recovery_plan

    def add_min_satisfactory_grade(self, min_satisfactory_grade):
        # disjoint from pass fail application date
        if self.enrollmentDetails.passFailApplicationDate:
            del self.enrollmentDetails.passFailApplicationDate
        self.enrollmentDetails.minSatisfactoryGrade = min_satisfactory_grade

    def add_letter_grade(self, letter_grade):
        # disjoint from incomplete recovery plan
        if self.enrollmentDetails.incRecoveryPlan:
            raise ValidationError('This class was incomplete. No letter grade received.')
        self.enrollmentDetails.letterGrade = letter_grade

    def add_pass_fail_application_date(self, pass_fail_application_date):
        # disjoint from minimum satisfactory grade, but we want it to simply remove the satisfactory grade, if exists.
        if self.enrollmentDetails.minSatisfactoryGrade:
            del self.enrollmentDetails.minSatisfactoryGrade
        self.enrollmentDetails.passFailApplicationDate = pass_fail_application_date

    meta = {'collection': 'enrollments',
            'indexes': [
                {'unique': True, 'fields': ['student', 'section'], 'name': 'enrollments_uk_01'},
                {'unique': True, 'fields': ['semester', 'sectionYear', 'departmentAbbreviation', 'courseNumber',
                                            'student'], 'name': 'enrollments_uk_02'}
            ]}

    def clean(self):
        self.semester = self.section.semester
        self.sectionYear = self.section.sectionYear
        self.departmentAbbreviation = self.section.course.department.departmentAbbreviation
        self.courseNumber = self.section.course.courseNumber

    def __init__(self, student, section, enrollmentDetails, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        self.section = section
        self.enrollmentDetails = enrollmentDetails

    def __str__(self):
        return f"Enrollment:\n  {self.section.semester} {self.section.sectionYear} " \
               f"\n  Student - {self.student.firstName} {self.student.lastName}" \
               f"\n  Section - {self.section.course.department.departmentName} {self.section.course.courseNumber} " \
               f"S{self.section.sectionNumber}\n"

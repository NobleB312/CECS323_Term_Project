import mongoengine
from mongoengine import *
from Section import Section
from Student import Student
from EnrollmentDetails import EnrollmentDetails


class Enrollment(Document):
    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.CASCADE)
    section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.CASCADE)

    # DESIGN CHANGE - enrollmentDetails must be non-nullable due to complete inheritance for minSatisfactory and P/NP
    enrollmentDetails = EmbeddedDocumentField(EnrollmentDetails, db_field='enrollment_details', required=True)

    # Add the add methods for enrollment details
    def add_inc_recovery_plan(self, recovery_plan):
        # disjoint from letter grade
        if self.enrollmentDetails.letterGrade:
            raise ValidationError('Letter grade already received. Enrollment cannot be marked as incomplete.')
        self.enrollmentDetails.set_inc_recovery_plan(recovery_plan)

    def add_min_satisfactory_grade(self, min_satisfactory_grade):
        # disjoint from pass fail application date
        if self.enrollmentDetails.passFailApplicationDate:
            raise ValidationError('This course is being taken as pass fail. No five letter grade will be received.')
        self.enrollmentDetails.set_min_satisfactory_grade(min_satisfactory_grade)

    def add_letter_grade(self, letter_grade):
        # disjoint from incomplete recovery plan
        if self.enrollmentDetails.incRecoveryPlan:
            raise ValidationError('This class was incomplete. No leter grade received.')
        self.enrollmentDetails.set_letter_grade(letter_grade)

    def add_pass_fail_application_date(self, pass_fail_application_date):
        # disjoint from minimum satisfactory grade, but we want it to simply remove the satisfactory grade, if exists.
        if self.enrollmentDetails.minSatisfactoryGrade:
            del self.enrollmentDetails.minSatisfactoryGrade
        self.enrollmentDetails.set_pass_fail_application_date(pass_fail_application_date)

    def __init__(self, student, section, *args, **values):
        super().__init__(*args, **values)
        self.student = student
        self.section = section
        self.enrollmentDetails = EnrollmentDetails()

    def __str__(self):
        return f"Enrollment:\n  {self.section.semester} {self.section.sectionYear} " \
               f"\n  Student - {self.student.firstName} {self.student.lastName}" \
               f"\n  Section - {self.section.course.department.departmentName} {self.section.course.courseNumber} " \
               f"S{self.section.sectionNumber}\n"

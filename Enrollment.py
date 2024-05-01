import mongoengine
from mongoengine import *
from Section import Section
from Student import Student
from EnrollmentDetails import EnrollmentDetails
class Enrollment(Document):
    student = ReferenceField(Student, required=True, reverse_delete_rule=mongoengine.CASCADE)
    section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.CASCADE)

    enrollmentDetails = EmbeddedDocumentField(EnrollmentDetails, db_field='enrollment_details')

    # TODO: add the add methods for enrollment details
    # Singleton design pattern for EnrollmentDetails embedded object
    def enrollmentDetailsInstance(self):
        if not self.enrollmentDetails:
            self.enrollmentDetails = EnrollmentDetails()

    # If there are no more enrollment details, clear the field
    def cleanEnrollmentDetailsInstance(self):
        print()
        #TODO: fix.

    def __init__(self, student, section, *args, **values):
        super().__init__(*args, **values)
        self.student = student
        self.section = section

    def __str__(self):
        return f"Enrollment:\n  {self.section.semester} {self.section.sectionYear} " \
                 f"\n  Student - {self.student.firstName} {self.student.lastName}" \
                 f"\n  Section - {self.section.course.department.departmentName} {self.section.course.courseNumber} " \
                 f"S{self.section.sectionNumber}\n"

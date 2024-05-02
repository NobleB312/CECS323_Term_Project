from mongoengine import *
from datetime import datetime

from LetterGrade import LetterGrade
from PassingLetterGrade import PassingLetterGrade


class EnrollmentDetails(EmbeddedDocument):
    letterGrade = EnumField(LetterGrade, db_field='letter_grade')
    passFailApplicationDate = DateField(db_field='pass_fail_application_date')
    minSatisfactoryGrade = EnumField(PassingLetterGrade, db_field='min_satisfactory_grade')
    incRecoveryPlan = StringField(db_field='inc_recovery_plan')

    def set_letter_grade(self, letter_grade: LetterGrade):
        self.letterGrade = letter_grade

    def set_pass_fail_application_date(self, pass_fail_application_date: datetime):
        self.passFailApplicationDate = pass_fail_application_date

    def set_min_satisfactory_grade(self, min_satisfactory_grade: PassingLetterGrade):
        self.minSatisfactoryGrade = min_satisfactory_grade

    def set_inc_recovery_plan(self, inc_recovery_plan: str):
        self.incRecoveryPlan = inc_recovery_plan

    # don't allow Pass/Fail application date to be in the future
    def clean(self):
        if self.passFailApplicationDate > datetime.now():
            raise ValidationError("Pass/Fail application date cannot be in the future")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        result = 'Enrollment Details:\n'
        if self.letterGrade:
            result += '  Letter grade - ' + str(self.letterGrade) + '\n'
        if self.passFailApplicationDate:
            result += '  Pass/Fail application Date - ' + str(self.passFailApplicationDate) + '\n'
        if self.minSatisfactoryGrade:
            result += '  Minimum satisfactory grade - ' + str(self.minSatisfactoryGrade) + '\n'
        if self.incRecoveryPlan:
            result += '  Incomplete recovery plan - ' + self.incRecoveryPlan + '\n'

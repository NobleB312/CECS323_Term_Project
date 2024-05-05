from mongoengine import *
from datetime import datetime

from LetterGrade import LetterGrade
from PassingLetterGrade import PassingLetterGrade


class EnrollmentDetails(EmbeddedDocument):
    letterGrade = EnumField(LetterGrade, db_field='letter_grade')
    passFailApplicationDate = DateField(db_field='pass_fail_application_date')
    minSatisfactoryGrade = EnumField(PassingLetterGrade, db_field='min_satisfactory_grade')
    incRecoveryPlan = StringField(db_field='inc_recovery_plan')

    # don't allow Pass/Fail application date to be in the future
    def clean(self):
        if self.passFailApplicationDate:
            if self.passFailApplicationDate > datetime.now():
                raise ValidationError("Pass/Fail application date cannot be in the future")

    # The student defaults to having a minimum satisfactory grade. They can change to Pass/Fail later.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        result = 'Enrollment Details:\n'
        if self.letterGrade:
            result += '  Letter grade - ' + self.letterGrade.name + '\n'
        if self.passFailApplicationDate:
            result += '  Pass/Fail application Date - ' + str(self.passFailApplicationDate) + '\n'
        if self.minSatisfactoryGrade:
            result += '  Minimum satisfactory grade - ' + self.minSatisfactoryGrade.name + '\n'
        if self.incRecoveryPlan:
            result += '  Incomplete recovery plan - ' + self.incRecoveryPlan + '\n'
        return result

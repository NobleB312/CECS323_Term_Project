from mongoengine import *
import pymongo
from pprint import pprint
from ConstraintUtilities import *
from EnrollmentDetails import EnrollmentDetails
from Utilities import Utilities
from Department import Department
from Course import Course
from Major import Major
from Student import Student
from Section import Section
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from pymongo import monitoring, MongoClient
from Menu import Menu
from Option import Option
from menu_definitions import *
import DepartmentBuilding
from datetime import datetime

'''--- Start of Miscellaneous Functions---'''

def prompt_for_enum(prompt: str, cls, attribute_name: str):
    """
    MongoEngine attributes can be regulated with an enum.  If they are, the definition of
    that attribute will carry the list of choices allowed by the enum (as well as the enum
    class itself) that we can use to prompt the user for one of the valid values.  This
    represents the 'don't let bad data happen in the first place' strategy rather than
    wait for an exception from the database.
    :param prompt:          A text string telling the user what they are being prompted for.
    :param cls:             The class (not just the name) of the MongoEngine class that the
                            enumerated attribute belongs to.
    :param attribute_name:  The NAME of the attribute that you want a value for.
    :return:                The enum class member that the user selected.
    """
    attr = getattr(cls, attribute_name)  # Get the enumerated attribute.
    if type(attr).__name__ == 'EnumField':  # Make sure that it is an enumeration.
        enum_values = []
        for choice in attr.choices:  # Build a menu option for each of the enum instances.
            enum_values.append(Option(choice.value, choice))
        # Build an "on the fly" menu and prompt the user for which option they want.
        return Menu('Enum Menu', prompt, enum_values).menu_prompt()
    else:
        raise ValueError(f'This attribute is not an enum: {attribute_name}')



'''--- Start of Menu Loop Functions ---'''

def menu_loop(menu: Menu):
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)

def add():
    menu_loop(add_select)

def select():
    menu_loop(select_select)

def delete():
    menu_loop(delete_select)

def update():
    menu_loop(update_select)

def list():
    menu_loop(list_select)

def update_enrollment_details():
    menu_loop(update_enrollment_details_select)

'''--- Start of Select Functions ---'''

def select_department():
    return select_general(Department)


def select_course():
    return select_general(Course)


def select_major():
    return select_general(Major)


def select_student():
    return select_general(Student)


def select_section():
    return select_general(Section)

def select_student_major():
    success = False
    while True:
        major = select_major()
        student = select_student()
        for student_major in student.studentMajors:
            if student_major.major == major:
                return student_major
        print('Student major not found.')


def select_enrollment():
    return select_general(Enrollment)

'''--- Start of Add Functions ---'''

def add_department():
    """
    Create a new Department instance.
    """
    success = False
    while not success:
        try:
            department_name = input('Enter the department name: ')
            department_abbreviation = input('Enter the department abbreviation: ')
            department_chair_name = input('Enter the department chair name: ')
            department_building = prompt_for_enum('Enter the department building: ', Department, 'departmentBuilding')
            department_office = input('Enter the department office number: ')
            department_description = input('Enter the department description: ')

            new_department = Department(
                departmentName=department_name,
                departmentAbbreviation=department_abbreviation,
                departmentChairName=department_chair_name,
                departmentBuilding=department_building,
                departmentOffice=department_office,
                departmentDescription=department_description
            )

            new_department.save()
            print(f'Successfully added department: {new_department.departmentName}')
            success = True

        except Exception as e:
            print(e)

def add_course():
    """
    Create a new Course instance.
    """
    success = False
    new_course = None
    while not success:
        try:
            department = select_department()
            course_number = int(input('Enter the course number: '))
            course_name = input('Enter the course name: ')
            course_description = input('Enter the course description: ')
            course_units = int(input('Enter the number of course units: '))

            # create new course instance
            new_course = Course(
                department=department,
                courseNumber=course_number,
                courseName=course_name,
                courseDescription=course_description,
                courseUnits=course_units
            )

            # attempt to save the new course to the database
            new_course.save()

            department.add_course(new_course)
            department.save()
            print(f'Successfully added course: {new_course}')
            success = True

        except Exception as e:
            print(e)

def add_section():
    """
    Create a new Section instance.
    """
    success = False

    new_section = None
    while not success:
        try:
            course = select_course()
            section_number = int(input('Enter the section number: '))
            semester = prompt_for_enum('Select the semester: ', Section, 'semester')
            section_year = int(input('Enter the section year: '))
            building = prompt_for_enum('Select the building: ', Section, 'building')
            room = int(input('Enter the room number: '))
            schedule = prompt_for_enum('Select the weekly meeting days: ', Section, 'schedule')
            hour = int(input('Start time - enter the hour:'))
            minute = int(input('Start time - enter the minute:'))
            # we just want the time; calendar date does not matter for start_time.
            start_time = datetime(year=1, month=1, day=1, hour=hour, minute=minute)
            instructor = input('Enter the instructor for this section: ')

            new_section = Section(
                course=course,
                sectionNumber=section_number,
                semester=semester,
                sectionYear=section_year,
                building=building,
                room=room,
                schedule=schedule,
                startTime=start_time,
                instructor=instructor
            )

            new_section.save()

            course.add_section(new_section)
            course.save()

            print(f'Successfully added section: {new_section}')
            success = True

        except Exception as e:
            print(e)

def add_student():
    """
    Create a new Department instance.
    """
    success = False
    while not success:
        try:
            first_name = input('Enter the student first name: ')
            last_name = input('Enter the student last name: ')
            email = input('Enter the student email: ')

            new_student = Student(
                firstName=first_name,
                lastName=last_name,
                eMail=email
            )

            new_student.save()
            print(f'Successfully added student: {new_student.firstName} {new_student.lastName}')
            success = True

        except Exception as e:
            print(e)

def add_major():
    """
     Create a new Major instance.
     """
    success = False
    while not success:
        try:
            department = select_department()
            major_name = input('Enter the major name (up to 20 characters): ')
            major_description = input('Enter the major description (up to 800 characters): ')

            new_major = Major(
                majorName=major_name,
                majorDescription=major_description,
                department=department
            )

            new_major.save()

            department.add_major(new_major)
            department.save()
            print(f'Successfully added major: {new_major.majorName}')
            success = True

        except Exception as e:
            print(e)

def add_enrollment():
    """
     Create a new Major instance.
     """
    success = False
    while not success:
        try:
            student = select_student()
            section = select_section()

            new_enrollment = Enrollment(
                student=student,
                section=section
            )

            new_enrollment.add_min_satisfactory_grade((prompt_for_enum('Enter the minimum satisfactory grade:',
                                                                       EnrollmentDetails, 'minSatisfactoryGrade')))
            new_enrollment.save()

            # now we must add to both student and section
            student.enroll_in_section(new_enrollment)
            student.save()
            section.enroll_student(new_enrollment)
            section.save()
            print(f'Successfully enrolled:\n{new_enrollment.student}\n{new_enrollment.section}')
            success = True

        except Exception as e:
            print(e)

def add_major_student():
    success = False
    while not success:
        try:
            student = select_student()
            major = select_major()

            student.add_major(major)
            student.save()

            print(f'Successfully declared:\n  {student}')
            success = True

        except Exception as e:
            print(e)


'''--- Start of Update Enrollment Functions ---'''
def assign_letter_grade():
    try:
        enrollment = select_enrollment()

        letter_grade = prompt_for_enum('Enter the letter grade received for this section', EnrollmentDetails,
                                       'letterGrade')
        enrollment.add_letter_grade(letter_grade)
        enrollment.save()
        print(f'Letter grade added. \n{enrollment}')
    except Exception as e:
        print(e)

def update_pass_fail_application_date():
    try:
        enrollment = select_enrollment()
        # we can make pass fail application date set to today, given that we wanted to apply today.
        pass_fail_application_date = datetime.now().date()
        enrollment.add_pass_fail_application_date(pass_fail_application_date)
        enrollment.save()
        print(f'Pass/Fail grading applied. \n{enrollment}')

    except Exception as e:
        print(e)

def update_min_satisfactory_grade():
    try:
        enrollment = select_enrollment()

        letter_grade = prompt_for_enum('Enter the minimum satisfactory grade for this section', EnrollmentDetails,
                                       'minSatisfactoryGrade')
        enrollment.add_min_satisfactory_grade(letter_grade)
        enrollment.save()
        print(f'Minimum satisfactory grade added. \n{enrollment}')
    except Exception as e:
        print(e)

def update_inc_recovery_plan():
    try:
        enrollment = select_enrollment()

        inc_recovery_plan = input('Enter your recovery plan for your incomplete course:')
        enrollment.add_inc_recovery_plan(inc_recovery_plan)
        enrollment.save()
        print(f'Incomplete recovery plan applied. \n{enrollment}')

    except Exception as e:
        print(e)

'''--- Start of Delete Functions ---'''

def delete_department():
    try:
        department = select_department()
        # delete any cascading section or studentMajor references
        students = Student.objects()
        for student in students:
            for enrollment in student.enrollments:
                if enrollment.section.course.department == department:
                    student.unenroll_in_section(enrollment)

            for student_major in student.studentMajors:
                if student_major.major.department == department:
                    student.remove_major(student_major)
                    student.save()

        department.delete()

        print(f'Deleted department: \n{department}')
    except Exception as e:
        print(e)

def delete_course():
    try:
        #find the course by its ID and delete it
        course = select_course()
        #first remove from the list of departments
        course.department.remove_course(course)
        course.department.save()

        # delete any cascading section reference
        students = Student.objects()
        for student in students:
            for enrollment in student.enrollments:
                if enrollment.section.course == course:
                    student.unenroll_in_section(enrollment)

        course.delete()
        print(f'Deleted course: \n{course}')
    except Exception as e:
        print(e)

def delete_section():
    
    section = select_section()

    try:
        section.course.remove_section(section)
        section.course.save()
        for enrolled in section.enrollments:
            enrolled.student.unenroll_in_section(enrolled)
            enrolled.student.save()
        section.delete()
        print(f"Delete section: \n{section}")
    except Exception as e:
        print(e)

def delete_major():
    major = select_major()
    
    try:
        
        # need to query every student to remove the studentmajor with the major being deleted.
        
        students = Student.objects()

        for student in students:
            for studentmajor in student.studentMajors:
                if studentmajor.major == major:
                    student.remove_major(studentmajor)
                    student.save()
                
        major.department.remove_major(major)
        major.department.save()
        
        major.delete()
        print(f"Delete major: \n{major}")
    except Exception as e:
        print(e)

def delete_student():
    student = select_student()
    
    try:
        # student_major CASCADES by effect of removing students.
        # enrollments will also CASCADE.
        # doing manual unenrollment instead like how prof brown did in one to many.
        for enrolled in student.enrollments:
            #student.unenroll_in_section(enrolled)
            #not necessary since student is going bye-bye.
            
            # we only need to fix section's references to its enrollments.
            enrolled.section.unenroll_student(enrolled)
            enrolled.section.save()
        
        student.delete()
        print(f"Delete student: \n{student}")
    except Exception as e:
        print(e)

def delete_major_student():
    try:
        student = select_student()
        student_majors = student.studentMajors
        menu_items: [Option] = []

        for student_major in student_majors:
            menu_items.append(Option(student_major.__str__(), student_major))

        student_major = Menu('Student Major Menu','Choose which student major to remove', menu_items).menu_prompt()
        student.remove_major(student_major)
        student.save()
        print(f"Delete Student Major: {student_major}")
    except Exception as e:
        print(e)

def delete_enrollment():
    
    enrollment = select_enrollment()
    
    try:
        enrollment.student.unenroll_in_section(enrollment)
        enrollment.student.save()
        enrollment.section.unenroll_student(enrollment)
        enrollment.section.save()
        enrollment.delete()
        print(f"Delete enrollment: \n{enrollment}")
    except Exception as e:
        print(e)
    
# list section

'''--- Start of List Functions ---'''

def list_department():
    departments = Department.objects()
    for item in departments:
        pprint(item)

def list_course():
    courses = Course.objects()
    for item in courses:
        pprint(item)

def list_section():
    sections = Section.objects()
    for item in sections:
        pprint(item)

def list_enrollment():
    enrollments = Enrollment.objects()
    for item in enrollments:
        pprint(item)

def list_student():
    students = Student.objects()
    for item in students:
        pprint(item)

def list_major():
    majors = Major.objects()
    for item in majors:
        pprint(item)

def list_student_major():
    students = Student.objects()
    for student in students:
        if student.studentMajors:
            for item in student.studentMajors:
                pprint(item)



if __name__ == '__main__':
    print('Starting in main.')
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)

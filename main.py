from mongoengine import *

from ConstraintUtilities import *
from Utilities import Utilities
from Department import Department
from Course import Course
from Major import Major
from Student import Student
from Section import Section
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from pymongo import monitoring
from Menu import Menu
from Option import Option
from menu_definitions import menu_main, add_select, select_select, delete_select, update_select
import DepartmentBuilding


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



#add, delete for all objects
def menu_loop(menu: Menu):
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


def prompt_for_input(prompt_message):
    return input(prompt_message)


def add():
    menu_loop(add_select)


def select():
    menu_loop(select_select)


def delete():
    menu_loop(delete_select)


def update():
    menu_loop(update_select)


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
    return select_general(StudentMajor)


def select_enrollment():
    return select_general(Enrollment)

def add_department():
    """
    Create a new Department instance.
    """
    success = False
    while not success:
        try:
            department_name = prompt_for_input('Enter the department name: ')
            department_abbreviation = prompt_for_input('Enter the department abbreviation: ')
            department_chair_name = prompt_for_input('Enter the department chair name: ')
            department_building = prompt_for_enum('Enter the department building: ', Department, 'departmentBuilding')
            department_office = prompt_for_input('Enter the department office number: ')
            department_description = prompt_for_input('Enter the department description: ')

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
            print('An error occurred: ', Utilities.print_exception(e))


def add_course():
    """
    Create a new Course instance.
    """
    success = False
    new_course = None
    while not success:
        try:
            department = select_department()
            course_number = int(prompt_for_input('Enter the course number: '))
            course_name = prompt_for_input('Enter the course name: ')
            course_description = prompt_for_input('Enter the course description: ')
            course_units = int(prompt_for_input('Enter the number of course units: '))

            #create new course instance
            new_course = Course(
                department=department,
                courseNumber=course_number,
                courseName=course_name,
                courseDescription=course_description,
                courseUnits=course_units
            )
            
            #attempt to save the new course to the database
            new_course.save()

            department.add_course(new_course)
            department.save()
            print(f'Successfully added course: {new_course}')
            success = True

        except Exception as e:
            Utilities.print_exception(e)


# def add_major():
#     """
#     Create a new Major instance.
#     """
#     success = False
#     while not success:
#         try:
#             major_name = prompt_for_input('Enter the major name (up to 20 characters): ')
#             major_description = prompt_for_input('Enter the major description (up to 800 characters): ')
#
#             department_name = prompt_for_input('Enter the department name: ')
#             department = Department.objects.get(departmentName=department_name)
#
#             new_major = Major(
#                 majorName=major_name,
#                 majorDescription=major_description,
#                 department=department
#             )
#
#             new_major.save()
#             print(f'Successfully added major: {new_major.majorName}')
#             success = True
#
#         except Exception as e:
#             print(f'An error occurred: {e}')


#function to delete a course
def delete_course():
    try:
        #find the course by its ID and delete it
        course = select_course()
        course.delete()
        print(f'Deleted course: {course}')
    except Exception as e:
        print(f'Error deleting course: {e}')


if __name__ == '__main__':
    print('Starting in main.')
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
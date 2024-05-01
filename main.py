from Utilities import Utilities
from Department import Department
from Course import Course
from pymongo import monitoring
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from Menu import Menu
from Option import Option
from menu_definitions import menu_main


if __name__ == '__main__':
    print('Starting in main.')
    db = Utilities.startup()
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)


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


def add_course():
    """
    Create a new Course instance.
    """
    success = False
    new_course = None
    while not success:
        try:
            department_name = prompt_for_input('Enter the department name: ')
            department = Department.objects(departmentName=department_name).first()
            if not department:
                print("Department not found.")

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
            print(f'Successfully added course: {new_course}')
            success = True

        except NotUniqueError as nue:
            print('Error: The course violates one or more uniqueness constraints. Please enter unique values.')

#function to delete a course
def delete_course(course_id):
    try:
        #find the course by its ID and delete it
        course = Course.objects(id=course_id).get()
        course.delete()
        print(f'Deleted course with ID {course_id}')
    except Exception as e:
        print(f'Error deleting course: {e}')
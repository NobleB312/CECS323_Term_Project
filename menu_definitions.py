from Menu import Menu
import logging
from Option import Option

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add()"),
    Option("Delete existing instance", "delete()"),
    Option("Select existing instance", "select()"),
    Option("Update existing instance", "update()"),
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Department", "add_department()"),
    Option("Course", "add_course()"),
    Option("Major", "add_major()"),
    Option("Student", "add_student()"),
    Option("Section", "add_section()"),
    # Option("Enrollment", "add_enrollment()"),
    # Option("Major to Student", "add_major_student()"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Department", "delete_department()"),
    Option("Course", "delete_course()"),
    # Option("Major", "delete_major()"),
    # Option("Student", "delete_student()"),
    # Option("Section", "delete_section()"),
    # Option("Enrollment", "delete_enrollment()"),
    # Option("Major from Student", "delete_major_student()"),
    Option("Exit", "pass")
])

# options for testing the select functions
select_select = Menu('select select', 'Which type of object do you want to select:', [
    Option("Department", "print(select_department())"),
    Option("Course", "print(select_course())"),
    Option("Major", "print(select_major())"),
    Option("Student", "print(select_student())"),
    Option("Section", "print(select_section())"),
    Option("Enrollment", "print(select_enrollment())"),
    Option("Student Major", "print(select_student_major())"),
    Option("Exit", "pass")
])

# options for testing the update functions
update_select = Menu("update select", 'Which type of object do you want to update:', [
    Option("Enrollment details", "update_enrollment_details()"),
    Option("Exit", "pass")
])

update_enrollment_details_select = Menu("update enrollment details select", 'Which enrollment detail are you adding?:',
                                        [
                                            # Option("Letter grade", "update_letter_grade()"),
                                            # Option("Pass/Fail application date", "update_pass_fail_application_date()"),
                                            # Option("Minimum satisfactory grade", "update_min_satisfactory_grade()"),
                                            # Option("Incomplete recovery plan", "update_inc_recovery_plan()"),
                                            Option("Exit", "pass")
                                        ])

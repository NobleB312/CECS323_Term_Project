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
    # Option("Department", "add_department(db)"),
    Option("Course", "add_course(db)"),
    # Option("Major", "add_major(db)"),
    # Option("Student", "add_student(db)"),
    # Option("Section", "add_section(db)"),
    # Option("Enrollment", "add_enrollment(db)"),
    # Option("Student to Major", "add_student_major(db)"),
    # Option("Major to Student", "add_major_student(db)"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    # Option("Department", "delete_department(db)"),
    Option("Course", "delete_course(db)"),
    # Option("Major", "delete_major(db)"),
    # Option("Student", "delete_student(db)"),
    # Option("Section", "delete_section(db)"),
    # Option("Enrollment", "delete_enrollment(db)"),
    # Option("Student to Major", "delete_student_major(db)"),
    # Option("Major to Student", "delete_major_student(db)"),
    Option("Exit", "pass")
])

# options for testing the select functions
select_select = Menu('select select', 'Which type of object do you want to select:', [
    # Option("Department", "print(select_department(db))"),
    Option("Course", "print(select_course(db))"),
    # Option("Major", "print(select_major(db))"),
    # Option("Student", "print(select_student(db))"),
    # Option("Section", "print(select_section(db))"),
    # Option("Enrollment", "print(select_enrollment(db))"),
    # Option("Student Major", "print(select_student_major(db))"),
    Option("Exit", "pass")
])

# options for testing the update functions
update_select = Menu("update select", 'Which type of object do you want to update:', [
    # Option("Order", "update_enrollment_details()"),
    Option("Exit", "pass")
])

"""
This file is meant to be edited to insert mongo credentials. "MongoCredentials.py" is in the .gitignore.
To make your connection work, copy this info and paste into a new python file named "MongoCredentials.py".
Fill the information with your actual mongo connection info. it will be referenced in Utilities.py as:
mongodb+srv://{username}:{password}@{project}.{hash}.mongodb.net/?retryWrites=true&w=majority
"""
password: str = "password"
username: str = 'username'
project: str = 'project'
hash_name: str = 'hash'
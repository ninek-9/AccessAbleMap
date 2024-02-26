''' # useless to delete later

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'  # Or other DB URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
'''
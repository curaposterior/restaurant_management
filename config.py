import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'veryfsdlkfksldlf23123lssdgfsdvb442ddsfd'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    MIN_THRESHOLD_INGRIEDIENTS = 100

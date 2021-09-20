import os
import secrets

# Database initialization
basedir = os.path.abspath(os.path.dirname(__file__))
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SECRET_KEY = secrets.token_urlsafe(32)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOADS_DEFAULT_DEST = os.path.join(basedir, '/static/medias')
UPLOAD_FOLDER = 'app/static/data/img'
# MASKRCNN_IMAGE = 'app/static/data/img/tmp/'


MASKRCNN_IMAGE = 'app/utils/tmp/'
WIDTH_TUBE = 2.5

'''
URL
'''
URL = "127.0.0.1"
PORT = 5001
URI_API = "/api/v1/foamtastic"
endpoint_api = URL + ":"+ str(PORT) + URI_API
TESTING = False

'''
MONITORING
'''
PYBRAKE_PROJECT_ID = 333995
PYBRAKE_PROJECT_KEY = '552f307be8f27424695bb37ad4b73b53'
PYBRAKE_ENVIRONNEMENT = 'production'

'''
CELERY
'''
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
'''
UPLOAD_FOLDER = os.path.join('static', 'image')
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
FILE_UPLOAD_MAX_MEMORY_SIZE = 1000
'''
import os
import click
from flask import Flask
from celery import Celery


def create_app():
    print("create app")
    print("WELCOME it's FOAMTASTIC")
    # Flask stuff
    app = Flask(__name__, template_folder='templates',
                static_folder='static', instance_relative_config=True)
    app.config.from_object('config')
    # Celery configuration
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    with app.app_context():
        from . import routes
        return app


def init_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.control.purge()
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app = create_app()
celery = init_celery(app)
celery.finalize()
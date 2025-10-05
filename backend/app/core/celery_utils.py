from celery import Celery

celery_app = Celery(__name__)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery_app.conf.update(
        imports=('app.tasks.posting_tasks', 'app.tasks.ai_tasks')
    )
    # ---------------------------------

    celery_app.config_from_object(app.config, namespace='CELERY')
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app
from celery import Celery
from celery.schedules import crontab,timedelta

celery= Celery(__name__)


def init_celery(app):
    celery.conf.broker_url=app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend=app.config["CELERY_RESULT_BACKEND"]
    celery.conf.timezone="Asia/Kolkata"
    celery.conf.enable_utc=False
    
    
    celery.conf.beat_schedule= {
        "daily_remainder": {
            "task": "daily_reminder",
            "schedule": timedelta(seconds=30),

            # "schedule": crontab(hour=9,minute=0)
        },
        "monthly-report": {
            "task": "monthly_report",
            "schedule": crontab(
                day_of_month=1,
                hour=8,
                minute=0
            )
        }
    }
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery.Task=ContextTask
    
    celery.autodiscover_tasks(["placementportalcode.tasks"])
    
    return celery
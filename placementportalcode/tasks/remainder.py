from placementportalcode.celery_utils import celery


@celery.task(name="daily_reminder")
def daily_reminder():

    print("=" * 50)

    print("DAILY REMINDER TASK")

    print("=" * 50)
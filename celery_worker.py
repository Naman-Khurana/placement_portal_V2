from placementportalcode import create_app
from placementportalcode.celery_utils import celery, init_celery

app = create_app()

init_celery(app)
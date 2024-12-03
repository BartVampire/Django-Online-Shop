__all__ = ["app"]

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from djangoProject_all.celery import app

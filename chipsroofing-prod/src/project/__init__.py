try:
  from .celery import app as celery_app
except ImportError:
  pass

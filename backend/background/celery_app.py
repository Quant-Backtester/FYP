from celery import Celery
from configs import settings

app = Celery(
  main="BackgroundQueue",
  broker=settings
)

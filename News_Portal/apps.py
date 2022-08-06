import redis
from django.apps import AppConfig


class NewsPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News_Portal'


red = redis.Redis(
    host='redis-15312.c281.us-east-1-2.ec2.cloud.redislabs.com',
    port=15312,
    password='l0BMntBOyTYWIIjLUCYeXkiMPKvQgxXE',
)


class AppointmentConfig(AppConfig):
   name = 'News_Portal'

   def ready(self):
       import News_Portal.signals

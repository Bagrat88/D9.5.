from celery import shared_task
from .models import Order


def send_mails():
    print('Hello')


@shared_task
def complete_order(oid):
    order = Order.objects.get(pk=oid)
    order.complete = True
    order.save()

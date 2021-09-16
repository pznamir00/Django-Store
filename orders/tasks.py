from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone
from .models import Cart


"""
System that delete expired carts.
Application triggers this function 1 time per day
"""
@periodic_task(run_every=crontab(day=2))
def delete_expired_carts():
    Cart.objects.filter(expire_time__lte=timezone.now()).delete()
    return 'Deleted expired carts'
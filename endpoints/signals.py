from django import dispatch
from django.core.exceptions import PermissionDenied
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from endpoints import models
from endpoints import constants
import logging

logger = logging.getLogger(__name__)
del logging

@receiver(pre_delete, sender=models.AppUser)
def delete_user(sender, instance, **kwargs,):
    print(instance.user_type)
    if instance.user_type=='AD' and instance.is_superuser:
        raise PermissionDenied()
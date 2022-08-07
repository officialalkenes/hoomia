import uuid

from django.utils.translation import gettext_lazy as _

from django.db import models

class BaseModel(models.Model):
    """
    An Abstract class (Redundancy Elimination)
    """
    id = models.UUIDField(default=uuid.uuid4, verbose_name=_("Unique Model Id"),
                          unique=True, editable=False)
    pkid = models.BigAutoField(primary_key=True, editable=False,
                               verbose_name=_("Auto Increment Field"),
                               help_text=_("Not to be exposed to users"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
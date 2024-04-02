from django.db import models
from django.conf import settings
from management.models import Camera

# Create your models here.
class ExitEmailSend(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete = models.CASCADE)
    wait_for_sec = models.FloatField()
    from_email = models.TextField()
    text = models.TextField()
    date = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'exit_tbl'
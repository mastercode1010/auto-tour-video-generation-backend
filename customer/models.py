from django.db import models
from django.conf import settings

# Create your models here.
class Client(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    get_same_video = models.BooleanField(default=False)
    appears_in_others_video = models.BooleanField(default=False)
    voice_can_be_recorded = models.BooleanField(default=False)
    be_shown_potential = models.BooleanField(default=False)
    be_shown_public_business = models.BooleanField(default=False)
    be_shown_social_media = models.BooleanField(default=False)
    paid_status = models.BooleanField(default = False)
    rfid_tag = models.CharField(max_length = 255)
    tour_status = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client_tbl'

class Children(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    children_name = models.CharField(max_length=255)
    rfid_tag = models.CharField(max_length = 255)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'children_tbl'
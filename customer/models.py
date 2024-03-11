from django.db import models

# Create your models here.
class Client(models.Model):
    customer_id = models.IntegerField()
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    get_same_video = models.BooleanField(default=False)
    appears_in_others_video = models.BooleanField(default=False)
    voice_can_be_recorded = models.BooleanField(default=False)
    be_shown_potential = models.BooleanField(default=False)
    be_shown_public_business = models.BooleanField(default=False)
    be_shown_social_media = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'client_tbl'

class Children(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    children_name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'children_tbl'

class FacialPictures(models.Model):
    SIDE_CHOICES = [(1, 'Front 1'), (2, 'Front 2'), (3, 'Left'), (4, 'Right')]
    side_key = models.IntegerField()
    img_url = models.ImageField(upload_to='facial_pictures/')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    face_type = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'facial_pictures_tbl'
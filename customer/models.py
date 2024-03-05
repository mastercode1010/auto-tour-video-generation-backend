from django.db import models

# Create your models here.
class Client(models.Model):
    customer_id = models.IntegerField()
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    get_same_video = models.BooleanField(default=False)
    appears_in_other_video = models.BooleanField(default=False)
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
    side_key = models.IntegerField()
    img_url = models.ImageField(upload_to='facial_pictures/')
    client_id = models.IntegerField()
    face_type = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'facial_pictures_tbl'

    def save(self, *args, **kwargs):
        if self.face_type == 1 and not self.children:
            raise ValueError("For face_type 1, children must be set.")
        elif self.face_type == 0:
            self.children = None
        super(FacialPictures, self).save(*args, **kwargs)
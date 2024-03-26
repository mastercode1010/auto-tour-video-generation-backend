from django.db import models
from django.conf import settings
from management.models import Camera

# Create your models here.
class ColoringPage(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete = models.CASCADE)
    coloringpage = models.FileField(upload_to='coloringpage/')
    wait_for_sec = models.FloatField()
    text = models.TextField()
    date = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'coloring_page_tbl'
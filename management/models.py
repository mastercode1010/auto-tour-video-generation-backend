from click import File
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
import os
from io import BytesIO
from moviepy.editor import VideoFileClip
from PIL import Image
import io

os.environ["TMPDIR"] = "../media/thumbnailtemp"

class Camera(models.Model):
    camera_user_name = models.CharField(max_length=255)
    camera_name = models.CharField(max_length=255, blank=True, default='')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    camera_ip = models.CharField(max_length=255)
    camera_port = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'camera_tbl'
        constraints = [
            models.UniqueConstraint(fields=['camera_ip', 'camera_port'], name='unique_camera_ip_port')
        ]
        
class CameraVoice(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete = models.CASCADE)
    wait_for_sec = models.FloatField()
    enter_or_exit_code = models.BooleanField()
    text = models.TextField()
    date = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = 'camera_voice_tbl'

class Header(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_path = models.FileField(upload_to='headers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='headers/thumbnail/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the real save() method first.
        if not self.thumbnail:  # Check if the thumbnail already exists.
            self.generate_thumbnail()

    def generate_thumbnail(self):
        clip = VideoFileClip(self.video_path.path)
        temp_thumb = io.BytesIO()
        # Extract frame as an image
        frame = clip.get_frame(t=1)
        image = Image.fromarray(frame)
        image.save(temp_thumb, format='JPEG')  # Explicitly specify the format
        temp_thumb.seek(0)

        self.thumbnail.save(f"{self.pk}_thumbnail.jpg", ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        clip.close()
        self.save()
            
    class Meta:
        db_table = 'header_tbl'

class Video(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_path = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='videos/thumbnail/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the real save() method first.
        if not self.thumbnail:  # Check if the thumbnail already exists.
            self.generate_thumbnail()

    def generate_thumbnail(self):
        clip = VideoFileClip(self.video_path.path)
        temp_thumb = io.BytesIO()
        # Extract frame as an image
        frame = clip.get_frame(t=1)
        image = Image.fromarray(frame)
        image.save(temp_thumb, format='JPEG')  # Explicitly specify the format
        temp_thumb.seek(0)

        self.thumbnail.save(f"{self.pk}_thumbnail.jpg", ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        clip.close()
        self.save()

    class Meta:
        db_table = 'video_tbl'
        
class Footer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_path = models.FileField(upload_to='footers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='footers/thumbnail/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the real save() method first.
        if not self.thumbnail:  # Check if the thumbnail already exists.
            self.generate_thumbnail()

    def generate_thumbnail(self):
        clip = VideoFileClip(self.video_path.path)
        temp_thumb = io.BytesIO()
        # Extract frame as an image
        frame = clip.get_frame(t=1)
        image = Image.fromarray(frame)
        image.save(temp_thumb, format='JPEG')  # Explicitly specify the format
        temp_thumb.seek(0)

        self.thumbnail.save(f"{self.pk}_thumbnail.jpg", ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        clip.close()
        self.save()
            
    class Meta:
        db_table = 'footer_tbl'

class VideosPath(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, related_name='videos', on_delete=models.CASCADE)
    video_path = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'videos_tbl'

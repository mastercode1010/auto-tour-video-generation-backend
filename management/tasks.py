from celery import shared_task
from moviepy.editor import VideoFileClip
from django.core.files.base import ContentFile
from .models import Header, Thumbnail
import os

@shared_task
def generate_thumbnail(header_id):
    header = Header.objects.get(id=header_id)
    video_path = header.video_path.path
    clip = VideoFileClip(video_path)
    frame = clip.get_frame(1)  # Get a frame at 1 second into the video
    
    # Save frame to an image file
    frame_file_path = f"thumbnails/{header_id}_thumbnail.png"
    frame_file = ContentFile(frame)
    thumbnail = Thumbnail(header=header)
    thumbnail.image_path.save(frame_file_path, frame_file)
    thumbnail.save()
import time
from django.core.management.base import BaseCommand
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.conf import settings

class MediaChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.event_type == 'created' or event.event_type == 'modified':
            print("Media file changed, reloading server...")
            # Perform server reload here

class Command(BaseCommand):
    help = 'Watch media directory for changes'

    def handle(self, *args, **options):
        event_handler = MediaChangeHandler()
        observer = Observer()
        print(settings.MEDIA_ROOT)
        observer.schedule(event_handler, path=settings.MEDIA_ROOT, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

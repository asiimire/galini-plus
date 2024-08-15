import os
from django.core.management.base import BaseCommand
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from pathlib import Path

class Command(BaseCommand):
    help = 'Upload media files from local storage to S3'

    def handle(self, *args, **kwargs):
        s3_storage = S3Boto3Storage()
        local_media_path = Path(settings.MEDIA_ROOT)

        if not local_media_path.exists():
            self.stdout.write(self.style.ERROR(f"Media directory '{local_media_path}' does not exist."))
            return

        for root, dirs, files in os.walk(local_media_path):
            for filename in files:
                local_file_path = Path(root) / filename
                relative_path = local_file_path.relative_to(local_media_path)
                s3_path = str(relative_path)

                if s3_storage.exists(s3_path):
                    self.stdout.write(self.style.WARNING(f"'{s3_path}' already exists in S3. Skipping..."))
                else:
                    with local_file_path.open('rb') as file:
                        s3_storage.save(s3_path, file)
                        self.stdout.write(self.style.SUCCESS(f"Uploaded '{s3_path}' to S3"))

        self.stdout.write(self.style.SUCCESS("All files uploaded successfully."))

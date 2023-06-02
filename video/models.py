from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=255)  # Add s3_key field
    video_file = models.FileField(upload_to='videos/')

class SubtitleKeyword(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

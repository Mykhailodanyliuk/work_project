from django.db import models


class Patent(models.Model):
    patent_application_number = models.CharField(max_length=128, unique=True)
    invention_title = models.TextField()
    data = models.JSONField()
    upload_at = models.DateTimeField(auto_now=True)
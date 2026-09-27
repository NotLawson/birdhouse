from django.db import models
import uuid

# Files
class File(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fileType        = models.CharField(max_length=255) # mimetype
    location        = models.CharField(max_length=255) # storage provider name. either 'disk' or 's3'

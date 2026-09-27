from django.db import models
from datetime import datetime as dt, timedelta as td, timezone as tz
from api.models import File
import uuid

# Snapshot Data
def currentTimestampUTC(): return dt.now(tz.utc)
class Snapshot(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp       = models.TimeField(default=currentTimestampUTC())

    thumbnail       = models.ForeignKey(to=File.id, on_delete=models.SET_NULL, null=True) # TODO: Update this with default thumbnail
    videoSnapshot   = models.ForeignKey(to=File.id, on_delete=models.SET_NULL, null=True)
    archived        = models.BooleanField(default=False) # after 30 days, archive video for storage space

    temperature     = models.FloatField()
    humidity        = models.IntegerField()
    lightIntensity  = models.IntegerField()

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Queue archive task in 30 days
            from .tasks import archiveSnapshot
            archiveSnapshot.enqueue(snapshot=self, run_after=dt.now(tz.utc) + td(days=30))
        super().save(*args, **kwargs)

from django.tasks import task
from .models import Snapshot

@task
def archiveSnapshot(snapshot: Snapshot):
    # Archive snapshot video by offloading to external service e.g. Drive
    snapshot.archived = True
    snapshot.save()
    return 
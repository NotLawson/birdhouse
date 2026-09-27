from django.shortcuts import render
from django.http import response, request
from dashboard.models import Snapshot

# Upload Snapshot
def uploadSnapshot(req: request.HttpRequest):
    if req.method == "POST":
        # download video + thumbnail
        


    
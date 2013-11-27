import os
import uuid

from django.conf import settings


def handle_uploaded_file(f):
    unique_id = str(uuid.uuid4())
    filename = os.path.join(settings.MEDIA_ROOT, unique_id)
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    print "$$$$$$$$$$$$", unique_id
    return unique_id

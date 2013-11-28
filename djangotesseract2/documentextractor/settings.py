from django.conf import settings

PAGINATE_BY = getattr(settings, "PAGINATE_BY", 10)

IMAGE_RESOLUTION = getattr(settings, "IMAGE_RESOLUTION", 200)
COMPRESSION_QUALITY = getattr(settings, "COMPRESSION_QUALITY", 70)

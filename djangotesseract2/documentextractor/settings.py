from django.conf import settings

PAGINATE_BY = getattr(settings, "PAGINATE_BY", 10)

import os

from django.conf import settings

from celery import task
import requests

from .core import DocumentExtractor

@task
def send_ocr_results(file_id, cb_url, token):
    filepath = os.path.join(settings.MEDIA_ROOT, file_id)

    document = DocumentExtractor(filepath)
    total_pages = document.file.numPages

    for page_dict in document:
        page_num = page_dict['page']
        payload = {
            'corpus': page_dict['text'],
            'page': page_num,
            'is_last_page': 1 if page_num == total_pages else 0,
            'token': token,
        }
        r = requests.post(cb_url, data=payload)
        r.raise_for_status()
    return

import os

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from rest_framework.pagination import PaginationSerializer
import requests

from documentextractor.serializers import DocumentSerializer

from .core import DocumentExtractor
from .utils import handle_uploaded_file
from .settings import PAGINATE_BY


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


class Document(APIView):
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request, format=None):
        file_obj = request.FILES['file']
        file_id = handle_uploaded_file(file_obj)

        serializer = DocumentSerializer(data={'fileid': file_id})
        if not serializer.is_valid():
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        cb_url = request.POST.get('callback_url', None)
        if cb_url:
            send_ocr_results(file_id, cb_url, request.auth.key)
        return Response(serializer.data,
            status=status.HTTP_201_CREATED)


class Pages(APIView):
    def get(self, request, format=None):
        fileid = request.GET.get('fileid', None)
        if not fileid:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        filepath = os.path.join(settings.MEDIA_ROOT, fileid)

        try:
            document = DocumentExtractor(filepath)
        except IOError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        paginator = Paginator(document, PAGINATE_BY)
        page_param = request.QUERY_PARAMS.get('page', 1)

        try:
            page = paginator.page(int(page_param))
        except EmptyPage:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = PaginationSerializer(instance=page)
        serializer.data.update({
            'title': document.file.documentInfo.title,
            'author': document.file.documentInfo.author,
            'subject': document.file.documentInfo.subject,
        })

        return Response(serializer.data)

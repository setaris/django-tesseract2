from django.conf.urls import patterns, url

from .views import Document, Pages

urlpatterns = patterns('',
    url(r'^document/', Document.as_view()),
    url(r'^pages/', Pages.as_view())
)

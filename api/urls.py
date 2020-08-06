from django.conf.urls import url
from .views import GetCheck, NewCheck, PdfCheck

urlpatterns = [
    url(r'^create_checks/$', GetOrder.as_view(), name='create_checks'),
    url(r'^new_checks/(?P<api_key>\w+)/$', NewCheck.as_view(), name='new_checks'),
    url(r'^check/(?P<api_key>\w+)/(?P<check_id>\d+)/$', PdfCheck.as_view(), name='check'),
]


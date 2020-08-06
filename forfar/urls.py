from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/checks/', include('checks.urls', namespace='checks')),
    url(r'^django-rq/', include('django_rq.urls'))
]

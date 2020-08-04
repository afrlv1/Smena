from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^", include("api.urls")),
]
# For django_rq
urlpatterns += [
    url(r'^django-rq/', include('django_rq.urls')),
]

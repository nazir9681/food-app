from django.urls import include, path
from rest_framework import routers 
from django.conf import settings 
from django.conf.urls.static import static
from . import views
app_name= 'notification'

urlpatterns = [
    path('sendFirebaseNotification',views.sendFirebaseNotification,name="sendFirebaseNotification"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
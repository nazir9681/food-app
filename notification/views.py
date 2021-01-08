from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import Response
from rest_framework.decorators import api_view
from firstapi.models import *
from firstapi.serializers import *
#from pyfcm import FCMNotification
from fcm_django.models import FCMDevice

# Create your views here.

@api_view(['POST'])
def sendFirebaseNotification(request):
    return Response("hello")
    # data = MyUser.objects.all()
    # myData = MyUserSerializer(data, many=True).data
    # return Response(myData)

    # push_service = FCMNotification(api_key="AAAAlt2NKes:APA91bGXFhsEQVkeROWZyUhvLIOt45K_gxYtoAfZPbVnqmBmMvX3auPzYq8C_KCuGV62p19_p9bGxtZYnIsBtNTg8S5mVFhEUiJAhTQ05-RwQHdoMMtuaMT6bo17BcO8AyC-e-9mbzSG")

    # registration_id = "dX6crLP4SB4:APA91bHhxXTylNyFiKJT4HE1khcHa9lH53mghHdEFx3pdxWZ_cVpyJSBSdbpzscCkuaA1jjPkppqHfu6jI133bxMvbO-IHh9KcLO2MhTnnGAouqLxVy-zY30aRH3BdJLJ5kH-X2C5oky"
    # message_title = "hello"
    # message_body = "DIGISUN"
    # result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    # return Response(result)
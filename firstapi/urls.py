from django.urls import include, path
from rest_framework import routers 
from django.conf import settings 
from django.conf.urls.static import static
from . import views
app_name= 'firstapi'

urlpatterns = [
    path('sendOtp',views.sendOtp,name="sendOTP"),
    path('socialLogin',views.socialLogin,name="socialLogin"),
    path('userRegistration',views.userRegistration,name="userRegistration"),
    path('userLogin',views.userLogin,name="userLogin"),
    path('changeUserPassword',views.changeUserPassword,name="changeUserPassword"),
    path('forgotPassword',views.forgotPassword,name="forgotPassword"),
    path('addPhoneNumber',views.addPhoneNumber,name="addPhoneNumber"),
    path('homeApi',views.homeApi,name="homeApi"),
    path('editProfile',views.editProfile,name="editProfile"),
    path('orderCategory',views.orderCategory,name="orderCategory"),
    path('showHotelBookingData',views.showHotelBookingData,name="showHotelBookingData"),
    path('orderPlaceApi',views.orderPlaceApi,name="orderPlaceApi"),
    path('orderCategoryFood',views.orderCategoryFood,name="orderCategoryFood"),
    path('orderHomeFood',views.orderHomeFood,name="orderHomeFood"),
    path('addCartApi',views.addCartApi,name="addCartApi"),
    path('showCartApi',views.showCartApi,name="showCartApi"),
    path('doubleAddCartApi',views.doubleAddCartApi,name="doubleAddCartApi"),
    path('deleteCartApi',views.deleteCartApi,name="deleteCartApi"),
    path('orderHistoryApi',views.orderHistoryApi,name="orderHistoryApi"),
    path('demo',views.demo,name="demo"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
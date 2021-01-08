from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import Response
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
import random
import string
import requests
from django.db import connection
from django.contrib.auth.hashers import make_password
import datetime
import json
import time


@api_view(['POST'])
def sendOtp(request):
    if request.POST['user_phone']:
        phone=request.POST['user_phone']
        key = random.randint(999,9999)
        print(key)
        if key:
            link = f'http://zapsms.co.in/vendorsms/pushsms.aspx?user=dpandit&password=sandeep1&msisdn={phone}&sid=CELEVN&msg={key}&fl=0&gwid=2'
            requests.get(link)
            return Response({
                'status' : 'Success',
                'detail' : 'OTP sent successfully.',
                'user' : 'true',
                'OTP' : key
                })
        else:
            return Response({
                'status' : False,
                'detail' : 'Sending OTP error.'
                })
    else:
        return Response({"status":"failed","msg":"Invalid Request"})

@api_view(['POST'])
def socialLogin(request):
    if request.POST['user_social_id']:
        social_id=request.POST['user_social_id']
        checkSocialID=MyUser.objects.filter(user_social_id=social_id)
        if len(checkSocialID)==0:
            serializer = MyUserSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"status":"Success","msg":"Login successfully","user":"true","data":serializer.data})
            else:
                return Response({"Error":"Invalid details"})
        else:
            check=MyUser.objects.get(user_social_id=social_id)
            data=MyUserSerializer(check).data
            if data['user_status'] == "0":
                return Response({"status":"User is Suspended"})
            else:
                if not data['user_phone']:
                    return Response({"status":"Success","msg":"Login successfully","user":"true","data":data})
                else:    
                    return Response({"status":"Success","msg":"Login successfully","user":"false","data":data})
    else:
        return Response({"status":"failed","msg":"Invalid Request"})

@api_view(['POST'])
def userRegistration(request):
    if request.POST['user_email']:
        userEmail=request.POST['user_email']
        userPhone=request.POST['user_phone']
        chechEmailID = MyUser.objects.filter(user_email = userEmail)
        if len(chechEmailID) == 0:
            checkPhone = MyUser.objects.filter(user_phone = userPhone)
            if len(checkPhone) == 0:
                serializer = MyUserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status":"Success","msg":"Login successfully","user":"true","data":serializer.data})
                else:
                    return Response({"status":"failed","msg":"invalid Request"})
            else:
                return Response({"status":"failure","msg":"Phone Number is already registered"})
        else:
            return Response({"status":"failure","msg":"Email is already registered"})
    else:
        return Response({"status":"failed","msg":"invalid Request"})

@api_view(['POST'])
def userLogin(request):
    if request.POST['user_email']:
        userEmail=request.POST['user_email']
        password=request.POST['user_password']
        chechEmailID = MyUser.objects.filter(user_email = userEmail)
        if len(chechEmailID) != 0:
            checkPassword = MyUser.objects.filter(user_password = password, user_email = userEmail)
            if len(checkPassword) != 0:
                userData = MyUser.objects.get(user_email = userEmail)
                data = MyUserSerializer(userData).data
                return Response({"status":"Success","msg":"Login successfully","data":data})
            else:
                return Response({"status":"Failure","msg":"Password Wrong"})
        else:
            return Response({"status":"Failure","msg":"Email is not registered..! please signup"})
    else:
        return Response({"status":"failed","msg":"invalid Request"})

@api_view(['POST','PUT'])
def changeUserPassword(request):
    if request.POST['id'] and request.POST['old_password']:
        user_id = request.POST['id']
        oldPassword = request.POST['old_password']
        checkPassword = MyUser.objects.filter(user_password = oldPassword, id = user_id)
        if len(checkPassword)==0:
            return Response("old password is wrong")
        else:
            check = MyUser.objects.get(id= user_id)
            data = MyUserSerializer(check).data
            return Response(data)
            serializer = MyUserSerializer(check, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status":"Success","msg":"password changed successfully"})
            else:
                return Response({"msg":"Complete Password requirement"})
    else:
        return Response({"status":"failed","msg":"invalid Request"})

@api_view(['POST','PUT'])
def addPhoneNumber(request):
    if request.POST['user_id'] and request.POST['user_phone']:
        user_id = request.POST['user_id']
        check = MyUser.objects.get(id= user_id)
        serializer = MyUserSerializer(check, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"Success","msg":"Login successfully"})
        else:
            return Response({"status":"Failure","msg":"Login Failed"})
    else:
        return Response({"status":"failed","msg":"invalid Request"})

@api_view(['POST','PUT'])
def forgotPassword(request):
    userEmail = request.POST['user_email']
    checkEmailExist = MyUser.objects.filter(user_email = userEmail)
    if len(checkEmailExist)==0:
        return Response({"status":"Failure","msg":"Email is not exist please register your email"})
    else: 
        obj = MyUser.objects.get(user_email = userEmail)
        dataCheck = MyUserSerializer(obj).data
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        check = MyUser.objects.get(id= dataCheck['id'])
        check.user_password= result_str
        check.save()

        return Response({"status":"Success","msg":"password changed successfully"})

@api_view(['POST'])
def editProfile(request):
    if request.POST['user_id']:
        userID = request.POST['user_id']
        checkUser = MyUser.objects.get(id = userID)
        serializer = MyUserSerializer(checkUser, data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = MyUserSerializer(checkUser).data
            return Response({"status":"Success","msg":"Profile Edit Successfully","data":data})
        else:
            return Response({"status":"Failure","msg":"invalid Request"})
    else:
        return Response({"status":"Failure","msg":"invalid Request"})

@api_view(['GET'])
def homeApi(request):
    banner = MyBanner.objects.filter(status = '1')
    foodbanner=MyBannerSerializer(banner,many=True).data

    check=MyFoodItem.objects.filter(status = '1')
    data=MyFoodItemSerializer(check,many=True).data

    hotel = MyHotel.objects.filter(status = '1')
    goOut=MyHotelSerializer(hotel,many=True).data

    return Response({"status":"Success","banner":foodbanner,"data":data,"GoOut":goOut})

@api_view(['POST'])
def showHotelBookingData(request):
    if request.POST['hotel_id']:
        hotelID = request.POST['hotel_id']
        hotel = MyHotel.objects.filter(status = '1' , id= hotelID)

        if len(hotel)==0:
            return Response({"status":"Failure","msg":"invalid"})
        else:
            check = MyHotel.objects.get(id= hotelID)
            serializer = MyHotelSerializer(check).data

            a = int(serializer['hotel_total_seats'])

            personSeat = []
            for i in range (1,a+1):
                personSeat.append({"noSeats":str(i)})

            datess = []
            base = datetime.datetime.today()

            for x in range(1, 6):
                dateFormat = base + datetime.timedelta(days=x)
                dateFormat = dateFormat.strftime("%d %b")
                datess.append({"bookingDate":dateFormat})

            start_time = serializer['hotel_open_time']
            start_time=start_time[:-3]
            
            end_time = serializer['hotel_close_time']
            end_time=end_time[:-3]

            slot_time = 30

            start_date = datetime.datetime.now().date()
            end_date = datetime.datetime.now().date() + datetime.timedelta(days=5)

            days = []
            date = start_date
            while date <= end_date:
                hours = []
                time = datetime.datetime.strptime(start_time, '%H:%M')
                end = datetime.datetime.strptime(end_time, '%H:%M')
                while time <= end:
                    hours.append({"bookingTime":time.strftime("%I:%M %p")})
                    time += datetime.timedelta(minutes=slot_time)
                date += datetime.timedelta(days=1)
                days.append(hours)

            return Response({"status":"Success","personSeat":personSeat,"date":datess, "time":hours})

    else:
        return Response({"status":"Failure","msg":"invalid Request"})

@api_view(['GET'])
def orderCategory(request):
    category = MainCategory.objects.filter(status = '1')
    categoryData=MainCategorySerializer(category,many=True).data
    
    for i in categoryData:
        for j in i['myFoodItem']:
            j['category_main_id'] = i['main_category_id']

    for i in categoryData:
        res = i['myFoodItem']
        for j in res:
            del(j['restaurant_detail']['restaurant_imageUpload'])
            del(j['restaurant_detail']['created_at'])
            del(j['restaurant_detail']['updated_at'])

    return Response({"status":"Success","data":categoryData})

@api_view(['POST'])
def orderCategoryFood(request):
    if request.POST['main_category_id'] and request.POST['id']:
        mainCategoryId = request.POST['main_category_id']
        userId = request.POST['my_users']
        restaurantId = request.POST['id']
        restaurantData = MyFoodItem.objects.filter(main_food_category = mainCategoryId, restaurant_detail = restaurantId)
        data = MyFoodItemSerializer(restaurantData,many=True).data

        cartobj = MyCart.objects.filter(my_users = userId,restaurant_id = restaurantId)
        myCart= MyCartSerializer(cartobj, many=True).data

        for resData in data:
            resData['inCart'] = 'False'
            for resCart in myCart:
                if resData['product_id'] == resCart['my_foods']:
                    resData['inCart'] = 'True'

            a=0
            for i in myCart:
                a+= int(i['total_number_items'])
            a=str(a)

        for i in data:
            del(i['restaurant_detail'])
            del(i['status'])

        return Response({"status":"Success","data":data,"cartCount":a,'restaurantId':restaurantId})


@api_view(['POST'])
def orderHomeFood(request):
    if request.POST['id']:
        restaurantId = request.POST['id']
        userId = request.POST['my_users']

        restaurantData = MyFoodItem.objects.filter(restaurant_detail = restaurantId)
        data = MyFoodItemSerializer(restaurantData,many=True).data

        cartobj = MyCart.objects.filter(my_users = userId,restaurant_id = restaurantId)
        myCart= MyCartSerializer(cartobj, many=True).data

        for resData in data:
            resData['inCart'] = 'False'
            for resCart in myCart:
                if resData['product_id'] == resCart['my_foods']:
                    resData['inCart'] = 'True'
                    
        
        a=0
        for i in myCart:
            a+= int(i['total_number_items'])
        a=str(a)


        for i in data:
            del(i['restaurant_detail'])
        return Response({"status":"Success","data":data,"cartCount":a,'restaurantId':restaurantId})
    else:
        return Response({"status":"Failure","msg":"invalid Request"})

@api_view(['POST'])
def addCartApi(request):
    if request.POST['my_users'] and request.POST['my_foods']:
        userId = request.POST['my_users']
        productId = request.POST['my_foods']
        restaurantId = request.POST['restaurant_id']

        cartData = MyCart.objects.filter(my_users = userId)
        if len(cartData)==0:
            
            serializer = MyCartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                status = "Success"
                msg = "item added Successfully"
            else:
                return Response({"status":"Failure","msg":"invalid Request"})
        else:
            cartobj1 = MyCart.objects.filter(my_foods = productId, my_users = userId)
            if len(cartobj1)==0:
                serializer = MyCartSerializer(data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                    status = "Success"
                    msg = "item added Successfully"
                else:
                    return Response({"status":"Failure","msg":"invalid Request"})
            else:
                status = "failure"
                msg = "item is already exist Go to Cart"
                


        cartobj3 = MyCart.objects.filter(my_users = userId, restaurant_id = restaurantId)
        myCart= MyCartSerializer(cartobj3, many=True).data
        
        a=0
        for i in myCart:
            a+= int(i['total_number_items'])
        a=str(a)
        return Response({"status":status,"msg":msg,"cart_count":a})
    else:
        return Response({"status":"Failure","msg":"invalid Request"})

@api_view(['POST'])
def doubleAddCartApi(request):
    if request.POST['my_foods'] and request.POST['my_users']:
        productId = request.POST['my_foods']
        userId = request.POST['my_users']


        #getting data from mycart
        cartobj = MyCart.objects.get(my_foods = productId, my_users = userId)
        cartItem = MyCartSerializer(cartobj).data

        #getting amount from food item
        priceData = MyFoodItem.objects.get(id = productId)
        data = MyFoodItemSerializer(priceData).data

        #updating mycart
        check = MyCart.objects.get(id = cartItem['id'])
        dataC = MyCartSerializer(check).data
        
         
        check.total_number_items= int(dataC['total_number_items']) +1
        check.total_price= int(data['food_item_discount']) * (int(dataC['total_number_items'])+1)
        check.save()
        status = "Success"
        msg = "item added Successfully"

        #show data from mycart
        cartobj1 = MyCart.objects.filter(my_users = userId)
        cartItem1 = MyCartSerializer(cartobj1, many=True).data

        return Response({"status":status,"msg":msg,"data":cartItem1})
    else:
        return Response({"status":"Failure","msg":"invalid Request"})

@api_view(['POST'])
def showCartApi(request):
    userId = request.POST['my_users']
    restaurantId = request.POST['id']

    cartobj = MyCart.objects.filter(my_users = userId , restaurant_id = restaurantId)
    myCart= MyCartSerializer(cartobj, many=True).data

    for cartData in myCart:
        restaurantData = MyFoodItem.objects.get(id = cartData['my_foods'])
        cartData['foodData'] = MyFoodItemSerializer(restaurantData).data

    for remData in myCart:
        del(remData['foodData']['restaurant_detail'])
        del(remData['my_users'])
        del(remData['created_at'])
        del(remData['updated_at'])

    countItemData =0
    countPriceData =0
    for counData in myCart:
        countItemData += int(counData['total_number_items'])
        countPriceData += int(counData['total_price'])

    return Response({"status":"Success","itemTotalCount":countItemData,"priceTotalCount":countPriceData,"data":myCart})

@api_view(['POST'])
def deleteCartApi(request):
    if request.POST['my_users'] and request.POST['my_foods']:
        userId = request.POST['my_users']
        foodId = request.POST['my_foods']

        checkData = MyCart.objects.filter(my_users = userId,my_foods = foodId)

        if len(checkData) ==0:
            return Response({"status":"failure","msg":"Item not found"})

        else:
            #getting amount from food item
            priceData = MyFoodItem.objects.get(id = foodId)
            dataprice = MyFoodItemSerializer(priceData).data

            #getting data from Cart
            cartGetData = MyCart.objects.get(my_users = userId,my_foods = foodId)
            data = MyCartSerializer(cartGetData).data

            cartGetData.total_number_items= int(data['total_number_items']) -1
            cartGetData.total_price= int(dataprice['food_item_discount']) * (int(data['total_number_items'])-1)
            cartGetData.save()

            cartGetData1 = MyCart.objects.get(my_users = userId,my_foods = foodId)
            data1 = MyCartSerializer(cartGetData1).data

            #deleting data from mycart
            if data1['total_number_items'] < '1':
                cartGetData.delete()
                return Response({"status":"Success","msg":"food item deleted"})

            else:
                return Response({"status":"Success","msg":"Item is deleted"})
                
    else:
        return Response({"status":"Failure","msg":"invalid Request"})

@api_view(['POST'])
def orderHistoryApi(request):
    user_ID = request.POST['user_id']

    orderHistoryData = OrderHistory.objects.filter(user_id = user_ID)
    data = OrderHistorySerializer(orderHistoryData,many=True).data

    return Response({"status":"Success","data":data})



@api_view(['POST'])
def orderPlaceApi(request):
    if request.POST['user_id']:
        return Response("OK")
    else:
        return Response({"status":"Failure","msg":"invalid Request"})

@api_view(['POST'])
def demo(request):
    a = request.POST['text1']

    b = request.POST['text2']
    
    test_keys = a.split(',') 
    test_values = b.split(',') 

    res = {} 
    for key in test_keys: 
        for value in test_values: 
            res[key] = value 
            test_values.remove(value) 
            break      
    return Response(res)
    
from rest_framework import serializers

from .models import *

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

class MyRestaurantSerializer(serializers.ModelSerializer):
    #myFoodItem=serializers.SerializerMethodField()
    restaurant_id = serializers.IntegerField(source='id')
    class Meta:
        model = MyRestaurant
        fields=['restaurant_id','restaurant_name','restaurant_imageUpload','restaurant_address','status']
        #fields = '_all_'
        

    # def get_myFoodItem(self,object):
    #     queryset=object.restaurantdetail.filter().order_by('-id')[:1]
    #     myData = MyFoodItemSerializer(queryset,many=True).data
    #     return myData

class MyRestaurantDataSerializer(serializers.ModelSerializer):
    #myFoodItem=serializers.SerializerMethodField()
    #restaurant_id = serializers.IntegerField(source='id')
    class Meta:
        model = MyRestaurant
        fields=['id','restaurant_name','restaurant_address','status','myFoodItem']
        #fields = '_all_'
        

    # def get_myFoodItem(self,object):
    #     #queryset=object.restaurantdetail.filter().order_by('-id')[:1]
    #     myData = MyFoodSerializer(queryset,many=True).data
    #     return myData

# class MyFoodSerializer(serializers.ModelSerializer):
    
#     product_id = serializers.IntegerField(source='id')
#     class Meta:
#         model = MyFoodItem
#         fields = ['product_id','food_item_name','food_item_imageUpload','food_item_discount','food_item_amount','food_item_rating','status']

class MyFoodItemSerializer(serializers.ModelSerializer):
    
    product_id = serializers.IntegerField(source='id')
    class Meta:
        model = MyFoodItem
        fields = ['product_id','food_item_name','food_item_imageUpload','food_item_discount','food_item_amount','food_item_rating','status','restaurant_detail']
        depth = 1



class MyBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBanner
        fields=['id','banner_name','banner_imageUpload','status']

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields=['hotel_imageUpload']


class MyHotelSerializer(serializers.ModelSerializer):
    myHotelImage=serializers.SerializerMethodField()
    hotel_id = serializers.IntegerField(source='id')
    class Meta:
        model = MyHotel
        fields=['hotel_id','hotel_name','food_category','myHotelImage','hotel_total_seats','Description','hotel_contact','hotel_address','hotel_discount','hotel_amount','hotel_open_time','hotel_close_time','hotel_rating','status']
        #fields = '_all_'

    def get_myHotelImage(self,object):
        queryset=object.myhotel.all()
        return HotelImageSerializer(queryset,many=True).data
    

class MainCategorySerializer(serializers.ModelSerializer):
    myFoodItem=serializers.SerializerMethodField()
    main_category_id = serializers.IntegerField(source='id')
    class Meta:
        model = MainCategory
        fields=['main_category_id','main_category_name','status','myFoodItem']
    

    def get_myFoodItem(self,object):
        queryset=object.mainfoodcategory.filter()
        return MyFoodItemSerializer(queryset,many=True).data

class MyCartSerializer(serializers.ModelSerializer):
    #my_cart_id = serializers.IntegerField(source='id')
    class Meta:
        model = MyCart
        #fields=['my_cart_id','my_users','my_foods','restaurant_id','total_number_items','total_price','created_at','updated_at']
        fields= '__all__'

class OrderHistorySerializer(serializers.ModelSerializer):
    order_history_id = serializers.IntegerField(source='id')
    class Meta:
        model = OrderHistory
        fields = ['order_history_id','user_id','transaction_id','paid_amount','payment_date']
    
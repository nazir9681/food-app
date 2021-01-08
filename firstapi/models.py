from django.db import models
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
STATUS_CHOICES = [
    ('0', 'Suspended'),
    ('1', 'Live'),
]
BANNER_CHOICES = [
    ('0', 'Main'),
]

STATUS = [
    ('1', 'ACTIVE'),
    ('0', 'INACIVE'),
    
]


class MyUser(models.Model):
    user_name = models.CharField(max_length=60, null=True, blank=True)
    user_email = models.EmailField(max_length=60, null=True, blank=True,unique=True)
    user_password = models.CharField(max_length=60, null=True, blank=True)
    user_phone = models.CharField(max_length=20,null=True, blank=True,unique=True)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)
    user_gender = models.CharField(max_length=60, null=True, blank=True)
    user_social_id = models.CharField(max_length=60, null=True, blank=True)
    user_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')
    user_dob = models.CharField(max_length=60, null=True, blank=True)
    user_address = models.CharField(max_length=200, null=True, blank=True)
    user_image = models.CharField(max_length=300, null=True, blank=True)
    user_imageUpload = models.ImageField('upload/images/',null=True, blank=True)
    login_type = models.CharField(max_length=60, null=True, blank=True)
    forgot_pass_token = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_name

class MyBanner(models.Model):
    banner_name = models.CharField(max_length=60, null=True, blank=True)
    banner_imageUpload = models.ImageField('upload/images/',null=True, blank=True)
    banner_type = models.CharField(max_length=1, choices=BANNER_CHOICES, default='1')
    status = models.CharField(max_length=1, choices=STATUS, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.banner_name

class MainCategory(models.Model):
    main_category_name = models.CharField(max_length=60, null=True, blank=True)
    main_category_imageUpload = models.ImageField('upload/images/',null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.main_category_name

class MyRestaurant(models.Model):
    restaurant_name = models.CharField(max_length=60, null=True, blank=True)
    restaurant_username = models.CharField(max_length=60, null=True, blank=True)
    restaurant_password = models.CharField(max_length=60, null=True, blank=True)
    restaurant_imageUpload = models.ImageField('upload/images/',null=True, blank=True)
    restaurant_address = models.CharField(max_length=60, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.restaurant_name

class MyFoodItem(models.Model):
    restaurant_detail = models.ForeignKey(MyRestaurant, on_delete=models.CASCADE,related_name='restaurantdetail')
    main_food_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE,related_name='mainfoodcategory')
    food_item_name = models.CharField(max_length=60, null=True, blank=True)
    food_item_imageUpload = models.ImageField('upload/images/',null=True, blank=True)
    food_item_discount = models.CharField(max_length=60, null=True, blank=True)
    food_item_amount = models.CharField(max_length=60, null=True, blank=True)
    food_item_rating = models.CharField(max_length=60, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.food_item_name


class MyHotel(models.Model):
    hotel_name = models.CharField(max_length=60, null=True, blank=True)
    food_category = models.CharField(max_length=60, null=True, blank=True)
    #hotel_imageUpload = models.ImageField('upload/images/',null=True, blank=True)
    hotel_address = models.CharField(max_length=60, null=True, blank=True)
    hotel_open_time = models.TimeField(null=True, blank=True)
    hotel_close_time = models.TimeField(null=True, blank=True)
    hotel_discount = models.CharField(max_length=60, null=True, blank=True)
    hotel_amount = models.CharField(max_length=60, null=True, blank=True)
    hotel_contact = models.CharField(max_length=60, null=True, blank=True)
    hotel_total_seats = models.CharField(max_length=60, null=True, blank=True)
    hotel_rating = models.CharField(max_length=60, null=True, blank=True)
    Description = RichTextUploadingField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.hotel_name

class HotelImage(models.Model):
    my_hotel = models.ForeignKey(MyHotel, on_delete=models.CASCADE,related_name='myhotel')
    hotel_imageUpload = models.ImageField('upload/images/',null=True, blank=True)


class MyCart(models.Model):
    my_users = models.ForeignKey(MyUser, on_delete=models.CASCADE,related_name='myuser')
    my_foods = models.ForeignKey(MyFoodItem, on_delete=models.CASCADE,related_name='myfood')
    restaurant_id = models.ForeignKey(MyRestaurant, on_delete=models.CASCADE,related_name='myfood')
    total_number_items = models.CharField(max_length=60, null=True, blank=True,default='1')
    total_price = models.CharField(max_length=60, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.total_number_items

class OrderHistory(models.Model):
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE,related_name='userID')
    transaction_id = models.CharField(max_length=60,null=True,blank=True)
    payment_type = models.CharField(max_length=60,null=True,blank=True)
    paid_amount = models.CharField(max_length=60,null=True,blank=True)
    payment_date = models.CharField(max_length=60,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.transaction_id
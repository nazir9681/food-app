from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.

admin.site.site_header = 'Food Delivery Dashboard'
admin.site.unregister(Group)


class InlineMyFoodItem(admin.StackedInline):
    model = MyFoodItem
    extra = 1

class InlineHotelImage(admin.StackedInline):
    model = HotelImage
    extra = 1

def make_activate_user(modeladmin,request,queryset):
    queryset.update(user_status='1')
make_activate_user.short_description = "Marks as Live user"

def make_inactivate_user(modeladmin,request,queryset):
    queryset.update(user_status='0')
make_inactivate_user.short_description = "Marks as Suspend user"

def make_activate(modeladmin,request,queryset):
    queryset.update(status='1')
make_activate.short_description = "Marks as Activate"

def make_inactivate(modeladmin,request,queryset):
    queryset.update(status='0')
make_inactivate.short_description = "Marks as Inactive"

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id','user_name','user_phone','user_email','user_status')
    list_display_links = ('user_name',)
    list_editable = ('user_status',)
    actions = [make_activate_user,make_inactivate_user]
    search_fields = ('id', 'user_name', 'user_email', )
    list_filter = ['created_at']
admin.site.register(MyUser,MyUserAdmin)

class MyBannerAdmin(admin.ModelAdmin):
    list_display = ('id','banner_name','banner_type','banner_imageUpload','status')
    list_editable = ('status',)
    actions = [make_activate,make_inactivate]
    search_fields = ('id', 'banner_name', )
admin.site.register(MyBanner,MyBannerAdmin)

class MyFoodItemAdmin(admin.ModelAdmin):
    list_display = ('id','food_item_name','food_item_imageUpload','food_item_amount','food_item_rating','status')
    list_display_links = ('food_item_name',)
    list_editable = ('status',)
    actions = [make_activate,make_inactivate]
    search_fields = ('id', 'food_item_name', )
admin.site.register(MyFoodItem,MyFoodItemAdmin)

class MyRestaurantAdmin(admin.ModelAdmin):
    inlines = [InlineMyFoodItem]
    list_display = ('id','restaurant_name','restaurant_address','restaurant_imageUpload','status')
    list_display_links = ('restaurant_name',)
    list_editable = ('status',)
    actions = [make_activate,make_inactivate]
    search_fields = ('id', 'restaurant_name', )
admin.site.register(MyRestaurant,MyRestaurantAdmin)

class MyHotelAdmin(admin.ModelAdmin):
    inlines = [InlineHotelImage]
    list_display = ('id','hotel_name','hotel_address','status')
    list_display_links = ('hotel_name',)
    list_editable = ('status',)
    actions = [make_activate,make_inactivate]
    search_fields = ('id', 'hotel_name', )
admin.site.register(MyHotel,MyHotelAdmin)

class MainCategoryAdmin(admin.ModelAdmin):
    inlines = [InlineMyFoodItem]
    list_display = ('id','main_category_name','status')
    actions = [make_activate,make_inactivate]
    search_fields = ('id', 'main_category_name', )
admin.site.register(MainCategory,MainCategoryAdmin)

class MyCartAdmin(admin.ModelAdmin):
    list_display = ('id','total_number_items','total_price')
    search_fields = ('id', )
admin.site.register(MyCart,MyCartAdmin)

class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('id','transaction_id','payment_type','payment_date')
    search_fields = ('id', )
admin.site.register(OrderHistory,OrderHistoryAdmin)

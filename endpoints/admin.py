from django.contrib import admin
from .models import AppUser
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin

class AppUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = AppUser
    list_display = ('id' ,'email', 'first_name', 'date_of_birth', 'is_staff', 'user_type',  'phone_number','occupation' ,'updated_at','date_joined' )
    list_filter = ('email', 'is_staff', 'is_active', )
    ordering = ('email', 'first_name', )
    search_fileds = ('email', 'first_name', 'date_joined', 'updated_at', )
    #to counter error: can't be specified for appuser model form as it is a non-editiable field
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'image', 'phone_number', 'education', 'address', 'occupation')}),
        ('User Info', {'fields': ('user_type', 'is_blocked', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',)}),
        ('Time Details', {'fields': ('date_joined', 'updated_at',)}),
    )

class RoomUserAdmin(admin.ModelAdmin):
    model = Room
    list_display = ('id', 'room_name', 'room_price', 'category_id', 'owner_id', 'is_rented')
    ordering = ('room_name', 'room_price', 'created_at', 'updated_at',)
    
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'category_name','created_at', 'updated_at')
    ordering = ('created_at', 'updated_at', )
    
class RentalDataAdmin(admin.ModelAdmin):
    model = RentalData
    list_display = ('id', 'tenant_id', 'room_id', 'next_payable_date', 'rating' ,'rent_till_now', 'last_paid_date', 'is_active', 'created_at', 'updated_at')
    ordering = ('tenant_id', 'room_id', 'rating','next_payable_date', 'created_at', 'updated_at',)
    
class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('id', 'room_id', 'tenant_id', 'created_at', 'updated_at')
    ordering = ('room_id', 'tenant_id', 'created_at', 'updated_at',)
    
class RoomRequestAdmin(admin.ModelAdmin):
    model = RoomRequest
    list_display = ('id', 'tenant_id', 'room_id', 'request_message', 'is_accepted', 'created_at', 'updated_at')
    ordering = ('tenant_id', 'room_id', 'created_at', 'updated_at',)
    
class RewardAdmin(admin.ModelAdmin):
    model = Reward
    list_display = ('id', 'reward_name', 'occur_after_days', 'reward_point', 'reward_type', 'reoccured_reward','created_at', 'updated_at')
    ordering = ('reward_name', 'occur_after_days', 'reward_point',  'created_at', 'updated_at',)

class RewardTrackerAdmin(admin.ModelAdmin):
    model = RewardTracker
    list_display = ('id', 'rentalData_id', 'reward_id', 'created_at', 'updated_at', )
    ordering = ('rentalData_id', 'created_at', 'updated_at',  )

class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ('id', 'notification_name', 'notification_type', 'notification_message', 'created_at', 'updated_at')
    ordering = ('notification_name', 'notification_type', 'created_at', 'updated_at',)
    
class HouseAdmin(admin.ModelAdmin):
    model = House
    list_display = ( 'id', 'owner_id', 'house_name', 'location','longitude', 'latitude','room_vacent', 'created_at', 'updated_at')
    ordering = ('id', 'owner_id', 'created_at', 'updated_at', )
    
class FeatureAdmin(admin.ModelAdmin):
    model = Feature
    list_display = ('id', 'name', 'room_id', 'created_at', 'updated_at')
    ordering = ('created_at', 'updated_at',)
        
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Room, RoomUserAdmin)
admin.site.register(Category)
admin.site.register(RentalData, RentalDataAdmin)
admin.site.register(RoomRequest, RoomRequestAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(RewardTracker, RewardTrackerAdmin)
admin.site.register(Notification, NotificationAdmin)


import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.lookups import LessThan
from django.utils.translation import ugettext_lazy as _
from .managers import AppUserManager
from django.utils import timezone

class AppUser(AbstractUser):    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=20,null=False)
    date_of_birth = models.DateField( blank=True, null=True)
    image = models.ImageField( null=True, blank=True, upload_to="images/")
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    education = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    occupation = models.CharField(max_length=20, null=True, blank=True)

    USER_TYPE = (
        ('LL', 'LANDLORD'),
        ('TN', 'TENANT'),
        ('AD', 'ADMIN'),
    )

    user_type = models.CharField(max_length=2, choices=USER_TYPE)
    """
        -to counter error: can't be specified for appuser model form as it is a non-editiable field
        -default= timezone.now will remove problem 
        -don't use auto_time = timezone.now
        -Why error came? auto_now or auto_now_true as editable = False but  ModelAdmin will treat them as editiable=True so error comes
    """
    
    updated_at = models.DateTimeField(default=timezone.now, null=False)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'password', 'username', 'phone_number', 'date_of_birth', 'user_type', 'address'  ]
    objects = AppUserManager()
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
  

class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    owner_id = models.ForeignKey('endpoints.AppUser', on_delete=models.CASCADE)
    house_name = models.CharField(max_length= 30, null=True)
    location = models.CharField(max_length=50, null=True)
    longitude = models.FloatField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(max_length=50, null=True, blank=True)
    room_vacent = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    
    def __str__(self):
        return self.house_name
        
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    category_name = models.CharField(max_length= 20, null=True)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    
    def __str__(self):
        return self.category_name

class Feature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    name = models.CharField(max_length = 1000, null=True)
    room_id = models.ForeignKey('endpoints.Room', on_delete=models.CASCADE, default=None, null=True, related_name='features')
    updated_at = models.DateTimeField(auto_now=timezone.now, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    
class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    room_name = models.CharField(max_length=50, null=True)
    room_description = models.TextField(null=True)
    room_price = models.PositiveIntegerField()
    room_image = models.ImageField(upload_to="images/")
    category_id = models.ForeignKey(Category, on_delete = models.CASCADE )
    owner_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    house_id = models.ForeignKey(House, on_delete=models.CASCADE, default=None, null=True, blank=True)
    ratings = models.PositiveIntegerField(default =  0.0)
    is_rented = models.BooleanField(default=False)
    is_internet_available = models.BooleanField(default=False)
    is_price_negotiable = models.BooleanField(default=True)

    PARKING_TYPE = (
        ('BK', 'BIKE'),
        ('CR', 'CAR'),
        ('NO', 'NONE'),
    )

    parking_type = models.CharField(choices=PARKING_TYPE, max_length=2, null=True)
    room_size = models.PositiveIntegerField() #size in feet
    room_area = models.PositiveIntegerField() #size in sqft
    room_expires_at = models.DateTimeField(auto_now=False, null=True)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=False)
    created_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.room_name

class RentalData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    room_id = models.ForeignKey(Room, on_delete=models.RESTRICT)
    tenant_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    rent_paying_interval = models.PositiveIntegerField(default=1)
    last_paid_date = models.DateTimeField(auto_now=False, null=True)
    next_payable_date = models.DateTimeField(auto_now=False, null=True)
    next_payable_rent = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=False)
    advance_paid_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    advance_rent = models.FloatField(default=0.0)
    rent_till_now = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=False)
    created_at = models.DateTimeField(auto_now=True, null=False)
    # reward_tracker = models.JSONField()
    
    def __str__(self):
        return str(self.room_id)

class Reward(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    reward_name = models.CharField(max_length=50,null=True)
    occur_after_days = models.PositiveBigIntegerField(default=0)
    
    REWARD_TYPE = (
        ('FTU', 'FIRST TIME USER'), 
        ('DER', 'DAILY EARNED REWARD'),
        ('RIT', 'RENT IN TIME'), 
        ('F2M', 'FIRST 2 MONTHS'),
        ('F4M', 'FIRST 4 MONTHS'),
        ('LHY', 'LIVED HALF YEAR '),
        ('F8M', 'FIRST 8 MONTHS'),
        ('L1Y', 'LIVED 1 YEAR'), 
        ('L2Y', 'LIVED 2 YEAR'), 
        ('L3Y', 'LIVED 3 YEAR'), 
        ('L4Y', 'LIVED 4 YEAR'), 
        
        )
    REWARD_POINT_TYPE = (
        (5.0, 'SIGNUP'),
        (0.1, 'DAILY'),
        (10.0, 'RIT'),
        (7.0, 'L2M'), #Lived 2 months
        (15.0, 'LHY'),
        (30.0, 'L1Y'),
    )
    
    """
    RENT DISCOUT IN DAYS
    
    (DISCOUNT_DAYS, REWARD_POINTS)
    """
    
    REWARD_DISCOUNT_TYPE = (
        (0.2, 5.0), 
    )
    
    """
    RENT REWARD IN DAYS DISCOUNT
    
    (DISCOUNT_DAYS, REOCCURED REWARD)
    """
    REWARD_REOCCURED_TYPE = (
        (0, 'None'),
        (5, 'RIT-3'),
        (7, 'RIT-6'),
        (10, 'RIT-10'),
        (12, 'RIT-12'),
        (15, 'RIT-15'),
    )
    
    reward_point = models.FloatField(default = 0.2, choices=REWARD_POINT_TYPE)
    reward_type = models.CharField(max_length=3, choices=REWARD_TYPE)
    reoccured_reward = models.PositiveIntegerField(default=0, choices=REWARD_REOCCURED_TYPE)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    
    def __str__(self):
        return self.reward_name

class RewardTracker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    rentalData_id = models.ForeignKey(RentalData, on_delete=models.CASCADE, related_name = 'rewards')
    reward_id = models.ForeignKey(Reward, on_delete = models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=False)
    created_at = models.DateTimeField(auto_now = True, null=False, blank=False)

    def __str__(self):
        return str(self.rentalData_id) + str("__"+str(self. reward_id))
           
class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    room_id = models.ForeignKey(Room, on_delete=models.RESTRICT)
    tenant_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=False)
    created_at = models.DateTimeField(auto_now=True, null=False)
    
    def __str__(self):
        return str(self.room_id)

class RoomRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    tenant_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    request_message = models.CharField(max_length=3000, null=True)
    is_accepted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=False)
    created_at = models.DateTimeField(auto_now=True, null=False)
    
    def __str__(self):
        return str(self.tenant_id)

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, null=False)
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    notification_name = models.CharField(max_length=50, null=True)
    notification_message = models.CharField(max_length=3000, null=True)
    notification_type = models.CharField(max_length=20, null=True)
    updated_at = models.DateTimeField(auto_now=timezone.now, null=False)
    created_at = models.DateTimeField(auto_now=True, null=False)
    
    def __str__(self):
        return self.notification_name
    

    
    
    
    
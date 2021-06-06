from django_filters import rest_framework
from endpoints.models import Room, RentalData

class RoomFilter(rest_framework.FilterSet):
    min_price = rest_framework.NumberFilter(field_name = 'room_price', lookup_expr = 'gte')
    max_price = rest_framework.NumberFilter(field_name = 'room_price', lookup_expr = 'lte')
    
    class Meta:
        model = Room
        fields = ['room_name','category_id', 'owner_id', 'house_id',  'room_price', 'is_internet_available', 'is_price_negotiable', 'parking_type', 'min_price', 'max_price', 'created_at', ]
    
class RentalDataFilter(rest_framework.FilterSet):
    min_rating = rest_framework.NumberFilter(field_name = 'rating', lookup_expr = 'gte' )
    max_rating = rest_framework.NumberFilter(field_name = 'rating', lookup_expr = 'lte')
    
    min_advance_rent = rest_framework.NumberFilter(field_name = 'advance_rent', lookup_expr = 'gte')
    max_advance_rent = rest_framework.NumberFilter(field_name = 'advance_rent', lookup_expr = 'lte')  
    
    min_next_payable_rent = rest_framework.NumberFilter(field_name = 'next_payable_rent', lookup_expr = 'gte')
    max_next_payable_rent = rest_framework.NumberFilter(field_name = 'next_payable_rent', lookup_expr = 'lte')
    
    min_rent_till_now = rest_framework.NumberFilter(field_name = 'rent_till_now', lookup_expr = 'gte')
    max_rent_till_now = rest_framework.NumberFilter(field_name = 'rent_till_now', lookup_expr = 'lte')
        
    class Meta:
        model = RentalData
        fields = ['room_id', 'tenant_id', 'room_id__owner_id', 'room_id__house_id',  'is_active', 'max_rating', 'min_rating', 'max_advance_rent', 'min_advance_rent', 'max_next_payable_rent', 'min_next_payable_rent', 'max_rent_till_now', 'min_rent_till_now', 'advance_paid_date', 'next_payable_date', 'last_paid_date', 'created_at', ]
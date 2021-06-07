"""
All the business logic, which actally talks to the models
"""

import re
from rest_framework import serializers
from MailChecker import MailChecker

def validate_password(self, value):
    """
    Password must contain: 
    8-20 Charaters
    at least 1 lowercase
    at least 1 uppercase
    at least 1 numeric digit 
    at least 1 special character.
    """
    if not re.search("^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,20}$",value):
        return serializers.ValidationError("Password must be between 8 to 20 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character.")
    
    elif not value:
        return serializers.ValidationError("Password mustn't be empty")
    
    return value
        
def validate_username(self, value):
    
    if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',value):
        return serializers.ValidationError("Invalid Email.")
    
    elif not value:
        return serializers.ValidationError("Empty mustn't be empty")
    
    return value

"""
validate_email_api:
-validating only email if it blacklisted on or not
-if email has right format or not

"""
def validate_email_api(self, value):
    if MailChecker.is_valid(value):
        print("valid email")
        
        return value
    print("invalid email")
    return serializers.ValidationError("Invalid email address")
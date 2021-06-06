from email import header
from django.test import TestCase
import requests

from requests.api import head

def get_token():
    url = "http://127.0.0.1:8000/o/getToken/"

    # grant_type = 'password'
    username = 'ab9arpan@gmail.com'
    password = 'harekrishna@762'
    # client_id = 'IvRhNX7hvg7zUwRulaz7dxOrgyEB9VYZHo5SMYNt'
    # client_secret  = '9uoGmkitFOSyvrsVWFhHSGQaIZK5vMybLBY0aHB0gw706AhyBj3KgacAHBOPEUw1IshDqnOQmwqtT5etjw1AUkLS7KDcUZNswm4yKGbF356RWxNaVHHERuzExvxZsCne'

    data = {
        # 'grant_type' : grant_type,
        'username' : username,
        'password' : password,
        'fuck': "fuck",
        # 'client_id' : client_id,
        # 'client_secret': client_secret
        
    }

    result = requests.request('POST', url, data=data, )

    # print(result.text)
    print(result)
    

# get_token()

def delete_token():
    url = "http://127.0.0.1:8000/o/revoke_token/"
    token = "4gGFEurCSAulkIN5PtAAf80GWiopJu"
    client_id = 'IvRhNX7hvg7zUwRulaz7dxOrgyEB9VYZHo5SMYNt'
    client_secret = '9uoGmkitFOSyvrsVWFhHSGQaIZK5vMybLBY0aHB0gw706AhyBj3KgacAHBOPEUw1IshDqnOQmwqtT5etjw1AUkLS7KDcUZNswm4yKGbF356RWxNaVHHERuzExvxZsCne'
    
    data = {
        'token' : token,
        'client_id' : client_id,
        'client_secret': client_secret,
        'token_type_hint' : 'refresh_token',
    }
    
    result = requests.request('POST', url, data=data,)
    print(result.text)


def refresh_token():
    url = "http://127.0.0.1:8000/o/token/"
    token = "Wurpjdt1QyUaLIGuOpkqWJJRFQ6Q0U"
    refresh_token = "4gGFEuACSAulkIN5PtAAf80GWiopJu"
    client_id = 'IvRhNX7hvg7zUwRulaz7dxOrgyEB9VYZHo5SMYNt'
    client_secret = '9uoGmkitFOSyvrsVWFhHSGQaIZK5vMybLBY0aHB0gw706AhyBj3KgacAHBOPEUw1IshDqnOQmwqtT5etjw1AUkLS7KDcUZNswm4yKGbF356RWxNaVHHERuzExvxZsCne'
    grant_type = 'refresh_token'
    
    data = {
        'grant_type' : grant_type,
        'client_id' : client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        
        
    }

    result = requests.request('POST', url, data=data,)
    print(result)
    
def get_rooms():
    url = "http://127.0.0.1:8000/rooms/"
    
    token = "Wurpjdt1QyUaLIGuOpkqWJJRFQ6Q0U"

    data = {
        
        
    }

    headers = {
        'Authorization': 'Bearer '+ token
    }

    result = requests.request('GET', url, headers=headers )
    
    print(result.text)
    # print(result)
    
get_token()
from django.contrib.auth.hashers import PBKDF2PasswordHasher

# class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
#     """
#     A subclass of PBKDF2PasswordHasher that uses 200 times iterations.
    
#     """
    
#     iterations = PBKDF2PasswordHasher.iterations * 100
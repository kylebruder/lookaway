#!/usr/bin/python3
# Make a random key for a Django project
if __name__ == "__main__":
    try:
        from django.core.management.utils import get_random_secret_key
        print(get_random_secret_key())
    except:
        print('Are the modules installed? Try pip install -r requirements.txt')
else:
    pass

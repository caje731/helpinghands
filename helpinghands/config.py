"""
    Environment configuration for helpinghands

    Settings that need to differ by environment should be
    defined in here.
"""
import os

ENV_CODES = {
    "DEV": 1,
    "PRD": 2,
}

def get_env():
    """ Return the current environment code, as defined in ENV_CODES """
    
    env_value = os.getenv('HH_ENV', default='DEV').upper()
    if env_value not in ENV_CODES.keys():
        return ENV_CODES['DEV']
    else:
        return ENV_CODES[env_value]

def get_db_settings():
    """ Return a dictionary of database-related settings """

    if get_env() == ENV_CODES['PRD']:
        return {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'helpinghands',
                'USER': 'caje731',
                'PASSWORD': 'caje731',
                'HOST': 'caje731.mysql.pythonanywhere-services.com',
                'PORT': '3306',
            }
        }
    else:
        return {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'helpinghands',
                'USER': 'root',
                'PASSWORD': 'sqltoor',
                'HOST': '127.0.0.1',
                'PORT': '3306',
            }
        }

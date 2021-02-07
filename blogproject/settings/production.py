# SECURITY WARNING: keep the secret key used in production secret!
from .common import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost ', '.iwannnn.cn', '47.98.63.97']

from django.urls import path
from .views import *
urlpatterns = [
    path('', boot, name='boot'),

]
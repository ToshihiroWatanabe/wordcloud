from django.urls import path
from .views import homefunc, resultfunc

urlpatterns = [
    path('', homefunc, name='home'),
    path('result/', resultfunc, name='result'),
]

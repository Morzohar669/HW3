from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index.html'),
    path('index.html', views.index, name='index.html'),
    path('Query.html', views.Query, name='Query.html'),
    path('Add.html', views.Add, name='Add.html'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index.html'),
    path('index.html', views.index, name='index.html'),
    path('Query.html', views.query, name='Query.html'),
    path('Add.html', views.add, name='Add.html'),
]
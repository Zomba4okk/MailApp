from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path(r'register/', views.create_user, name='register'),
    url(r'login/', views.CustomLoginView.as_view(), name='login'),
    url(r'logout/', views.CustomLogoutView.as_view(), name='logout'),
]
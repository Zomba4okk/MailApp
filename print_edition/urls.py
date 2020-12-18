from django.urls import path
from . import views

urlpatterns = [
    path(r'<int:print_edition_id>/price', views.get_price, name='price'),
]
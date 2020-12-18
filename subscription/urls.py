from django.urls import path
from . import views

urlpatterns = [
    path(r'request/', views.create_request, name='request'),
    path(r'requests/', views.get_requests, name='requests'),
    path(r'report/', views.get_report, name='report'),
    path(r'approve/<int:request_id>/', views.approve, name='approve'),
    path(r'month-subscriptions/', views.get_month_subscriptions, name='month_subscriptions'),
    path(r'generate-report', views.Report.report, name='generate_report'),
]
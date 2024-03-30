from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('add_location/', views.add_location, name='add_location'),
    path('create_trip_plan/', views.create_trip_plan, name='create_trip_plan'),
    path('create_event/<int:trip_plan_id>/', views.create_event, name='create_event'),
    path('select_plan/<int:trip_plan_id>/', views.select_plan, name='select_plan'),
    path('add_expenditure/<int:event_id>/', views.add_expenditure, name='add_expenditure'),
    path('compare_plans/<int:trip_plan_id>/', views.compare_plans, name='compare_plans'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.homepage, name='home'),
]

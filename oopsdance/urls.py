from django.urls import path
from .views import RegisterView, LoginView, SignOutView, AddClassView, ClassListView, ClassDetailAPIView, ScheduleListView, AddScheduleView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signout/', SignOutView.as_view(), name='signout'),
    path('add_class/', AddClassView.as_view(), name='add_class'),
    path('class-list/', ClassListView.as_view(), name='class-list'),
    path('class/<int:pk>/', ClassDetailAPIView.as_view(), name='class-detail'),
    path('schedule-list/', ScheduleListView.as_view(), name='schedule-list'),
    path('add_schedule/', AddScheduleView.as_view(), name='add_schedule'),
      
]

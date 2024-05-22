from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home, RegisterView, LoginView, SignOutView, AddClassView, ClassListView, ClassDetailAPIView,
    ScheduleListView, AddScheduleView, ScheduleDetailAPIView, AddRoomView, RoomListView,
    RoomDetailAPIView, BookingStatusListCreateAPIView, BookingListCreateAPIView, BookingDetailAPIView,
    BookingGuestListCreateAPIView, BookingGuestDetailAPIView,
    RevenueListCreateAPIView, RevenueDetailAPIView, AvailableRoomsAPIView
)
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('signout/', SignOutView.as_view(), name='signout'),
    
    path('add_class/', AddClassView.as_view(), name='add_class'),
    path('class-list/', ClassListView.as_view(), name='class-list'),
    path('class/<int:pk>/', ClassDetailAPIView.as_view(), name='class-detail'),
    
    path('schedule-list/', ScheduleListView.as_view(), name='schedule-list'),
    path('add_schedule/', AddScheduleView.as_view(), name='add_schedule'),
    path('schedule/<int:pk>/', ScheduleDetailAPIView.as_view(), name='schedule-detail'),
     # New endpoints for Room
    path('add-room/', AddRoomView.as_view(), name='add-room'),
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    
    ## BOOKING ##
    path('booking-statuses/', BookingStatusListCreateAPIView.as_view(), name='booking-status-list-create'),
    path('bookings/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('booking-guests/', BookingGuestListCreateAPIView.as_view(), name='booking-guest-list-create'),
    path('booking-guests/<int:pk>/', BookingGuestDetailAPIView.as_view(), name='booking-guest-detail'),
    path('available-rooms/', AvailableRoomsAPIView.as_view(), name='available-rooms'),  
    
    ## REVENUE ##
    path('revenues/', RevenueListCreateAPIView.as_view(), name='revenue-list-create'),
    path('revenues/<int:pk>/', RevenueDetailAPIView.as_view(), name='revenue-detail'),
    
    
]
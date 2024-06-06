from django.urls import path
from rest_framework.routers import DefaultRouter

from oopsdance.Users.views import home, RegisterView, LoginView, LogoutView, test_token
from oopsdance.Classes.views import AddClassView, ClassListView, ClassDetailAPIView, ScheduleListView, AddScheduleView, ScheduleDetailAPIView, ClassCountByInstructorView, ClassesTodayByInstructorView, ClassesToday
from oopsdance.Rooms.views import AddRoomView, RoomListView, RoomDetailAPIView, AvailableRoomsAPIView
from oopsdance.Bookings.views import BookingStatusListCreateAPIView, BookingListCreateAPIView, BookingDetailAPIView, BookingGuestListCreateAPIView, BookingGuestDetailAPIView, RevenueListCreateAPIView, RevenueDetailAPIView
from oopsdance.Attendance.views import AttendanceCountByInstructorView, AttendanceListView, AttendanceRecordsByInstructorView, AttendanceDetailAPIView

router = DefaultRouter()

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('test-token/', test_token, name='test-token'),
    
    # Classes
    path('add_class/', AddClassView.as_view(), name='add_class'),
    path('class-list/', ClassListView.as_view(), name='class-list'),
    path('class/<int:pk>/', ClassDetailAPIView.as_view(), name='class-detail'),
    path('schedule-list/', ScheduleListView.as_view(), name='schedule-list'),
    path('add_schedule/', AddScheduleView.as_view(), name='add_schedule'),
    path('schedule/<int:pk>/', ScheduleDetailAPIView.as_view(), name='schedule-detail'),
    path('class_count_by_instructor/<int:instructor_id>/', ClassCountByInstructorView.as_view(), name='class-count-by-instructor'),
    path('classes_today/', ClassesToday.as_view(), name='classes-today'),
    path('classes_today/<int:instructor_id>/', ClassesTodayByInstructorView.as_view(), name='classes-today-by-instructor'),

    # Rooms
    path('add-room/', AddRoomView.as_view(), name='add-room'),
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    path('available-rooms/', AvailableRoomsAPIView.as_view(), name='available-rooms'),

    # Bookings
    path('booking-statuses/', BookingStatusListCreateAPIView.as_view(), name='booking-status-list-create'),
    path('bookings/', BookingListCreateAPIView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', BookingDetailAPIView.as_view(), name='booking-detail'),
    path('booking-guests/', BookingGuestListCreateAPIView.as_view(), name='booking-guest-list-create'),
    path('booking-guests/<int:pk>/', BookingGuestDetailAPIView.as_view(), name='booking-guest-detail'),
    path('revenues/', RevenueListCreateAPIView.as_view(), name='revenue-list-create'),
    path('revenues/<int:pk>/', RevenueDetailAPIView.as_view(), name='revenue-detail'),
    
    #Attendance
    path('attendance_count_by_instructor/<int:instructor_id>/', AttendanceCountByInstructorView.as_view(), name='attendance-count-by-instructor'),
    path('attendance-list/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance-list/<int:instructor_id>', AttendanceRecordsByInstructorView.as_view(), name='attendance-list-by-instructor-list'),
    path('attendance/<int:pk>/', AttendanceDetailAPIView.as_view(), name='attendance-detail'),
    
    
]

urlpatterns += router.urls
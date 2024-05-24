from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    api_view
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import (
    get_user_model,
    login,
    logout,
    authenticate
)
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from datetime import datetime, time, date, timedelta
from .serializers import (
    UserSerializer,
    ClassSerializer,
    LoginSerializer,
    ScheduleSerializer,
    RoomSerializer,
    BookingSerializer,
    BookingGuestSerializer,
    BookingStatusSerializer,
    RevenueSerializer
)
from .models import (
    Class,
    ClassSchedule,
    Room,
    Booking,
    BookingGuest,
    BookingStatus,
    Revenue,
    User
)
import qrcode
import io
from django.db.models import Q

import logging


User = get_user_model()

def home(request):
    return HttpResponse("Welcome to OopsDanceStudio!")

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.set_password(request.data['password'])
#             user.save()
#             token = Token.objects.create(user=user)
#             return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = authenticate(username=request.data['username'], password=request.data['password'])
#             if user is not None:
#                 # Kiểm tra xem người dùng đã có token hay chưa
#                 try:
#                     token = Token.objects.get(user=user)
#                     token.delete()  # Xóa token hiện tại
#                 except Token.DoesNotExist:
#                     pass
                
#                 token = Token.objects.create(user=user)  # Tạo token mới
#                 login(request, user)
#                 user_serializer = UserSerializer(user)
#                 return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             errors = dict(serializer.errors)
#             errors['message'] = "credentials don't match"
#             return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     authentication_classes = [TokenAuthentication]

#     def post(self, request):
#         try:
#             request.user.auth_token.delete()  # Xóa token hiện tại
#             logout(request)
#             return Response({"message": "Logout success"}, status=status.HTTP_200_OK)
#         except:
#             return Response({"message": "Logout failed"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    user = request.user
    logger.info(f"User: {user}")
    return Response({
        'message': 'Token is valid',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'full_name': user.full_name,
            'role': user.role,
        }
    })
# def test_token(request):
#     return Response("passed for {}".format(request.user.email))



#################################

class AddClassView(APIView):
    def post(self, request, format=None):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['message'] = "Success"
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            errors = dict(serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClassListView(APIView):
    def get(self, request, format=None):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)
    
class ClassDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    
class ScheduleListView(APIView):
    def get(self, request, format=None):
        schedule = ClassSchedule.objects.all()
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)
    
class AddScheduleView(APIView):
    def post(self, request, format=None):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['message'] = "Success"
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            errors = dict(serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
class ScheduleDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ClassSchedule.objects.all()
    serializer_class = ScheduleSerializer
    
# New Views for Room and Booking
@method_decorator(csrf_exempt, name='dispatch')
class AddRoomView(APIView):
    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['message'] = "Success"
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = dict(serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class RoomListView(APIView):
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

class RoomDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


#############################################################################################################################################################

############################        BOOKING        #####################################
# Booking Status API
class BookingStatusListCreateAPIView(APIView):
    def get(self, request):
        statuses = BookingStatus.objects.all()
        serializer = BookingStatusSerializer(statuses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############ Booking API ##################

#### Booking Create & Booking List
class BookingListCreateAPIView(APIView):
    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['message'] = "Success"
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return None

    def get(self, request, pk):
        booking = self.get_object(pk)
        if booking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk):
        booking = self.get_object(pk)
        if booking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = self.get_object(pk)
        if booking is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Booking Guest API
class BookingGuestListCreateAPIView(APIView):
    def get(self, request):
        guests = BookingGuest.objects.all()
        serializer = BookingGuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingGuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingGuestDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return BookingGuest.objects.get(pk=pk)
        except BookingGuest.DoesNotExist:
            return None

    def get(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookingGuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookingGuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        if guest is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
################ API Available Room ###############

    ## function merge time slots ##
def merge_time_slots(time_slots):
    if not time_slots:
        return []

    merged_slots = []
    start_time, end_time = time_slots[0]

    for current_start, current_end in time_slots[1:]:
        if current_start == end_time:
            end_time = current_end
        else:
            merged_slots.append((start_time, end_time))
            start_time, end_time = current_start, current_end

    merged_slots.append((start_time, end_time))
    return merged_slots

    ## function get time slots ##
def get_time_slots(start_time, end_time, interval_minutes=30):
    time_slots = []
    current_time = datetime.combine(date.today(), start_time)
    end_time = datetime.combine(date.today(), end_time)
    while current_time + timedelta(minutes=interval_minutes) <= end_time:
        slot_end_time = current_time + timedelta(minutes=interval_minutes)
        time_slots.append((current_time.time(), slot_end_time.time()))
        current_time = slot_end_time
    return time_slots

    ## function calculate available time slots ##
def calculate_available_time_slots(bookings, classes, date):
    start_time = time(8, 0)
    end_time = time(22, 0)
    
    all_time_slots = get_time_slots(start_time, end_time)
    booked_time_slots = [] #save the unavailable room time here
    
    # get booked time slot in booking table
    for booking in bookings:
        booked_time_slots.extend(get_time_slots(booking.checkin_time, booking.checkout_time))

    # get scheduled time slot of classes
    day_of_week = date.strftime('%w')  # 0=Sunday, 1=Monday, ..., 6=Saturday
    class_time_slots = []
    
    for cls in classes:
        for schedule in cls.schedules.filter(day_of_the_week=day_of_week):
            class_time_slots.extend(get_time_slots(schedule.start_time, schedule.end_time))

    # add to booked_time_slots
    booked_time_slots.extend(class_time_slots)

    available_time_slots = [
        slot for slot in all_time_slots if all(
            not (slot[0] < b_end and slot[1] > b_start)
            for b_start, b_end in booked_time_slots
        )
    ]

    return merge_time_slots(available_time_slots)

class AvailableRoomsAPIView(APIView):
    def get(self, request, format=None):
        date_str = request.query_params.get('date', None)
        if date_str is None:
            return Response({"error": "Date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date = parse_date(date_str)
            if date is None:
                raise ValueError
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

        rooms = Room.objects.all()
        available_time_slots = {}

        for room in rooms:
            bookings = Booking.objects.filter(date=date, room=room, status__status_name__in=['pending', 'approved'])
            classes = Class.objects.filter(room=room)

            if not bookings.exists() and not classes.exists():
                # Không có lịch đặt phòng và lớp nào vào ngày này
                available_time_slots[room.name] = [(datetime.time(8, 0).strftime("%H:%M"), datetime.time(22, 0).strftime("%H:%M"))]
            else:
                available_time_slots_for_room = calculate_available_time_slots(bookings, classes, date)
                available_time_slots[room.name] = [(slot[0].strftime("%H:%M"), slot[1].strftime("%H:%M")) for slot in available_time_slots_for_room]

        return Response(available_time_slots, status=status.HTTP_200_OK)


##################################################################################################################################################################
# Revenue API
class RevenueListCreateAPIView(APIView):
    def get(self, request):
        revenues = Revenue.objects.all()
        serializer = RevenueSerializer(revenues, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RevenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RevenueDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Revenue.objects.get(pk=pk)
        except Revenue.DoesNotExist:
            return None

    def get(self, request, pk):
        revenue = self.get_object(pk)
        if revenue is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RevenueSerializer(revenue)
        return Response(serializer.data)

    def put(self, request, pk):
        revenue = self.get_object(pk)
        if revenue is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RevenueSerializer(revenue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        revenue = self.get_object(pk)
        if revenue is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        revenue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

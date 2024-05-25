from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta, date, time
from .serializers import RoomSerializer
from ..models import Room, Booking, Class

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

# Các hàm hỗ trợ cho API Available Room
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

def get_time_slots(start_time, end_time, interval_minutes=30):
    time_slots = []
    current_time = datetime.combine(date.today(), start_time)
    end_time = datetime.combine(date.today(), end_time)
    while current_time + timedelta(minutes=interval_minutes) <= end_time:
        slot_end_time = current_time + timedelta(minutes=interval_minutes)
        time_slots.append((current_time.time(), slot_end_time.time()))
        current_time = slot_end_time
    return time_slots

def calculate_available_time_slots(bookings, classes, date):
    start_time = time(8, 0)
    end_time = time(22, 0)
    
    all_time_slots = get_time_slots(start_time, end_time)
    booked_time_slots = [] 
    
    for booking in bookings:
        booked_time_slots.extend(get_time_slots(booking.checkin_time, booking.checkout_time))

    day_of_week = date.strftime('%w')
    class_time_slots = []
    
    for cls in classes:
        for schedule in cls.schedules.filter(day_of_the_week=day_of_week):
            class_time_slots.extend(get_time_slots(schedule.start_time, schedule.end_time))

    booked_time_slots.extend(class_time_slots)

    available_time_slots = [
        slot for slot in all_time_slots if all(
            not (slot[0] < b_end and slot[1] > b_start)
            for b_start, b_end in booked_time_slots
        )
    ]

    return merge_time_slots(available_time_slots)

@permission_classes([AllowAny])
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
                available_time_slots[room.name] = [(time(8, 0).strftime("%H:%M"), time(22, 0).strftime("%H:%M"))]
            else:
                available_time_slots_for_room = calculate_available_time_slots(bookings, classes, date)
                available_time_slots[room.name] = [(slot[0].strftime("%H:%M"), slot[1].strftime("%H:%M")) for slot in available_time_slots_for_room]

        return Response(available_time_slots, status=status.HTTP_200_OK)
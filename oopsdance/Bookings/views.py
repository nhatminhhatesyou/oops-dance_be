from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date, time
from django.utils.dateparse import parse_date
from .serializers import BookingSerializer, BookingGuestSerializer, BookingStatusSerializer, RevenueSerializer
from oopsdance.models import Booking, BookingGuest, BookingStatus, Revenue, Room, Class
from rest_framework.permissions import AllowAny


from rest_framework.decorators import (
    permission_classes
)
# status
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

# list
@permission_classes([AllowAny])
class BookingListCreateAPIView(APIView):
    def get(self, request):
        guest_id = request.query_params.get('guest_id', None)
        if guest_id is not None:
            bookings = Booking.objects.filter(guest_id=guest_id)
        else:
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

@permission_classes([AllowAny])
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

# booking guest
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
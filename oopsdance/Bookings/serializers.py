from rest_framework import serializers
from datetime import time
from oopsdance.models import Booking, BookingGuest, BookingStatus, Revenue, Room
from ..Rooms.serializers import RoomSerializer

class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'

class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingStatus
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    checkin_time = serializers.TimeField(default=time(0, 0), format='%H:%M')
    checkout_time = serializers.TimeField(default=time(0, 0), format='%H:%M')
    date = serializers.DateField(required=True)
    status_name = serializers.SerializerMethodField()
    room_name = serializers.CharField(write_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'guest', 'room', 'room_name', 'checkin_time', 'checkout_time', 'date', 'status', 'status_name','deposite','bank_transfer','cash','details','deposite_status')
        read_only_fields = ('status_name', 'room')

    def validate(self, data):
        if data['checkin_time'] >= data['checkout_time']:
            raise serializers.ValidationError("Checkout time must be after checkin time.")
        return data

    def get_status_name(self, obj):
        return obj.status.status_name

    def create(self, validated_data):
        room_name = validated_data.pop('room_name')
        try:
            room = Room.objects.get(name=room_name)
            validated_data['room'] = room
        except Room.DoesNotExist:
            raise serializers.ValidationError("Invalid room name.")

        if 'status' not in validated_data:
            default_status = BookingStatus.objects.get(status_name="pending")
            validated_data['status'] = default_status

        booking = Booking.objects.create(**validated_data)
        return booking

class BookingGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingGuest
        fields = '__all__'
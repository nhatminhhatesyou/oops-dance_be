from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Class, ClassSchedule, Room, Revenue, Booking, BookingGuest, BookingStatus
from datetime import time



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'contact_number', 'role', 'date_of_birth','username')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data.setdefault('role', 'guest')
        user = User.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Thông tin đăng nhập không chính xác.")
    
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
    
class ClassScheduleSerializer(serializers.ModelSerializer):
    day_of_the_week_value = serializers.CharField(source='get_day_of_the_week_display', read_only=True)
    start_time = serializers.TimeField(default=time(0, 0), format='%H:%M')
    end_time = serializers.TimeField(default=time(0, 0), format='%H:%M')
    
    class Meta:
        model = ClassSchedule
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    day_of_the_week = serializers.ChoiceField(choices=ClassSchedule.DAYS_OF_THE_WEEK)
    day_of_the_week_value = serializers.CharField(source='get_day_of_the_week_display', read_only=True)
    start_time = serializers.TimeField(default=time(0, 0), format='%H:%M')
    end_time = serializers.TimeField(default=time(0, 0), format='%H:%M')

    class Meta:
        model = ClassSchedule
        fields = ('id', 'day_of_the_week', 'start_time', 'end_time', 'day_of_the_week_value')

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data

class ClassSerializer(serializers.ModelSerializer):
    instructor_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='instructor'), source='instructor', required=True)
    class_name = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True) 
    instructor_detail = UserSerializer(source='instructor', read_only=True)
    schedules_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    schedules = ClassScheduleSerializer(many=True, read_only=True)  
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', required=False)  
    room_detail = RoomSerializer(source='room', read_only=True)
    
    class Meta:
        model = Class
        fields = ('id', 'class_name', 'instructor_id', 'price', 'instructor_detail', 'schedules', 'schedules_ids', 'room_id', 'room_detail')
        
    def validate(self, data):
        existing_class = Class.objects.filter(class_name=data.get('class_name')).first()
        if existing_class and self.instance and self.instance.id != existing_class.id:
            raise serializers.ValidationError("Class already exists with this class name.")
        elif existing_class and not self.instance:
            raise serializers.ValidationError("Class already exists with this class name.")
        return data
    
    def create(self, validated_data):
        schedules_ids = validated_data.pop('schedules_ids', [])
        class_instance = Class.objects.create(**validated_data)
        class_instance.schedules.set(schedules_ids)
        return class_instance

    def update(self, instance, validated_data):
        schedules_ids = validated_data.pop('schedules_ids', None)
        if schedules_ids is not None:
            instance.schedules.set(schedules_ids)
        return super().update(instance, validated_data)
       
class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'

#new

class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingStatus
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    checkin_time = serializers.TimeField(required=True)
    checkout_time = serializers.TimeField(required=True)
    date = serializers.DateField(required=True)
    status_name = serializers.SerializerMethodField()
    room_name = serializers.CharField(write_only=True)

    class Meta:
        model = Booking
        fields = ('guest','room' ,'room_name', 'checkin_time', 'checkout_time', 'date', 'status', 'status_name')
        read_only_fields = ('status_name','room')
        

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

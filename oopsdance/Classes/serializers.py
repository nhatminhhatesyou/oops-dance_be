from rest_framework import serializers
from datetime import time
from oopsdance.models import Class, ClassSchedule, Room
from ..Rooms.serializers import RoomSerializer
from ..Users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

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
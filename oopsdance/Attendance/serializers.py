from rest_framework import serializers
from oopsdance.models import Attendance

# Import Serializers
from ..Classes.serializers import ClassSerializer
from ..Rooms.serializers import RoomSerializer
from ..Users.serializers import UserSerializer
# Import Models
from oopsdance.models import Class, Room, User

class AttendanceSerializer(serializers.ModelSerializer):
    class_instance_id = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), source='class_instance', required=True)
    class_instance_detail = ClassSerializer(source='class_instance', read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='instructor'), source='instructor', required=True)
    instructor_detail = UserSerializer(source='instructor', read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', required=True)
    room_detail = RoomSerializer(source='room', read_only=True)
    status = serializers.ChoiceField(choices=Attendance.STATUS_CHOICES)

    class Meta:
        model = Attendance
        fields = ('id', 'class_instance_id', 'class_instance_detail', 'instructor_id', 'instructor_detail', 'room_id', 'room_detail', 'date', 'checkin_time', 'checkout_time', 'status')

    def validate(self, data):
        if data['checkin_time'] >= data['checkout_time']:
            raise serializers.ValidationError("Checkout time must be after checkin time.")
        return data
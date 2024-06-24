from rest_framework import serializers
from oopsdance.models import Attendance, StudentAttendance
from datetime import time

# Import Serializers
from ..Classes.serializers import ClassSerializer, ClassSimpleSerializer
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
    checkin_time = serializers.TimeField(default=time(0, 0), format='%H:%M')
    checkout_time = serializers.TimeField(default=time(0, 0), format='%H:%M')

    class Meta:
        model = Attendance
        fields = ('id', 'class_instance_id', 'class_instance_detail', 'instructor_id', 'instructor_detail', 'room_id', 'room_detail', 'date', 'checkin_time', 'checkout_time', 'status','checkin_proof','checkout_proof','details')

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    class_instance = ClassSimpleSerializer(read_only=True)  # Use the nested serializer for class instance
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='guest'), source='student', write_only=True
    )
    class_instance_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(), source='class_instance', write_only=True
    )
    class_id = serializers.IntegerField(source='class_instance.id', read_only=True)

    class Meta:
        model = StudentAttendance
        fields = ['id', 'date', 'class_id', 'class_instance', 'student', 'status', 'details', 'student_id', 'class_instance_id']

    def create(self, validated_data):
        student_id = validated_data.pop('student')
        class_instance_id = validated_data.pop('class_instance')
        
        if StudentAttendance.objects.filter(student=student_id, class_instance=class_instance_id, date=validated_data['date']).exists():
            raise serializers.ValidationError("Attendance record already exists for this student in the selected class on this date.")
        
        return StudentAttendance.objects.create(student=student_id, class_instance=class_instance_id, **validated_data)
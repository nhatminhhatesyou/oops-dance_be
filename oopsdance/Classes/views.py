from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from .serializers import ClassSerializer, ScheduleSerializer
from ..Attendance.serializers import AttendanceSerializer
from oopsdance.models import Class, ClassSchedule, Attendance, User

import datetime

from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    permission_classes
)

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

@permission_classes([AllowAny])
class ClassListView(APIView):
    def get(self, request, format=None):
        instructor_id = request.query_params.get('instructor_id', None)
        guest_id = request.query_params.get('guest_id', None)

        if instructor_id is not None:
            classes = Class.objects.filter(instructor_id=instructor_id)
        elif guest_id is not None:
            classes = Class.objects.filter(students__id=guest_id)
        else:
            classes = Class.objects.all()
            
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)

@permission_classes([AllowAny])
class ClassDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    parser_classes = (MultiPartParser, FormParser)
    
class RemoveStudentFromClassView(APIView):
    def patch(self, request, pk, format=None):
        try:
            class_instance = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

        student_id = request.data.get('student_id')
        if not student_id:
            return Response({'error': 'Student ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = User.objects.get(pk=student_id)
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        if student not in class_instance.students.all():
            return Response({'error': 'Student is not in this class'}, status=status.HTTP_400_BAD_REQUEST)

        class_instance.students.remove(student)
        return Response({'message': 'Student removed successfully'}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
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
    
class ClassCountByInstructorView(APIView):
    def get(self, request, instructor_id, format=None):
        try:
            class_count = Class.objects.filter(instructor_id=instructor_id).count()
            return Response({"instructor_id": instructor_id, "class_count": class_count}, status=status.HTTP_200_OK)
        except Class.DoesNotExist:
            return Response({"error": "Instructor not found"}, status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([AllowAny])
class ClassesTodayByInstructorView(APIView):
    def get(self, request, instructor_id, format=None):
        today = timezone.localtime().date()
        classes_today = Attendance.objects.filter(
            instructor_id=instructor_id,
            date = today
        ).distinct()

        serializer = AttendanceSerializer(classes_today, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class ClassesToday(APIView):
    def get(self, request, format=None):
        today = timezone.localtime().date()
        classes_today = Attendance.objects.filter(
            date=today
        ).values_list('class_instance_id', flat=True).distinct()

        return Response(list(classes_today), status=status.HTTP_200_OK)
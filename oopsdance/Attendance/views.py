from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from oopsdance.models import Attendance
from .serializers import AttendanceSerializer

from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    permission_classes
)

class AddAttendanceView(APIView):
    def post(self, request, format=None):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data.copy()
            data['message'] = "Success"
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = dict(serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
 
# @permission_classes([AllowAny])   
class AttendanceListView(APIView):
    def get(self, request, format=None):
        attendance_records = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)
    
@permission_classes([AllowAny])
class AttendanceDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    
# @permission_classes([AllowAny])
class AttendanceCountByInstructorView(APIView):
    def get(self, request, instructor_id, format=None):
        try:
            attendance_count = Attendance.objects.filter(instructor_id=instructor_id, status='completed').count()
            return Response({"instructor_id": instructor_id, "attendance_count": attendance_count}, status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({"error": "Instructor not found"}, status=status.HTTP_404_NOT_FOUND)

# @permission_classes([AllowAny])
class AttendanceRecordsByInstructorView(APIView):
    def get(self, request, instructor_id, format=None):
        attendance_records = Attendance.objects.filter(instructor_id=instructor_id)
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)
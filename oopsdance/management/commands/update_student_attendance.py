import datetime
from django.core.management.base import BaseCommand
from oopsdance.models import Class, StudentAttendance, User

class Command(BaseCommand):
    help = 'Update StudentAttendance table for the upcoming week based on Class and ClassSchedule'

    def handle(self, *args, **kwargs):
        today = datetime.date.today()

        classes_today = Class.objects.filter(schedules__day_of_the_week=today.weekday())
        self.stdout.write(self.style.WARNING(f'Class HOM NAY NE: {classes_today}'))

        for class_instance in classes_today:
            students = class_instance.students.all()
            for student in students:
                student_attendance, created = StudentAttendance.objects.get_or_create(
                    class_instance=class_instance,
                    date=today,
                    student=student,
                    defaults={'status': 'pending', 'details': ''}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created attendance for {student} in {class_instance} on {today}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Attendance already exists for {student} in {class_instance} on {today}'))

        self.stdout.write(self.style.SUCCESS('Student attendance update completed'))
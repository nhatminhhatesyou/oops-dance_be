import datetime
from django.core.management.base import BaseCommand
from oopsdance.models import Class, ClassSchedule, Attendance, User, Room

class Command(BaseCommand):
    help = 'Update Attendance table for the upcoming week based on Class and ClassSchedule'

    def handle(self, *args, **kwargs):
        today = datetime.date.today()
        # start_of_week = today + datetime.timedelta(days=(7 - today.weekday()))  # Next Monday
        # end_of_week = start_of_week + datetime.timedelta(days=6)  # Following Sunday
        
        start_of_week = today - datetime.timedelta(days=today.weekday())  # This Monday
        end_of_week = start_of_week + datetime.timedelta(days=6)  # This Sunday


        classes = Class.objects.all()
        for class_instance in classes:
            schedules = class_instance.schedules.all()
            for schedule in schedules:
                day_offset = int(schedule.day_of_the_week)
                class_date = start_of_week + datetime.timedelta(days=day_offset)

                if class_date <= end_of_week:
                    attendance, created = Attendance.objects.get_or_create(
                        class_instance=class_instance,
                        date=class_date,
                        defaults={
                            'instructor': class_instance.instructor,
                            'room': class_instance.room,
                            'checkin_time': None,
                            'checkout_time': None,
                            'status': 'pending',
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created attendance for {class_instance} on {class_date}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Attendance already exists for {class_instance} on {class_date}'))

        self.stdout.write(self.style.SUCCESS('Attendance update completed'))
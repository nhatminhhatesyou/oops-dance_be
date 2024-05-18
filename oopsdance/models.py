from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

import datetime

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Người dùng phải có địa chỉ email')
        if not username:
            raise ValueError('Người dùng phải có tên đăng nhập')

        # Gán mặc định role là 'student' cho mọi người dùng mới
        extra_fields.setdefault('role', 'student')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Bạn có thể thêm trường role 'admin' cho superuser nếu muốn

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=(('instructor', 'Giáo viên'), ('student', 'Học viên')), blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)  
    contact_number = models.CharField(max_length=15, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    # method to calculate age
    def calculate_age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Class(models.Model):
    class_name = models.CharField(max_length=255, verbose_name='Tên lớp')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'}, verbose_name='Giáo viên')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Giá')
    schedules = models.ManyToManyField('ClassSchedule', verbose_name='Lịch học', blank=True)

    def __str__(self):
        return self.class_name
    
class ClassSchedule(models.Model):
    DAYS_OF_THE_WEEK = [
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday'),
        ('8', 'Sunday'),
    ]
    day_of_the_week = models.CharField(max_length=10, choices=DAYS_OF_THE_WEEK, verbose_name='Day of the Week')
    start_time = models.TimeField(verbose_name='Start Time', default=datetime.time(0,0))
    end_time = models.TimeField(verbose_name='End Time', default=datetime.time(0,0))

    def __str__(self):
        return f"{self.get_day_of_the_week_display()} from {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}"
    
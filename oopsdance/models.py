from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

import datetime

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The user must have an email address')
        if not username:
            raise ValueError('The user must have a username')

        extra_fields.setdefault('role', 'student')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=10, choices=(('instructor', 'Instructor'), ('student', 'Student'), ('staff', 'Staff'), ('guest', 'Guest')), blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def calculate_age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Room(models.Model):
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Class(models.Model):
    class_name = models.CharField(max_length=255, verbose_name='Tên lớp')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'}, verbose_name='Giáo viên')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Giá')
    schedules = models.ManyToManyField('ClassSchedule', verbose_name='Lịch học', blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Phòng', null=True, blank=True)  # Thêm trường này

    def __str__(self):
        return self.class_name
    
class ClassSchedule(models.Model):
    DAYS_OF_THE_WEEK = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('0', 'Sunday'),
    ]
    day_of_the_week = models.CharField(max_length=10, choices=DAYS_OF_THE_WEEK, verbose_name='Day of the Week')
    start_time = models.TimeField(verbose_name='Start Time', default=datetime.time(0,0))
    end_time = models.TimeField(verbose_name='End Time', default=datetime.time(0,0))

    def __str__(self):
        return f"{self.get_day_of_the_week_display()} from {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}"
    
class FixedRental(models.Model):
    date = models.DateField()  # Ngày
    staff = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'staff'})  # Nhân viên phụ trách
    rental_details = models.CharField(max_length=255)  # Nội dung thuê
    payment_method = models.BooleanField()  # Hình thức thanh toán (False: tiền mặt, True: chuyển khoản)
    status = models.ForeignKey('BookingStatus', on_delete=models.CASCADE, verbose_name='Trạng thái đặt chỗ')


    def __str__(self):
        return f"Fixed rental on {self.date} by {self.staff.full_name}"

class BookingStatus(models.Model):
    status_name = models.CharField(max_length=50, verbose_name='Tên trạng thái')

    def __str__(self):
        return self.status_name

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Phòng')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Khách hàng')
    status = models.ForeignKey(BookingStatus, on_delete=models.CASCADE, verbose_name='Trạng thái đặt chỗ', default=1)
    date = models.DateField(verbose_name='Ngày', default=timezone.now)
    checkin_time = models.TimeField(verbose_name='Thời gian check-in', default=datetime.time(0, 0))
    checkout_time = models.TimeField(verbose_name='Thời gian check-out', default=datetime.time(0, 0))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} - {self.room.name} - {self.guest.email}"

class BookingGuest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, verbose_name='Đặt chỗ')
    guest_type = models.CharField(max_length=50, verbose_name='Loại khách hàng')

    def __str__(self):
        return f"BookingGuest {self.id} - {self.booking.id} - {self.guest_type}"

class Revenue(models.Model):
    date = models.DateField()  # Ngày
    time = models.TimeField()  # Giờ
    staff = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'staff'})  # Tham chiếu tới staffID
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)  # Tổng doanh thu
    actual_revenue = models.DecimalField(max_digits=10, decimal_places=2)  # Thực thu
    actual_value_room1 = models.DecimalField(max_digits=10, decimal_places=2)  # Giá trị thực Room 1
    cash_room1 = models.DecimalField(max_digits=10, decimal_places=2)  # Đăng ký trực tiếp Room 1
    transfer_room1 = models.DecimalField(max_digits=10, decimal_places=2)  # Chuyển khoản Room 1
    actual_value_room2 = models.DecimalField(max_digits=10, decimal_places=2)  # Giá trị thực Room 2
    cash_room2 = models.DecimalField(max_digits=10, decimal_places=2)  # Đăng ký trực tiếp Room 2
    transfer_room2 = models.DecimalField(max_digits=10, decimal_places=2)  # Chuyển khoản Room 2
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Đặt chỗ')  # Liên kết với đặt chỗ

    def save(self, *args, **kwargs):
        self.total_revenue = self.actual_value_room1 + self.actual_value_room2
        self.actual_revenue = self.cash_room1 + self.transfer_room1 + self.cash_room2 + self.transfer_room2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Revenue on {self.date}"
    
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, role='client', **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, role=role, **extra_fields)
        user.set_password(password or self.make_random_password(length=6))
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(phone_number=phone_number, role='super_admin', **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # To Normalize phone to 2547XXXXXXXX format. hii inasaidia pia kwa postman api testing.
    def normalize_phone(self, phone):
        phone = phone.strip().replace(" ", "").replace("+", "")

        if phone.startswith("07") and len(phone) == 10:
            return "254" + phone[1:]
        elif phone.startswith("254") and len(phone) == 12:
            return phone
        elif phone.startswith("1") and len(phone) == 9:
            return "254" + phone
        else:
            raise ValueError("Invalid phone number format. Expected 07XXXXXXXX or 2547XXXXXXXX.")
    

#Class now to determine the roles

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('super_admin', 'Super Admin'),
    )

    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
         return f"{self.phone_number or self.email} ({self.role})"


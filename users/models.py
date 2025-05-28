from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password, name, phone, role, department, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        
        user = self.model(email=email, name=name, phone=phone, role=role, department=department, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, phone, department, **extra_fields):
        extra_fields.setdefault('role', 1)
        return self.create_user(email,password, name, department, phone, role=1, **extra_fields)


class Role(models.IntegerChoices):
    ADMIN = 1, 'Admin'
    TEACHER = 2, 'Teacher'
    STUDENT = 3, 'Student'

class Departments(models.IntegerChoices):
    ADMIN = 1, 'Admin'
    COMPUTER_SCIENCE = 2, 'Computer Science'
    ELECTRICAL_ENGINEERING = 3, 'Electrical Engineering'
    MECHANICAL_ENGINEERING = 4, 'Mechanical Engineering'
    CIVIL_ENGINEERING = 5, 'Civil Engineering'
    CHEMICAL_ENGINEERING = 6, 'Chemical Engineering'
    SOFTWARE_ENGINEERING = 7, 'Software Engineering'
    INFORMATION_TECHNOLOGY = 8, 'Information Technology'
    BUSINESS_ADMINISTRATION = 9, 'Business Administration'
    ECONOMICS = 10, 'Economics'
    MATHEMATICS = 11, 'Mathematics'
    PHYSICS = 12, 'Physics'
    CHEMISTRY = 13, 'Chemistry'
    BIOLOGY = 14, 'Biology'
    ENGLISH = 15, 'English'
    PSYCHOLOGY = 16, 'Psychology'
    SOCIOLOGY = 17, 'Sociology'
    EDUCATION = 18, 'Education'
    ARCHITECTURE = 19, 'Architecture'
    LAW = 20, 'Law'
    PHARMACY = 21, 'Pharmacy'
    MEDICAL_SCIENCES = 22, 'Medical Sciences'
    ISLAMIC_STUDIES = 23, 'Islamic Studies'
    ENVIRONMENTAL_SCIENCE = 24, 'Environmental Science'
    

class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150,unique=True)
    role = models.IntegerField(choices=Role.choices)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True)
    department = models.IntegerField(choices=Departments.choices, blank=True, null=True,default=Departments.ADMIN)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','role']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
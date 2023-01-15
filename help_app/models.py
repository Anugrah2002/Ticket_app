from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    is_administrator = models.BooleanField(default=False)
    is_branch_user = models.BooleanField(default=False)
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Branch(models.Model):
    branch_name = models.CharField(max_length=32, unique=True, error_messages={"unique": "Branch already Present"})
    branch_code = models.CharField(max_length=3, unique=True, error_messages={"unique": "Branch code already assign to other Branch"})

    def __str__(self):
        return self.branch_name


class Branch_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch_name = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    emp_id = models.CharField(max_length=16)
    contact_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket_counter(models.Model):
    date = models.DateField(unique=True)
    count_number = models.PositiveIntegerField(default=0)


class Ticket(models.Model):
    ticket_no = models.CharField(max_length=16, unique=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=64)
    reg_no = models.CharField(max_length=12)
    branch_name = models.ForeignKey(Branch, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=2048)
    ticket_status = models.CharField(max_length=16)
    date_time = models.DateTimeField()
    solution = models.CharField(max_length=2048, null=True, blank=True)
    solved_by = models.ForeignKey(Branch_user, on_delete=models.CASCADE, null=True, blank=True)

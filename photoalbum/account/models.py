from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class AccountManager(BaseUserManager):
  def create_user(self, firstname, lastname, email, password, date_of_birth=None, gender=None):
    if not email:
      raise ValueError('Users must have an email address')

    user = self.model(
      firstname=firstname,
      lastname=lastname,
      email=self.normalize_email(email),
      date_of_birth=date_of_birth,
      gender=gender
    )
    
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, firstname, lastname, email, password, date_of_birth, gender):
    user = self.create_user(
        firstname,
        lastname,
        email,
        password,
        date_of_birth,
        gender
    )

    user.is_admin = True
    user.save(using=self._db)
    return user

GENDER_CHOICES = (
  ('M', 'Male'),
  ('F', 'Female')
)

class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, blank=False, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.firstname +" "+self.lastname

    def get_short_name(self):
        return self.firstname

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None): #general access ctrl
      return True #TODO: Implement me!

    def has_module_perms(self, app_label): # module level access ctrl
      return True #TODO: implement me!

    @property
    def is_staff(self):
        return self.is_admin

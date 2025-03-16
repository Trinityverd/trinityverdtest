from django.db import models
from django.contrib.auth.models import User


class SubCounty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Field Officer', 'Field Officer'),
        ('supervisor', 'supervisor'),
        ('Project Manager', 'Project Manager')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    sub_county = models.ManyToManyField(SubCounty, related_name='supervisor')


    def __str__(self):
        return f'{self.user.username} - {','.join(str(sc) for sc in self.sub_county.all())}'


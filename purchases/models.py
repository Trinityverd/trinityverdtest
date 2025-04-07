from django.db import models
from authentication.models import UserProfile, User, SubCounty
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits.')

class Purchases(models.Model):
    COUNTY_CHOICES = [
        ('Kitui', 'Kitui'),
        ('Makueni', 'Makueni'),
    ]

    purchased_on = models.DateTimeField(auto_now_add=True)
    farmer_id = models.AutoField(primary_key=True)
    farmer_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=15, unique=True, error_messages={'unique': 'ID Number already exists'})
    phone_number = models.CharField(max_length=10, validators=[phone_validator], unique=True, error_messages={'unique': 'Phone Number Number already exists'})
    county = models.CharField(max_length=100, choices=COUNTY_CHOICES)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, related_name="purchase_data")
    ward = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    clean_castor = models.DecimalField(max_digits=5, decimal_places=2)
    husk_castor = models.DecimalField(max_digits=5, decimal_places=2)
    threshed_castor = models.DecimalField(max_digits=5, decimal_places=2)
    field_officer = models.ForeignKey("authentication.UserProfile", on_delete=models.CASCADE, related_name="purchases_fielddata", limit_choices_to={'role': 'field_officer'})

    def __str__(self):
        return f"{self.farmer_name} | {self.phone_number} | {self.sub_county} | {self.ward} | {self.village}"


from django.db import models
from authentication.models import UserProfile, User, SubCounty
from recruitment.models import FieldData
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits.')


class SeedDistri(models.Model):
    COUNTY_CHOICE = [
        ('Kitui', 'Kitui'),
        ('Makueni', 'Makueni'),
    ]

    farmer_recruited = models.ForeignKey(FieldData, on_delete=models.SET_NULL, to_field='farmer_id', db_column='farmer_ref', null=True, blank=True, related_name="seed_data")
    issued_on = models.DateTimeField(auto_now_add=True)
    farmer_id = models.AutoField(primary_key=True)
    farmer_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=15, unique=True, error_messages={'unique': 'ID Number already exists'})
    phone_number = models.CharField(max_length=10, validators=[phone_validator], unique=True, error_messages={'unique': 'Phone Number Number already exists'})
    county = models.CharField(max_length=100, choices=COUNTY_CHOICE)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE)
    ward = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    acres = models.DecimalField(max_digits=5, decimal_places=2)
    seed_amount = models.DecimalField(max_digits=5, decimal_places=2)
    variety = models.CharField(max_length=50)
    field_officer = models.ForeignKey("authentication.UserProfile", on_delete=models.CASCADE, related_name="seed_distribution_fielddata", limit_choices_to={'role': 'field_officer'})

    def __str__(self):
        return f"{self.farmer_name} | {self.phone_number} | {self.sub_county} | {self.ward} | {self.village}"

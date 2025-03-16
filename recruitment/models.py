from django.db import models
from authentication.models import UserProfile, User, SubCounty

class FieldData(models.Model):
    COUNTY_CHOICES = [
        ('Kitui', 'Kitui'),
        ('Makueni', 'Makueni'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    farmer_id = models.AutoField(primary_key=True)
    farmer_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15)
    county = models.CharField(max_length=100, choices=COUNTY_CHOICES)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, related_name="data")
    ward = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    acres = models.DecimalField(max_digits=5, decimal_places=2)
    field_officer = models.ForeignKey("authentication.UserProfile", on_delete=models.CASCADE, related_name="recruitment_fielddata", limit_choices_to={'role': 'field_officer'})

    def __str__(self):
        return f"{self.farmer_name} | {self.phone_number} | {self.sub_county} | {self.ward} | {self.village}"

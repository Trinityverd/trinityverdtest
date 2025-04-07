from django import forms
from django_select2.forms import Select2Widget
from . models import SeedDistri
from recruitment.models import FieldData
from authentication.models import SubCounty


class SeedDistriForm(forms.ModelForm):
    class Meta:
        model = SeedDistri
        fields = [
            "farmer_recruited", "farmer_name", "id_number", "phone_number", "county", "sub_county", "ward", "village", "acres", "seed_amount", "variety"
        ]
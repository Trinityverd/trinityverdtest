from django import forms
from . models import FieldData


class FieldDataForm(forms.ModelForm):
    class Meta:
        model = FieldData
        fields = [
            "farmer_name", "id_number", "phone_number", "county", "sub_county", "ward", "village", "acres"
        ]
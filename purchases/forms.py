from django import forms
from . models import Purchases


class PurchasesForm(forms.ModelForm):
    class Meta:
        model = Purchases
        fields = [
            "farmer_name", "id_number", "phone_number", "county", "sub_county", "ward", "village", "clean_castor", "husk_castor", "threshed_castor"
        ]
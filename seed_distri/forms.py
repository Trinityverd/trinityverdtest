from django import forms
from django_select2.forms import Select2Widget
from . models import SeedDistri
from recruitment.models import FieldData
from authentication.models import SubCounty


class SeedDistriForm(forms.ModelForm):
    farmer_recruited = forms.ModelChoiceField(queryset=FieldData.objects.all().order_by('farmer_name'),
                                              required=False, label= "Check if Farmer exists:",
                                              empty_label="Select a Farmer",
                                              widget=forms.Select(attrs={"id": "farmerDropdown"}))

    farmer_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"id": "farmer_name"}))
    id_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"id": "id_number"}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"id": "phone_number"}))
    county = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"id": "county"}))
    sub_county = forms.ModelChoiceField(queryset=SubCounty.objects.all(), required=False, widget=forms.Select(attrs={"id": "sub_county"}))
    ward = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"id": "ward"}))
    village = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"id": "village"}))
    acres = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"id": "acres"}))
    seed_amount = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"id": "seed_amount"}))
    variety = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={"id": "variety"}))


    class Meta:
        model = SeedDistri
        fields = [
            "farmer_recruited", "farmer_name", "id_number", "phone_number", "county", "sub_county", "ward", "village", "acres", "seed_amount", "variety"
        ]


    def clean(self):
        cleaned_data = super().clean()
        farmer_recruited = cleaned_data.get('farmer_recruited')
        farmer_name = cleaned_data.get('farmer_name')

        if not farmer_recruited and not farmer_name:
            raise forms.ValidationError("You must select a recruited farmer or enter a new farmer's details.")
        return cleaned_data
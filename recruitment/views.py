from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import openpyxl
from django.http import JsonResponse

from recruitment.forms import FieldDataForm
from recruitment.models import FieldData


@login_required
def recruitment(request):
    user_profile = request.user.userprofile

    if user_profile.role != "Field Officer":
        return redirect("dashboard")

    if request.method == "POST":
        form = FieldDataForm(request.POST)
        if form.is_valid():
            farmer_data = form.save(commit=False)
            farmer_data.field_officer = user_profile
            farmer_data.save()
            return redirect("recruited_farmers")

    else:
        form = FieldDataForm()

    return render(request, 'recruitment.html', {"form": form})


@login_required
def recruited_farmers(request):
    user_profile = request.user.userprofile

    if user_profile.role == "Field Officer":
        data = FieldData.objects.filter(field_officer=user_profile)

    elif user_profile.role == "supervisor":
        data = FieldData.objects.filter(sub_county__in=user_profile.sub_county.all())

    elif user_profile.role == "Project Manager":
        data = FieldData.objects.all()

    else:
        data = FieldData.objects.none()

    return render(request, "recruited_farmers.html", {"data": data})


@login_required
def export_farmers(request):
    user_profile = request.user.userprofile
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Farmers'

    columns = ['S/No', 'Date', 'Farmer Name', 'ID Number', 'Phone Number', 'County', 'Sub-County', 'Ward', 'Village', 'Acres', 'Field Officer']
    worksheet.append(columns)

    if user_profile.role == "Field Officer":
        farmers = FieldData.objects.filter(field_officer=user_profile).order_by('-created_at')

    elif user_profile.role == "supervisor":
        supervised_sub_counties = user_profile.sub_county.all()
        farmers = FieldData.objects.filter(sub_county__in=supervised_sub_counties).order_by('-created_at')

    elif user_profile.role == "Project Manager":
        farmers = FieldData.objects.all().order_by('-created_at')

    else:
        farmers = FieldData.objects.none()

    for idx, farmer in enumerate(farmers, start=1):
        worksheet.append([
            idx,
            farmer.created_at.strftime('%d-%m-%Y'),
            farmer.farmer_name,
            farmer.id_number,
            farmer.phone_number,
            farmer.county,
            str(farmer.sub_county),
            farmer.ward,
            farmer.village,
            farmer.acres,
            str(farmer.field_officer)
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    response['Content-Disposition'] = 'attachment; filename=farmers.xlsx'

    workbook.save(response)
    return response

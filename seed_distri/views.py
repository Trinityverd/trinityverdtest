from gc import get_objects

import openpyxl
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from recruitment.models import FieldData
from seed_distri.forms import SeedDistriForm
from seed_distri.models import SeedDistri


@login_required
def seed_distribution(request):
    user_profile = request.user.userprofile

    if user_profile.role != "Field Officer":
        return redirect("dashboard")

    if request.method == "POST":
        form = SeedDistriForm(request.POST)
        if form.is_valid():
            farmer_data = form.save(commit=False)
            farmer_data.field_officer = user_profile
            farmer_data.save()
            return redirect("seed_distributed")

    else:
        form = SeedDistriForm()

    return render(request, 'seed_distribution.html', {"form": form})


@login_required
def seed_distributed(request):
        user_profile = request.user.userprofile

        if user_profile.role == "Field Officer":
            seed_data = SeedDistri.objects.filter(field_officer=user_profile)

        elif user_profile.role == "supervisor":
            seed_data = SeedDistri.objects.filter(sub_county__in=user_profile.sub_county.all())

        elif user_profile.role == "Project Manager":
            seed_data = SeedDistri.objects.all()

        else:
            seed_data = SeedDistri.objects.none()

        return render(request, "seed_distributed.html", {"seed_data": seed_data})


@login_required
def get_farmer_details(request, farmer_id):
    farmer = get_object_or_404(FieldData, farmer_id=farmer_id)
    if farmer:
        data = {
            "farmer_name": farmer.farmer_name,
            "id_number": farmer.id_number,
            "phone_number": farmer.phone_number,
            "county": farmer.county,
            "sub_county": farmer.sub_county.name if farmer.sub_county else None,
            "ward": farmer.ward,
        }
        return JsonResponse(data)


@login_required
def export_seed(request):
    user_profile = request.user.userprofile
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Seed Distribution'

    columns = ['S/No', 'Date', 'Farmer Name', 'ID Number', 'Phone Number', 'County', 'Sub-County', 'Ward', 'Village', 'Acres', 'Seed(KG)', 'Variety', 'Field Officer']
    worksheet.append(columns)

    if user_profile.role == "Field Officer":
        farmers = SeedDistri.objects.filter(field_officer=user_profile).order_by('-created_at')

    elif user_profile.role == "supervisor":
        supervised_sub_counties = user_profile.sub_county.all()
        farmers = SeedDistri.objects.filter(sub_county__in=supervised_sub_counties).order_by('-created_at')

    elif user_profile.role == "Project Manager":
        farmers = SeedDistri.objects.all().order_by('-created_at')

    else:
        farmers = SeedDistri.objects.none()

    for idx, farmer in enumerate(farmers, start=1):
        worksheet.append([
            idx,
            farmer.issued_on.strftime('%d-%m-%Y'),
            farmer.farmer_name,
            farmer.id_number,
            farmer.phone_number,
            farmer.county,
            str(farmer.sub_county),
            farmer.ward,
            farmer.village,
            farmer.acres,
            farmer.seed_amount,
            farmer.variety,
            str(farmer.field_officer)
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    response['Content-Disposition'] = 'attachment; filename=farmers.xlsx'

    workbook.save(response)
    return response

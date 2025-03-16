from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import openpyxl
from django.http import JsonResponse

from purchases.forms import PurchasesForm
from purchases.forms import Purchases

@login_required
def purchases(request):
    user_profile = request.user.userprofile

    if user_profile.role != "Field Officer":
        return redirect("dashboard")

    if request.method == "POST":
        form = PurchasesForm(request.POST)
        if form.is_valid():
            farmer_data = form.save(commit=False)
            farmer_data.field_officer = user_profile
            farmer_data.save()
            return redirect("dashboard")

    else:
        form = PurchasesForm()

    return render(request, 'purchase.html', {"form": form})

@login_required
def purchased(request):
    user_profile = request.user.userprofile

    if user_profile.role == "Field Officer":
        data = Purchases.objects.filter(field_officer=user_profile)

    elif user_profile.role == "supervisor":
        data = Purchases.objects.filter(sub_county__in=user_profile.sub_county.all())

    elif user_profile.role == "Project Manager":
        data = Purchases.objects.all()

    else:
        data = Purchases.objects.none()

    return render(request, "purchased.html", {"data": data})


@login_required
def export_purchases(request):
    user_profile = request.user.userprofile
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Purchases'

    columns = ['S/No', 'Date', 'Farmer Name', 'ID Number', 'Phone Number', 'County', 'Sub-County', 'Ward', 'Village', 'Clean Castor(KG)', 'Unclean Castor(KG)', 'Threshed Castor(KG)', 'Field Officer']
    worksheet.append(columns)

    if user_profile.role == "Field Officer":
        farmers = Purchases.objects.filter(field_officer=user_profile).order_by('-purchased_on')

    elif user_profile.role == "supervisor":
        supervised_sub_counties = user_profile.sub_county.all()
        farmers = Purchases.objects.filter(sub_county__in=supervised_sub_counties).order_by('-purchased_on')

    elif user_profile.role == "Project Manager":
        farmers = Purchases.objects.all().order_by('-purchased_on')

    else:
        farmers = Purchases.objects.none()

    for idx, farmer in enumerate(farmers, start=1):
        worksheet.append([
            idx,
            farmer.purchased_on.strftime('%d-%m-%Y'),
            farmer.farmer_name,
            farmer.id_number,
            farmer.phone_number,
            farmer.county,
            str(farmer.sub_county),
            farmer.ward,
            farmer.village,
            farmer.clean_castor,
            farmer.husk_castor,
            farmer.threshed_castor,
            str(farmer.field_officer)
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
    response['Content-Disposition'] = 'attachment; filename=purchases.xlsx'

    workbook.save(response)
    return response
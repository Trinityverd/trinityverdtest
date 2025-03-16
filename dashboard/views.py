from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator
from recruitment.models import FieldData
from seed_distri.models import SeedDistri
from purchases.models import Purchases


@login_required
def dashboard(request):
    user_profile = request.user.userprofile

    if user_profile.role == "Field Officer":
        data = FieldData.objects.filter(field_officer=user_profile).order_by('-created_at')
        seed_data = SeedDistri.objects.filter(field_officer=user_profile).order_by('-issued_on')
        purchase = Purchases.objects.filter(field_officer=user_profile).order_by('-purchased_on')

    elif user_profile.role == "supervisor":
        supervised_sub_counties = user_profile.sub_county.all()
        data = FieldData.objects.filter(sub_county__in=supervised_sub_counties).order_by('-created_at')
        seed_data = SeedDistri.objects.filter(sub_county__in=supervised_sub_counties).order_by('-issued_on')
        purchase = Purchases.objects.filter(sub_county__in=supervised_sub_counties).order_by('-purchased_on')

    elif user_profile.role == "Project Manager":
        data = FieldData.objects.all().order_by('-created_at')
        seed_data = SeedDistri.objects.all().order_by('-issued_on')
        purchase = Purchases.objects.all().order_by('-purchased_on')

    else:
        data = FieldData.objects.none()
        seed_data = SeedDistri.objects.none()
        purchase = Purchases.objects.none()

    display_data = data[:10]
    display_seed = seed_data[:10]
    display_purchase = purchase[:10]
    total_farmers = data.count()
    total_seed_farmers = seed_data.count()
    total_purchase_farmers = purchase.count()
    total_acres = data.aggregate(total_acres=Sum("acres"))["total_acres"] or 0
    total_seed = seed_data.aggregate(total_seed=Sum("seed_amount"))["total_seed"] or 0
    total_clean = purchase.aggregate(total_clean=Sum("clean_castor"))["total_clean"] or 0
    total_husk = purchase.aggregate(total_husk=Sum("husk_castor"))["total_husk"] or 0
    total_threshed = purchase.aggregate(total_threshed=Sum("threshed_castor"))["total_threshed"] or 0

    return render(request, 'dashboard.html', {"display_data": display_data,
                                              "display_seed": display_seed,
                                              "display_purchase": display_purchase,
                                              "total_farmers": total_farmers,
                                              "total_seed_farmers": total_seed_farmers,
                                              "total_purchase_farmers": total_purchase_farmers,
                                              "total_acres": total_acres,
                                              "total_seed": total_seed,
                                              "total_clean": total_clean,
                                              "total_husk": total_husk,
                                              "total_threshed": total_threshed})

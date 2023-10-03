from django.shortcuts import render
from .models import Profile

def my_profile_view(request):
    xValues = []
    myRefData = []
    referredUsersWithPaymentData = []
    profile= Profile.objects.get(user=request.user)
    my_ref= profile.get_recommened_profiles()
    referred_users_with_payment = profile.get_referred_users_with_payment()
    refelcode = profile.get_code()
    growth = profile.get_growth()
    xValues.append(profile.created.strftime("%d"))
    my_ref_length = len(profile.get_recommened_profiles())
    myRefData.append(my_ref_length)

    referred_users_length = len(profile.get_referred_users_with_payment())
    referredUsersWithPaymentData.append(referred_users_length)

    context = {
        'my_ref': my_ref,
        'referred_users_with_payment': referred_users_with_payment,
        'refelcode': refelcode,
        'growth' : growth,
        'xValues': xValues,
        'myRefData': myRefData,
        'referredUsersWithPaymentData': referredUsersWithPaymentData,
    }
    return render(request, 'profiles/main.html', context)


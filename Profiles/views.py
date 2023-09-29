from django.shortcuts import render
from .models import Profile

def my_profile_view(request):
    profile= Profile.objects.get(user=request.user)
    my_ref= profile.get_recommened_profiles()
    context = {
        'my_ref': my_ref
    }
    return render(request, 'profiles/main.html', context)
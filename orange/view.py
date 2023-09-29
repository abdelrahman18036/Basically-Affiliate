from django.shortcuts import render, redirect
from Profiles.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



def main_view(request, *args, **kwargs):
    code = kwargs.get('code')
    try:
        qs = Profile.objects.get(code=code)
        request.session['ref_profile'] = qs.id
        print(id , qs.id)
    except:
        pass
    if 'session_key' in request.session:
        expiry_date = request.session.get('session_key').get('_session_expiry')
        print(expiry_date)
    else:
        print("Session key not found in request session.")
        print(request.session.get_expiry_date())
    return render(request, 'main.html', {})


def register_view(request, *args, **kwargs):
    profile_id = request.session.get('ref_profile')
    print(profile_id)
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile = Profile.objects.get(id=profile_id)
            instance = form.save()
            registered_user = User.objects.get(id=instance.id)
            registered_profile = Profile.objects.get(user=registered_user)
            registered_profile.reffeled_by = recommended_by_profile
            registered_profile.save()
        else:
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user= authenticate(username=username, password=password)
        login(request, user)
        return redirect('main_view')


    return render(request, 'register.html', {'form':form, 'profile_id':profile_id})
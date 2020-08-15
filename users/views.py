from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import json
from .serializers import UserSerailizer
from django.http import JsonResponse

# create new user
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


# create/update new profile
@login_required
def profile(request):
    if request.method == "POST":
        # instance=request.user to know which User and Profile to update
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else: 
        # populate the form with the current user infomation
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


# get the user profile settings from the server instead of using local settings
@login_required
def userSettings(request):
    setting = request.user.profile
    seralizer = UserSerailizer(setting, many=False)
    return JsonResponse(seralizer.data, safe=False)


# update the profile settings on the user on the database
@login_required
def updateTheme(request):
    data = json.loads(request.body)
    theme = data['theme']
    setting = request.user.profile
    setting.theme = theme
    setting.save()
    print('Request:', theme)
    return JsonResponse('Updated..', safe=False)
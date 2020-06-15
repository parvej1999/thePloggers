from django.shortcuts import render, redirect
from .forms import registrationForm, User_form, UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = registrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your username is "{username}"')
            return redirect('login')
    else:
        form = registrationForm()
    return render(request, 'Users/registerForm.html', {"form": form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = User_form(request.POST, instance=request.user)
        user_profile = UserProfile(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and user_profile.is_valid():
            user_form.save()
            user_profile.save()
            messages.success(request, 'Profile Have Been Updated Successfully')
            return redirect('profile')
    else:
        user_form = User_form(instance=request.user)
        user_profile = UserProfile(instance=request.user.profile)
    return render(request, 'users/profile.html', {"user_form": user_form, 'profile_form': user_profile})

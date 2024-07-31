from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from .models import Profile


def home_view(request):
    return render(request, 'accounts/home.html')

print("Loading views.py")

def signup_view(request):
    print("Loading views.py")
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                profile_picture=form.cleaned_data.get('profile_picture'),
                address_line1=form.cleaned_data.get('address_line1'),
                city=form.cleaned_data.get('city'),
                state=form.cleaned_data.get('state'),
                pincode=form.cleaned_data.get('pincode')
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)
    profile_picture_url = profile.profile_picture.url if profile.profile_picture else None
    return render(request, 'accounts/dashboard.html', {'profile': profile, 'profile_picture_url': profile_picture_url})
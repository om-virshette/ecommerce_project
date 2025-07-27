from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, login, logout
from .forms import SignupForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()           
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            print(user)
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            print(user)
            login(request, user)
            print("success")
            return redirect('product_list')            
        else:
            print("error") 
            return render(request, 'login.html', {'error':'Invalid username or password'})
                      
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'profile.html', {'user':request.user}) 

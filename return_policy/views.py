from django.shortcuts import render

def return_policy(request):
    return render(request, 'return_policy.html')  # Will look in templates/
# Create your views here.

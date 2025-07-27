from django.shortcuts import render
from django.views.decorators.http import require_GET

@require_GET
def privacy_policy(request):
    return render(request, 'privacy_policy.html')
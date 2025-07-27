from django.shortcuts import render
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def terms_view(request):
    sections = [
        {
            'title': '1. Acceptance of Terms',
            'content': 'By accessing this website, you agree to be bound by these Terms...'
        },
        {
            'title': '2. User Responsibilities',
            'content': 'You agree not to use the service for any illegal purpose...'
        },
        # Add more sections as needed
    ]
    return render(request, 'terms.html', {'sections': sections})
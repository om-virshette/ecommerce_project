from django.shortcuts import render
from .models import FAQ

def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'faq.html', {'faqs': faqs})

def faq_list(request):
    faqs = [
        {'question': 'How do I return an item?', 'answer': 'Visit our return policy page for details.'},
        {'question': 'What payment methods do you accept?', 'answer': 'We accept all major credit cards.'},
        # Add more FAQs here or fetch from database
    ]
    return render(request, 'faq.html', {'faqs': faqs})
# Create your views here.

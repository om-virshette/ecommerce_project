from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            message = form.save()
            
            # Send email
            send_mail(
                subject=f"New Contact Form Submission from {message.name}",
                message=message.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            return redirect('contact:success')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')


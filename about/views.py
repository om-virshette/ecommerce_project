from django.shortcuts import render

def about_page(request):
    team_members = [
        {'name': 'Om Virshette', 'bio': 'Full Stack Python Developer', 'image': 'team/john.jpg'},
        
    ]
    
    stats = [
        {'value': '10K+', 'label': 'Happy Customers'},
        {'value': '2025', 'label': 'Founded In'},
        
        {'value': '24/7', 'label': 'Support'},
    ]
    
    return render(request, 'about.html', {
        'team': team_members,
        'stats': stats,
    })
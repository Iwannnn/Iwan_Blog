from django.shortcuts import render

# Create your views here.


def contact(request):
    return render(request, 'interface/contact.html')


def about(request):
    return render(request, 'interface/about.html')


def admin(request):
    return render(request, 'admin/')

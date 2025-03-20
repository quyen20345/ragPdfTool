from django.shortcuts import render
from .models import Item

def home(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
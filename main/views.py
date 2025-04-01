from django.shortcuts import render,HttpResponse,get_object_or_404
from .models import Aisle,Item


# Create your views here.
def index(request):
    return render(request,"index.html")

def restocking(request):
    aisles = Aisle.objects.all()
    return render(request, 'restocking.html', {'aisles': aisles})

def restocking_aisle(request, aisle_id):
    aisle = get_object_or_404(Aisle, id=aisle_id)
    items = Item.objects.filter(aisle=aisle)
    return render(request, 'restocking_aisle.html', {'aisle': aisle, 'items': items})

def inventory_management(request):
    return render(request,'ims.html')
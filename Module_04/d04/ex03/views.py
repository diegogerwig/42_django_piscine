from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    total_shades = 50
    increment = 255 / (total_shades - 1)
    
    shades = [
        "{:02X}".format(int(i * increment)) 
        for i in range(total_shades)
    ]

    context = {
        "range": shades
    }

    return render(request, 'ex03/index.html', context)

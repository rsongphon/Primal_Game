from django.shortcuts import render
from .forms import PrimalsForm
from django.urls import reverse
from django.http import JsonResponse
import requests
from PrimalGameAPI.models import RPiBoards , Primals

# Create your views here.
def home(request):
    return render(request, "index.html")


def primals(request):
    if request.method == 'POST':
        form = PrimalsForm(request.POST)
        if form.is_valid():
            # Serialize the form data
            data = {
                'name': form.cleaned_data['name'],
            }
            
             # URL of the API endpoint
            url = request.build_absolute_uri(reverse('api:primals'))
            
            # Make a POST request to your API endpoint
            response = requests.post(url, data=data)
            if response.status_code == 201:
                # Return True to indicate javascript to process futher
                return JsonResponse({'success': True})
            # authenthication failed
            elif response.status_code == 401:
                return JsonResponse({'errors': 'Unauthorized'})
    else:
        form = PrimalsForm()
    return render(request, 'register-primals.html', {'form': form})


def start_game(request):
    rpi_list = RPiBoards.objects.all()  # Query data from the database
    primal_list = Primals.objects.all()  # Query data from the database
    return render(request, 'start-game.html', {'rpi_list': rpi_list , 'primal_list': primal_list})
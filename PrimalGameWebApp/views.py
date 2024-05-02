from django.shortcuts import render , redirect
from .forms import PrimalsForm , UserUpdateForm , StartGameForm
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import requests
from PrimalGameAPI.models import RPiBoards , Primals , Games
from django.contrib import messages
from datetime import datetime

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
    if request.method == 'POST':
        form = StartGameForm(request.POST)
        if form.is_valid():
            # Serialize the form data
            data = {
                'rpiboard': form.cleaned_data['rpi_name'],
                'primal': form.cleaned_data['primal_name'],
                'game': form.cleaned_data['game_name'],
                'login_hist' : datetime.now()
            }
            
            # POST to /api/games-instances
            url = request.build_absolute_uri(reverse('api:game-instance'))
            
            # Make a POST request to your API endpoint
            response = requests.post(url, data=data)
            
            if response.status_code == 201:
                # Redict to dashboard page
                return redirect('webapp') # placeholder
            # authenthication failed
            elif response.status_code == 401:
                return JsonResponse({'errors': 'Unauthorized'})
    
    
    else:
        form = StartGameForm()
        return render(request, 'start-game.html', {'form': form})




def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, instance=user)
        print('1')
        if form.is_valid():
            user_form = form.save()
            print('test')
            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('webapp:profile', user_form.username)

        for error in list(form.errors.values()):
            print(error)
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'profile.html', context={'form': form})

    return redirect("")
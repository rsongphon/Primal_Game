from django.shortcuts import render , redirect
from .forms import PrimalsForm , UserUpdateForm , StartGameForm
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import requests
from PrimalGameAPI.models import RPiBoards , Primals , Games , RPiStates , GameInstances
from django.contrib import messages
from datetime import datetime
from PrimalGameAPI import views as APIviews
from django.http import HttpRequest , HttpResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import Http404


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

            # Get current user in session
            user = User.objects.get(username=request.user)
            
            # Assuming you have already generated a token for the user
            token = Token.objects.get(user=user)

            #Serialize the form data
            
            rpiboard = form.cleaned_data['rpi_name']
            primal = form.cleaned_data['primal_name']
            game = form.cleaned_data['game_name']
            
            
            data = {
               'rpiboard': rpiboard,
                'primal': primal,
                'game': game,
                'login_hist' : str(datetime.now())
            }
            # Set up the request headers with the token
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'  # Adjust content type if necessary
            }
            # POST to /api/games-instances
            url = request.build_absolute_uri(reverse('api:game-instance'))
            
            # Make a POST request to your API endpoint
            # Send the POST request with the data and headers
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 201:
                
                # User is alreay authenthecated, we can now edit the model directly
                
                # Gameinstance create successful
                # send a signal to start a game on target RPI board
                
                # Access the ID of the newly created instance from the response
                game_instance_id = response.json().get('id')
                
                # get the state of the target RPI board
                # Replace `pk_value` with the actual primary key value you want to retrieve
                rpi_state = RPiStates.objects.get(rpiboard=rpiboard)
                # Flag signal to start the game
                rpi_state.is_occupied = False
                rpi_state.start_game = True  
                rpi_state.game_instance_running = game_instance_id  
                rpi_state.save()
                # Redict to dashboard page
                return redirect('/') # placeholder
            # authenthication failed
            elif response.status_code == 401:
                return JsonResponse({'errors': 'Unauthorized'})
            else:
                print(response)
                return JsonResponse({'errors': 'something wrong'})
    
    
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


def game_push_button_handle_signal(request, gameinstance):
    
    event = request.GET['event']
    
    try:
        # get gameinstance object 
        gameinst =  GameInstances.objects.get(pk=gameinstance)
        
        # Get info
        rpiboard_id = gameinst.rpiboard.pk

        try : 
            # get rpi state
            rpi_state = RPiStates.objects.get(rpiboard=rpiboard_id)
            
        except RPiStates.DoesNotExist:
            raise Http404("No RPiStates matches the given query.")
        
        if event == 'press':
            # Handle the signal here
            rpi_state.gp17 = True
            rpi_state.save()
            # For simplicity, let's just print a message
            print("button press")
        elif event == 'release':
            rpi_state.gp17 = False
            rpi_state.save()
            print("button leave")
            
        return HttpResponse("Signal received")
        
    except GameInstances.DoesNotExist:
        raise Http404("No GameInstances matches the given query.")
    
    
    


    
 



def game_push_button_page(request, gameinstance):
    return render(request, 'game_push_button.html')
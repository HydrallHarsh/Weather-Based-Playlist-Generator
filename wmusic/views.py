import os
import requests
from django.http import JsonResponse
from django.shortcuts import render,redirect
from dotenv import load_dotenv
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)
import pprint
import spotipy
import urllib.parse
from .models import UserWeather
from django.contrib.auth.models import User
load_dotenv()
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Log the user in
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request , 'register.html' , {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def get_weather(request):
    # request.session.flush() #Clearing Sessions for TESTIING PURPOSE
    api_key = os.getenv('WEATHER_API_KEY')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    

    # Check if lat and lon are present
    if not lat or not lon:
        return JsonResponse({'error': 'Latitude and Longitude must be provided.'}, status=400)

    # Fetch weather data
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    weather_data = response.json()

    if weather_data and weather_data.get('cod') == 200:
        location = weather_data['name']
        weather_condition = weather_data['weather'][0]['main']
        temprature = round(weather_data['main']['temp'] - 273 , 3)

        UserWeather.objects.update_or_create(user = request.user,
                                             defaults={'location': location,
                                                       'temprature': temprature,
                                                       'weather_condition': weather_condition,
                                                       }
                                             )

        return JsonResponse({
            'location': weather_data['name'],
            'Weather': weather_data['weather'][0]['main'],
            'temperature': round(weather_data['main']['temp'] - 273 , 3),
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': round(weather_data['wind']['speed'] * 3.6 , 3),
        })
    else:
        return JsonResponse({'error': 'Could not retrieve weather data.'}, status=400)

# Handle Spotify callback


# Spotify credentials in settings.py
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_SCOPE = 'playlist-read-private playlist-modify-public user-library-read app-remote-control streaming playlist-modify-private user-follow-read user-follow-modify user-read-currently-playing user-read-playback-state'

# # @login_required
def spotify_login(request):
    scope = urllib.parse.quote(SPOTIFY_SCOPE)
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={SPOTIFY_CLIENT_ID}&scope={scope}&redirect_uri={SPOTIFY_REDIRECT_URI}"
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')

    if not code:
        return render(request, 'error.html', {'message': 'No authorization code returned'})

    # Exchange authorization code for access token
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(token_url, data=token_data)
    token_info = response.json()

    if 'access_token' in token_info:
        access_token = token_info['access_token']
        # Store the token in the session (or a database if preferred)
        request.session['auth_token'] = access_token
        return redirect('user_playlists')
    else:
        return render(request, 'error.html', {'message': 'Failed to get access token'})
    

def spotify_success(request):
    return render(request, 'success.html', {'message': 'Spotify authentication successful!'})

def user_playlists(request):
    access_token = request.session.get('auth_token')

    if not access_token:
        return redirect('spotify_login')

    sp = spotipy.Spotify(auth=access_token)

    playlists = sp.current_user_playlists()
    curr_play = sp.currently_playing()
    # pprint.pprint(curr_play['item']['album']['artists'])
    if playlists:
        playlist_data = []
        for playlist in playlists['items']:
            playlist_data.append({
                'name': playlist['name'],
                'uri': playlist['uri'],
                'owner': playlist['owner']['display_name'],
            })
        return render(request, 'playlists.html', {'playlists': playlist_data})
    else:
        return render(request, 'error.html', {'message': 'No playlists found'})

def get_weather_data(user):
    try:
        weather_data = UserWeather.objects.filter(user = user).latest('timestamp')
        return weather_data
    except UserWeather.DoesNotExist:
        return None
    

def generate_playlists(request):
    user = request.user
    weather_data_user = get_weather_data(user)

    access_token = request.session.get('auth_token')

    if not access_token:
        return redirect('spotify_login')

    sp = spotipy.Spotify(auth=access_token)

   

    if(weather_data_user != None):
        weather_condition = weather_data_user.weather_condition 
        print(weather_condition)
        if weather_condition == 'thunderstorm':
            seed_genres = ['rock, metal, industrial']
            min_acousticness = 0.1
            max_acousticness = 0.4
            min_danceability = 0.4
            max_danceability = 0.7
            min_duration_ms = 180000
            max_duration_ms = 360000
            min_energy = 0.7
            max_energy = 1.0
            min_instrumentalness = 0.0
            max_instrumentalness = 0.5
        elif weather_condition == 'rain':
            seed_genres = ['acoustic, folk, indie']
            min_acousticness = 0.6
            max_acousticness = 1.0
            min_danceability = 0.4
            max_danceability = 0.6
            min_duration_ms = 120000
            max_duration_ms = 300000
            min_energy = 0.3
            max_energy = 0.6
            min_instrumentalness = 0.1
            max_instrumentalness = 0.8
        elif weather_condition == 'cloud':
            seed_genres = ['indie, chill, ambient']
            min_acousticness = 0.4
            max_acousticness = 0.7
            min_danceability = 0.4
            max_danceability = 0.6
            min_duration_ms = 150000
            max_duration_ms = 300000
            min_energy = 0.4
            max_energy = 0.7
            min_instrumentalness = 0.1
            max_instrumentalness = 0.6
        elif weather_condition == 'sun':
            seed_genres = ['pop, dance']
            min_acousticness = 0.2
            max_acousticness = 0.5
            min_danceability = 0.7
            max_danceability = 1.0
            min_duration_ms = 120000
            max_duration_ms = 300000
            min_energy = 0.6
            max_energy = 1.0
            min_instrumentalness = 0.0
            max_instrumentalness = 0.3
        elif weather_condition == 'Clear':
            seed_genres = ['country, pop']
            min_acousticness = 0.3
            max_acousticness = 0.6
            min_danceability = 0.5
            max_danceability = 0.8
            min_duration_ms = 120000
            max_duration_ms = 300000
            min_energy = 0.5
            max_energy = 0.8
            min_instrumentalness = 0.0
            max_instrumentalness = 0.4
        elif weather_condition == 'snow':
            seed_genres = ['classical, jazz, acoustic']
            min_acousticness = 0.6
            max_acousticness = 1.0
            min_danceability = 0.3
            max_danceability = 0.5
            min_duration_ms = 180000
            max_duration_ms = 400000
            min_energy = 0.2
            max_energy = 0.5
            min_instrumentalness = 0.4
            max_instrumentalness = 1.0
        elif weather_condition == 'mist':
            seed_genres = ['ambient, chillout, lofi']
            min_acousticness = 0.5
            max_acousticness = 0.8
            min_danceability = 0.3
            max_danceability = 0.5
            min_duration_ms = 150000
            max_duration_ms = 300000
            min_energy = 0.3
            max_energy = 0.6
            min_instrumentalness = 0.2
            max_instrumentalness = 0.7
        elif weather_condition == 'fog':
            seed_genres = ['ambient, post-rock, experimental']
            min_acousticness = 0.5
            max_acousticness = 0.9
            min_danceability = 0.2
            max_danceability = 0.5
            min_duration_ms = 180000
            max_duration_ms = 400000
            min_energy = 0.2
            max_energy = 0.5
            min_instrumentalness = 0.5
            max_instrumentalness = 1.0
        elif weather_condition == 'Smoke':
            seed_genres = ['jazz, blues, soul']
            
            min_acousticness = 0.4
            max_acousticness = 0.8
            min_danceability = 0.3
            max_danceability = 0.6
            min_duration_ms = 180000
            max_duration_ms = 360000
            min_energy = 0.4
            max_energy = 0.7
            min_instrumentalness = 0.1
            max_instrumentalness = 0.5
        elif weather_condition == 'haze':
            seed_genres = ['ambient, experimental, downtempo']
            min_acousticness = 0.5
            max_acousticness = 0.8
            min_danceability = 0.3
            max_danceability = 0.6
            min_duration_ms = 150000
            max_duration_ms = 350000
            min_energy = 0.3
            max_energy = 0.6
            min_instrumentalness = 0.4
            max_instrumentalness = 0.8
        elif weather_condition in ['dust', 'sand', 'ash', 'squall']:
            seed_genres = ['world, tribal, ambient']
            min_acousticness = 0.3
            max_acousticness = 0.7
            min_danceability = 0.4
            max_danceability = 0.7
            min_duration_ms = 150000
            max_duration_ms = 300000
            min_energy = 0.4
            max_energy = 0.8
            min_instrumentalness = 0.3
            max_instrumentalness = 0.7

        
        recom = sp.recommendations(limit=20,
                                   
                                   seed_genres = seed_genres,
                                   min_acousticness = min_acousticness,
                                   max_acousticness = max_acousticness,
                                   min_danceability = min_danceability,
                                   max_danceability = max_danceability,
                                   min_duration_ms = min_duration_ms,
                                   max_duration_ms = max_duration_ms,
                                   min_energy = min_energy,
                                   max_energy = max_energy,
                                   min_instrumentalness = min_instrumentalness,
                                   max_instrumentalness = max_instrumentalness )
        pprint.pprint(recom)
        tracks = []
        for track in recom['tracks']:
            tracks.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'preview_url': track['preview_url'],
                'spotify_url': track['external_urls']['spotify']
            })

        context = {
            'weather_condition': weather_condition,
            'tracks': tracks
        }

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(context)
        else:
            return render(request, 'recommendation.html', context)
     
import os
import time

from cs50 import SQL
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from functools import wraps
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Flask application for server-side sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'spotify_'

Session(app)

# Set secret key for session management
app.secret_key = os.getenv("SECRET_KEY")

# Load Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Define required Spotify scopes for user authorization
scope = ['playlist-modify-public', 'user-library-modify', 'user-library-read', 'user-read-email', 'user-read-private', 'user-top-read']

# Initialize SpotifyOAuth object for handling OAuth authentication
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)

# Connect to SQLite database using cs50 library
db = SQL("sqlite:///music.db")

# Decorator function to enforce login requirement for specific routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("token_info") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Custom Jinja filter function to format numbers with thousand separators
def number_format(value):
    formatted_value = "{:,.0f}".format(value)
    return formatted_value.replace(",", ".")

app.jinja_env.filters['number_format'] = number_format

# Function to retrieve and refresh Spotify access token
def get_token():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    now = int(time.time())

    if token_info['expires_at'] - now < 60:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        if not token_info:
            return redirect(url_for('login'))       
        session['token_info'] = token_info

    return token_info['access_token']

# Function to save user information to database
def save_user_to_database(user_info):
    user_id = db.execute("SELECT user_id FROM users WHERE spotify_user_id = ?", user_info['id'])

    if not user_id:
        db.execute("INSERT INTO users (spotify_user_id, display_name, email, country) VALUES (?, ?, ?, ?)",
        user_info['id'],
        user_info['display_name'],
        user_info.get('email'),
        user_info.get('country'))
    else:
        db.execute("UPDATE users SET spotify_user_id = ?, display_name = ?, email = ?, country = ?",
        user_info['id'],
        user_info['display_name'],
        user_info.get('email'),
        user_info.get('country'))


# Ensure responses are not cached for secure content handling
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Route for rendering index page
@app.route("/")
def index():
    if 'token_info' in session:
        access_token = get_token()
        sp = Spotify(auth=access_token)
        user_info = sp.current_user()
        return render_template('index.html', user_info=user_info)
    else:
        return render_template('index.html')


# Route for handling user login
@app.route("/login")
def login():
    session.clear()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


# Route for OAuth callback handling
@app.route("/callback")
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    if not token_info or 'access_token' not in token_info:
        return redirect(url_for('login'))
    
    session["token_info"] = token_info
    access_token = token_info['access_token']
    sp = Spotify(auth=access_token)
    user_info = sp.current_user()
    session['user_info'] = user_info
    save_user_to_database(user_info)
    return redirect('/')


# Route for fetching and displaying new releases
@app.route("/new_releases")
@login_required
def new_releases():
    access_token = get_token()
    sp = Spotify(auth=access_token)
    releases = sp.new_releases(limit=50)
    if not releases:
        return render_template('error.html', error_message="An error occurred while fetching new releases. Please try again later.")
    
    albums = releases['albums']['items']
    return render_template('new_releases.html', albums=albums)
    

# Route for fetching and displaying user's top tracks
@app.route("/top_tracks")
@login_required
def top_tracks():
    access_token = get_token()
    time_range = request.args.get('time_range')
    if time_range:
        sp = Spotify(auth=access_token)
        top_tracks = sp.current_user_top_tracks(limit=20, time_range=time_range)
        if not top_tracks or not top_tracks['items']:
            return render_template('error.html', error_message="An error occurred while fetching top tracks. Please try again later.")
        
        return render_template('top_tracks.html', top_tracks=top_tracks['items'], time_range=time_range)
    else:
        return render_template('top_tracks.html', top_tracks=[], time_range=None)
    

# Route for fetching and displaying user's top artists
@app.route("/top_artists")
@login_required
def top_artists():
    access_token = get_token()
    time_range = request.args.get('time_range')
    if time_range:
        sp = Spotify(auth=access_token)
        top_artists = sp.current_user_top_artists(limit=20, time_range=time_range)
        if not top_artists or not top_artists['items']:
            return render_template('error.html', error_message="An error occurred while fetching top artists. Please try again later.")
        
        return render_template('top_artists.html', top_artists=top_artists['items'], time_range=time_range)
    else:
        return render_template('top_artists.html', top_artists=[], time_range=None)
    

# Route for recommending tracks based on user's top tracks
@app.route("/recommender", methods=["GET", "POST"])
@login_required
def recommender():
    access_token = get_token()
    sp = Spotify(auth=access_token)
    time_range = request.args.get('time_range') or request.form.get('time_range')
    
    if time_range and request.method == "GET":
        top_tracks = sp.current_user_top_tracks(limit=20, time_range=time_range)

        if not top_tracks or not top_tracks['items']:
            return render_template('error.html', error_message="An error occurred while fetching top tracks. Please try again later.")
        
        seed_tracks = [track['id'] for track in top_tracks['items'][:5]]
        recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=30)
        
        if not recommendations:
            return render_template('error.html', error_message="An error occurred while fetching recommended tracks. Please try again later.")
        
        recommendation_ids = [track['id'] for track in recommendations['tracks']]
        saved_tracks_info = sp.current_user_saved_tracks_contains(tracks=recommendation_ids)

        if not saved_tracks_info:
            return render_template('error.html', error_message="An error occurred while fetching recommended tracks. Please try again later.")
        
        filtered_recommendations = [track for track, is_saved in zip(recommendations['tracks'], saved_tracks_info) if not is_saved]

        session['recommendations'] = filtered_recommendations
        session['time_range'] = time_range

        return render_template('recommender.html', recommendations=filtered_recommendations, time_range=time_range)
    
    elif request.method == "POST":
        recommendations = session.get('recommendations')
        if not recommendations:
            return render_template('error.html', error_message="An error occurred while fetching recommended tracks. Please try again later.")
        
        track_uris = [track['uri'] for track in recommendations]
        user_id = session['user_info']['id']
        playlist = sp.user_playlist_create(user_id, "Discover ur Feelings", public=True, collaborative=False, 
                                           description='Enjoy your personalized playlist created just for you, based on your favorite songs!')
        if not playlist:
            return render_template('error.html', error_message="An error occurred while creating playlist. Please try again later.")
        
        sp.playlist_add_items(playlist['id'], track_uris)

        return render_template('playlist_created.html')
    
    else:
        return render_template('recommender.html', recommendations=[], time_range=None)


# Route for saving a track to user's library
@app.route("/save_track/<track_id>", methods=["POST"])
@login_required
def save_track(track_id):
    access_token = get_token()
    sp = Spotify(auth=access_token)
    sp.current_user_saved_tracks_add(tracks=[track_id])
    return '', 204


# Route for logging out user and clearing session data
@app.route("/logout")
def logout():
    session.clear()

    cache_path = ".cache"
    if os.path.exists(cache_path):
        os.remove(cache_path)

    session_dir = './flask_session/'
    for file in os.listdir(session_dir):
        os.remove(os.path.join(session_dir, file))
    
    return render_template('logout_redirect.html')
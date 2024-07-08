# Discover ur Feelings

#### Description:
Discover ur Feelings is a personalized music discovery platform that enhances your listening experience by providing tailored recommendations and insights based on your Spotify listening habits.

## Built With
- **Flask**
- **Python**
- **SQLite3**
- **HTML**
- **CSS**
- **JavaScript**
- **Spotipy Library**
- **Spotify API**

## Features
- **User Authentication**: Log in with your Spotify account using OAuth2.
- **Personalized Recommendations**: Get song recommendations based on your Spotify listening history. Recommendations are filtered to exclude songs that the user has previously liked.
- **View Top Tracks and Artists**: See your favorite tracks and artists over different time periods.
- **Discover New Releases**: Stay updated with the latest music releases.
- **Create Playlists**: Save tracks and create playlists directly from the application.
- **Responsive Design**: Enjoy a seamless experience on all devices with a responsive design powered by Bootstrap 5.
- **Error Handling**: User-friendly error pages to handle any issues gracefully.
- **Data Storage**: Securely store user information in an SQLite3 database.

## Installation
Before running the application, make sure you have Python and pip installed on your system.

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/nyctophilia96/discover-ur-feelings.git
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
This will install all necessary Python packages.

3. **Create and set up .env file:**
Create a .env file in the root directory and add the following lines:
    ```bash
    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIPY_REDIRECT_URI=your_spotify_redirect_uri
    SECRET_KEY=your_flask_secret_key
Replace your_spotify_client_id, your_spotify_client_secret, your_spotify_redirect_uri, and your_flask_secret_key with your own values obtained from Spotify Developer Dashboard and Flask application setup.

4. **Set up SQLite database:**
The application uses SQLite database to store user information. Create the database and the relevant table by running the following commands:
    ```bash
    1. sqlite3 music.db

    2. CREATE TABLE users (
           user_id INTEGER PRIMARY KEY,
           spotify_user_id TEXT NOT NULL UNIQUE,
           display_name TEXT,
           email TEXT,
           country TEXT
       );
This will create the necessary table structure (users) to store user data.

5. **Run the application:**
    ```bash
    flask run
By default, the application will be accessible at http://localhost:5000/.

## File Descriptions
### app.py
The main application file that initializes the Flask app, handles routes, and interacts with the Spotify API using the Spotipy library.

### templates/
This folder contains all HTML templates used in the application. Key files include:
- **layout.html**: The base template that includes the navigation bar and common page elements.
- **index.html**: The homepage that welcomes the user and explains the app's features.
- **top_tracks.html**: Displays the user's top tracks over different time periods.
- **top_artists.html**: Displays the user's top artists over different time periods.
- **recommender.html**: Provides song recommendations based on the user's listening history.
- **playlist_created.html**: Confirmation page for successful playlist creation.
- **new_releases.html**: Lists the latest music releases.
- **logout_redirect.html**: Handles the logout process and redirects the user.
- **error.html**: Displays error messages.

### static/
Contains static files such as stylesheet and images.
- **styles.css**: Custom CSS for styling the application.
- **bg.jpg**: Background image used in the application.
- **spotify-logo.png**: Spotify logo used in the navigation bar.
- **heart-64.png**: Heart icon used for liking tracks.
- **heart-64-after.png**: Heart icon used after liking the tracks.
- **I_heart_validator.png**: Validator image used in the application.
- **favicon.ico**: Favicon for the web application.

### music.db
SQLite3 database file that stores user information including user_id, spotify_user_id, display_name, email, and country.

### .env
Environment file containing sensitive information such as:
- `spotify_client_id`
- `spotify_client_secret`
- `spotipy_redirect_uri`
- `secret_key`
These values should be obtained from the Spotify Developer Dashboard and Flask application setup.

### .gitignore
Specifies files and directories to be ignored by Git, including `__pycache__`, `.env` and `music.db`.

### requirements.txt
A file that typically lists the Python packages required for the project to run. It allows users to install all necessary dependencies at once using 'pip install -r requirements.txt'.

## Design Choices
### User Authentication
User authentication is handled using OAuth2, allowing users to log in with their Spotify accounts. Upon successful login, the user's information is stored in an SQLite3 database.

### Data Storage
User data is stored in the `music.db` SQLite3 database. This includes user_id, spotify_user_id, display_name, email, and country.

### API Interaction
The Spotipy library is used to interact with the Spotify API. This allows the app to fetch user data, retrieve new releases, top tracks, top artists, and provide song recommendations.

### Frontend Design
Bootstrap 5 is used for responsive design, ensuring the app works well on various devices. Custom CSS is used to enhance the visual appearance and provide a unique look and feel.

### Error Handling
Errors are handled gracefully, with users being redirected to an error page (`error.html`) displaying a relevant message.

## Challenges and Solutions
One of the main challenges was handling the asynchronous nature of API calls and ensuring the app remains responsive. This was addressed by optimizing API calls and using efficient data processing techniques. 

Another challenge was designing a user-friendly interface that provides a seamless experience, which was achieved by incorporating Bootstrap and custom CSS.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Author
Kagan Saglam.

## Contact
For questions or feedback, feel free to contact me at nyctophilia11@outlook.com.
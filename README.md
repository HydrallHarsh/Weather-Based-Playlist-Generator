# Weather-Based Playlist Generator 🎵🌤️

A dynamic web application that creates personalized music playlists based on real-time weather conditions. This project combines weather data with music recommendations to enhance your listening experience by matching songs to the current weather mood.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Repository Stats
```
Primary Language: Jupyter Notebook (71.8%)
Other Languages: HTML (12.9%), Python (10.7%), CSS (4.5%), JavaScript (0.1%)
Maintained by: @HydrallHarsh
Repository ID: 889350423
```

## 🎯 Features
- Real-time weather data integration
- Dynamic playlist generation based on weather conditions
- Customizable mood-weather mappings
- User preference tracking
- Weather history logging
- Responsive web interface

## 🛠️ Tech Stack
```
# Core Technologies
Python          3.8+      # Core Programming Language
Django          4.2+      # Web Framework
Jupyter Notebook         # Data Analysis & Development
HTML/CSS/JavaScript     # Frontend Development
```

## 📋 Prerequisites
- Python 3.8 or higher
- Django 4.2 or higher
- OpenWeather API Key
- Spotify Developer Account

## 🗂️ Project Structure
```
Weather-Based-Playlist-Generator/
├── manage.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── weather_playlist/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── notebooks/
│   ├── weather_analysis.ipynb
│   └── playlist_generation.ipynb
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── responsive.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── playlist.html
│   └── weather.html
└── utils/
    ├── weather_utils.py
    └── spotify_utils.py
```

## ⚙️ Installation
```bash
# Clone the repository
git clone https://github.com/HydrallHarsh/Weather-Based-Playlist-Generator.git
cd Weather-Based-Playlist-Generator

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows

# Install required packages
pip install -r requirements.txt
```

## 🔑 Environment Variables
Create a `.env` file in the root directory:
```
DJANGO_SECRET_KEY=your_django_secret_key
WEATHER_API_KEY=your_openweather_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
DEBUG=True
```

## 🚀 Getting Started
```bash
# Apply database migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## 📦 Dependencies
```
django>=4.2.0
requests>=2.28.0
pandas>=2.0.0
spotipy>=2.22.0
python-dotenv>=1.0.0
numpy>=1.23.0
```

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Project Status
- ✅ Core Framework Setup
- ✅ Weather API Integration
- ✅ Basic Playlist Generation
- ⏳ Advanced User Preferences
- ⏳ Social Features

## 🙏 Acknowledgments
- OpenWeather API
- Spotify Web API
- Django Documentation
- Python Community

## 📞 Contact
- GitHub: [@HydrallHarsh](https://github.com/HydrallHarsh)

---

⭐ Star this repository if you find it helpful!

📧 For bug reports, feature requests, or contributions, please open an issue.

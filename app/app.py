import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

API_KEY = os.environ.get('WEATHER_API_KEY', '6b82667deb60df790deeac868820d972')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Weather Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 60px auto;
            background: #f0f4f8;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h1 { color: #2d3748; }
        input {
            padding: 10px;
            width: 70%;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background: #4299e1;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover { background: #3182ce; }
        .weather {
            margin-top: 30px;
            padding: 20px;
            background: #ebf8ff;
            border-radius: 8px;
        }
        .temp { font-size: 48px; font-weight: bold; color: #2b6cb0; }
        .desc { font-size: 20px; color: #4a5568; text-transform: capitalize; }
        .details { margin-top: 15px; color: #718096; }
        .error { color: red; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌤️ Weather Dashboard - Auto Deployed!</h1>
        <form method="POST">
            <input name="city" placeholder="Enter city name eg. Pune" value="{{ city }}"/>
            <button type="submit">Search</button>
        </form>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        {% if weather %}
        <div class="weather">
            <h2>{{ weather.city }}, {{ weather.country }}</h2>
            <div class="temp">{{ weather.temp }}°C</div>
            <div class="desc">{{ weather.description }}</div>
            <div class="details">
                <p>💧 Humidity: {{ weather.humidity }}%</p>
                <p>💨 Wind Speed: {{ weather.wind }} m/s</p>
                <p>🌡️ Feels Like: {{ weather.feels_like }}°C</p>
                <p>⬆️ Max: {{ weather.temp_max }}°C | ⬇️ Min: {{ weather.temp_min }}°C</p>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    error = None
    city = ''

    if request.method == 'POST':
        city = request.form.get('city', '')
        if city:
            try:
                response = requests.get(BASE_URL, params={
                    'q': city,
                    'appid': API_KEY,
                    'units': 'metric'
                })
                data = response.json()

                if response.status_code == 200:
                    weather = {
                        'city': data['name'],
                        'country': data['sys']['country'],
                        'temp': round(data['main']['temp']),
                        'feels_like': round(data['main']['feels_like']),
                        'temp_min': round(data['main']['temp_min']),
                        'temp_max': round(data['main']['temp_max']),
                        'humidity': data['main']['humidity'],
                        'wind': data['wind']['speed'],
                        'description': data['weather'][0]['description']
                    }
                else:
                    error = f"City '{city}' not found. Please try again."
            except Exception as e:
                error = f"Error fetching weather: {str(e)}"

    return render_template_string(HTML, weather=weather, error=error, city=city)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
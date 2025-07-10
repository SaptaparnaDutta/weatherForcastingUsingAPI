from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

API_KEY = "your api key here"  # Replace with your actual API key

@app.route('/')
def serve_index():
    return send_from_directory('static', 'indx.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required."}), 400

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        weather_data = response.json()

        if response.status_code != 200:
            return jsonify({"error": weather_data.get("message", "Unknown error")}), 400

        result = {
            "location": weather_data.get('name', 'Unknown'),
            "weather": weather_data.get('weather', [{}])[0].get('main', 'N/A'),
            "description": weather_data.get('weather', [{}])[0].get('description', 'N/A'),
            "temperature": weather_data.get('main', {}).get('temp', 'N/A'),
            "humidity": weather_data.get('main', {}).get('humidity', 'N/A'),
            "rainfall": weather_data.get('rain', {}).get('1h', 0)
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

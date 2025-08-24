import requests

def get_city_and_weather(ip, api_key):
    # Obtener ciudad por IP
    geo_url = f"http://ip-api.com/json/{ip}?fields=city,country,lat,lon,status"
    geo_resp = requests.get(geo_url, timeout=3)
    geo_data = geo_resp.json()
    if geo_data.get('status') != 'success':
        return None, None, None
    city = geo_data.get('city')
    lat = geo_data.get('lat')
    lon = geo_data.get('lon')
    # Obtener clima por lat/lon
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
    weather_resp = requests.get(weather_url, timeout=3)
    weather_data = weather_resp.json()
    if weather_data.get('cod') != 200:
        return city, None, None
    temp = weather_data['main']['temp']
    desc = weather_data['weather'][0]['description']
    return city, temp, desc

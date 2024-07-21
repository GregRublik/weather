from flask import Flask, render_template, request, jsonify, make_response, session
from db.database import select_cities_name, insert_into, get_history, del_history, new_history_user, new_user, get_user
from db.database import get_history_user, engine, fill_city
from db.models import metadata_obj
from flask_sqlalchemy import SQLAlchemy
import requests
import uuid
import json

app = Flask(__name__)
app.secret_key = '1123089745928374'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
db = SQLAlchemy(app)


@app.route('/')
def index():
    if get_user(session['user_id']) == []:
        session['user_id'] = str(uuid.uuid4())
        new_user(session['user_id'])
    print(get_user(session['user_id']))
    last_city = request.cookies.get('last_city')
    return render_template('index.html', last_city=last_city)


@app.route('/get_statistic')
def statistic():
    response = get_history()
    return jsonify(response)


@app.route('/del_statistic')
def del_statistic():
    del_history()
    response = jsonify({"info": 'история очищена'})
    response.set_data(json.dumps({"info": 'история очищена'}, ensure_ascii=False).encode('utf8'))
    return response


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '')
    response = [city for city in select_cities_name() if term.lower() in city.lower()]
    return jsonify(response)


@app.route('/get_weather', methods=['POST'])
def get_weather():
    weather_info = None
    error = None
    city = request.form['city']
    if city:
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}")
        data = response.json()
        if data.get('results'):
            latitude = data['results'][0]['latitude']
            longitude = data['results'][0]['longitude']
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()
            if 'current_weather' in weather_data:

                city_id = insert_into(city)
                try:
                    new_history_user(user := get_user(session['user_id'])[0][0], city=city_id)
                    history = get_history_user(user)[::-1]
                except Exception:
                    history = []
                weather_info = {
                    'temperature': weather_data['current_weather']['temperature'],
                    'wind_speed': weather_data['current_weather']['windspeed'],
                    'weather_code': weather_data['current_weather']['weathercode']
                }
                response = make_response(render_template('index.html', weather_info=weather_info, last_city=city, history=history))
                response.set_cookie('last_city', city)
                return response
            else:
                error = 'Не найден прогноз погоды'
        else:
            error = 'Такого города не существует'
    else:
        error = 'Не введен город'

    return render_template('index.html', weather_info=weather_info, error=error, last_city=city)


if __name__ == '__main__':

    metadata_obj.create_all(engine)
    fill_city()
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Constantes
API_KEY = "631b3d1b84c325f70b8a1ced5a35bbeb"

# Rota principal - página inicial
@app.route('/')
def home():
    return render_template('acesso-inicial.html')


@app.route('/tempo')
def tempo():
    city = request.args.get('city')
    if not city:
        # Se quiser, pode renderizar uma página com formulário para digitar a cidade
        return render_template('pagina-tempo.html', error="Parâmetro 'city' é obrigatório")

    try:
        # Obter dados atuais do clima
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&lang=pt_br&units=metric"
        )
        weather_response = requests.get(weather_url)
        if weather_response.status_code != 200:
            return render_template('pagina-tempo.html', error="Cidade não encontrada")
        weather_data = weather_response.json()

        # Obter previsão para 5 dias (intervalo de 3h)
        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={API_KEY}&units=metric&lang=pt_br"
        )
        forecast_response = requests.get(forecast_url)
        if forecast_response.status_code != 200:
            return render_template('pagina-tempo.html', error="Não foi possível obter previsão")
        forecast_data = forecast_response.json()

        # Processar dados de previsão para obter máximas e mínimas diárias
        daily = {}
        for item in forecast_data['list']:
            from datetime import datetime
            date_obj = datetime.utcfromtimestamp(item['dt'])
            day = date_obj.strftime('%a')  # Dia da semana abreviado (em inglês)
            temp = item['main']['temp']

            if day not in daily:
                daily[day] = {'max': temp, 'min': temp}
            else:
                daily[day]['max'] = max(daily[day]['max'], temp)
                daily[day]['min'] = min(daily[day]['min'], temp)

        days = list(daily.keys())[:7]
        temp_max = [daily[day]['max'] for day in days]
        temp_min = [daily[day]['min'] for day in days]

        # Montar resultado para passar ao template
        result = {
            "temperature": round(weather_data['main']['temp']),
            "description": weather_data['weather'][0]['description'].capitalize(),
            "humidity": weather_data['main']['humidity'],
            "wind_speed": round(weather_data['wind']['speed']),
            "icon": weather_data['weather'][0]['icon'],
            "main_weather": weather_data['weather'][0]['main'].lower(),
            "forecast_days": days,
            "forecast_max": temp_max,
            "forecast_min": temp_min,
            "city": city
        }

        return render_template('pagina-tempo.html', weather=result)

    except Exception as e:
        return render_template('pagina-tempo.html', error=str(e))


# Rota para conversão de moedas
@app.route('/conversao', methods=['GET', 'POST'])
def conversao():
    resultado = None
    taxa = None
    moedaDe = "USD"
    moedaPara = "BRL"
    quantia = None

    if request.method == 'POST':
        moedaDe = request.form.get('moedaDe', moedaDe)
        moedaPara = request.form.get('moedaPara', moedaPara)
        quantia_str = request.form.get('quantia', '0')
        try:
            quantia = float(quantia_str)
        except ValueError:
            quantia = 0

        # Consulta API para taxa de câmbio
        url = f'https://economia.awesomeapi.com.br/json/last/{moedaDe}-{moedaPara}'
        response = requests.get(url)
        dados = response.json()
        chave = f'{moedaDe}{moedaPara}'
        taxa = float(dados[chave]['bid'])
        resultado = quantia * taxa
        resultado = round(resultado, 2)

    return render_template(
        'pagina-conversao.html',
        resultado=resultado,
        taxa=taxa,
        moedaDe=moedaDe,
        moedaPara=moedaPara,
        quantia=quantia
    )

if __name__ == '__main__':
    app.run(debug=True)

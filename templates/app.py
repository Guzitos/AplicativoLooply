from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    taxa = None
    moedaDe = "USD"
    moedaPara = "BRL"
    quantia = None

    if request.method == 'POST':
        moedaDe = request.form['moedaDe']
        moedaPara = request.form['moedaPara']
        quantia = float(request.form['quantia'])

        url = f'https://economia.awesomeapi.com.br/json/last/{moedaDe}-{moedaPara}'
        response = requests.get(url)
        dados = response.json()
        chave = f'{moedaDe}{moedaPara}'
        taxa = float(dados[chave]['bid'])
        resultado = quantia * taxa

    return render_template('index.html',
                           resultado=resultado,
                           taxa=taxa,
                           moedaDe=moedaDe,
                           moedaPara=moedaPara,
                           quantia=quantia)

if __name__ == '__main__':
    app.run(debug=True)
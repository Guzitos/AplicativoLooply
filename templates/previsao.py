import requests,pprint



api_key = "655609400c34433cb6e143957251109"

link_api = "http://api.weatherapi.com/v1/current.json"

resposta = requests.get(link_api)

print(resposta.status_code)
print(resposta.content)

parametros = {
    'key': api_key,
    'q': 'São Paulo',
    'lang': 'pt',

}

resposta = requests.get(link_api, params = parametros)

print(resposta.status_code)
print(resposta.content)

if resposta.status_code == 200:
    dados_requisicao = resposta.json()
    pprint.pprint(dados_requisicao)
    temp = dados_requisicao['current']['temp_c']
    descricao = dados_requisicao['current']['condition']['text']
    print(temp)
    print(descricao)

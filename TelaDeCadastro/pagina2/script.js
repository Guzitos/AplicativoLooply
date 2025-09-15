let taxaAtual = 0;

function buscarTaxa() {
  const moedaDe = document.getElementById('moedaDe').value;
  const moedaPara = document.getElementById('moedaPara').value;

  // Atualiza o texto da taxa para mostrar que está carregando
  document.getElementById('exchange-rate').innerText = 'Carregando taxa...';

  fetch(`https://open.er-api.com/v6/latest/${moedaDe}`)
    .then(response => response.json())
    .then(data => {
      if (data.result === 'success') {
        taxaAtual = data.rates[moedaPara];
        if (!taxaAtual) {
          document.getElementById('exchange-rate').innerText = 'Moeda não suportada';
          taxaAtual = 0;
          return;
        }
        document.getElementById('exchange-rate').innerText = `1 ${moedaDe} = ${taxaAtual} ${moedaPara}`;
      } else {
        document.getElementById('exchange-rate').innerText = 'Erro ao carregar taxa';
        taxaAtual = 0;
      }
    })
    .catch(error => {
      console.error(error);
      document.getElementById('exchange-rate').innerText = 'Erro ao carregar taxa';
      taxaAtual = 0;
    });
}

function converter() {
  const quantia = parseFloat(document.getElementById('quantia').value);
  if (!quantia || taxaAtual === 0) {
    alert('Informe uma quantia');
    return;
  }
  const resultado = (quantia * taxaAtual).toFixed(2);
  const moedaPara = document.getElementById('moedaPara').value;
  document.getElementById('result').value = `${resultado} ${moedaPara}`;
}

// Atualizar a taxa quando mudar as moedas
document.getElementById('moedaDe').addEventListener('change', buscarTaxa);
document.getElementById('moedaPara').addEventListener('change', buscarTaxa);

// Buscar taxa inicial ao carregar a página
window.onload = buscarTaxa;
 

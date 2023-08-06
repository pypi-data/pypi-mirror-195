import yfinance as yf
from typing import Dict, List
import requests
from bs4 import BeautifulSoup


class BerryCheck():

    def converte_moeda(self, moeda: str, moeda2: str, valor_em_dolares: float):
        """
        Converte um valor de uma moeda para outra.

        Parameters:
            moeda (str): código da moeda que será convertida.
            moeda2 (str): código da moeda para qual será convertida.
            valor_em_dolares (float): valor a ser convertido em dólares.

        Returns:
            float: valor convertido para a moeda especificada, com duas casas decimais.
        """
        cotacao_dolar = BerryCheck.obtem_cotacao(moeda, moeda2)["cotacao"]
        resultado = cotacao_dolar * valor_em_dolares
        return float(f'{resultado:.2f}')


    def calcular_valor_acoes(self, empresa: str, quantidade: float, valores_acoes: Dict[str, Dict[str, float]]) -> float:
        """
        Calcula o valor total de ações de uma empresa.

        Parameters:
            empresa (str): nome da empresa para a qual será calculado o valor total das ações.
            quantidade (float): quantidade de ações da empresa.
            valores_acoes (Dict[str, Dict[str, float]]): dicionário contendo os valores das ações das empresas.

        Returns:
            float: valor total das ações da empresa.

        Raises:
            ValueError: caso não seja possível obter o valor da ação para a empresa.
        """
        valor_acao = valores_acoes.get(empresa, {}).get('valor')
        if valor_acao is None:
            raise ValueError(f"Não foi possível obter o valor da ação para a empresa {empresa}")
        return quantidade * valor_acao

    def obtem_cotacao(self, moeda: str, moeda2: str):
        """
        Obtém a cotação atual de uma moeda em relação a outra.

        Parameters:
            moeda (str): A sigla da moeda desejada.
            moeda2 (str): A sigla da moeda de referência.

        Returns:
            Um dicionário contendo as seguintes informações:
            - cotacao (float): O valor da cotação atual da moeda em relação à moeda de referência.
            - maximo (float): O valor máximo que a moeda alcançou no dia.
            - minimo (float): O valor mínimo que a moeda alcançou no dia.
            - variacao (float): A variação da cotação em relação ao valor anterior.
        """
        requisicao = requests.get(f"https://economia.awesomeapi.com.br/last/{moeda}-{moeda2}")
        requisicao_dic = requisicao.json()

        cotacao = requisicao_dic[f"{moeda}{moeda2}"]["bid"]
        maximo = requisicao_dic[f"{moeda}{moeda2}"]["high"]
        minimo = requisicao_dic[f"{moeda}{moeda2}"]["low"]
        variacao = requisicao_dic[f"{moeda}{moeda2}"]["varBid"]

        cotacao = float(cotacao)
        cotacao = round(cotacao, 2)

        return {
            "cotacao": float(cotacao),
            "maximo": float(maximo),
            "minimo": float(minimo),
            "variacao": float(variacao)
        }



    def obter_valores_acoes(self, empresas: List[str], api_key: str = "SCL4MVJ4B7C1SC3M") -> Dict[str, Dict[str, float]]:
        """
        Obtém os valores das ações de uma lista de empresas.

        Parameters:
            empresas (List[str]): A lista de siglas das empresas desejadas.
            api_key (str): A chave da API usada para acessar os valores das ações (padrão é "SCL4MVJ4B7C1SC3M").

        Returns:
            Um dicionário contendo as informações das empresas solicitadas. Cada chave é uma sigla de empresa e cada valor é
            um dicionário contendo as seguintes informações:
            - valor (float): O valor atual da ação da empresa.
        """
        resultados: Dict[str, Dict[str, float]] = {}
        for empresa in empresas:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={empresa}&apikey={api_key}"
            requisicao = requests.get(url)
            if requisicao.status_code == 200:
                requisicao_json = requisicao.json()
                valor = float(requisicao_json["Global Quote"]["05. price"])
                resultados[empresa] = {"valor": valor}
        return resultados
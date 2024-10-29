import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_excel('hoteis.xlsx')

# Define os headers da requisição
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

dados_hoteis = []

# Itera sobre cada linha do DataFrame
for index, row in df.iterrows():
    Nome = row['Nome_Hotel']  # Substitua 'Nome_Hotel' pelo nome da coluna no seu Excel
    Check_in = row['Check_in']
    Check_out = row['Check_out']
    Adultos = row['Adultos']

    target_url = f"https://www.booking.com/hotel/br/{Nome}.html?checkin={Check_in}&checkout={Check_out}&group_adults={Adultos}&group_children=0&no_rooms=1&selected_currency=BRL"
    resp = requests.get(target_url, headers=headers)

    soup = BeautifulSoup(resp.text, 'html.parser')

    try:
        Propriedade = soup.find("h2", {"class": "d2fee87262 pp-header__title"}).text
        Tarifa = soup.find("span", {"class": "prco-valign-middle-helper"}).text.strip("\n")
        Quarto = soup.find("span", {"class": "hprt-roomtype-icon-link"}).text.strip("\n")
        print("{} Tarifa:{} Tipo de Quarto: {} Check-in:{}  Checkout:{} Qtd Adultos:{}".format(Propriedade, Tarifa,
                                                                                               Quarto, Check_in,
                                                                                               Check_out, Adultos))
    except AttributeError:
        print(f"Não foi possível encontrar informações para o hotel {Nome}")

    dados_hotel = {
        'Nome': Propriedade,
        'Tarifa': Tarifa,
        'Quarto': Quarto,
        'Check_in': Check_in,
        'Check_out': Check_out,
        'Adultos': Adultos,
    }
    dados_hoteis.append(dados_hotel)

df_resultados = pd.DataFrame(dados_hoteis)
pd.set_option('display.width', None)
print(df_resultados)

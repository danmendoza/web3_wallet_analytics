import sys
import os
sys.path.append(os.path.abspath('C:/Users/danie/Documents/Repos/general/web3_wallet_analytics/'))

import requests
from datetime import datetime, timedelta
from data.bsc_chain import tokens, wallet_address, bsc_api_key

# Configuración
BSC_API_KEY = bsc_api_key  # Obtén una API key gratuita en BscScan
WALLET_ADDRESS = wallet_address  # Dirección de la cartera en BSC
BSC_BASE_URL = "https://api.bscscan.com/api"

# Diccionario con los contratos de los tokens más comunes en BSC
# Función para obtener el número de bloque en una fecha específica
def get_block_number_by_timestamp(timestamp):
    url = f"{BSC_BASE_URL}?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={BSC_API_KEY}"
    response = requests.get(url).json()
    return response.get("result")

# Función para obtener el saldo de BNB en un bloque específico
def get_bnb_balance_at_block(block_number):
    url = f"{BSC_BASE_URL}?module=account&action=balance&address={WALLET_ADDRESS}&blockno={block_number}&apikey={BSC_API_KEY}"
    response = requests.get(url).json()
    balance_wei = response.get("result", 0)
    return int(balance_wei) / 10**18  # Convertir de Wei a BNB

# Función para obtener el saldo de un token BEP-20 en un bloque específico
def get_token_balance_at_block(block_number, contract_address):
    url = f"{BSC_BASE_URL}?module=account&action=tokenbalance&contractaddress={contract_address}&address={WALLET_ADDRESS}&blockno={block_number}&apikey={BSC_API_KEY}"
    response = requests.get(url).json()
    balance_wei = response.get("result", 0)
    return int(balance_wei) / 10**18  # Convertir de Wei a la unidad estándar del token

# Obtener saldo de los últimos 30 días para cada token
def get_data(token):
    token = token.upper()
    data = []
    for i in range(30):
        date = datetime.utcnow() - timedelta(days=i)
        timestamp = int(date.timestamp())
        block_number = get_block_number_by_timestamp(timestamp)

        if block_number:
            balances = {"Fecha": date.strftime("%Y-%m-%d"), "Bloque": block_number}

            # Obtener saldo de cada token en la lista
            contract = tokens.get(token)
            if contract:
                balances[token] = get_token_balance_at_block(block_number, contract)
            else:
                # token == BNB
                balances[token] = get_bnb_balance_at_block(block_number)

            data.append(balances)
    
    return data

token_name = "XRP"

def generate_csv(token_name):

    data = get_data(token_name)
    # Crear un DataFrame con los resultados
    df = pd.DataFrame(data)
    print(df)

    # Guardar en un archivo CSV (opcional)
    df.to_csv("{}_balances_last_30_days.csv".format(token_name), index=False)

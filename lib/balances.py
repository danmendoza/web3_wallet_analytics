# ABI estándar de un token ERC-20/BEP-20 para llamar al método balanceOf
from web3 import Web3
import requests
from data.bsc_chain import tokens, wallet_address, web3, bsc_api_key
from datetime import datetime, timedelta

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]

BSC_API_KEY = bsc_api_key  # Obtén una API key gratuita en BscScan
WALLET_ADDRESS = wallet_address  # Dirección de la cartera en BSC
BSC_BASE_URL = "https://api.bscscan.com/api"

def get_token_balance(token_address=None):
    if not token_address:
        balance_wei = web3.eth.get_balance(wallet_address)
        return web3.from_wei(balance_wei, "ether")
        #return ""
    token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    balance = token_contract.functions.balanceOf(wallet_address).call()
    return web3.from_wei(balance, "ether")  # Convertir de Wei a la unidad del token

def get_balances_and_prices():
    balances = {}
    for symbol, address in tokens.items():
        balance = get_token_balance(address)
        price = get_token_price_from_binance(symbol)  # Obtener el precio usando Binance
        if price is not None:
            value_in_usdt = float(balance) * price  # Asegúrate de convertir el precio a flotante
            balances[symbol] = {
                "balance": balance,
                "price": price,
                "value_in_usdt": value_in_usdt
            }
    return balances

def get_token_price_from_binance(token_symbol):

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={token_symbol}USDC"
    try:
        response = requests.get(url)
        data = response.json()
        if "price" in data:
            return float(data["price"])  # Retorna el precio como un número flotante
        else:
            print(f"No se pudo obtener el precio para el token {token_symbol}")
            return None
    except Exception as e:
        print(f"Error al obtener el precio del token {token_symbol}: {e}")
        return None
    


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
def get_data(token, days=30):
    token = token.upper()
    data = []
    for i in range(days):
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

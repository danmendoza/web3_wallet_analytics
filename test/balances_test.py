import sys
import os
import requests


sys.path.append(os.path.abspath('C:/Users/danie/Documents/Repos/general/web3_wallet_analytics/'))

from web3 import Web3
from data.bsc_chain import web3

# Conectar a un nodo de Binance Smart Chain (BSC)
BSC_RPC_URL = "https://bsc-dataseed.binance.org/"  # Nodo público de BSC
web3_provider = Web3(Web3.HTTPProvider(BSC_RPC_URL))

# Dirección de la billetera que quieres consultar
wallet_address = "0x1DE379558E5C3B78412f9B377D89d46666aa8aA3"

# Contratos de los tokens BEP-20 en BSC
tokens = {
    "XRP": r"0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe",
    "ETH": r"0x2170ed0880ac9a755fd29b2688956bd959f933f8",
    "USDT": r"0x55d398326f99059ff775485246999027b3197955",
    "BNB": r"0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    "CAKE": r"0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
    "DOT": r"0x7083609fce4d1d8dc0c979aab8c869ea2c873402",
    "PEPE": "0x25d887Ce7a35172C62FeBFD67a1856F20FaEbB00",
}

# ABI estándar de un token ERC-20/BEP-20 para llamar al método balanceOf
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]

# Tu CoinMarketCap API key
# Función para obtener el precio de un token BEP-20 desde Binance API
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

# Obtener los balances
def get_token_balance(token_address):
    token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    balance = token_contract.functions.balanceOf(wallet_address).call()
    return web3.from_wei(balance, "ether")  # Convertir de Wei a la unidad del token

# Obtener el balance y el valor de cada token en USDT
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

# Mostrar balances y valores en USDT
balances = get_balances_and_prices()
print("Balances y valores en Binance Smart Chain (en USDT):")
for symbol, data in balances.items():
    print(f"{symbol}: {data['balance']} | Precio: {data['price']} USDT | Valor en USDT: {data['value_in_usdt']}")
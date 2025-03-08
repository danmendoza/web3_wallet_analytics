# ABI estándar de un token ERC-20/BEP-20 para llamar al método balanceOf
from web3 import Web3
import requests
from data.bsc_chain import tokens, wallet_address, web3

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]

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
        if symbol == 'BNB':
            balance = get_token_balance(None)
        else:
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
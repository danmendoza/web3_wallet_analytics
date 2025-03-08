from web3 import Web3

# Conectar a un nodo de Binance Smart Chain (BSC)
BSC_RPC_URL = "https://bsc-dataseed.binance.org/"  # Nodo público de BSC
web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
wallet_address = "0x1DE379558E5C3B78412f9B377D89d46666aa8aA3"

# Contratos de los tokens BEP-20 en BSC
tokens = {
    "XRP": "0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe",
    "ETH": "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
    "USDT": "0x55d398326f99059ff775485246999027b3197955",
    "BNB": "",
    "CAKE": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
    "DOT": "0x7083609fce4d1d8dc0c979aab8c869ea2c873402",
    "PEPE": "0x25d887Ce7a35172C62FeBFD67a1856F20FaEbB00",
}

"""
Конфигурация торговых пар для мониторинга
"""

# Полный список доступных торговых пар на Bybit SPOT (USDC)
TRADING_PAIRS = [
    "BTCUSDC",      # Bitcoin - Самая ликвидная
    "ETHUSDC",      # Ethereum
    "SOLUSDC",      # Solana
    "XRPUSDC",      # Ripple
    "ADAUSDC",      # Cardano
    "AVAXUSDC",     # Avalanche
    "DOTUSDC",      # Polkadot
    "SUIUSDC",      # Sui
    "NEARUSDC",     # NEAR Protocol
    "LINKUSDC",     # Chainlink
    "HBARUSDC",     # Hedera
    "APTUSDC",      # Aptos
    "RENDERUSDC",   # Render
    "STXUSDC",      # Stacks
    "ARBUSDC",      # Arbitrum
    "ALGOUSDC",     # Algorand
    "AAVEUSDC",     # Aave
    "EIGENUSDC",    # EigenLayer
    "ENAUSDC",      # Ethena
    "JUPUSDC",      # Jupiter
    "PYTHUSDC",     # Pyth Network
    "ORDIUSDC",     # ORDI
    "ENSUSDC",      # Ethereum Name Service
    "DYDXUSDC",     # dYdX
    "JTOUSDC",      # Jito
    "CRVUSDC",      # Curve Finance
    "ARUSDC",       # Arweave
    "MOVEUSDC",     # Movement
    "BERAUSDC",     # Berachain
    "MANAUSDC",     # Decentraland
    "SANDUSDC",     # The Sandbox
    "LTCUSDC",      # Litecoin
    "XLMUSDC",      # Stellar
    "SUSDC",        # Sonic
    "AIXBTUSDC",    # aixbt
]

# Группировка по категориям
MAJOR_PAIRS = [
    "BTCUSDC",      # Bitcoin
    "ETHUSDC",      # Ethereum
    "SOLUSDC",      # Solana
    "XRPUSDC",      # Ripple
    "ADAUSDC",      # Cardano
]

LAYER1_PAIRS = [
    "AVAXUSDC",     # Avalanche
    "DOTUSDC",      # Polkadot
    "SUIUSDC",      # Sui
    "NEARUSDC",     # NEAR Protocol
    "APTUSDC",      # Aptos
    "STXUSDC",      # Stacks
    "ALGOUSDC",     # Algorand
    "LTCUSDC",      # Litecoin
    "XLMUSDC",      # Stellar
]

LAYER2_PAIRS = [
    "ARBUSDC",      # Arbitrum
    "MOVEUSDC",     # Movement
]

DEFI_PAIRS = [
    "LINKUSDC",     # Chainlink
    "AAVEUSDC",     # Aave
    "EIGENUSDC",    # EigenLayer
    "ENAUSDC",      # Ethena
    "JUPUSDC",      # Jupiter
    "PYTHUSDC",     # Pyth Network
    "ENSUSDC",      # Ethereum Name Service
    "DYDXUSDC",     # dYdX
    "JTOUSDC",      # Jito
    "CRVUSDC",      # Curve Finance
]

GAMING_METAVERSE_PAIRS = [
    "MANAUSDC",     # Decentraland
    "SANDUSDC",     # The Sandbox
]

OTHER_PAIRS = [
    "HBARUSDC",     # Hedera
    "RENDERUSDC",   # Render
    "ORDIUSDC",     # ORDI
    "ARUSDC",       # Arweave
    "BERAUSDC",     # Berachain
    "SUSDC",        # Sonic
    "AIXBTUSDC",    # aixbt
]

# Пары, которые НЕ доступны на Bybit SPOT
UNAVAILABLE_PAIRS = [
    "USDTUSDC",     # Tether - не торгуется
    "MATICUSDC",    # Polygon - не доступна (возможно POL)
    "WUSDC",        # Wormhole - не доступна
    "PENDLEUSDC",   # Pendle - не доступна
    "GALAUSDC",     # Gala - не доступна
]

def get_all_pairs():
    """Получить все доступные пары"""
    return TRADING_PAIRS.copy()

def get_pairs_by_category(category):
    """
    Получить пары по категории

    Args:
        category: 'major', 'layer1', 'layer2', 'defi', 'gaming', 'other', 'all'
    """
    categories = {
        'major': MAJOR_PAIRS,
        'layer1': LAYER1_PAIRS,
        'layer2': LAYER2_PAIRS,
        'defi': DEFI_PAIRS,
        'gaming': GAMING_METAVERSE_PAIRS,
        'other': OTHER_PAIRS,
        'all': TRADING_PAIRS,
    }
    return categories.get(category, []).copy()

def get_pair_count():
    """Получить количество доступных пар"""
    return len(TRADING_PAIRS)

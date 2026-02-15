# Торговые пары

## ✅ Доступные пары (35)

Все пары торгуются против USDC на Bybit SPOT.

### 💎 Основные (Major) - 5 пар
| Символ | Название | Категория |
|--------|----------|-----------|
| BTCUSDC | Bitcoin | Самая ликвидная |
| ETHUSDC | Ethereum | Layer 1 |
| SOLUSDC | Solana | Layer 1 |
| XRPUSDC | Ripple | Payment |
| ADAUSDC | Cardano | Layer 1 |

### 🏗️ Layer 1 Blockchains - 9 пар
| Символ | Название |
|--------|----------|
| AVAXUSDC | Avalanche |
| DOTUSDC | Polkadot |
| SUIUSDC | Sui |
| NEARUSDC | NEAR Protocol |
| APTUSDC | Aptos |
| STXUSDC | Stacks |
| ALGOUSDC | Algorand |
| LTCUSDC | Litecoin |
| XLMUSDC | Stellar |

### ⚡ Layer 2 Solutions - 2 пары
| Символ | Название |
|--------|----------|
| ARBUSDC | Arbitrum |
| MOVEUSDC | Movement |

### 🏦 DeFi Projects - 10 пар
| Символ | Название |
|--------|----------|
| LINKUSDC | Chainlink |
| AAVEUSDC | Aave |
| EIGENUSDC | EigenLayer |
| ENAUSDC | Ethena |
| JUPUSDC | Jupiter |
| PYTHUSDC | Pyth Network |
| ENSUSDC | Ethereum Name Service |
| DYDXUSDC | dYdX |
| JTOUSDC | Jito |
| CRVUSDC | Curve Finance |

### 🎮 Gaming & Metaverse - 2 пары
| Символ | Название |
|--------|----------|
| MANAUSDC | Decentraland |
| SANDUSDC | The Sandbox |

### 🔧 Other Projects - 7 пар
| Символ | Название |
|--------|----------|
| HBARUSDC | Hedera |
| RENDERUSDC | Render |
| ORDIUSDC | ORDI |
| ARUSDC | Arweave |
| BERAUSDC | Berachain |
| SUSDC | Sonic |
| AIXBTUSDC | aixbt |

---

## ❌ Недоступные пары (5)

Эти пары не торгуются на Bybit SPOT или не поддерживаются с USDC:

| Символ | Название | Причина |
|--------|----------|---------|
| USDTUSDC | Tether | Не торгуется (стейблкоин к стейблкоину) |
| MATICUSDC | Polygon/POL | Не доступна на SPOT |
| WUSDC | Wormhole | Не доступна на SPOT |
| PENDLEUSDC | Pendle | Не доступна на SPOT |
| GALAUSDC | Gala | Не доступна на SPOT |

---

## 📊 Использование в коде

```python
from trading_pairs import (
    TRADING_PAIRS,      # Все 35 пар
    MAJOR_PAIRS,        # Только основные 5
    DEFI_PAIRS,         # Только DeFi проекты
    get_all_pairs(),    # Функция для получения всех пар
    get_pairs_by_category('major')  # Получить по категории
)

# Примеры
print(f"Всего пар: {len(TRADING_PAIRS)}")
print(f"Основные: {MAJOR_PAIRS}")
print(f"DeFi проекты: {get_pairs_by_category('defi')}")
```

## 🔥 Активность (пример за 60 секунд)

```
SOLUSDC     | 35 сделок  | 3,522 USDC  | 🔥🔥
BTCUSDC     | 34 сделки  | 15,129 USDC | 🔥🔥
ETHUSDC     | 24 сделки  | 4,869 USDC  | 🔥🔥
XRPUSDC     | 18 сделок  | 14,131 USDC | 🔥
```

**Легенда активности:**
- 🔥🔥🔥 Очень высокая (>50 сделок/мин)
- 🔥🔥 Высокая (20-50 сделок/мин)
- 🔥 Средняя (5-20 сделок/мин)
- 💤 Низкая (<5 сделок/мин)

"""
Упрощенный пример WebSocket с выводом сделок
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pybit.unified_trading import WebSocket
from config import Config
from utils.encoding import fix_windows_encoding
from datetime import datetime

fix_windows_encoding()


def trade_handler(message):
    """Обработчик сделок с красивым выводом"""
    sys.stdout.flush()  # Принудительный вывод

    if 'data' in message:
        for trade in message['data']:
            # Парсинг данных
            timestamp = datetime.fromtimestamp(int(trade['T']) / 1000).strftime('%H:%M:%S')
            symbol = trade['s']
            side = trade['S']
            price = float(trade['p'])
            qty = float(trade['v'])
            volume = price * qty

            # Форматирование
            if side == "Buy":
                marker = "🟢 ПОКУПКА "
            else:
                marker = "🔴 ПРОДАЖА "

            # Вывод
            print(f"{marker} {symbol:10} | {price:>10,.2f} USDC × {qty:>8,.6f} = {volume:>10,.2f} USDC | {timestamp}")
            sys.stdout.flush()


print("=" * 80)
print("  💹 WebSocket: Последние сделки в реальном времени")
print("=" * 80)
print(f"Режим: {'TESTNET' if Config.TESTNET else 'MAINNET'}")
print()

# Подключение - можно использовать несколько пар или все
from trading_pairs import TRADING_PAIRS, MAJOR_PAIRS

# Используем только основные пары для простого примера
symbols = MAJOR_PAIRS  # ['BTCUSDC', 'ETHUSDC', 'SOLUSDC', 'XRPUSDC', 'ADAUSDC']

# Для мониторинга всех 35 пар используйте:
# symbols = TRADING_PAIRS

print("Подписка на пары:")
for symbol in symbols:
    print(f"  • {symbol}")
print()
print("Ожидание данных... (Ctrl+C для остановки)")
print("=" * 80)
print()

sys.stdout.flush()

# WebSocket
ws = WebSocket(testnet=Config.TESTNET, channel_type="spot")

# Подписка на все пары
for symbol in symbols:
    ws.trade_stream(symbol=symbol, callback=trade_handler)

print(f"✅ Подключено к WebSocket для {len(symbols)} пар\n")
sys.stdout.flush()

# Бесконечный цикл
try:
    import time
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n⚠️ Остановлено пользователем")

"""
Пример получения последних сделок в реальном времени через WebSocket
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from websocket_client import BybitWebSocketClient
from config import Config
from utils.logger import setup_logger
from utils.encoding import fix_windows_encoding
from datetime import datetime

# Исправление кодировки для Windows
fix_windows_encoding()


def custom_trade_handler(message):
    """
    Кастомный обработчик сделок с более детальной информацией
    """
    if 'data' in message:
        for trade in message['data']:
            # Парсинг данных сделки
            timestamp = datetime.fromtimestamp(int(trade['T']) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            symbol = trade['s']
            side = trade['S']  # Buy или Sell
            price = float(trade['p'])
            qty = float(trade['v'])
            trade_id = trade['i']

            # Расчет объема в USDC
            volume_usdc = price * qty

            # Цветовая индикация для Buy/Sell
            if side == "Buy":
                side_marker = "🟢 ПОКУПКА"
                side_color = "\033[92m"  # Зеленый
            else:
                side_marker = "🔴 ПРОДАЖА"
                side_color = "\033[91m"  # Красный

            reset_color = "\033[0m"

            # Форматированный вывод
            print(f"{side_color}[{timestamp}] {side_marker} {symbol}{reset_color}")
            print(f"  Цена: {price:,.2f} USDC")
            print(f"  Количество: {qty:,.6f}")
            print(f"  Объем: {volume_usdc:,.2f} USDC")
            print(f"  Trade ID: {trade_id}")
            print("-" * 60)


def main():
    # Настройка логирования
    logger = setup_logger()

    print("=" * 60)
    print("  WebSocket: Последние сделки в реальном времени")
    print("=" * 60)
    print(f"Режим: {'TESTNET' if Config.TESTNET else 'MAINNET'}")
    print()

    # Список символов для отслеживания
    symbols = ['BTCUSDC', 'SOLUSDC', 'ETHUSDC']

    print("Отслеживаемые пары:")
    for symbol in symbols:
        print(f"  • {symbol}")
    print()
    print("Ожидание данных... (Нажмите Ctrl+C для остановки)")
    print("-" * 60)
    print()

    # Создание WebSocket клиента (для spot пар используем channel_type="spot")
    ws_client = BybitWebSocketClient(testnet=Config.TESTNET, channel_type="spot")

    # Подписка на поток сделок с кастомным обработчиком
    ws_client.subscribe_trades(symbols, callback=custom_trade_handler)

    # Запуск (блокирующий вызов)
    ws_client.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма остановлена пользователем.")
    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()

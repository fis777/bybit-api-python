"""
Расширенный пример WebSocket с несколькими типами данных
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from websocket_client import BybitWebSocketClient
from config import Config
from utils.logger import setup_logger
from utils.encoding import fix_windows_encoding
from datetime import datetime
import threading

# Исправление кодировки для Windows
fix_windows_encoding()


class MultiStreamMonitor:
    """Мониторинг нескольких потоков данных одновременно"""

    def __init__(self, symbols):
        self.symbols = symbols
        self.last_prices = {symbol: None for symbol in symbols}
        self.trade_count = {symbol: 0 for symbol in symbols}
        self.lock = threading.Lock()

    def trade_handler(self, message):
        """Обработчик сделок"""
        if 'data' in message:
            for trade in message['data']:
                symbol = trade['s']
                price = float(trade['p'])
                qty = float(trade['v'])
                side = trade['S']

                with self.lock:
                    self.last_prices[symbol] = price
                    self.trade_count[symbol] += 1

                timestamp = datetime.fromtimestamp(int(trade['T']) / 1000).strftime('%H:%M:%S')
                side_marker = "🟢" if side == "Buy" else "🔴"

                print(f"[{timestamp}] {side_marker} {symbol:12} {price:>12,.2f} USDC × {qty:>10,.6f} "
                      f"(сделок: {self.trade_count[symbol]})")

    def ticker_handler(self, message):
        """Обработчик тикеров"""
        if 'data' in message:
            data = message['data']
            symbol = data['symbol']
            price = float(data['lastPrice'])
            change_pct = float(data['price24hPcnt']) * 100
            volume = float(data['volume24h'])

            change_indicator = "📈" if change_pct > 0 else "📉"

            print(f"\n{change_indicator} {symbol} Ticker Update:")
            print(f"   Цена: {price:,.2f} USDC | Изменение 24h: {change_pct:+.2f}% | Объем: {volume:,.2f}")

    def orderbook_handler(self, message):
        """Обработчик стакана"""
        if 'data' in message:
            data = message['data']
            symbol = data['s']

            if 'a' in data and data['a'] and 'b' in data and data['b']:
                best_ask = float(data['a'][0][0])
                best_bid = float(data['b'][0][0])
                spread = best_ask - best_bid
                spread_pct = (spread / best_ask) * 100

                print(f"\n📊 {symbol} OrderBook:")
                print(f"   Bid: {best_bid:,.2f} | Ask: {best_ask:,.2f} | Спред: {spread:.2f} ({spread_pct:.4f}%)")

    def print_summary(self):
        """Вывод сводки"""
        print("\n" + "=" * 80)
        print("СВОДКА ПО ЦЕНАМ:")
        with self.lock:
            for symbol in self.symbols:
                price = self.last_prices[symbol]
                count = self.trade_count[symbol]
                if price:
                    print(f"  {symbol:12} {price:>12,.2f} USDC (сделок: {count})")
                else:
                    print(f"  {symbol:12} {'Ожидание данных...':>12}")
        print("=" * 80 + "\n")


def main():
    # Настройка логирования
    logger = setup_logger()

    print("=" * 80)
    print("  WebSocket Advanced: Многопотоковый мониторинг рынка")
    print("=" * 80)
    print(f"Режим: {'TESTNET' if Config.TESTNET else 'MAINNET'}")
    print()

    # Список символов для отслеживания
    symbols = ['BTCUSDC', 'SOLUSDC', 'ETHUSDC']

    # Создание монитора
    monitor = MultiStreamMonitor(symbols)

    print("Подписка на потоки данных:")
    print("  ✓ Сделки (publicTrade)")
    print("  ✓ Тикеры (24h статистика)")
    print("  ✓ Стакан заявок (orderbook)")
    print()
    print("Отслеживаемые пары:")
    for symbol in symbols:
        print(f"  • {symbol}")
    print()
    print("Нажмите Ctrl+C для остановки")
    print("=" * 80)
    print()

    # Создание WebSocket клиента (для spot пар используем channel_type="spot")
    ws_client = BybitWebSocketClient(testnet=Config.TESTNET, channel_type="spot")

    # Подписка на разные потоки
    ws_client.subscribe_trades(symbols, callback=monitor.trade_handler)
    ws_client.subscribe_ticker(symbols, callback=monitor.ticker_handler)
    ws_client.subscribe_orderbook(symbols, depth=1, callback=monitor.orderbook_handler)

    # Вывод сводки каждые 30 секунд
    def periodic_summary():
        import time
        while True:
            time.sleep(30)
            monitor.print_summary()

    summary_thread = threading.Thread(target=periodic_summary, daemon=True)
    summary_thread.start()

    # Запуск
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

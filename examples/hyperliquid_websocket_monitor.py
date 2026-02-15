"""
WebSocket: Мониторинг цен Hyperliquid в реальном времени
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hyperliquid_websocket import HyperliquidWebSocket
from trading_pairs import TRADING_PAIRS
from utils.encoding import fix_windows_encoding
from datetime import datetime
from collections import defaultdict
import threading

fix_windows_encoding()


class HyperliquidMonitor:
    """Мониторинг Hyperliquid цен"""

    def __init__(self, symbols):
        self.symbols = symbols
        self.last_prices = {}
        self.trade_counts = defaultdict(int)
        self.lock = threading.Lock()
        self.start_time = datetime.now()

    def all_mids_handler(self, message):
        """Обработчик всех средних цен"""
        sys.stdout.flush()

        try:
            if isinstance(message, dict) and 'mids' in message:
                mids = message['mids']
                timestamp = datetime.now().strftime('%H:%M:%S')

                with self.lock:
                    # Обновляем цены для наших символов
                    for symbol in self.symbols:
                        if symbol in mids:
                            price = float(mids[symbol])
                            old_price = self.last_prices.get(symbol)
                            self.last_prices[symbol] = price

                            # Показываем только если цена изменилась
                            if old_price is None or abs(price - old_price) > 0.0001:
                                # Определяем направление изменения
                                if old_price is not None:
                                    if price > old_price:
                                        direction = "⬆️"
                                    elif price < old_price:
                                        direction = "⬇️"
                                    else:
                                        direction = "➡️"
                                else:
                                    direction = "📊"

                                print(f"[{timestamp}] {direction} {symbol:10} | {price:>15,.4f}")
                                sys.stdout.flush()

        except Exception as e:
            print(f"Ошибка: {e}")

    def print_summary(self):
        """Сводка по ценам"""
        uptime = (datetime.now() - self.start_time).total_seconds()

        print("\n" + "=" * 80)
        print(f"{'СВОДКА ПО ЦЕНАМ HYPERLIQUID':^80}")
        print(f"{'Время работы: ' + str(int(uptime)) + ' сек':^80}")
        print("=" * 80)
        print(f"{'Символ':^12} | {'Цена':^20} | {'Статус':^15}")
        print("-" * 80)

        with self.lock:
            for symbol in sorted(self.symbols):
                price = self.last_prices.get(symbol)
                if price:
                    print(f"{symbol:^12} | {price:>20,.4f} | {'✅ Активен':^15}")
                else:
                    print(f"{symbol:^12} | {'Нет данных':^20} | {'⏳ Ожидание':^15}")

        print("=" * 80 + "\n")


def main():
    print("=" * 80)
    print(f"{'💹 Hyperliquid WebSocket: Real-time мониторинг':^80}")
    print("=" * 80)
    print()

    # Создаем список базовых символов
    base_symbols = [pair.replace("USDC", "") for pair in TRADING_PAIRS]

    # Фильтруем символы, которые есть на Hyperliquid
    # Для простоты берем самые популярные
    symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'ADA', 'AVAX', 'DOT', 'LINK',
               'NEAR', 'APT', 'ARB', 'AAVE', 'STX', 'RENDER']

    print("Отслеживаемые активы:")
    for i in range(0, len(symbols), 7):
        row = symbols[i:i+7]
        print("  " + "  ".join(f"{symbol:8}" for symbol in row))

    print()
    print("Ожидание данных... (Ctrl+C для остановки)")
    print("=" * 80)
    print()

    sys.stdout.flush()

    # Создание монитора
    monitor = HyperliquidMonitor(symbols)

    # WebSocket
    ws = HyperliquidWebSocket(testnet=False)

    # Подписка на все средние цены
    ws.subscribe_all_mids(callback=monitor.all_mids_handler)

    print("🔌 Подключение к Hyperliquid WebSocket...")
    sys.stdout.flush()

    # Запуск WebSocket
    ws.start()

    # Периодическая сводка
    def periodic_summary():
        import time
        while True:
            time.sleep(60)
            monitor.print_summary()

    summary_thread = threading.Thread(target=periodic_summary, daemon=True)
    summary_thread.start()

    # Бесконечный цикл
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Остановлено пользователем")
        print("\nФинальная сводка:")
        monitor.print_summary()


if __name__ == "__main__":
    main()

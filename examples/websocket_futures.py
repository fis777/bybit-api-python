"""
WebSocket: Мониторинг цен бессрочных фьючерсов в реальном времени
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pybit.unified_trading import WebSocket
from config import Config
from trading_pairs import TRADING_PAIRS
from utils.encoding import fix_windows_encoding
from datetime import datetime
from collections import defaultdict
import threading

fix_windows_encoding()


class FuturesMonitor:
    """Мониторинг фьючерсов"""

    def __init__(self, symbols):
        self.symbols = symbols
        self.last_prices = {}
        self.funding_rates = {}
        self.lock = threading.Lock()

    def ticker_handler(self, message):
        """Обработчик тикеров фьючерсов"""
        sys.stdout.flush()

        if 'data' in message:
            data = message['data']
            symbol = data['symbol']
            price = float(data['lastPrice'])
            funding_rate = float(data.get('fundingRate', 0)) * 100  # В процентах
            next_funding = data.get('nextFundingTime', '')

            with self.lock:
                self.last_prices[symbol] = price
                self.funding_rates[symbol] = funding_rate

            timestamp = datetime.now().strftime('%H:%M:%S')

            # Индикатор ставки финансирования
            if funding_rate > 0.05:
                funding_marker = "🔴"  # Высокая позитивная ставка
            elif funding_rate < -0.05:
                funding_marker = "🟢"  # Негативная ставка
            else:
                funding_marker = "⚪"  # Нормальная ставка

            print(f"[{timestamp}] {symbol:12} | Цена: {price:>12,.4f} | "
                  f"Funding: {funding_marker} {funding_rate:>7.4f}%")
            sys.stdout.flush()

    def print_summary(self):
        """Сводка по фьючерсам"""
        print("\n" + "=" * 90)
        print(f"{'СВОДКА ПО БЕССРОЧНЫМ ФЬЮЧЕРСАМ':^90}")
        print("=" * 90)
        print(f"{'Пара':^15} | {'Цена':^15} | {'Funding Rate':^12} | {'Статус':^20}")
        print("-" * 90)

        with self.lock:
            sorted_pairs = sorted(self.last_prices.items(), key=lambda x: x[0])

            for symbol, price in sorted_pairs:
                funding = self.funding_rates.get(symbol, 0)

                # Определяем статус по ставке финансирования
                if funding > 0.1:
                    status = "🔴 Очень дорого"
                elif funding > 0.05:
                    status = "🟠 Дорого"
                elif funding < -0.05:
                    status = "🟢 Дешево"
                elif funding < -0.1:
                    status = "🟢🟢 Очень дешево"
                else:
                    status = "⚪ Нормально"

                print(f"{symbol:^15} | {price:>15,.4f} | {funding:>12.4f}% | {status:^20}")

        print("=" * 90 + "\n")


def main():
    print("=" * 90)
    print(f"{'💹 WebSocket: Бессрочные фьючерсы в реальном времени':^90}")
    print("=" * 90)
    print(f"Режим: {'TESTNET' if Config.TESTNET else 'MAINNET'}")
    print()

    # Создаем список символов фьючерсов (USDT вместо USDC)
    futures_symbols = [pair.replace("USDC", "USDT") for pair in TRADING_PAIRS]

    print("Отслеживаемые фьючерсы:")
    for i in range(0, len(futures_symbols), 5):
        row = futures_symbols[i:i+5]
        print("  " + "  ".join(f"{symbol:12}" for symbol in row))

    print()
    print("Ожидание данных... (Ctrl+C для остановки)")
    print("=" * 90)
    print()

    sys.stdout.flush()

    # Создание монитора
    monitor = FuturesMonitor(futures_symbols)

    # WebSocket для linear (фьючерсы)
    ws = WebSocket(testnet=Config.TESTNET, channel_type="linear")

    # Подписка на тикеры
    print(f"🔌 Подключение к WebSocket для {len(futures_symbols)} фьючерсов...")
    for symbol in futures_symbols:
        ws.ticker_stream(symbol=symbol, callback=monitor.ticker_handler)

    print(f"✅ Подписка завершена для {len(futures_symbols)} фьючерсов\n")
    sys.stdout.flush()

    # Периодическая сводка
    def periodic_summary():
        import time
        while True:
            time.sleep(120)  # Каждые 2 минуты
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

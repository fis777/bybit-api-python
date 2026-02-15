"""
WebSocket: Мониторинг всех 35 торговых пар в реальном времени
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pybit.unified_trading import WebSocket
from config import Config
from trading_pairs import TRADING_PAIRS, get_pair_count
from utils.encoding import fix_windows_encoding
from datetime import datetime
from collections import defaultdict
import threading

fix_windows_encoding()


class AllPairsMonitor:
    """Мониторинг всех торговых пар"""

    def __init__(self):
        self.trade_counts = defaultdict(int)
        self.last_prices = {}
        self.total_volume = defaultdict(float)
        self.lock = threading.Lock()
        self.start_time = datetime.now()

    def trade_handler(self, message):
        """Обработчик сделок"""
        sys.stdout.flush()

        if 'data' in message:
            for trade in message['data']:
                symbol = trade['s']
                side = trade['S']
                price = float(trade['p'])
                qty = float(trade['v'])
                volume = price * qty
                timestamp = datetime.fromtimestamp(int(trade['T']) / 1000).strftime('%H:%M:%S')

                with self.lock:
                    self.trade_counts[symbol] += 1
                    self.last_prices[symbol] = price
                    self.total_volume[symbol] += volume

                # Индикация
                marker = "🟢" if side == "Buy" else "🔴"

                # Вывод сделки
                print(f"{marker} {symbol:12} | {price:>12,.4f} × {qty:>10,.6f} = {volume:>12,.2f} USDC | {timestamp}")
                sys.stdout.flush()

    def print_summary(self):
        """Вывод сводки по всем парам"""
        uptime = (datetime.now() - self.start_time).total_seconds()

        print("\n" + "=" * 100)
        print(f"{'СВОДКА ПО ВСЕМ ПАРАМ':^100}")
        print(f"{'Время работы: ' + str(int(uptime)) + ' сек':^100}")
        print("=" * 100)
        print(f"{'Пара':^15} | {'Последняя цена':^18} | {'Сделок':^10} | {'Объем (USDC)':^18} | {'Активность':^12}")
        print("-" * 100)

        with self.lock:
            # Сортировка по количеству сделок
            sorted_pairs = sorted(self.trade_counts.items(), key=lambda x: x[1], reverse=True)

            total_trades = 0
            total_vol = 0.0

            for symbol, count in sorted_pairs:
                price = self.last_prices.get(symbol, 0)
                volume = self.total_volume.get(symbol, 0)
                total_trades += count
                total_vol += volume

                # Индикатор активности
                if count > 50:
                    activity = "🔥🔥🔥"
                elif count > 20:
                    activity = "🔥🔥"
                elif count > 5:
                    activity = "🔥"
                else:
                    activity = "💤"

                print(f"{symbol:^15} | {price:>18,.4f} | {count:^10} | {volume:>18,.2f} | {activity:^12}")

            # Пары без активности
            inactive = set(TRADING_PAIRS) - set(self.trade_counts.keys())
            if inactive:
                print("-" * 100)
                print(f"{'Пары без активности: ' + str(len(inactive)):^100}")
                for symbol in sorted(inactive):
                    print(f"{symbol:^15} | {'Нет данных':^18} | {0:^10} | {0:>18,.2f} | {'💤':^12}")

        print("-" * 100)
        print(f"{'ИТОГО':^15} | {' ':^18} | {total_trades:^10} | {total_vol:>18,.2f} | {' ':^12}")
        print("=" * 100 + "\n")


def main():
    print("=" * 100)
    print(f"{'💹 WebSocket: Все торговые пары в реальном времени':^100}")
    print("=" * 100)
    print(f"Режим: {'TESTNET' if Config.TESTNET else 'MAINNET'}")
    print(f"Количество пар: {get_pair_count()}")
    print()

    print("Отслеживаемые пары:")
    # Вывод в 5 колонок
    for i in range(0, len(TRADING_PAIRS), 5):
        row = TRADING_PAIRS[i:i+5]
        print("  " + "  ".join(f"{pair:12}" for pair in row))

    print()
    print("Ожидание данных... (Ctrl+C для остановки)")
    print("=" * 100)
    print()

    sys.stdout.flush()

    # Создание монитора
    monitor = AllPairsMonitor()

    # WebSocket
    ws = WebSocket(testnet=Config.TESTNET, channel_type="spot")

    # Подписка на все пары
    print(f"🔌 Подключение к WebSocket для {len(TRADING_PAIRS)} пар...")
    for symbol in TRADING_PAIRS:
        ws.trade_stream(symbol=symbol, callback=monitor.trade_handler)

    print(f"✅ Подписка завершена для {len(TRADING_PAIRS)} пар\n")
    sys.stdout.flush()

    # Периодическая сводка каждые 60 секунд
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

"""
Арбитражный монитор: Bybit SPOT vs Hyperliquid Perpetuals в реальном времени
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pybit.unified_trading import WebSocket as BybitWebSocket
from hyperliquid_websocket import HyperliquidWebSocket
from config import Config
from utils.encoding import fix_windows_encoding
from datetime import datetime
from collections import defaultdict
import threading

fix_windows_encoding()


class ArbitrageMonitor:
    """Мониторинг арбитражных возможностей"""

    def __init__(self, symbols):
        self.symbols = symbols
        self.bybit_prices = {}
        self.hyperliquid_prices = {}
        self.spreads = {}
        self.lock = threading.Lock()
        self.alert_threshold = 1.0  # 1% спред для алерта

    def bybit_ticker_handler(self, message):
        """Обработчик Bybit тикеров"""
        try:
            if 'data' in message:
                data = message['data']
                symbol_full = data['symbol']  # BTCUSDC

                # Извлекаем базовый символ
                symbol = symbol_full.replace('USDC', '')

                if symbol in self.symbols:
                    price = float(data['lastPrice'])

                    with self.lock:
                        self.bybit_prices[symbol] = price
                        self._check_arbitrage(symbol)

        except Exception as e:
            pass

    def hyperliquid_mids_handler(self, message):
        """Обработчик Hyperliquid цен"""
        try:
            if isinstance(message, dict) and 'mids' in message:
                mids = message['mids']

                with self.lock:
                    for symbol in self.symbols:
                        if symbol in mids:
                            price = float(mids[symbol])
                            self.hyperliquid_prices[symbol] = price
                            self._check_arbitrage(symbol)

        except Exception as e:
            pass

    def _check_arbitrage(self, symbol):
        """Проверка арбитражной возможности"""
        bybit_price = self.bybit_prices.get(symbol)
        hl_price = self.hyperliquid_prices.get(symbol)

        if bybit_price and hl_price:
            spread = hl_price - bybit_price
            spread_percent = (spread / bybit_price) * 100

            self.spreads[symbol] = {
                'bybit': bybit_price,
                'hyperliquid': hl_price,
                'spread': spread,
                'spread_percent': spread_percent,
                'timestamp': datetime.now()
            }

            # Алерт при большом спреде
            if abs(spread_percent) >= self.alert_threshold:
                timestamp = datetime.now().strftime('%H:%M:%S')

                if spread > 0:
                    direction = "🚀 АРБИТРАЖ"
                    action = f"Купить на Bybit ({bybit_price:.4f}), продать на HL ({hl_price:.4f})"
                else:
                    direction = "🚀 АРБИТРАЖ"
                    action = f"Купить на HL ({hl_price:.4f}), продать на Bybit ({bybit_price:.4f})"

                print(f"\n{'='*90}")
                print(f"{direction} {symbol} | Спред: {abs(spread_percent):.3f}%")
                print(f"[{timestamp}] {action}")
                print(f"Потенциальная прибыль на $1000: ${abs(spread_percent) * 10:.2f}")
                print(f"{'='*90}\n")
                sys.stdout.flush()

    def print_summary(self):
        """Сводка по всем парам"""
        print("\n" + "=" * 100)
        print(f"{'АРБИТРАЖНАЯ СВОДКА':^100}")
        print("=" * 100)
        print(f"{'Символ':^10} | {'Bybit Spot':^15} | {'HL Perp':^15} | {'Спред':^12} | {'Спред %':^12} | {'Возможность':^18}")
        print("-" * 100)

        with self.lock:
            # Сортируем по абсолютному спреду
            sorted_spreads = sorted(
                self.spreads.items(),
                key=lambda x: abs(x[1]['spread_percent']),
                reverse=True
            )

            for symbol, data in sorted_spreads:
                bybit = data['bybit']
                hl = data['hyperliquid']
                spread = data['spread']
                spread_pct = data['spread_percent']

                if abs(spread_pct) >= 1.0:
                    marker = "🔥 ВЫСОКИЙ"
                elif abs(spread_pct) >= 0.5:
                    marker = "⚠️ СРЕДНИЙ"
                else:
                    marker = "✅ НИЗКИЙ"

                print(f"{symbol:^10} | {bybit:>15,.4f} | {hl:>15,.4f} | "
                      f"{spread:>12,.4f} | {spread_pct:>11,.3f}% | {marker:^18}")

        print("=" * 100 + "\n")


def main():
    print("=" * 100)
    print(f"{'🎯 АРБИТРАЖНЫЙ МОНИТОР: Bybit SPOT vs Hyperliquid Perpetuals':^100}")
    print("=" * 100)
    print()

    # Символы для мониторинга
    symbols = ['BTC', 'ETH', 'SOL', 'XRP', 'AVAX', 'NEAR', 'ARB', 'APT']

    print("Отслеживаемые пары:")
    for symbol in symbols:
        print(f"  • {symbol}")

    print()
    print(f"⚠️  Алерт при спреде >= 1.0%")
    print()
    print("Ожидание данных... (Ctrl+C для остановки)")
    print("=" * 100)
    print()

    sys.stdout.flush()

    # Создание монитора
    monitor = ArbitrageMonitor(symbols)

    # Bybit WebSocket
    bybit_ws = BybitWebSocket(testnet=Config.TESTNET, channel_type="spot")

    # Подписка на Bybit тикеры
    for symbol in symbols:
        bybit_symbol = f"{symbol}USDC"
        bybit_ws.ticker_stream(symbol=bybit_symbol, callback=monitor.bybit_ticker_handler)

    print("✅ Подключено к Bybit WebSocket")

    # Hyperliquid WebSocket
    hl_ws = HyperliquidWebSocket(testnet=False)
    hl_ws.subscribe_all_mids(callback=monitor.hyperliquid_mids_handler)
    hl_ws.start()

    print("✅ Подключено к Hyperliquid WebSocket")
    print()

    # Периодическая сводка каждые 2 минуты
    def periodic_summary():
        import time
        while True:
            time.sleep(120)
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

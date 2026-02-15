"""
Сравнение цен spot (USDC) и бессрочных фьючерсов (USDT) для всех пар
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bybit_client import BybitClient
from trading_pairs import TRADING_PAIRS
from utils.encoding import fix_windows_encoding
from datetime import datetime

fix_windows_encoding()


def main():
    client = BybitClient(api_key="", api_secret="")

    print("=" * 100)
    print(f"{'СРАВНЕНИЕ ЦЕН SPOT И БЕССРОЧНЫХ ФЬЮЧЕРСОВ':^100}")
    print(f"{'Время: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^100}")
    print("=" * 100)
    print()
    print(f"{'Пара':^12} | {'Spot (USDC)':^15} | {'Futures (USDT)':^15} | {'Спред':^12} | {'Спред %':^10} | {'Направление':^12}")
    print("-" * 100)

    results = []

    for pair in TRADING_PAIRS:
        # Получаем базовый символ (убираем USDC)
        base_symbol = pair.replace("USDC", "")

        try:
            data = client.get_spot_and_futures_price(base_symbol)

            spot_price = data['spot']['price']
            futures_price = data['futures']['price']
            spread = data['spread']
            spread_percent = data['spread_percent']

            if spot_price and futures_price:
                # Определяем направление
                if spread > 0:
                    direction = "🔺 Contango"  # Фьючерс дороже спота
                elif spread < 0:
                    direction = "🔻 Backw."    # Фьючерс дешевле спота
                else:
                    direction = "➖ Равно"

                # Цветовая индикация по величине спреда
                if abs(spread_percent) > 1.0:
                    spread_marker = "🔥"
                elif abs(spread_percent) > 0.5:
                    spread_marker = "⚠️"
                else:
                    spread_marker = "✅"

                print(f"{base_symbol:^12} | {spot_price:>15,.4f} | {futures_price:>15,.4f} | "
                      f"{spread:>12,.4f} | {spread_marker} {spread_percent:>6.3f}% | {direction:^12}")

                results.append({
                    'symbol': base_symbol,
                    'spread_percent': abs(spread_percent),
                    'spread': spread,
                    'spot': spot_price,
                    'futures': futures_price
                })
            else:
                print(f"{base_symbol:^12} | {'N/A':^15} | {'N/A':^15} | {'N/A':^12} | {'N/A':^10} | {'N/A':^12}")

        except Exception as e:
            print(f"{base_symbol:^12} | {'ERROR':^15} | {'ERROR':^15} | {'ERROR':^12} | {'ERROR':^10} | {str(e)[:12]:^12}")

    print("-" * 100)
    print()

    # Топ пар по величине спреда
    if results:
        print("=" * 100)
        print(f"{'ТОП-10 ПАР ПО ВЕЛИЧИНЕ СПРЕДА':^100}")
        print("=" * 100)
        print(f"{'#':^5} | {'Пара':^12} | {'Спред %':^12} | {'Спред (USDT)':^15} | {'Spot':^15} | {'Futures':^15}")
        print("-" * 100)

        # Сортируем по абсолютному значению спреда
        sorted_results = sorted(results, key=lambda x: x['spread_percent'], reverse=True)

        for i, item in enumerate(sorted_results[:10], 1):
            print(f"{i:^5} | {item['symbol']:^12} | {item['spread_percent']:>12.3f}% | "
                  f"{item['spread']:>15,.4f} | {item['spot']:>15,.4f} | {item['futures']:>15,.4f}")

        print("=" * 100)

    print()
    print("Легенда:")
    print("  🔺 Contango - фьючерс дороже спота (нормально для криптовалют)")
    print("  🔻 Backwardation - фьючерс дешевле спота (редко)")
    print("  🔥 Спред > 1% - очень большой спред")
    print("  ⚠️  Спред 0.5-1% - заметный спред")
    print("  ✅ Спред < 0.5% - нормальный спред")
    print()


if __name__ == "__main__":
    main()

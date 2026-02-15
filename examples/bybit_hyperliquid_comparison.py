"""
Сравнение цен Bybit SPOT (USDC) с Hyperliquid Perpetual Futures
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bybit_client import BybitClient
from hyperliquid_client import HyperliquidClient
from trading_pairs import TRADING_PAIRS
from utils.encoding import fix_windows_encoding
from datetime import datetime

fix_windows_encoding()


def main():
    # Инициализация клиентов
    bybit = BybitClient(api_key="", api_secret="")
    hyperliquid = HyperliquidClient(testnet=False)

    print("=" * 110)
    print(f"{'СРАВНЕНИЕ: BYBIT SPOT vs HYPERLIQUID PERPETUAL FUTURES':^110}")
    print(f"{'Время: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^110}")
    print("=" * 110)
    print()

    # Получаем список доступных символов на Hyperliquid
    print("Получение списка активов на Hyperliquid...")
    hl_symbols = hyperliquid.get_available_symbols()
    print(f"Доступно активов на Hyperliquid: {len(hl_symbols)}")
    print()

    # Создаем список базовых символов из trading_pairs
    base_symbols = [pair.replace("USDC", "") for pair in TRADING_PAIRS]

    # Фильтруем только те символы, которые есть на обеих биржах
    common_symbols = [s for s in base_symbols if s in hl_symbols]

    print(f"Общих символов для сравнения: {len(common_symbols)}")
    print()

    print(f"{'Пара':^12} | {'Bybit Spot':^18} | {'Hyperliquid Perp':^18} | {'Спред':^15} | {'Спред %':^12} | {'Направление':^15}")
    print("-" * 110)

    results = []

    for symbol in common_symbols:
        try:
            # Bybit spot цена
            bybit_symbol = f"{symbol}USDC"
            bybit_data = bybit.get_tickers(category="spot", symbol=bybit_symbol)
            bybit_price = None

            if bybit_data['retCode'] == 0 and bybit_data['result']['list']:
                bybit_price = float(bybit_data['result']['list'][0]['lastPrice'])

            # Hyperliquid futures цена
            hl_ticker = hyperliquid.get_ticker(symbol)
            hl_price = hl_ticker.get('price')

            if bybit_price and hl_price:
                # Расчет спреда
                spread = hl_price - bybit_price
                spread_percent = (spread / bybit_price) * 100

                # Определяем направление
                if spread > 0:
                    direction = "🔺 HL дороже"  # Hyperliquid дороже
                elif spread < 0:
                    direction = "🔻 HL дешевле"  # Hyperliquid дешевле
                else:
                    direction = "➖ Равно"

                # Индикация по величине спреда
                if abs(spread_percent) > 1.0:
                    spread_marker = "🔥"
                elif abs(spread_percent) > 0.5:
                    spread_marker = "⚠️"
                else:
                    spread_marker = "✅"

                print(f"{symbol:^12} | {bybit_price:>18,.4f} | {hl_price:>18,.4f} | "
                      f"{spread:>15,.4f} | {spread_marker} {spread_percent:>7.3f}% | {direction:^15}")

                results.append({
                    'symbol': symbol,
                    'bybit': bybit_price,
                    'hyperliquid': hl_price,
                    'spread': spread,
                    'spread_percent': abs(spread_percent)
                })
            else:
                print(f"{symbol:^12} | {'N/A':^18} | {'N/A':^18} | {'N/A':^15} | {'N/A':^12} | {'N/A':^15}")

        except Exception as e:
            print(f"{symbol:^12} | {'ERROR':^18} | {'ERROR':^18} | {'ERROR':^15} | {'ERROR':^12} | {str(e)[:15]:^15}")

    print("-" * 110)
    print()

    # Топ пар по величине спреда
    if results:
        print("=" * 110)
        print(f"{'ТОП-10 ПАР ПО ВЕЛИЧИНЕ СПРЕДА':^110}")
        print("=" * 110)
        print(f"{'#':^5} | {'Пара':^12} | {'Спред %':^15} | {'Спред':^18} | {'Bybit Spot':^18} | {'HL Futures':^18}")
        print("-" * 110)

        sorted_results = sorted(results, key=lambda x: x['spread_percent'], reverse=True)

        for i, item in enumerate(sorted_results[:10], 1):
            print(f"{i:^5} | {item['symbol']:^12} | {item['spread_percent']:>15.3f}% | "
                  f"{item['spread']:>18,.4f} | {item['bybit']:>18,.4f} | {item['hyperliquid']:>18,.4f}")

        print("=" * 110)
        print()

        # Статистика
        avg_spread = sum(r['spread_percent'] for r in results) / len(results)
        max_spread = max(r['spread_percent'] for r in results)
        min_spread = min(r['spread_percent'] for r in results)

        print(f"Статистика спредов:")
        print(f"  Средний спред: {avg_spread:.3f}%")
        print(f"  Максимальный:  {max_spread:.3f}%")
        print(f"  Минимальный:   {min_spread:.3f}%")

    print()
    print("Легенда:")
    print("  🔺 HL дороже - Hyperliquid futures дороже Bybit spot")
    print("  🔻 HL дешевле - Hyperliquid futures дешевле Bybit spot")
    print("  🔥 Спред > 1% - очень большой спред (арбитраж?)")
    print("  ⚠️  Спред 0.5-1% - заметный спред")
    print("  ✅ Спред < 0.5% - нормальный спред")
    print()
    print(f"Проанализировано {len(results)} пар")
    print()


if __name__ == "__main__":
    main()

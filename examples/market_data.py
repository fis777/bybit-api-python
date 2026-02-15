"""
Примеры получения рыночных данных через Bybit API
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bybit_client import BybitClient
from utils.logger import setup_logger
from utils.encoding import fix_windows_encoding
import json

# Исправление кодировки для Windows
fix_windows_encoding()


def main():
    # Настройка логирования
    logger = setup_logger()

    # Создание клиента (без API ключей для публичных данных)
    client = BybitClient(api_key="", api_secret="")

    print("=== Примеры получения рыночных данных Bybit ===\n")

    # 1. Время сервера
    print("1. Время сервера:")
    server_time = client.get_server_time()
    print(json.dumps(server_time, indent=2))
    print()

    # 2. Тикер BTC/USDT
    print("2. Тикер BTC/USDT (spot):")
    ticker = client.get_tickers(category="spot", symbol="BTCUSDT")
    if ticker['retCode'] == 0:
        data = ticker['result']['list'][0]
        print(f"  Цена: {data['lastPrice']}")
        print(f"  24h High: {data['highPrice24h']}")
        print(f"  24h Low: {data['lowPrice24h']}")
        print(f"  24h Volume: {data['volume24h']}")
    print()

    # 3. Свечи (kline)
    print("3. Последние 5 свечей BTC/USDT (1 час):")
    klines = client.get_kline(
        category="spot",
        symbol="BTCUSDT",
        interval="60",  # 1 час
        limit=5
    )
    if klines['retCode'] == 0:
        for candle in klines['result']['list'][:5]:
            timestamp, open_p, high, low, close, volume, _ = candle
            print(f"  Time: {timestamp} | O: {open_p} | H: {high} | L: {low} | C: {close} | V: {volume}")
    print()

    # 4. Стакан заявок
    print("4. Стакан заявок BTC/USDT (топ 5):")
    orderbook = client.get_orderbook(category="spot", symbol="BTCUSDT", limit=5)
    if orderbook['retCode'] == 0:
        print("  Asks (продажа):")
        for ask in orderbook['result']['a'][:5]:
            print(f"    {ask[0]} - {ask[1]}")
        print("  Bids (покупка):")
        for bid in orderbook['result']['b'][:5]:
            print(f"    {bid[0]} - {bid[1]}")
    print()


if __name__ == "__main__":
    main()

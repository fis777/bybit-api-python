"""
Примеры торговых операций через Bybit API
ВНИМАНИЕ: Эти примеры для демонстрации. Используйте testnet для тестирования!
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bybit_client import BybitClient
from config import Config
from utils.logger import setup_logger
from utils.encoding import fix_windows_encoding
import json

# Исправление кодировки для Windows
fix_windows_encoding()


def main():
    # Настройка логирования
    logger = setup_logger()

    # Проверка наличия API ключей
    try:
        Config.validate()
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    # Создание клиента с API ключами
    client = BybitClient()

    print("=== Примеры торговых операций Bybit ===")
    print(f"Режим: {'TESTNET' if Config.TESTNET else 'MAINNET'}")
    print()

    # 1. Проверка баланса
    print("1. Баланс кошелька:")
    try:
        balance = client.get_wallet_balance(accountType="UNIFIED")
        if balance['retCode'] == 0:
            coins = balance['result']['list'][0]['coin']
            for coin in coins[:5]:  # Показываем первые 5
                if float(coin['walletBalance']) > 0:
                    print(f"  {coin['coin']}: {coin['walletBalance']}")
    except Exception as e:
        print(f"  Ошибка: {e}")
    print()

    # 2. Пример размещения лимитного ордера (закомментирован для безопасности)
    print("2. Размещение ордера (пример закомментирован):")
    print("""
    # ВНИМАНИЕ: Раскомментируйте только если понимаете, что делаете!
    # order = client.place_order(
    #     category="spot",
    #     symbol="BTCUSDT",
    #     side="Buy",
    #     orderType="Limit",
    #     qty="0.001",
    #     price="30000",  # Укажите актуальную цену
    #     timeInForce="GTC"
    # )
    # print(json.dumps(order, indent=2))
    """)
    print()

    # 3. Получение открытых ордеров
    print("3. Открытые ордера:")
    try:
        open_orders = client.get_open_orders(category="spot", symbol="BTCUSDT")
        if open_orders['retCode'] == 0:
            orders = open_orders['result']['list']
            if orders:
                for order in orders:
                    print(f"  ID: {order['orderId']} | {order['side']} {order['qty']} @ {order['price']}")
            else:
                print("  Нет открытых ордеров")
    except Exception as e:
        print(f"  Ошибка: {e}")
    print()

    # 4. Отмена ордера (пример)
    print("4. Отмена ордера (пример закомментирован):")
    print("""
    # cancel = client.cancel_order(
    #     category="spot",
    #     symbol="BTCUSDT",
    #     orderId="your_order_id_here"
    # )
    # print(json.dumps(cancel, indent=2))
    """)
    print()


if __name__ == "__main__":
    main()

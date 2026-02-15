"""
WebSocket клиент для Hyperliquid
"""
from hyperliquid.websocket_manager import WebsocketManager
from hyperliquid.utils import constants
import logging
import time
from datetime import datetime
from collections import defaultdict
import threading


class HyperliquidWebSocket:
    """Класс для работы с Hyperliquid WebSocket"""

    def __init__(self, testnet=False):
        """
        Инициализация WebSocket клиента

        Args:
            testnet: Использовать testnet (по умолчанию False)
        """
        self.testnet = testnet
        self.subscriptions = {}
        self.callbacks = {}
        self.ws_manager = None

        # Выбор базового URL
        if testnet:
            base_url = constants.TESTNET_API_URL
        else:
            base_url = constants.MAINNET_API_URL

        self.base_url = base_url
        logging.info(f"Hyperliquid WebSocket инициализирован ({'testnet' if testnet else 'mainnet'})")

    def subscribe_trades(self, symbols, callback=None):
        """
        Подписка на поток сделок

        Args:
            symbols: Список символов (например, ['BTC', 'ETH'])
            callback: Функция обработки данных
        """
        if callback is None:
            callback = self._default_trade_handler

        for symbol in symbols:
            subscription = {"type": "trades", "coin": symbol}
            self.subscriptions[symbol] = subscription
            self.callbacks[symbol] = callback

        logging.info(f"Подписка на trades для {len(symbols)} символов")

    def subscribe_orderbook(self, symbols, callback=None):
        """
        Подписка на поток обновлений стакана

        Args:
            symbols: Список символов
            callback: Функция обработки данных
        """
        if callback is None:
            callback = self._default_orderbook_handler

        for symbol in symbols:
            subscription = {"type": "l2Book", "coin": symbol}
            self.subscriptions[symbol] = subscription
            self.callbacks[symbol] = callback

        logging.info(f"Подписка на orderbook для {len(symbols)} символов")

    def subscribe_all_mids(self, callback=None):
        """
        Подписка на все средние цены (all mids)

        Args:
            callback: Функция обработки данных
        """
        if callback is None:
            callback = self._default_all_mids_handler

        subscription = {"type": "allMids"}
        self.subscriptions["all_mids"] = subscription
        self.callbacks["all_mids"] = callback

        logging.info("Подписка на all mids")

    def _default_trade_handler(self, message):
        """Стандартный обработчик сделок"""
        try:
            if isinstance(message, list):
                for trade in message:
                    if isinstance(trade, dict) and 'coin' in trade:
                        symbol = trade['coin']
                        side = trade.get('side', 'unknown')
                        price = float(trade.get('px', 0))
                        size = float(trade.get('sz', 0))
                        time_ms = trade.get('time', 0)

                        timestamp = datetime.fromtimestamp(time_ms / 1000).strftime('%H:%M:%S')

                        side_marker = "🟢" if side == "B" else "🔴"

                        print(f"[{timestamp}] {side_marker} {symbol:8} | {price:>12,.4f} × {size:>10,.6f}")
        except Exception as e:
            logging.error(f"Ошибка обработки trade: {e}")

    def _default_orderbook_handler(self, message):
        """Стандартный обработчик стакана"""
        try:
            if isinstance(message, dict) and 'coin' in message:
                symbol = message['coin']

                print(f"\n=== OrderBook: {symbol} ===")

                # Asks
                if 'levels' in message and message['levels']:
                    asks = [l for l in message['levels'] if l.get('n') > 0][:5]
                    if asks:
                        print("Asks:")
                        for ask in asks:
                            print(f"  {ask['px']} - {ask['sz']}")

                # Bids
                if 'levels' in message:
                    bids = [l for l in message['levels'] if l.get('n') < 0][:5]
                    if bids:
                        print("Bids:")
                        for bid in bids:
                            print(f"  {bid['px']} - {bid['sz']}")

                print()
        except Exception as e:
            logging.error(f"Ошибка обработки orderbook: {e}")

    def _default_all_mids_handler(self, message):
        """Стандартный обработчик all mids"""
        try:
            if isinstance(message, dict) and 'mids' in message:
                mids = message['mids']
                timestamp = datetime.now().strftime('%H:%M:%S')

                # Показываем только топ-10 по алфавиту
                items = list(mids.items())[:10]

                print(f"\n=== All Mids Update [{timestamp}] ===")
                for symbol, price in items:
                    print(f"{symbol:8} {float(price):>12,.4f}")
                print()
        except Exception as e:
            logging.error(f"Ошибка обработки all mids: {e}")

    def start(self):
        """Запуск WebSocket соединения"""
        try:
            # Создаем WebSocket manager
            self.ws_manager = WebsocketManager(base_url=self.base_url)

            # Подписываемся на все добавленные подписки
            for key, subscription in self.subscriptions.items():
                callback = self.callbacks.get(key, self._default_trade_handler)

                # Подписываемся
                self.ws_manager.subscribe(subscription, callback)

            logging.info("WebSocket соединения установлены")
            print("✅ WebSocket подключен к Hyperliquid")
            print()

        except Exception as e:
            logging.error(f"Ошибка запуска WebSocket: {e}")
            raise

    def run(self):
        """Запуск и поддержание соединения"""
        self.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Остановка WebSocket...")
            self.stop()

    def stop(self):
        """Остановка WebSocket соединения"""
        try:
            if self.ws_manager:
                # WebsocketManager автоматически закрывается при выходе
                pass
            logging.info("WebSocket соединение закрыто")
        except Exception as e:
            logging.error(f"Ошибка при закрытии WebSocket: {e}")

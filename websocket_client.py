"""
WebSocket клиент для получения данных в реальном времени от Bybit
"""
from pybit.unified_trading import WebSocket
from config import Config
import logging
import time
from datetime import datetime


class BybitWebSocketClient:
    """Класс для работы с WebSocket потоками Bybit"""

    def __init__(self, testnet=None, channel_type="spot"):
        """
        Инициализация WebSocket клиента

        Args:
            testnet: Использовать testnet (если None, берется из config)
            channel_type: Тип канала - "spot", "linear", "inverse", "option", "private"
        """
        self.testnet = testnet if testnet is not None else Config.TESTNET
        self.channel_type = channel_type
        self.callbacks = {}

        # Для приватных каналов нужны ключи
        if channel_type == "private":
            self.ws = WebSocket(
                testnet=self.testnet,
                channel_type=channel_type,
                api_key=Config.API_KEY,
                api_secret=Config.API_SECRET
            )
        else:
            self.ws = WebSocket(
                testnet=self.testnet,
                channel_type=channel_type
            )

        logging.info(f"WebSocket клиент инициализирован (testnet={self.testnet}, channel={channel_type})")

    def subscribe_trades(self, symbols, callback=None):
        """
        Подписка на поток последних сделок

        Args:
            symbols: Список символов (например, ['BTCUSDC', 'ETHUSDC'])
            callback: Функция обработки данных
        """
        if callback is None:
            callback = self._default_trade_handler

        for symbol in symbols:
            topic = f"publicTrade.{symbol}"
            self.ws.trade_stream(
                symbol=symbol,
                callback=callback
            )
            self.callbacks[topic] = callback
            logging.info(f"Подписка на trades для {symbol}")

    def subscribe_orderbook(self, symbols, depth=1, callback=None):
        """
        Подписка на поток изменений стакана заявок

        Args:
            symbols: Список символов
            depth: Глубина стакана (1, 50, 200, 500)
            callback: Функция обработки данных
        """
        if callback is None:
            callback = self._default_orderbook_handler

        for symbol in symbols:
            topic = f"orderbook.{depth}.{symbol}"
            self.ws.orderbook_stream(
                depth=depth,
                symbol=symbol,
                callback=callback
            )
            self.callbacks[topic] = callback
            logging.info(f"Подписка на orderbook (depth={depth}) для {symbol}")

    def subscribe_kline(self, symbols, interval="1", callback=None):
        """
        Подписка на поток свечей

        Args:
            symbols: Список символов
            interval: Интервал свечей (1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, W, M)
            callback: Функция обработки данных
        """
        if callback is None:
            callback = self._default_kline_handler

        for symbol in symbols:
            topic = f"kline.{interval}.{symbol}"
            self.ws.kline_stream(
                interval=interval,
                symbol=symbol,
                callback=callback
            )
            self.callbacks[topic] = callback
            logging.info(f"Подписка на kline (interval={interval}) для {symbol}")

    def subscribe_ticker(self, symbols, callback=None):
        """
        Подписка на поток тикеров (24h статистика)

        Args:
            symbols: Список символов
            callback: Функция обработки данных
        """
        if callback is None:
            callback = self._default_ticker_handler

        for symbol in symbols:
            topic = f"tickers.{symbol}"
            self.ws.ticker_stream(
                symbol=symbol,
                callback=callback
            )
            self.callbacks[topic] = callback
            logging.info(f"Подписка на ticker для {symbol}")

    # === Default Handlers ===

    def _default_trade_handler(self, message):
        """Стандартный обработчик сделок"""
        try:
            if 'data' in message:
                for trade in message['data']:
                    timestamp = datetime.fromtimestamp(int(trade['T']) / 1000).strftime('%H:%M:%S.%f')[:-3]
                    symbol = trade['s']
                    side = trade['S']  # Buy или Sell
                    price = trade['p']
                    qty = trade['v']

                    # Цветовая индикация для Buy/Sell
                    side_marker = "🟢" if side == "Buy" else "🔴"

                    print(f"[{timestamp}] {side_marker} {symbol}: {price} × {qty} ({side})")
        except Exception as e:
            logging.error(f"Ошибка обработки trade: {e}")

    def _default_orderbook_handler(self, message):
        """Стандартный обработчик стакана заявок"""
        try:
            if 'data' in message:
                data = message['data']
                symbol = data['s']

                print(f"\n=== OrderBook: {symbol} ===")

                # Asks (продажа)
                if 'a' in data and data['a']:
                    print("Asks (продажа):")
                    for ask in data['a'][:5]:
                        print(f"  {ask[0]} - {ask[1]}")

                # Bids (покупка)
                if 'b' in data and data['b']:
                    print("Bids (покупка):")
                    for bid in data['b'][:5]:
                        print(f"  {bid[0]} - {bid[1]}")
                print()
        except Exception as e:
            logging.error(f"Ошибка обработки orderbook: {e}")

    def _default_kline_handler(self, message):
        """Стандартный обработчик свечей"""
        try:
            if 'data' in message:
                for kline in message['data']:
                    timestamp = datetime.fromtimestamp(int(kline['start']) / 1000).strftime('%H:%M:%S')
                    symbol = kline['symbol']

                    print(f"[{timestamp}] {symbol} - O: {kline['open']} H: {kline['high']} "
                          f"L: {kline['low']} C: {kline['close']} V: {kline['volume']}")
        except Exception as e:
            logging.error(f"Ошибка обработки kline: {e}")

    def _default_ticker_handler(self, message):
        """Стандартный обработчик тикеров"""
        try:
            if 'data' in message:
                data = message['data']
                symbol = data['symbol']

                print(f"\n=== Ticker: {symbol} ===")
                print(f"Цена: {data['lastPrice']}")
                print(f"24h High: {data['highPrice24h']}")
                print(f"24h Low: {data['lowPrice24h']}")
                print(f"24h Volume: {data['volume24h']}")
                print(f"24h Change: {data['price24hPcnt']}")
                print()
        except Exception as e:
            logging.error(f"Ошибка обработки ticker: {e}")

    def run(self):
        """Запуск WebSocket соединения (блокирующий вызов)"""
        logging.info("WebSocket соединение запущено. Нажмите Ctrl+C для остановки.")
        print("\n✅ WebSocket подключен. Ожидание данных...\n")
        try:
            # Бесконечный цикл для поддержания соединения
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Остановка WebSocket соединения...")
            self.stop()

    def stop(self):
        """Остановка WebSocket соединения"""
        try:
            if hasattr(self.ws, 'exit'):
                self.ws.exit()
            logging.info("WebSocket соединение закрыто")
        except Exception as e:
            logging.error(f"Ошибка при закрытии WebSocket: {e}")

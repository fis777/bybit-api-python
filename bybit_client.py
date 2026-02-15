"""
Клиент для работы с Bybit API
"""
from pybit.unified_trading import HTTP
from config import Config
import logging


class BybitClient:
    """Основной класс для взаимодействия с Bybit API"""

    def __init__(self, api_key=None, api_secret=None, testnet=None):
        """
        Инициализация клиента

        Args:
            api_key: API ключ (если None, берется из config)
            api_secret: API secret (если None, берется из config)
            testnet: Использовать testnet (если None, берется из config)
        """
        self.api_key = api_key or Config.API_KEY
        self.api_secret = api_secret or Config.API_SECRET
        self.testnet = testnet if testnet is not None else Config.TESTNET

        # Инициализация HTTP клиента
        self.client = HTTP(
            testnet=self.testnet,
            api_key=self.api_key,
            api_secret=self.api_secret
        )

        logging.info(f"Bybit клиент инициализирован (testnet={self.testnet})")

    # === Market Data Methods ===

    def get_server_time(self):
        """Получить время сервера"""
        try:
            response = self.client.get_server_time()
            return response
        except Exception as e:
            logging.error(f"Ошибка получения времени сервера: {e}")
            raise

    def get_tickers(self, category="spot", symbol=None):
        """
        Получить информацию о тикерах

        Args:
            category: Тип рынка (spot, linear, inverse, option)
            symbol: Символ торговой пары (например, BTCUSDT)
        """
        try:
            params = {"category": category}
            if symbol:
                params["symbol"] = symbol

            response = self.client.get_tickers(**params)
            return response
        except Exception as e:
            logging.error(f"Ошибка получения тикеров: {e}")
            raise

    def get_kline(self, category="spot", symbol="BTCUSDT", interval="1", limit=200):
        """
        Получить данные свечей (kline)

        Args:
            category: Тип рынка
            symbol: Символ пары
            interval: Интервал (1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, W, M)
            limit: Количество свечей (макс 1000)
        """
        try:
            response = self.client.get_kline(
                category=category,
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            return response
        except Exception as e:
            logging.error(f"Ошибка получения kline: {e}")
            raise

    def get_orderbook(self, category="spot", symbol="BTCUSDT", limit=25):
        """
        Получить стакан заявок

        Args:
            category: Тип рынка
            symbol: Символ пары
            limit: Глубина стакана (макс 500)
        """
        try:
            response = self.client.get_orderbook(
                category=category,
                symbol=symbol,
                limit=limit
            )
            return response
        except Exception as e:
            logging.error(f"Ошибка получения orderbook: {e}")
            raise

    # === Account Methods ===

    def get_wallet_balance(self, accountType="UNIFIED"):
        """
        Получить баланс кошелька

        Args:
            accountType: Тип аккаунта (UNIFIED, CONTRACT, SPOT)
        """
        try:
            response = self.client.get_wallet_balance(accountType=accountType)
            return response
        except Exception as e:
            logging.error(f"Ошибка получения баланса: {e}")
            raise

    # === Trading Methods ===

    def place_order(self, category, symbol, side, orderType, qty, price=None, **kwargs):
        """
        Разместить ордер

        Args:
            category: Тип рынка (spot, linear, inverse)
            symbol: Символ пары
            side: Buy или Sell
            orderType: Тип ордера (Market, Limit)
            qty: Количество
            price: Цена (для лимитных ордеров)
            **kwargs: Дополнительные параметры
        """
        try:
            params = {
                "category": category,
                "symbol": symbol,
                "side": side,
                "orderType": orderType,
                "qty": str(qty)
            }

            if price:
                params["price"] = str(price)

            params.update(kwargs)

            response = self.client.place_order(**params)
            logging.info(f"Ордер размещен: {response}")
            return response
        except Exception as e:
            logging.error(f"Ошибка размещения ордера: {e}")
            raise

    def get_open_orders(self, category, symbol=None):
        """
        Получить открытые ордера

        Args:
            category: Тип рынка
            symbol: Символ пары (опционально)
        """
        try:
            params = {"category": category}
            if symbol:
                params["symbol"] = symbol

            response = self.client.get_open_orders(**params)
            return response
        except Exception as e:
            logging.error(f"Ошибка получения открытых ордеров: {e}")
            raise

    def cancel_order(self, category, symbol, orderId=None, orderLinkId=None):
        """
        Отменить ордер

        Args:
            category: Тип рынка
            symbol: Символ пары
            orderId: ID ордера
            orderLinkId: Пользовательский ID ордера
        """
        try:
            params = {
                "category": category,
                "symbol": symbol
            }

            if orderId:
                params["orderId"] = orderId
            elif orderLinkId:
                params["orderLinkId"] = orderLinkId
            else:
                raise ValueError("Необходимо указать orderId или orderLinkId")

            response = self.client.cancel_order(**params)
            logging.info(f"Ордер отменен: {response}")
            return response
        except Exception as e:
            logging.error(f"Ошибка отмены ордера: {e}")
            raise

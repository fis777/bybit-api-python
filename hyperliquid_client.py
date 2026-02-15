"""
Клиент для работы с Hyperliquid API
"""
from hyperliquid.info import Info
from hyperliquid.utils import constants
import logging


class HyperliquidClient:
    """Класс для взаимодействия с Hyperliquid API"""

    def __init__(self, testnet=False):
        """
        Инициализация клиента Hyperliquid

        Args:
            testnet: Использовать testnet (по умолчанию False - mainnet)
        """
        self.testnet = testnet

        # Выбор базового URL
        if testnet:
            base_url = constants.TESTNET_API_URL
        else:
            base_url = constants.MAINNET_API_URL

        # Инициализация Info клиента (для чтения данных)
        self.info = Info(base_url=base_url, skip_ws=True)

        logging.info(f"Hyperliquid клиент инициализирован ({'testnet' if testnet else 'mainnet'})")

    def get_all_mids(self):
        """
        Получить средние цены (mid prices) для всех активов

        Returns:
            dict: {symbol: mid_price}
        """
        try:
            response = self.info.all_mids()
            return response
        except Exception as e:
            logging.error(f"Ошибка получения all_mids: {e}")
            raise

    def get_meta(self):
        """
        Получить метаданные о всех доступных активах

        Returns:
            dict: Информация об активах (название, размер контракта, и т.д.)
        """
        try:
            response = self.info.meta()
            return response
        except Exception as e:
            logging.error(f"Ошибка получения meta: {e}")
            raise

    def get_ticker(self, symbol):
        """
        Получить тикер для конкретного символа

        Args:
            symbol: Символ актива (например, 'BTC', 'ETH')

        Returns:
            dict: Данные тикера
        """
        try:
            # Получаем все средние цены
            all_mids = self.get_all_mids()

            if symbol in all_mids:
                return {
                    'symbol': symbol,
                    'price': float(all_mids[symbol])
                }
            else:
                return {
                    'symbol': symbol,
                    'price': None,
                    'error': 'Symbol not found'
                }
        except Exception as e:
            logging.error(f"Ошибка получения ticker для {symbol}: {e}")
            raise

    def get_multiple_tickers(self, symbols):
        """
        Получить тикеры для нескольких символов

        Args:
            symbols: Список символов (например, ['BTC', 'ETH', 'SOL'])

        Returns:
            dict: {symbol: price}
        """
        try:
            all_mids = self.get_all_mids()

            result = {}
            for symbol in symbols:
                if symbol in all_mids:
                    result[symbol] = float(all_mids[symbol])
                else:
                    result[symbol] = None

            return result
        except Exception as e:
            logging.error(f"Ошибка получения multiple tickers: {e}")
            raise

    def get_orderbook(self, symbol, depth=20):
        """
        Получить стакан заявок для актива

        Args:
            symbol: Символ актива
            depth: Глубина стакана

        Returns:
            dict: Данные стакана (bids, asks)
        """
        try:
            response = self.info.l2_snapshot(symbol)
            return response
        except Exception as e:
            logging.error(f"Ошибка получения orderbook для {symbol}: {e}")
            raise

    def get_funding_rate(self, symbol):
        """
        Получить ставку финансирования (funding rate) для актива

        Args:
            symbol: Символ актива

        Returns:
            dict: Данные о funding rate
        """
        try:
            meta = self.get_meta()

            # Ищем актив в метаданных
            for asset in meta['universe']:
                if asset['name'] == symbol:
                    # Funding rate обычно в поле funding
                    return {
                        'symbol': symbol,
                        'funding_rate': None  # Hyperliquid API может предоставлять это по-другому
                    }

            return {'symbol': symbol, 'funding_rate': None}
        except Exception as e:
            logging.error(f"Ошибка получения funding rate для {symbol}: {e}")
            raise

    def get_available_symbols(self):
        """
        Получить список всех доступных символов на Hyperliquid

        Returns:
            list: Список символов
        """
        try:
            meta = self.get_meta()
            symbols = [asset['name'] for asset in meta['universe']]
            return symbols
        except Exception as e:
            logging.error(f"Ошибка получения available symbols: {e}")
            raise

    def compare_with_bybit_spot(self, bybit_client, symbols):
        """
        Сравнить цены Hyperliquid futures с Bybit spot

        Args:
            bybit_client: Экземпляр BybitClient
            symbols: Список базовых символов (например, ['BTC', 'ETH'])

        Returns:
            list: Список словарей с данными сравнения
        """
        try:
            results = []

            # Получаем все цены Hyperliquid
            hl_prices = self.get_multiple_tickers(symbols)

            for symbol in symbols:
                hl_price = hl_prices.get(symbol)

                if hl_price is None:
                    continue

                # Получаем Bybit spot цену
                bybit_symbol = f"{symbol}USDC"
                try:
                    bybit_data = bybit_client.get_tickers(category="spot", symbol=bybit_symbol)
                    bybit_price = None

                    if bybit_data['retCode'] == 0 and bybit_data['result']['list']:
                        bybit_price = float(bybit_data['result']['list'][0]['lastPrice'])

                    # Расчет спреда
                    spread = None
                    spread_percent = None

                    if bybit_price and hl_price:
                        spread = hl_price - bybit_price
                        spread_percent = (spread / bybit_price) * 100

                    results.append({
                        'symbol': symbol,
                        'bybit_spot': bybit_price,
                        'hyperliquid_futures': hl_price,
                        'spread': spread,
                        'spread_percent': spread_percent
                    })

                except Exception as e:
                    logging.warning(f"Ошибка получения Bybit данных для {symbol}: {e}")
                    continue

            return results

        except Exception as e:
            logging.error(f"Ошибка сравнения с Bybit: {e}")
            raise

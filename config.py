"""
Конфигурация для подключения к Bybit API
"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()


class Config:
    """Настройки для Bybit API"""

    # API credentials
    API_KEY = os.getenv('BYBIT_API_KEY', '')
    API_SECRET = os.getenv('BYBIT_API_SECRET', '')

    # Testnet или mainnet
    TESTNET = os.getenv('BYBIT_TESTNET', 'True').lower() == 'true'

    # Базовые URL
    if TESTNET:
        BASE_URL = 'https://api-testnet.bybit.com'
    else:
        BASE_URL = 'https://api.bybit.com'

    # Настройки таймаутов
    REQUEST_TIMEOUT = 10  # секунды

    # Логирование
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/bybit_api.log'

    @classmethod
    def validate(cls):
        """Проверка наличия обязательных параметров"""
        if not cls.API_KEY or not cls.API_SECRET:
            raise ValueError(
                "API ключи не настроены! "
                "Скопируйте .env.example в .env и добавьте свои ключи."
            )
        return True

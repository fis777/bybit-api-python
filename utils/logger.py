"""
Настройка логирования для проекта
"""
import logging
import os
from datetime import datetime


def setup_logger(name='bybit_api', log_file=None, level=logging.INFO):
    """
    Настройка логгера

    Args:
        name: Имя логгера
        log_file: Путь к файлу лога
        level: Уровень логирования
    """
    # Создаем директорию для логов если не существует
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Настройка логгера
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

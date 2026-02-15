"""
Утилита для исправления проблем с кодировкой в Windows
"""
import sys
import os


def fix_windows_encoding():
    """
    Исправляет проблемы с отображением UTF-8 в консоли Windows.

    Вызывайте эту функцию в начале скрипта для корректного отображения
    русского текста в консоли Windows.

    Пример:
        from utils.encoding import fix_windows_encoding
        fix_windows_encoding()
    """
    if sys.platform == 'win32':
        # Установка UTF-8 для вывода в консоль
        if hasattr(sys.stdout, 'reconfigure'):
            if sys.stdout.encoding != 'utf-8':
                sys.stdout.reconfigure(encoding='utf-8')
            if sys.stderr.encoding != 'utf-8':
                sys.stderr.reconfigure(encoding='utf-8')

        # Установка консоли Windows в режим UTF-8
        os.system('chcp 65001 > nul')

        return True
    return False

# Инструкция по работе с виртуальным окружением

## Виртуальное окружение создано!

**Python версия:** 3.14.0
**Директория:** `venv/`

## Установленные пакеты:

```
certifi            2026.1.4
charset-normalizer 3.4.4
idna               3.11
pybit              5.14.0      # Официальная библиотека Bybit
pycryptodome       3.23.0
python-dotenv      1.2.1       # Управление .env файлами
requests           2.32.5
urllib3            2.6.3
websocket-client   1.9.0       # WebSocket поддержка
```

---

## Как использовать

### Активация виртуального окружения

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Проверка активации

После активации в начале строки терминала появится `(venv)`:
```bash
(venv) user@computer:~/PythonApi$
```

### Запуск скриптов

После активации venv запускайте скрипты как обычно:

```bash
# Активируем окружение
source venv/Scripts/activate

# Запускаем примеры
python examples/market_data.py
python examples/websocket_simple.py
python examples/spot_futures_comparison.py
```

### Деактивация

```bash
deactivate
```

---

## Обновление зависимостей

Если были изменения в `requirements.txt`:

```bash
source venv/Scripts/activate
pip install -r requirements.txt --upgrade
```

---

## Добавление новых пакетов

```bash
# Активируем venv
source venv/Scripts/activate

# Устанавливаем пакет
pip install package-name

# Обновляем requirements.txt
pip freeze > requirements.txt
```

---

## Удаление виртуального окружения

Просто удалите директорию:

```bash
rm -rf venv/
# Или через проводник Windows
```

Затем создайте заново:
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

---

## Важно

1. **Не коммитьте директорию `venv/` в git** (уже добавлено в `.gitignore`)
2. **Всегда активируйте venv** перед работой с проектом
3. **Используйте `requirements.txt`** для управления зависимостями
4. **Каждый проект** должен иметь свое виртуальное окружение

---

## Полезные команды

```bash
# Список установленных пакетов
pip list

# Информация о пакете
pip show pybit

# Поиск пакета
pip search package-name

# Обновление pip
python -m pip install --upgrade pip

# Проверка устаревших пакетов
pip list --outdated
```

---

## Советы

1. **VS Code**: Выберите интерпретатор из venv
   - Ctrl+Shift+P -> "Python: Select Interpreter"
   - Выберите `./venv/Scripts/python.exe`

2. **PyCharm**: Настройка interpreter
   - Settings -> Project -> Python Interpreter
   - Add Interpreter -> Existing -> `venv/Scripts/python.exe`

3. **Автоактивация**: Добавьте в `.bashrc` или `.bash_profile`
   ```bash
   cd /c/projects/ApiExample/PythonApi && source venv/Scripts/activate
   ```

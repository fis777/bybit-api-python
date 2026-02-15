# Настройка GitHub репозитория

## 🚀 Быстрый старт

### Вариант 1: Через веб-интерфейс (проще)

#### 1. Создайте репозиторий на GitHub:
- Откройте: https://github.com/new
- Repository name: `bybit-api-python`
- Description: `Python client for Bybit API with WebSocket support for 35 trading pairs`
- Visibility: **Public** или **Private**
- ❌ **НЕ добавляйте** README, .gitignore или LICENSE

#### 2. Подключите локальный репозиторий:

```bash
# Замените YOUR_USERNAME на ваше имя пользователя GitHub
git remote add origin https://github.com/YOUR_USERNAME/bybit-api-python.git

# Переименуйте ветку master в main (опционально)
git branch -M main

# Загрузите код на GitHub
git push -u origin main
```

---

## 📦 Вариант 2: Через GitHub CLI (автоматически)

### 1. Установите GitHub CLI:

**Windows (через winget):**
```powershell
winget install --id GitHub.cli
```

**Windows (через Chocolatey):**
```powershell
choco install gh
```

**Или скачайте с:** https://cli.github.com/

### 2. Авторизуйтесь:
```bash
gh auth login
```

Выберите:
- GitHub.com
- HTTPS
- Login with a web browser (или через токен)

### 3. Создайте репозиторий автоматически:

```bash
gh repo create bybit-api-python --public --source=. --remote=origin --push
```

Или для приватного репозитория:
```bash
gh repo create bybit-api-python --private --source=. --remote=origin --push
```

---

## ✅ Проверка

После настройки проверьте:

```bash
# Проверить remote
git remote -v

# Проверить что код загружен
git log --oneline
```

Откройте ваш репозиторий:
```
https://github.com/YOUR_USERNAME/bybit-api-python
```

---

## 📝 Рекомендуемое описание репозитория

**About (на странице репозитория):**
```
Python client for Bybit cryptocurrency exchange API. Features REST API client, WebSocket real-time data streaming, support for 35 SPOT/USDC trading pairs with automatic monitoring and statistics.
```

**Topics (теги):**
```
python bybit cryptocurrency trading api websocket crypto bitcoin ethereum altcoins
```

---

## 🔒 Важно

Убедитесь, что файл `.env` **НЕ** загружен на GitHub:
```bash
git status
```

Если `.env` в списке, это ошибка! Он должен быть в `.gitignore`.

**Никогда не коммитьте:**
- `.env` - ваши API ключи
- `*.key` - приватные ключи
- Любые файлы с паролями или токенами

---

## 📄 Лицензия (опционально)

Если хотите добавить лицензию:

```bash
# MIT License (самая популярная для open source)
gh repo edit --add-license mit

# Или создайте вручную файл LICENSE
```

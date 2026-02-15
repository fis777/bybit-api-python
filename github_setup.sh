#!/bin/bash
# Скрипт для подключения к GitHub репозиторию
#
# ИНСТРУКЦИЯ:
# 1. Создайте репозиторий на https://github.com/new
# 2. Замените YOUR_USERNAME на ваше имя пользователя GitHub
# 3. Замените REPO_NAME на название вашего репозитория (например: bybit-api-python)
# 4. Запустите: bash github_setup.sh

# Замените эти значения:
GITHUB_USERNAME="fis777@gmail.com"
REPO_NAME="bybit-api-python"

# Добавление remote origin
git remote add origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

# Переименование ветки в main (если нужно)
git branch -M main

# Первый push
git push -u origin main

echo ""
echo "✅ Репозиторий подключен и код загружен на GitHub!"
echo "🔗 URL: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"

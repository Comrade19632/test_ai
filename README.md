# USD/RUB Telegram Bot

Бот отвечает на **каждое входящее текстовое сообщение** текущим курсом рубля к доллару (USD/RUB) по данным ЦБ РФ.

## Что делает
- `/start` — краткая инструкция
- Любое текстовое сообщение — ответ:
  - текущий курс `1 USD = X RUB`
  - время обновления данных

Источник курса: `https://www.cbr-xml-daily.ru/daily_json.js`

---

## Локальный запуск

### 1) Требования
- Python 3.10+
- Telegram-бот (токен от BotFather)

### 2) Установка
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Переменные окружения
```bash
cp .env.example .env
# впиши реальный BOT_TOKEN в .env
export $(grep -v '^#' .env | xargs)
```

### 4) Старт
```bash
python bot.py
```

---

## Деплой в prod на внешний сервер (Ubuntu 22.04+)

### 1) Подготовить сервер
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv git
```

### 2) Клонировать репозиторий
```bash
git clone git@github.com:Comrade19632/test_ai.git
cd test_ai
```

### 3) Настроить приложение
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Создать env-файл:
```bash
cat > .env << 'EOF'
BOT_TOKEN=PASTE_YOUR_REAL_TELEGRAM_TOKEN
EOF
```

### 4) Создать systemd unit
```bash
sudo tee /etc/systemd/system/usd-rub-bot.service > /dev/null << 'EOF'
[Unit]
Description=USD/RUB Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/test_ai
EnvironmentFile=/home/$USER/test_ai/.env
ExecStart=/home/$USER/test_ai/.venv/bin/python /home/$USER/test_ai/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

### 5) Запустить и включить автозапуск
```bash
sudo systemctl daemon-reload
sudo systemctl enable usd-rub-bot
sudo systemctl start usd-rub-bot
```

### 6) Проверка
```bash
systemctl status usd-rub-bot --no-pager
journalctl -u usd-rub-bot -f
```

### 7) Обновление версии в будущем
```bash
cd ~/test_ai
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart usd-rub-bot
```

## Безопасность
- Никогда не коммить `BOT_TOKEN` в репозиторий.
- Используй отдельного пользователя на сервере под бота.
- Ограничь SSH-доступ (ключи, fail2ban, закрыть root login).

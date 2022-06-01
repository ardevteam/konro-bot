# Konro-Bot
Konro merupakan aplikasi E-Portfolio berbasis web based yang digunakan untuk menampilkan hasil project yang telah dibuat dan terdapat sistem untuk review dan penilaian dari masing-masing project. Sedangkan Konro Bot digunakan untuk manage Aplikasi Konro melalui telegram bot.

## Introduction
Konro Bot ini menggunakan bahasa pemrograman Python dengan library [python-telegram-bot](https://python-telegram-bot.org/) v20 untuk terhubung ke [Telegram Bot API](https://core.telegram.org/bots/api).

## Documentation
- [Doc python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Wiki python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Installation
1. Library python-telegram-bot v20:
```bash
  pip install python-telegram-bot --pre
```

2. Edit koneksi database pada file `dbfunction.py`
```python
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",      
  database="db_konro"
)
```

3. Edit Token Telegram Bot pada file `bot.py`
```python
application = ApplicationBuilder().token("YOUR TOKEN HERE").read_timeout(7).get_updates_read_timeout(42).build()
```

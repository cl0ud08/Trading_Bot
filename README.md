# 🤖 Binance Futures Trading Bot

A lightweight CLI-based Python trading bot for placing **MARKET** and **LIMIT** orders on **Binance Futures Testnet (USDT-M)**. Built with clean layered architecture, structured logging, and robust error handling.

---

## 📁 Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py           # Binance API client — auth, HMAC signing, HTTP calls
│   ├── orders.py           # Order placement logic and response parsing
│   ├── validators.py       # Input validation layer
│   └── logging_config.py   # Structured logging to file + console
├── cli.py                  # CLI entry point (argparse)
├── trading_bot.log         # Auto-generated log file
├── .env                    # API credentials (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/trading_bot.git
cd trading_bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Binance Testnet API credentials

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Sign in with GitHub
3. Top right → **API Management** → **Generate**
4. Copy your API Key and Secret

### 4. Create a `.env` file

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

---

## 🚀 How to Run

### Place a MARKET BUY order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a MARKET SELL order

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### Place a LIMIT BUY order

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000
```

### Place a LIMIT SELL order

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3000
```

### View all options

```bash
python cli.py --help
```

---

## 📋 CLI Arguments

| Argument     | Required | Description                              |
|--------------|----------|------------------------------------------|
| `--symbol`   | ✅ Yes   | Trading pair (e.g. `BTCUSDT`, `ETHUSDT`) |
| `--side`     | ✅ Yes   | `BUY` or `SELL`                          |
| `--type`     | ✅ Yes   | `MARKET` or `LIMIT`                      |
| `--quantity` | ✅ Yes   | Order quantity (e.g. `0.001`)            |
| `--price`    | ⚠️ LIMIT only | Limit price (e.g. `50000`)          |

---

## 📊 Example Output

```
=============================================
         ORDER REQUEST SUMMARY
=============================================
  Symbol     : BTCUSDT
  Side       : BUY
  Type       : MARKET
  Quantity   : 0.001
=============================================

=============================================
         ✅ ORDER PLACED SUCCESSFULLY
=============================================
  Order ID     : 4410647700
  Symbol       : BTCUSDT
  Status       : FILLED
  Side         : BUY
  Type         : MARKET
  Quantity     : 0.001
  Executed Qty : 0.001
  Avg Price    : 105432.50
=============================================
```

---

## 📝 Logging

All activity is logged automatically to `trading_bot.log`.

| Destination    | Level         | Contains                              |
|----------------|---------------|---------------------------------------|
| Console        | INFO and above | Order summaries, success/failure      |
| `trading_bot.log` | DEBUG and above | Full API requests, responses, errors |

Log format:
```
2026-07-01 10:00:00 | INFO     | orders | Order placed successfully — ID: 4410647700
2026-07-01 10:00:00 | DEBUG    | client | POST https://testnet.binancefuture.com/fapi/v1/order
```

Logs rotate automatically at 5MB and keep the last 3 files — so they never grow out of control.

---

## 🏗️ Architecture

The app is split into clear layers — each file has one job:

```
cli.py          →  parses user input from terminal
    ↓
validators.py   →  validates all inputs before any API call
    ↓
orders.py       →  builds request params, calls client, prints result
    ↓
client.py       →  signs request with HMAC-SHA256, makes HTTP call
    ↓
Binance Testnet API
```

This separation means you can test each layer independently and swap any layer without touching the others.

---

## 🔐 Authentication

Binance Futures requires **HMAC-SHA256** signing on all private endpoints. The `client.py` layer handles this automatically:

1. Adds a `timestamp` to every request (Binance rejects requests older than 5 seconds)
2. Converts all params to a query string
3. Signs it using your secret key via HMAC-SHA256
4. Attaches the signature to the request

Your secret key is never logged or printed.

---

## ⚠️ Assumptions

- This bot targets **Binance Futures Testnet only** — not for live trading
- LIMIT orders use `GTC` (Good Till Cancelled) time-in-force by default
- Minimum quantity for `BTCUSDT` on testnet is `0.001`
- Python 3.8+ required

---

## 📦 Requirements

```
requests==2.31.0
python-dotenv==1.0.0
```

---

## 📤 Submission

Built for the **Primetrade.ai Python Developer Intern** assignment.

Log files from at least one MARKET and one LIMIT order are included in the repository as `trading_bot.log`.
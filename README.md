# 📳 Ping-My-Phone

![Python](https://img.shields.io/badge/python-3.11-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**A Raspberry Pi project that listens for RF signals (like a doorbell or button) and sends instant notifications to your phone via Telegram.**

---

## 🚀 Features

* Detects specific RF codes using the `rpi-rf` library
* Filters out noise; only alerts for configured RF codes
* Sends instant Telegram messages to your phone
* Lightweight Python scripts, compatible with Raspberry Pi OS / DietPi

---

## 🧰 Requirements

* Raspberry Pi with GPIO pins
* 433MHz RF receiver
* Python 3.x
* Python packages: `RPi.GPIO`, `rpi-rf`, `requests`, `python-dotenv`, `python-telegram-bot`
* Telegram bot token and chat ID

---

## ⚙️ Setup

1. **Clone and install dependencies:**
```bash
git clone https://github.com/thousand-leaves/ping-my-phone.git
cd ping-my-phone

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Note:** GPIO access requires sudo, so when running scripts use `sudo venv/bin/python3` to access packages from your venv.

2. **Configure environment variables:**
Create a `.env` file in the project root:
```bash
nano .env
```

Add your Telegram credentials:
```env
BOT_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
GPIO_DATA_PIN=27
```

**Note:** GPIO pin defaults to 27 (physical pin 13) if not specified.

3. **Connect your RF receiver to GPIO pin 27 (physical pin 13)**

4. **Discover your button code:**
```bash
sudo venv/bin/python3 src/button_discovery_tool.py
```
Press your RF button several times, then press Ctrl+C. The tool will identify and save your button code.

5. **Run the doorbell system:**
```bash
sudo venv/bin/python3 src/doorbell.py
```

---

## 🔧 Running as a Service

To run as a background service that starts automatically:

```bash
# Copy service file
sudo cp doorbell.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable doorbell.service
sudo systemctl start doorbell.service

# Check status
sudo systemctl status doorbell.service
```

**Service Management:**
```bash
sudo systemctl start doorbell.service    # Start
sudo systemctl stop doorbell.service     # Stop
sudo systemctl restart doorbell.service  # Restart
sudo journalctl -u doorbell.service -f   # View logs
```

---

## 💡 Development

⚠️ **Important:** If the doorbell service is running, stop it before running scripts manually:

```bash
sudo systemctl stop doorbell.service
sudo python3 src/doorbell.py
```

The service and manual execution cannot run simultaneously due to GPIO pin exclusivity.

---

## 🔧 Troubleshooting

**GPIO busy errors:**
```bash
sudo python3 cleanup-gpio.py
```

**Check if service is running:**
```bash
sudo systemctl status doorbell.service
```

---

## ⚖️ License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

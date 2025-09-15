# 📳 Ping-My-Phone

![Python](https://img.shields.io/badge/python-3.11-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**A Raspberry Pi project that listens for RF signals (like a doorbell or button) and sends instant notifications to your phone via Telegram.**

---

## 🚀 Features

* Detects specific RF codes using GPIO
* Filters out noise; only alerts for configured signals
* Sends instant Telegram messages to your phone
* Lightweight Python scripts, compatible with Raspberry Pi OS / DietPi

---

## 🧰 Requirements

* Raspberry Pi with GPIO pins
* 433MHz RF receiver
* Python 3.x
* Python packages: `RPi.GPIO`, `requests`
* Telegram bot token and chat ID

---

## ⚙️ Setup

1. Clone the repo:

```bash
git clone https://github.com/yourusername/ping-my-phone.git
cd ping-my-phone
```

2. Create and activate a virtual environment:

```bash
python3 -m venv rf-env
source rf-env/bin/activate
pip install -r requirements.txt
```

3. Configure your `BOT_TOKEN` and `CHAT_ID` in the script.
4. Connect your RF receiver to the designated GPIO pin.
5. Run the script:

```bash
python3 rf_receiver_telegram.py
```

---

## 💡 Usage

* Press your button or trigger your RF device.
* Only configured codes (e.g., your doorbell) send Telegram alerts.
* Console logs show real-time detection of signals.

---

## ⚖️ License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

---

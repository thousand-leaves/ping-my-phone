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

# Install system dependencies (using system Python for GPIO access)
sudo pip3 install --break-system-packages python-dotenv
```

**Note:** This project uses system Python (`/usr/bin/python3`) because:
- GPIO access requires root privileges
- System RPi.GPIO (0.7.2) has better compatibility than venv versions
- Most dependencies (requests, rpi-rf, RPi.GPIO) are already available system-wide

The `--break-system-packages` flag is needed on modern Python installations that protect system packages. This only installs `python-dotenv` which isn't available via apt.

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
sudo python3 src/button_discovery_tool.py
```
Press your RF button several times, then press Ctrl+C. The tool will identify and save your button code.

5. **Test the doorbell system:**
```bash
# First, ensure GPIO is clean
sudo python3 cleanup-gpio.py

# Then run the doorbell system
sudo python3 src/main.py
```

The doorbell should start and display: `🔔 Doorbell System - Monitoring button code [your_code]`

If you see errors, check the [Troubleshooting](#-troubleshooting) section below.

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
sudo python3 src/main.py
```

The service and manual execution cannot run simultaneously due to GPIO pin exclusivity.

**Note:** All scripts use system Python (`/usr/bin/python3`) for clean GPIO access. No virtual environment needed.

---

## 🔧 Troubleshooting

**GPIO busy errors:**
```bash
sudo python3 cleanup-gpio.py
```

**"Failed to add edge detection" error:**
If you encounter `RuntimeError: Failed to add edge detection` when running `main.py`:

1. Ensure no other processes are using the GPIO pin:
   ```bash
   sudo python3 cleanup-gpio.py
   sudo systemctl stop doorbell.service  # If service is running
   ```

2. Verify GPIO pin is available:
   ```bash
   gpioinfo | grep GPIO27
   ```
   Should show `GPIO27` as `unused`.

3. Check kernel messages for GPIO issues:
   ```bash
   sudo dmesg | tail -20 | grep -i gpio
   ```

4. If the error persists, this may indicate a hardware/library compatibility issue. Try:
   - Verifying your RF receiver is properly connected
   - Checking if GPIO pin 27 is correct for your setup
   - Testing with a different GPIO pin (update `GPIO_DATA_PIN` in `.env`)

**Check if service is running:**
```bash
sudo systemctl status doorbell.service
```

**View service logs:**
```bash
sudo journalctl -u doorbell.service -n 50
```

---

## ⚖️ License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

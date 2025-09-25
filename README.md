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
* Python packages: `RPi.GPIO`, `requests`, `python-dotenv`
* Telegram bot token and chat ID

---

## ⚙️ Setup

1. Clone the repo:

```bash
git clone https://github.com/thousand-leaves/ping-my-phone.git
cd ping-my-phone
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **First-time setup - Discover your button:**
```bash
# Run the button discovery tool to find your RF button code
python3 src/button_discovery_tool.py
```

4. **Configure environment variables:**
Create a `.env` file in the project root:
```bash
# Copy the example and edit with your values
cp .env.example .env
nano .env
```

Add your Telegram credentials:
```env
BOT_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
```

5. Connect your RF receiver to the designated GPIO pin.
6. Run the doorbell system:

```bash
python3 src/doorbell.py
```

### **Optional: Install as System Service**

To run the doorbell as a background service that starts automatically:

```bash
# Install to system directory (recommended for production)
sudo mkdir -p /opt/ping-my-phone
sudo cp -r . /opt/ping-my-phone/
sudo chown -R root:root /opt/ping-my-phone

# Copy the service file to systemd directory
sudo cp doorbell.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable doorbell.service

# Start the service
sudo systemctl start doorbell.service

# Check service status
sudo systemctl status doorbell.service
```

**Alternative: Run from home directory**
If you prefer to keep it in your home directory, edit the service file:
```bash
# Edit the service file to use your home directory
sudo nano /etc/systemd/system/doorbell.service
# Change WorkingDirectory and ExecStart paths to your home directory
```

---

## 💡 Usage

### **Button Discovery (First Time Only)**
Before using the doorbell system, you need to discover your button's unique code:

```bash
python3 src/button_discovery_tool.py
```

This tool will:
- Monitor RF signals for 30 seconds
- Show you all detected button codes
- Automatically save your button code to `button_config.json`
- Help you identify which code belongs to your doorbell

### **Running the Doorbell System**
Once configured:
* Press your button or trigger your RF device
* Only configured codes (e.g., your doorbell) send Telegram alerts
* Console logs show real-time detection of signals
* The system filters out noise and only responds to your specific button

---

## 🔧 Service Management (Systemd)

If you've set up the doorbell as a systemd service, use these commands to manage it:

### **Basic Service Commands**
```bash
# Start the doorbell service
sudo systemctl start doorbell.service

# Stop the doorbell service
sudo systemctl stop doorbell.service

# Restart the doorbell service
sudo systemctl restart doorbell.service

# Check service status
sudo systemctl status doorbell.service

# Enable service to start on boot
sudo systemctl enable doorbell.service

# Disable service from starting on boot
sudo systemctl disable doorbell.service
```

### **Monitoring and Debugging**
```bash
# View real-time logs
sudo journalctl -u doorbell.service -f

# View recent logs (last 50 lines)
sudo journalctl -u doorbell.service -n 50

# Check if service is running
sudo systemctl is-active doorbell.service

# Check if service is enabled for boot
sudo systemctl is-enabled doorbell.service
```

### **Troubleshooting**
```bash
# If service won't stop, check for running processes
pgrep -f doorbell

# Force kill if needed (use with caution)
sudo pkill -f doorbell

# Check service configuration
sudo systemctl cat doorbell.service
```

### **Easy Management Script**
For convenience, use the included management script:

```bash
# Make it executable (first time only)
chmod +x manage_doorbell.sh

# Start the doorbell
./manage_doorbell.sh start

# Stop the doorbell
./manage_doorbell.sh stop

# Check status
./manage_doorbell.sh status

# View real-time logs
./manage_doorbell.sh logs

# Show all available commands
./manage_doorbell.sh help
```

---

## ⚖️ License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file.

---

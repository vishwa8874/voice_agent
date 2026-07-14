# Ngrok Setup & Configuration Guide

## 🔌 Ngrok Installation

### macOS
```bash
brew install ngrok
```

### Linux
```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok-v3-stable-linux-amd64.zip -o ngrok.zip
unzip ngrok.zip
sudo mv ngrok /usr/local/bin/
```

### Windows
Download from https://ngrok.com/download and extract

## 🔐 Authentication

### 1. Create Account
Visit: https://dashboard.ngrok.com/signup

### 2. Get Auth Token
Go to: https://dashboard.ngrok.com/get-started/your-authtoken

### 3. Authenticate Locally
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

## 🚀 Running the Dashboard with Ngrok

### Terminal 1: Start Dashboard
```bash
cd dashboard
source venv/bin/activate
python app.py
```

### Terminal 2: Start Ngrok
```bash
ngrok http 5000
```

You'll see output:
```
Forwarding https://abc123.ngrok.io -> http://localhost:5000
```

## ⚙️ Configure Twilio Webhooks

1. Go to https://console.twilio.com/phone-numbers
2. Select your phone number
3. Configure webhooks:
   - **A Call Comes In:** `https://YOUR_NGROK_URL/api/twilio/incoming`
   - **Status Callbacks:** `https://YOUR_NGROK_URL/api/twilio/status`

## 🎤 Configure Deepgram Webhooks

1. Go to https://console.deepgram.com/settings/webhooks
2. Add webhook: `https://YOUR_NGROK_URL/api/deepgram/callback`

## 📊 Access Your Dashboard

- Dashboard: `https://YOUR_NGROK_URL`
- API Docs: `https://YOUR_NGROK_URL/api/health`
- Logs: `https://YOUR_NGROK_URL/api/logs`
- Summary: `https://YOUR_NGROK_URL/api/summary`

## 📝 .env File Setup

Create `.env` in dashboard directory:
```
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key
DEEPGRAM_API_KEY=your-deepgram-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

## 💡 Pro Tips

- Free ngrok URLs change on restart (upgrade for permanent URLs)
- Use HTTPS (auto-upgraded by ngrok)
- Monitor requests: `http://127.0.0.1:4040` (ngrok inspector)
- Keep auth token private
- Use custom domain for production: `ngrok http --domain=myapp 5000`

## 🔗 Useful Links

- Ngrok Dashboard: https://dashboard.ngrok.com
- Ngrok Docs: https://ngrok.com/docs
- Twilio Console: https://console.twilio.com
- Deepgram Console: https://console.deepgram.com

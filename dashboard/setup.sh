#!/bin/bash

# White-Labeled Dashboard Setup Script

echo "🚀 Setting up Call Analytics Dashboard with Deepgram & Twilio Integration..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p data

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOF
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
DEEPGRAM_API_KEY=your-deepgram-api-key
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
EOF
fi

echo "✅ Setup complete!"
echo ""
echo "To start the dashboard:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Update .env with your Deepgram and Twilio credentials"
echo "  3. Run the app: python app.py"
echo ""
echo "Access the dashboard at: http://localhost:5000"

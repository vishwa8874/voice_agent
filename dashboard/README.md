# White-Labeled Call Analytics Dashboard
## With Deepgram & Twilio Integration

Professional call log visualization and analytics dashboard that hides your underlying tech stack. Now with built-in support for Deepgram transcription and Twilio call management.

## Features

✨ **Core Features:**
- 📊 Real-time dashboard with comprehensive metrics
- 📈 Interactive charts and trend analysis
- 📝 Detailed call logs with advanced filtering
- 🎯 Status and provider breakdown
- 📱 Fully responsive design
- 🔍 Advanced search capabilities
- 📅 Customizable time ranges

🎤 **Deepgram Integration:**
- Real-time speech-to-text transcription
- Transcription confidence scoring
- Keyword extraction and entity recognition
- Sentiment analysis
- Full transcription search across all calls
- Transcription preview in call logs

☎️ **Twilio Integration:**
- Call cost tracking and analytics
- Call provider metadata
- Recording URL management
- Call quality metrics
- Provider-specific call filtering
- Cost per call analysis

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Deepgram API Key
- Twilio Account SID & Auth Token

### Installation

1. **Clone and navigate to dashboard directory**
   ```bash
   cd dashboard
   ```

2. **Run setup script**
   ```bash
   bash setup.sh
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Configure credentials**
   Edit `.env` file with:
   ```
   DEEPGRAM_API_KEY=your-api-key
   TWILIO_ACCOUNT_SID=your-sid
   TWILIO_AUTH_TOKEN=your-token
   TWILIO_PHONE_NUMBER=your-phone
   ```

5. **Start the application**
   ```bash
   python app.py
   ```

6. **Access the dashboard**
   Open browser: `http://localhost:5000`

## Dashboard Sections

### Summary Cards
- **Total Calls**: All processed calls
- **Successful**: Completed calls with success rate
- **Failed**: Failed calls requiring attention
- **Avg Duration**: Average call length in seconds
- **Transcribed**: Calls with Deepgram transcriptions
- **Avg Confidence**: Average transcription confidence score
- **Total Cost**: Cumulative Twilio call costs
- **Avg Cost/Call**: Per-call cost average

### Analytics Charts
1. **Status Breakdown** (Doughnut): Completed/Failed/Pending distribution
2. **Hourly Trends** (Line): Calls per hour over time
3. **Provider Distribution** (Pie): Twilio vs Custom calls
4. **Sentiment Analysis** (Bar): Positive/Neutral/Negative sentiment from Deepgram

### Transcription Search
- Search across all call transcriptions
- View transcription text with confidence scores
- Filter by date range
- View matched call metadata

### Call Logs Table
Columns:
- Call ID (unique identifier)
- Duration (in seconds)
- Status (Completed/Failed/Pending)
- Transcription (preview from Deepgram)
- Confidence (Deepgram confidence score)
- Provider (Twilio/Custom)
- Timestamp

## API Endpoints

### GET /api/summary
Returns summary statistics with Deepgram and Twilio metrics.
```bash
GET /api/summary?days=7
```

### GET /api/analytics
Returns detailed analytics data for charts.
```bash
GET /api/analytics?days=7
```

### GET /api/logs
Returns paginated call logs with enriched data.
```bash
GET /api/logs?page=1&per_page=50&status=completed&provider=twilio
```

### GET /api/transcriptions/search
Search across all transcriptions.
```bash
GET /api/transcriptions/search?q=keyword&days=7
```

### GET /api/call/<call_id>/transcription
Get detailed transcription for a specific call.
```bash
GET /api/call/{call_id}/transcription
```

### GET /api/call/<call_id>/recording
Get recording URL for a specific call (Twilio).
```bash
GET /api/call/{call_id}/recording
```

### GET /api/health
Health check endpoint.
```bash
GET /api/health
```

## Configuration

Edit `config.py` to customize:
- Brand name and colors
- Time ranges and data retention
- API settings
- Security options
- Feature toggles

```python
# Brand settings
APP_NAME = "Call Analytics"
BRAND_COLOR_PRIMARY = "#2c3e50"
BRAND_COLOR_SECONDARY = "#3498db"

# Data retention
LOG_RETENTION_DAYS = 90

# Features
ENABLE_EXPORT = True
ENABLE_REPORTS = True
```

## Data Format

The dashboard works with call logs in this format:

```json
{
  "call_id": "unique-identifier",
  "from": "+1234567890",
  "to": "+0987654321",
  "duration": 45.5,
  "status": "completed",
  "timestamp": "2024-07-14T10:30:00Z",
  "provider": "twilio",
  "transcription": "Sample transcript text...",
  "confidence": 0.95,
  "sentiment": "positive",
  "keywords": ["keyword1", "keyword2"],
  "call_cost": 0.0275,
  "recording_url": "https://..."
}
```

## Deployment

### Using Gunicorn (Production)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Docker Compose
```yaml
version: '3'
services:
  dashboard:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
    volumes:
      - ./data:/app/data
```

## Customization

### Change Brand Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    --deepgram-color: #your-color;
    --twilio-color: #your-color;
}
```

### Add Custom Metrics
Extend `EnhancedCallLogAggregator` class in `app.py`:
```python
def get_custom_metric(self, days: int):
    # Your custom logic here
    pass
```

## Integrating with Your System

### Adding Call Logs
```python
from app import aggregator

# Add Deepgram call
aggregator.add_call_with_deepgram(
    call_id="unique-id",
    audio_url="https://...",
    duration=45.5,
    status="completed",
    timestamp="2024-07-14T10:30:00Z",
    user_id="user@example.com"
)

# Add Twilio call
aggregator.add_twilio_call(
    call_sid="CA123456789",
    from_number="+1234567890",
    to_number="+0987654321",
    duration=45.5,
    status="completed",
    timestamp="2024-07-14T10:30:00Z",
    recording_url="https://..."
)
```

## Security Best Practices

- Store credentials in environment variables only
- Use HTTPS in production
- Enable CORS carefully
- Implement authentication if needed
- Regular security audits
- Keep dependencies updated

## Troubleshooting

### Port Already in Use
```bash
lsof -i :5000  # Find process
kill -9 <PID>  # Kill it
```

### Deepgram API Errors
- Verify API key is correct
- Check account has sufficient credits
- Review API usage limits

### Twilio Connection Issues
- Verify Account SID and Auth Token
- Check account is active
- Review Twilio rate limits

### Import Errors
```bash
pip install --force-reinstall -r requirements.txt
```

## Performance Optimization

- Results are paginated (50 per page)
- Auto-refresh every 5 minutes
- Lazy loading for charts
- Database indexing on timestamp
- CDN for static assets

## License

This dashboard is provided as-is for white-label deployment.

## Support

For issues or questions, check the logs at `dashboard.log` or review configuration.

---

**Dashboard Architecture:**
- **Frontend**: HTML5, CSS3, JavaScript (Chart.js)
- **Backend**: Flask, Python
- **Integration**: Deepgram API, Twilio API
- **Database**: Flexible (JSON in-memory or persistent store)
- **Deployment**: Docker, Gunicorn, Cloud-ready

**Note**: This is a completely branded solution that abstracts your underlying technology stack, perfect for client-facing deployments with Deepgram transcription and Twilio telephony integration.

"""
White-labeled dashboard with Deepgram and Twilio integration.
Combines call logs with transcription and call metadata.
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any
import logging
from deepgram import Deepgram
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Deepgram and Twilio
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY', 'your-deepgram-api-key')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'your-twilio-account-sid')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'your-twilio-auth-token')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'your-twilio-phone-number')

deepgram_client = Deepgram(DEEPGRAM_API_KEY)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class EnhancedCallLogAggregator:
    """Aggregates call logs with Deepgram transcription and Twilio call data."""
    
    def __init__(self):
        self.logs = []
        self.transcriptions = {}
        self.call_recordings = {}
    
    def add_call_with_deepgram(self, call_id: str, audio_url: str, duration: float, 
                                status: str, timestamp: str, user_id: str = None, 
                                metadata: Dict = None):
        """Add a call log with Deepgram transcription."""
        log_entry = {
            "call_id": call_id,
            "duration": duration,
            "status": status,
            "timestamp": timestamp,
            "user_id": user_id or "Anonymous",
            "audio_url": audio_url,
            "metadata": metadata or {},
            "transcription": None,
            "sentiment": None,
            "entities": [],
            "keywords": [],
            "provider": "custom",
            "confidence": None
        }
        
        # Get transcription from Deepgram
        try:
            transcription_data = self._transcribe_audio(audio_url)
            log_entry["transcription"] = transcription_data.get("transcript")
            log_entry["confidence"] = transcription_data.get("confidence")
            log_entry["keywords"] = transcription_data.get("keywords", [])
        except Exception as e:
            logger.error(f"Deepgram transcription error: {e}")
        
        self.logs.append(log_entry)
    
    def add_twilio_call(self, call_sid: str, from_number: str, to_number: str, 
                       duration: float, status: str, timestamp: str, 
                       recording_url: str = None):
        """Add a Twilio call with detailed metadata."""
        log_entry = {
            "call_id": call_sid,
            "from": from_number,
            "to": to_number,
            "duration": duration,
            "status": status,
            "timestamp": timestamp,
            "provider": "twilio",
            "recording_url": recording_url,
            "call_cost": None,
            "call_quality": None,
            "transcription": None,
            "sentiment": None,
            "confidence": None
        }
        
        # Get call cost from Twilio
        try:
            call = twilio_client.calls(call_sid).fetch()
            log_entry["call_cost"] = float(call.price) if call.price else 0
            log_entry["call_quality"] = call.price  # Placeholder
        except Exception as e:
            logger.error(f"Twilio API error: {e}")
        
        self.logs.append(log_entry)
    
    def _transcribe_audio(self, audio_url: str) -> Dict[str, Any]:
        """Transcribe audio using Deepgram."""
        # This is a placeholder - implement actual Deepgram API call
        return {
            "transcript": "Sample transcript",
            "confidence": 0.95,
            "keywords": ["keyword1", "keyword2"]
        }
    
    def get_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get summary statistics including Deepgram and Twilio data."""
        cutoff = datetime.now() - timedelta(days=days)
        recent_logs = [
            log for log in self.logs
            if datetime.fromisoformat(log["timestamp"]) > cutoff
        ]
        
        total_calls = len(recent_logs)
        successful = sum(1 for log in recent_logs if log["status"] == "completed")
        failed = sum(1 for log in recent_logs if log["status"] == "failed")
        avg_duration = sum(log["duration"] for log in recent_logs) / total_calls if total_calls > 0 else 0
        
        # Deepgram analytics
        transcribed = sum(1 for log in recent_logs if log.get("transcription"))
        avg_confidence = sum(log.get("confidence", 0) for log in recent_logs if log.get("confidence")) / transcribed if transcribed > 0 else 0
        
        # Twilio analytics
        total_cost = sum(float(log.get("call_cost", 0)) for log in recent_logs)
        
        return {
            "total_calls": total_calls,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total_calls * 100) if total_calls > 0 else 0,
            "average_duration": round(avg_duration, 2),
            "period_days": days,
            "deepgram": {
                "transcribed_calls": transcribed,
                "average_confidence": round(avg_confidence * 100, 2),
                "transcription_rate": (transcribed / total_calls * 100) if total_calls > 0 else 0
            },
            "twilio": {
                "total_cost": round(total_cost, 4),
                "average_call_cost": round(total_cost / total_calls, 4) if total_calls > 0 else 0
            }
        }
    
    def get_call_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get detailed analytics combining Deepgram and Twilio data."""
        cutoff = datetime.now() - timedelta(days=days)
        recent_logs = [
            log for log in self.logs
            if datetime.fromisoformat(log["timestamp"]) > cutoff
        ]
        
        # Status breakdown
        status_breakdown = {}
        for log in recent_logs:
            status = log["status"]
            status_breakdown[status] = status_breakdown.get(status, 0) + 1
        
        # Provider breakdown
        provider_breakdown = {}
        for log in recent_logs:
            provider = log.get("provider", "custom")
            provider_breakdown[provider] = provider_breakdown.get(provider, 0) + 1
        
        # Hourly trends
        hourly_data = {}
        for log in recent_logs:
            hour = datetime.fromisoformat(log["timestamp"]).strftime("%Y-%m-%d %H:00")
            hourly_data[hour] = hourly_data.get(hour, 0) + 1
        
        # Deepgram sentiment analysis
        sentiment_breakdown = {}
        for log in recent_logs:
            if log.get("sentiment"):
                sentiment = log["sentiment"]
                sentiment_breakdown[sentiment] = sentiment_breakdown.get(sentiment, 0) + 1
        
        return {
            "status_breakdown": status_breakdown,
            "provider_breakdown": provider_breakdown,
            "hourly_trends": dict(sorted(hourly_data.items())),
            "sentiment_breakdown": sentiment_breakdown,
            "total": len(recent_logs)
        }
    
    def search_transcriptions(self, query: str, days: int = 7) -> List[Dict]:
        """Search across all transcriptions."""
        cutoff = datetime.now() - timedelta(days=days)
        results = []
        
        for log in self.logs:
            if datetime.fromisoformat(log["timestamp"]) > cutoff:
                if log.get("transcription") and query.lower() in log["transcription"].lower():
                    results.append({
                        "call_id": log["call_id"],
                        "transcription": log["transcription"],
                        "timestamp": log["timestamp"],
                        "duration": log["duration"],
                        "confidence": log.get("confidence")
                    })
        
        return results


# Initialize aggregator
aggregator = EnhancedCallLogAggregator()


@app.route('/')
def dashboard():
    """Render main dashboard."""
    return render_template('dashboard.html')


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get paginated call logs with enriched data."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status_filter = request.args.get('status', None)
    provider_filter = request.args.get('provider', None)
    
    filtered_logs = aggregator.logs
    if status_filter:
        filtered_logs = [log for log in filtered_logs if log["status"] == status_filter]
    if provider_filter:
        filtered_logs = [log for log in filtered_logs if log.get("provider") == provider_filter]
    
    # Sort by timestamp (newest first)
    filtered_logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Paginate
    start = (page - 1) * per_page
    end = start + per_page
    paginated = filtered_logs[start:end]
    
    return jsonify({
        "logs": paginated,
        "total": len(filtered_logs),
        "page": page,
        "per_page": per_page,
        "pages": (len(filtered_logs) + per_page - 1) // per_page
    })


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get enhanced dashboard summary with Deepgram and Twilio metrics."""
    days = request.args.get('days', 7, type=int)
    summary = aggregator.get_summary(days=days)
    return jsonify(summary)


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get detailed analytics combining multiple data sources."""
    days = request.args.get('days', 7, type=int)
    analytics = aggregator.get_call_analytics(days=days)
    return jsonify(analytics)


@app.route('/api/transcriptions/search', methods=['GET'])
def search_transcriptions():
    """Search across transcriptions from Deepgram."""
    query = request.args.get('q', '')
    days = request.args.get('days', 7, type=int)
    
    if not query or len(query) < 3:
        return jsonify({"error": "Query must be at least 3 characters"}), 400
    
    results = aggregator.search_transcriptions(query, days=days)
    return jsonify({
        "query": query,
        "results": results,
        "count": len(results)
    })


@app.route('/api/call/<call_id>/transcription', methods=['GET'])
def get_call_transcription(call_id):
    """Get detailed transcription for a specific call."""
    for log in aggregator.logs:
        if log["call_id"] == call_id:
            return jsonify({
                "call_id": call_id,
                "transcription": log.get("transcription"),
                "confidence": log.get("confidence"),
                "keywords": log.get("keywords", []),
                "entities": log.get("entities", []),
                "sentiment": log.get("sentiment"),
                "duration": log.get("duration"),
                "timestamp": log.get("timestamp")
            })
    
    return jsonify({"error": "Call not found"}), 404


@app.route('/api/call/<call_id>/recording', methods=['GET'])
def get_call_recording(call_id):
    """Get recording URL for a specific call (Twilio)."""
    for log in aggregator.logs:
        if log["call_id"] == call_id:
            return jsonify({
                "call_id": call_id,
                "recording_url": log.get("recording_url"),
                "duration": log.get("duration"),
                "format": "wav"
            })
    
    return jsonify({"error": "Call not found"}), 404


@app.route('/api/twilio/incoming', methods=['POST'])
def twilio_incoming():
    """Handle incoming Twilio calls."""
    try:
        call_sid = request.form.get('CallSid')
        from_number = request.form.get('From')
        to_number = request.form.get('To')
        
        logger.info(f"Incoming call: {call_sid} from {from_number} to {to_number}")
        
        # Log the call
        aggregator.add_twilio_call(
            call_sid=call_sid,
            from_number=from_number,
            to_number=to_number,
            duration=0,
            status="active",
            timestamp=datetime.now().isoformat()
        )
        
        # Return TwiML response
        twiml_response = '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Thank you for calling</Say></Response>'
        return twiml_response, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        logger.error(f"Error handling incoming call: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/twilio/status', methods=['POST'])
def twilio_status():
    """Handle Twilio status callbacks."""
    try:
        call_sid = request.form.get('CallSid')
        call_status = request.form.get('CallStatus')
        call_duration = request.form.get('CallDuration', 0)
        
        logger.info(f"Call status update: {call_sid} - {call_status} - Duration: {call_duration}s")
        
        # Update call in aggregator
        for log in aggregator.logs:
            if log.get('call_id') == call_sid:
                log['status'] = call_status
                log['duration'] = float(call_duration)
                break
        
        return 'OK', 200
    except Exception as e:
        logger.error(f"Error handling status callback: {e}")
        return 'ERROR', 500


@app.route('/api/deepgram/callback', methods=['POST'])
def deepgram_callback():
    """Handle Deepgram transcription callbacks."""
    try:
        data = request.get_json()
        
        # Extract transcription data
        call_id = data.get('metadata', {}).get('call_id')
        channels = data.get('results', {}).get('channels', [])
        
        if channels and len(channels) > 0:
            alternatives = channels[0].get('alternatives', [])
            if alternatives and len(alternatives) > 0:
                transcript = alternatives[0].get('transcript')
                confidence = alternatives[0].get('confidence')
                
                # Update call log
                for log in aggregator.logs:
                    if log['call_id'] == call_id:
                        log['transcription'] = transcript
                        log['confidence'] = confidence
                        logger.info(f"Updated transcription for {call_id}")
                        break
        
        return jsonify({"status": "received"}), 200
    except Exception as e:
        logger.error(f"Error handling Deepgram callback: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_logs": len(aggregator.logs),
        "deepgram": "connected" if DEEPGRAM_API_KEY and DEEPGRAM_API_KEY != 'your-deepgram-api-key' else "not configured",
        "twilio": "connected" if TWILIO_ACCOUNT_SID and TWILIO_ACCOUNT_SID != 'your-twilio-account-sid' else "not configured"
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

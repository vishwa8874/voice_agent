"""
White-labeled dashboard for voice agent call logs.
Abstracts underlying tech stack and provides branded interface.
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
from typing import List, Dict, Any
import logging

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CallLogAggregator:
    """Aggregates call logs from various sources without exposing tech stack."""
    
    def __init__(self):
        self.logs = []
    
    def add_log(self, call_id: str, duration: float, status: str, 
                timestamp: str, user_id: str = None, metadata: Dict = None):
        """Add a call log entry."""
        log_entry = {
            "call_id": call_id,
            "duration": duration,
            "status": status,
            "timestamp": timestamp,
            "user_id": user_id or "Anonymous",
            "metadata": metadata or {}
        }
        self.logs.append(log_entry)
    
    def get_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get summary statistics."""
        cutoff = datetime.now() - timedelta(days=days)
        recent_logs = [
            log for log in self.logs
            if datetime.fromisoformat(log["timestamp"]) > cutoff
        ]
        
        total_calls = len(recent_logs)
        successful = sum(1 for log in recent_logs if log["status"] == "completed")
        failed = sum(1 for log in recent_logs if log["status"] == "failed")
        avg_duration = sum(log["duration"] for log in recent_logs) / total_calls if total_calls > 0 else 0
        
        return {
            "total_calls": total_calls,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total_calls * 100) if total_calls > 0 else 0,
            "average_duration": round(avg_duration, 2),
            "period_days": days
        }


# Initialize aggregator
aggregator = CallLogAggregator()


@app.route('/')
def dashboard():
    """Render main dashboard."""
    return render_template('dashboard.html')


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get paginated call logs."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    status_filter = request.args.get('status', None)
    
    filtered_logs = aggregator.logs
    if status_filter:
        filtered_logs = [log for log in filtered_logs if log["status"] == status_filter]
    
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
    """Get dashboard summary statistics."""
    days = request.args.get('days', 7, type=int)
    summary = aggregator.get_summary(days=days)
    return jsonify(summary)


@app.route('/api/logs/stats', methods=['GET'])
def get_stats():
    """Get detailed statistics and trends."""
    days = request.args.get('days', 7, type=int)
    cutoff = datetime.now() - timedelta(days=days)
    
    recent_logs = [
        log for log in aggregator.logs
        if datetime.fromisoformat(log["timestamp"]) > cutoff
    ]
    
    # Group by status
    status_breakdown = {}
    for log in recent_logs:
        status = log["status"]
        status_breakdown[status] = status_breakdown.get(status, 0) + 1
    
    # Hourly trends
    hourly_data = {}
    for log in recent_logs:
        hour = datetime.fromisoformat(log["timestamp"]).strftime("%Y-%m-%d %H:00")
        hourly_data[hour] = hourly_data.get(hour, 0) + 1
    
    return jsonify({
        "status_breakdown": status_breakdown,
        "hourly_trends": dict(sorted(hourly_data.items())),
        "total": len(recent_logs)
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_logs": len(aggregator.logs)
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

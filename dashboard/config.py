"""
Configuration settings for white-labeled dashboard.
Customize branding, colors, and behavior here.
"""

# Application Settings
APP_NAME = "Call Analytics"
APP_VERSION = "1.0.0"
DEBUG = False
SECRET_KEY = "your-secret-key-here-change-in-production"

# Server Settings
HOST = "0.0.0.0"
PORT = 5000
WORKERS = 4

# Dashboard Settings
DEFAULT_TIME_RANGE_DAYS = 7
LOGS_PER_PAGE = 50
AUTO_REFRESH_INTERVAL = 5  # minutes

# Branding (Customize these for white-label)
BRAND_NAME = "Call Analytics"
BRAND_SUBTITLE = "Professional Call Management Dashboard"
BRAND_COLOR_PRIMARY = "#2c3e50"
BRAND_COLOR_SECONDARY = "#3498db"
BRAND_COLOR_SUCCESS = "#27ae60"
BRAND_COLOR_DANGER = "#e74c3c"

# Features
ENABLE_EXPORT = True
ENABLE_REPORTS = True
ENABLE_ALERTS = False

# Data Retention (days)
LOG_RETENTION_DAYS = 90

# API Configuration
API_RATE_LIMIT = 100  # requests per minute
API_TIMEOUT = 30  # seconds

# Security
CORS_ENABLED = False
ALLOWED_ORIGINS = ["localhost:5000"]
REQUIRE_AUTH = False

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "dashboard.log"

# Database (optional - for future expansion)
DATABASE_URL = None

# Third-party integrations
SLACK_WEBHOOK_URL = None
EMAIL_ALERTS_ENABLED = False

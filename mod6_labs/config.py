# config.py
"""Configuration management for the Weather App."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration."""
    
    # API Configuration
    API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    BASE_URL = os.getenv(
        "OPENWEATHER_BASE_URL", 
        "https://api.openweathermap.org/data/2.5/weather"
    )
    FORECAST_URL = os.getenv(
        "OPENWEATHER_FORECAST_URL", 
        "https://api.openweathermap.org/data/2.5/forecast"
    )
    
    # App Configuration
    APP_TITLE = "Weather App"
    APP_WIDTH = 430
    APP_HEIGHT = 932
    
    # API Settings
    UNITS = "metric"  # metric, imperial, or standard
    TIMEOUT = 10  # seconds
    IP_API_URL = "https://ipapi.co/json/"
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.API_KEY:
            raise ValueError(
                "OPENWEATHER_API_KEY not found. "
                "Please create a .env file with your API key."
            )
        return True

# Validate configuration on import
Config.validate()
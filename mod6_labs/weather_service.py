"""Weather API service layer."""

import httpx
from typing import Dict, Optional
from config import Config


class WeatherServiceError(Exception):
    """Custom exception for weather service errors."""
    pass


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = Config.API_KEY
        self.base_url = Config.BASE_URL
        self.forecast_url = Config.FORECAST_URL
        self.timeout = Config.TIMEOUT
    
    async def get_weather(self, city: str, units: Optional[str] = None) -> Dict:
        """
        Fetch weather data for a given city.
        """
        if not city:
            raise WeatherServiceError("City name cannot be empty")
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units or Config.UNITS,
        }
        
        # specific_error_context allows us to customize the 404 message
        return await self._make_request(
            self.base_url, 
            params, 
            city_context=city
        )
    
    async def get_weather_by_coordinates(self, lat: float, lon: float) -> Dict:
        """
        Fetch weather data by coordinates.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": Config.UNITS,
        }
        return await self._make_request(self.base_url, params)
    
    async def get_forecast(self, city: str, units: Optional[str] = None) -> Dict:
        """
        Get 5-day weather forecast.
        """
        if not city:
            raise WeatherServiceError("City name cannot be empty")
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units or Config.UNITS,
        }
        
        return await self._make_request(
            self.forecast_url, 
            params, 
            city_context=city
        )

    async def get_forecast_by_coordinates(self, lat: float, lon: float) -> Dict:
        """Fetch forecast data by coordinates."""
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": Config.UNITS,
        }
        return await self._make_request(self.forecast_url, params)

    async def _make_request(
        self, 
        url: str, 
        params: Dict, 
        city_context: Optional[str] = None
    ) -> Dict:
        """
        Helper method to handle HTTP requests and standardize error handling.
        
        Args:
            url: The API endpoint URL
            params: Query parameters
            city_context: Optional city name to provide better 404 error messages
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                
                # Handle specific HTTP status codes
                if response.status_code == 404:
                    msg = (f"City '{city_context}' not found. Please check the spelling." 
                           if city_context else "Location not found.")
                    raise WeatherServiceError(msg)
                    
                elif response.status_code == 401:
                    raise WeatherServiceError(
                        "Invalid API key. Please check your configuration."
                    )
                
                elif response.status_code >= 500:
                    raise WeatherServiceError(
                        "Weather service is currently unavailable. Please try again later."
                    )
                
                elif response.status_code != 200:
                    raise WeatherServiceError(f"Error: {response.status_code}")
                
                return response.json()
                
        except httpx.TimeoutException:
            raise WeatherServiceError(
                "Request timed out. Please check your internet connection."
            )
        except httpx.NetworkError:
            raise WeatherServiceError(
                "Network error. Please check your internet connection."
            )
        except httpx.HTTPError as e:
            raise WeatherServiceError(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            raise WeatherServiceError(f"An unexpected error occurred: {str(e)}")
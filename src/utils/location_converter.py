"""
Location Converter Module for Stoppage Reports
Converts latitude/longitude coordinates to readable location names using reverse geocoding.
"""

import re
import requests
import time
from typing import Tuple, Optional, Dict, Any
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocationConverter:
    """
    Convert latitude/longitude coordinates to readable location names.
    Supports multiple geocoding services with fallback options.
    """
    
    def __init__(self):
        self.cache = {}
        self.request_count = 0
        self.last_request_time = 0
        
    def parse_location_string(self, location_str: str) -> Optional[Tuple[float, float]]:
        """
        Parse location string in format "latitude/longitude" to extract coordinates.
        
        Args:
            location_str: String in format "28.7041/77.1025" or similar
            
        Returns:
            Tuple of (latitude, longitude) or None if parsing fails
        """
        if not location_str or not isinstance(location_str, str):
            return None
            
        try:
            # Handle format "latitude/longitude"
            if '/' in location_str:
                parts = location_str.strip().split('/')
                if len(parts) == 2:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return (lat, lon)
            
            # Handle format "latitude,longitude" 
            elif ',' in location_str:
                parts = location_str.strip().split(',')
                if len(parts) == 2:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return (lat, lon)
                    
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to parse location string '{location_str}': {e}")
            
        return None
    
    def _rate_limit(self, min_interval: float = 1.0):
        """Simple rate limiting to avoid overwhelming geocoding services."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            time.sleep(sleep_time)
            
        self.last_request_time = time.time()
        
    @lru_cache(maxsize=500)
    def _cached_reverse_geocode(self, lat: float, lon: float) -> Optional[str]:
        """Cached version of reverse geocoding to avoid repeated API calls."""
        return self._reverse_geocode_nominatim(lat, lon)
    
    def _reverse_geocode_nominatim(self, lat: float, lon: float) -> Optional[str]:
        """
        Use OpenStreetMap Nominatim service for reverse geocoding (free, no API key needed).
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            Human-readable location name or None if failed
        """
        try:
            self._rate_limit(1.1)  # Nominatim requires minimum 1 second between requests
            
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                'lat': lat,
                'lon': lon,
                'format': 'json',
                'zoom': 10,  # City/town level
                'addressdetails': 1,
                'extratags': 1
            }
            
            headers = {
                'User-Agent': 'FleetManagementSystem/1.0 (contact@company.com)'  # Required by Nominatim
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and 'display_name' in data:
                # Extract meaningful location components
                address = data.get('address', {})
                
                location_parts = []
                
                # Priority order for location components
                for key in ['village', 'town', 'city', 'municipality', 'district', 'county']:
                    if key in address and address[key]:
                        location_parts.append(address[key])
                        break
                
                # Add state/region
                for key in ['state', 'region', 'province']:
                    if key in address and address[key]:
                        location_parts.append(address[key])
                        break
                
                # Add country for international locations
                if 'country' in address and address['country']:
                    if address['country'] != 'India':  # Only show country if not India
                        location_parts.append(address['country'])
                
                if location_parts:
                    readable_location = ', '.join(location_parts)
                    logger.info(f"Geocoded ({lat}, {lon}) -> {readable_location}")
                    return readable_location
                else:
                    # Fallback to display_name but clean it up
                    display_name = data['display_name']
                    # Take first 3 components (usually most relevant)
                    parts = display_name.split(',')[:3]
                    return ', '.join(parts).strip()
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Nominatim API error for ({lat}, {lon}): {e}")
        except Exception as e:
            logger.error(f"Unexpected error in reverse geocoding ({lat}, {lon}): {e}")
            
        return None
    
    def _reverse_geocode_google(self, lat: float, lon: float, api_key: str) -> Optional[str]:
        """
        Use Google Maps Geocoding API for reverse geocoding (requires API key).
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            api_key: Google Maps API key
            
        Returns:
            Human-readable location name or None if failed
        """
        try:
            self._rate_limit(0.1)  # Google allows more requests per second
            
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'latlng': f"{lat},{lon}",
                'key': api_key,
                'result_type': 'locality|administrative_area_level_2|administrative_area_level_1'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                # Get the most specific result
                result = data['results'][0]
                formatted_address = result.get('formatted_address', '')
                
                # Clean up the address (remove postal codes, etc.)
                # Take meaningful parts before postal codes
                parts = formatted_address.split(',')
                clean_parts = []
                
                for part in parts:
                    part = part.strip()
                    # Skip postal codes and numbers
                    if not re.match(r'^\d+', part) and len(part) > 1:
                        clean_parts.append(part)
                        if len(clean_parts) >= 3:  # Limit to 3 parts
                            break
                
                if clean_parts:
                    readable_location = ', '.join(clean_parts)
                    logger.info(f"Google geocoded ({lat}, {lon}) -> {readable_location}")
                    return readable_location
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Google Maps API error for ({lat}, {lon}): {e}")
        except Exception as e:
            logger.error(f"Unexpected error in Google reverse geocoding ({lat}, {lon}): {e}")
            
        return None
    
    def convert_coordinates_to_location(self, lat: float, lon: float, google_api_key: Optional[str] = None) -> str:
        """
        Convert latitude/longitude to readable location name with fallback options.
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            google_api_key: Optional Google Maps API key for better accuracy
            
        Returns:
            Human-readable location name or formatted coordinates if conversion fails
        """
        # Input validation
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            logger.warning(f"Invalid coordinates: lat={lat}, lon={lon}")
            return f"Invalid Location ({lat}, {lon})"
        
        # Check cache first
        cache_key = f"{lat:.6f},{lon:.6f}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        readable_location = None
        
        # Try Google Maps first if API key is provided (more accurate)
        if google_api_key:
            readable_location = self._reverse_geocode_google(lat, lon, google_api_key)
        
        # Fallback to Nominatim (free but less accurate)
        if not readable_location:
            readable_location = self._cached_reverse_geocode(lat, lon)
        
        # Fallback to region-based naming for Indian coordinates
        if not readable_location:
            readable_location = self._get_region_name(lat, lon)
        
        # Final fallback - return formatted coordinates
        if not readable_location:
            readable_location = f"Location ({lat:.4f}, {lon:.4f})"
        
        # Cache the result
        self.cache[cache_key] = readable_location
        
        return readable_location
    
    def _get_region_name(self, lat: float, lon: float) -> Optional[str]:
        """
        Provide region-based names for common Indian coordinate ranges as fallback.
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            Region name or None
        """
        # Indian coordinate ranges (approximate)
        if 8.0 <= lat <= 37.6 and 68.7 <= lon <= 97.25:
            # Rough region mapping for India
            if 28.0 <= lat <= 32.0 and 75.0 <= lon <= 78.0:
                return "Punjab/Haryana Region"
            elif 26.0 <= lat <= 30.0 and 72.0 <= lon <= 78.0:
                return "Rajasthan Region"
            elif 23.0 <= lat <= 26.5 and 68.0 <= lon <= 74.0:
                return "Gujarat Region"
            elif 19.0 <= lat <= 21.0 and 72.0 <= lon <= 75.0:
                return "Maharashtra Region"
            elif 12.5 <= lat <= 16.0 and 74.0 <= lon <= 78.0:
                return "Karnataka Region"
            elif 25.0 <= lat <= 27.0 and 85.0 <= lon <= 88.0:
                return "West Bengal Region"
            elif 28.0 <= lat <= 30.0 and 77.0 <= lon <= 78.5:
                return "Delhi NCR Region"
            else:
                return "India"
        
        return None
    
    def convert_location_string(self, location_str: str, google_api_key: Optional[str] = None) -> str:
        """
        Convert location string (in format "lat/lon") to readable location name.
        
        Args:
            location_str: String in format "28.7041/77.1025"
            google_api_key: Optional Google Maps API key
            
        Returns:
            Human-readable location name
        """
        if not location_str:
            return "Unknown Location"
        
        coordinates = self.parse_location_string(location_str)
        if coordinates:
            lat, lon = coordinates
            return self.convert_coordinates_to_location(lat, lon, google_api_key)
        else:
            return f"Invalid Location ({location_str})"

# Global instance for easy import
location_converter = LocationConverter()

def convert_coordinates_to_readable_location(lat: float, lon: float, google_api_key: Optional[str] = None) -> str:
    """Convenience function for coordinate conversion."""
    return location_converter.convert_coordinates_to_location(lat, lon, google_api_key)

def convert_location_string_to_readable(location_str: str, google_api_key: Optional[str] = None) -> str:
    """Convenience function for location string conversion."""
    return location_converter.convert_location_string(location_str, google_api_key)

"""
Test script for location converter functionality
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

try:
    from src.utils.location_converter import LocationConverter, convert_location_string_to_readable
    
    def test_location_conversion():
        """Test various location conversion scenarios"""
        print("🧪 Testing Location Conversion System")
        print("=" * 50)
        
        converter = LocationConverter()
        
        # Test cases for different coordinate formats
        test_locations = [
            "28.7041/77.1025",  # Delhi area
            "19.0760/72.8777",  # Mumbai area  
            "22.5726/88.3639",  # Kolkata area
            "13.0827/80.2707",  # Chennai area
            "12.9716/77.5946",  # Bangalore area
            "23.0225/72.5714",  # Ahmedabad area
            "26.9124/75.7873",  # Jaipur area
            "30.7333/76.7794",  # Chandigarh area
        ]
        
        print("📍 Converting test coordinates to readable locations:")
        print("-" * 50)
        
        for location_str in test_locations:
            try:
                readable = convert_location_string_to_readable(location_str)
                print(f"✅ {location_str} → {readable}")
            except Exception as e:
                print(f"❌ {location_str} → Error: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Location conversion test completed!")
        
        # Test parsing functionality
        print("\n🔍 Testing coordinate parsing:")
        print("-" * 30)
        
        for location_str in test_locations[:3]:
            coords = converter.parse_location_string(location_str)
            if coords:
                lat, lon = coords
                print(f"📍 {location_str} → lat: {lat}, lon: {lon}")
            else:
                print(f"❌ Failed to parse: {location_str}")
    
    if __name__ == "__main__":
        test_location_conversion()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure the location converter module is properly installed.")

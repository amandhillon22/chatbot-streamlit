#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Distance Unit Detection and Conversion Utility
Handles smart detection of whether distance columns are in meters or kilometers
and provides conversion functions for the chatbot system.
"""

import re
from src.core.sql import db_manager, get_full_schema
import psycopg2

class DistanceUnitManager:
    def __init__(self):
        self.distance_columns = {}
        self.unit_hints = {}
        self._analyze_distance_columns()
    
    def _analyze_distance_columns(self):
        """Analyze all distance-related columns in the database to detect units."""
        print("🔍 Analyzing distance columns for unit detection...")
        
        schema_dict = get_full_schema()
        distance_keywords = ['distance', 'km', 'mile', 'meter', 'metre', 'mileage', 'odometer']
        
        # First pass: collect all distance columns and analyze names only
        distance_candidates = []
        
        for schema_name, tables in schema_dict.items():
            for table_name, columns in tables.items():
                table_key = f"{schema_name}.{table_name}"
                
                for col in columns:
                    col_lower = col.lower()
                    
                    # Check if this column likely contains distance data
                    if any(keyword in col_lower for keyword in distance_keywords):
                        column_key = f"{table_key}.{col}"
                        
                        # Determine likely unit based on column name
                        likely_unit = self._detect_unit_from_name(col_lower)
                        self.unit_hints[column_key] = likely_unit
                        
                        # Use name-based detection for now, avoid data sampling during startup
                        self.distance_columns[column_key] = likely_unit
                        
                        print(f"  📏 {column_key}: {likely_unit}")
                        
                        # Store for potential later data sampling
                        distance_candidates.append((schema_name, table_name, col, column_key))
        
        print(f"✅ Analyzed {len(self.distance_columns)} distance columns")
        
        # Optionally sample data for verification (but not during startup to avoid connection pool exhaustion)
        # This can be done lazily when needed or as a background task
        
        print(f"✅ Analyzed {len(self.distance_columns)} distance columns")
    
    def _detect_unit_from_name(self, column_name):
        """Detect likely unit from column name patterns."""
        column_name = column_name.lower()
        
        # Strong indicators for kilometers
        if any(keyword in column_name for keyword in ['km', 'kilometer', 'kilometre']):
            return 'kilometers'
        
        # Strong indicators for meters
        if any(keyword in column_name for keyword in ['meter', 'metre', 'm_', '_m', 'distance_m']):
            return 'meters'
        
        # Mileage usually in kilometers for vehicles
        if 'mileage' in column_name or 'odometer' in column_name:
            return 'kilometers'
        
        # Default assumption for transportation data
        return 'meters'  # Most distance data stored in meters
    
    def _detect_unit_from_data(self, schema_name, table_name, column_name):
        """Sample data to detect if values are in meters or kilometers."""
        try:
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    # Get sample non-null values
                    cur.execute(f"""
                        SELECT {column_name} 
                        FROM {schema_name}.{table_name} 
                        WHERE {column_name} IS NOT NULL 
                          AND {column_name} > 0 
                        ORDER BY RANDOM() 
                        LIMIT 10;
                    """)
                    
                    results = cur.fetchall()
            
            if not results:
                return None
            
            values = [float(row[0]) for row in results if row[0] is not None]
            if not values:
                return None
            
            avg_value = sum(values) / len(values)
            max_value = max(values)
            
            # Heuristic: If average > 1000 or max > 10000, likely meters
            # If average < 1000 and max < 5000, likely kilometers
            if avg_value > 1000 or max_value > 10000:
                return 'meters'
            elif avg_value < 1000 and max_value < 5000:
                return 'kilometers'
            else:
                # Ambiguous - use name-based detection
                return None
                
        except Exception as e:
            print(f"⚠️ Could not sample data for {schema_name}.{table_name}.{column_name}: {e}")
            return None
    
    def verify_column_unit_with_data(self, column_key):
        """Verify a specific column's unit by sampling data (use sparingly to avoid connection pool exhaustion)."""
        if column_key not in self.distance_columns:
            return None
            
        # Parse column key
        parts = column_key.split('.')
        if len(parts) != 3:
            return None
        schema_name, table_name, column_name = parts
        
        # Sample data to verify unit
        actual_unit = self._detect_unit_from_data(schema_name, table_name, column_name)
        
        if actual_unit:
            # Update our stored unit if data suggests different unit
            self.distance_columns[column_key] = actual_unit
            return actual_unit
        
        return self.distance_columns[column_key]
    
    def get_distance_columns_for_table(self, schema_name, table_name):
        """Get all distance columns for a specific table with their units."""
        table_key = f"{schema_name}.{table_name}"
        table_columns = {}
        
        for column_key, unit in self.distance_columns.items():
            if column_key.startswith(f"{table_key}."):
                column_name = column_key.split('.')[-1]
                table_columns[column_name] = unit
        
        return table_columns
    
    def generate_conversion_sql(self, column_name, unit, target_unit='kilometers'):
        """Generate SQL for distance conversion."""
        if unit == target_unit:
            return column_name
        
        if unit == 'meters' and target_unit == 'kilometers':
            return f"ROUND(({column_name}::NUMERIC / 1000), 2)"
        elif unit == 'kilometers' and target_unit == 'meters':
            return f"ROUND(({column_name}::NUMERIC * 1000), 0)"
        else:
            return column_name
    
    def get_conversion_instructions(self):
        """Get instructions for the LLM about distance conversions."""
        instructions = """
🚩 DISTANCE UNIT CONVERSION INSTRUCTIONS:

**Default Storage**: Most distance values in this database are stored in METERS.

**Automatic Conversion Rules**:
1. When user asks for distances in "kilometers" or "km", convert meters to km using: `ROUND((column_name::NUMERIC / 1000), 2)`
2. When user asks for distances in "meters" or "m", use values as-is if already in meters
3. For vehicle mileage/odometer readings, these are usually already in kilometers

**Column Detection**:
"""
        
        # Add detected columns
        for column_key, unit in self.distance_columns.items():
            instructions += f"- {column_key}: {unit}\n"
        
        instructions += """
**Usage Examples**:
- "total distance in km" → Use conversion: `ROUND((distance_column::NUMERIC / 1000), 2) AS distance_km`
- "show mileage" → Usually already in km, use as-is
- "distance covered in meters" → Use raw values if stored in meters

**Smart Detection**: The system automatically detects units based on:
1. Column names (km, meter, distance, etc.)
2. Data sampling (values > 1000 likely meters, < 1000 likely km)
3. Context (vehicle mileage usually km, GPS coordinates usually meters)
"""
        return instructions

# Global instance
distance_manager = DistanceUnitManager()

def get_distance_conversion_info():
    """Get distance conversion information for the query agent."""
    return distance_manager.get_conversion_instructions()

def get_distance_columns_info(schema_name, table_name):
    """Get distance column information for a specific table."""
    return distance_manager.get_distance_columns_for_table(schema_name, table_name)

if __name__ == "__main__":
    print("🚀 Testing Distance Unit Detection System")
    print("=" * 50)
    
    # Show detected distance columns
    for column_key, unit in distance_manager.distance_columns.items():
        print(f"{column_key}: {unit}")
    
    print("\n" + "=" * 50)
    print("📋 Conversion Instructions:")
    print(distance_manager.get_conversion_instructions())

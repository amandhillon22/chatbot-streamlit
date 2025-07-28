#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

EONINFOTECH Data Masking Utility
Centralized utility for masking EONINFOTECH references throughout the system
"""

import re
import json
from typing import Dict, List, Any, Union

class EoninfotechDataMasker:
    """
    Utility class for masking EONINFOTECH references in data, SQL, and responses.
    
    CRITICAL: EONINFOTECH is used internally to mark inactive vehicles.
    This should NEVER be displayed to users. Instead, show as:
    - Regions/Zones: "Inactive Region"
    - Status: "Inactive" 
    - Any reference: Hide or replace with business-friendly terms
    """
    
    def __init__(self):
        self.eoninfotech_variants = [
            'EONINFOTECH', 'eoninfotech', 'Eoninfotech',
            'EON INFOTECH', 'eon infotech', 'Eon InfoTech',
            'EON INFO TECH', 'eon info tech', 'Eon Info Tech'
        ]
        
        # EON OFFICE - Special case: vehicles are REMOVED (device removed)
        self.eon_office_variants = [
            'EON OFFICE', 'eon office', 'Eon Office',
            'EON_OFFICE', 'eon_office', 'Eon_Office'
        ]
        
        # Column types that need specific masking
        self.region_columns = [
            'region_name', 'district_name', 'zone_name', 'area_name',
            'location', 'region', 'district', 'zone', 'area'
        ]
        
        self.status_columns = [
            'status', 'vehicle_status', 'active_status', 'operational_status',
            'state', 'condition'
        ]
        
        self.plant_columns = [
            'plant_name', 'facility_name', 'plant', 'facility'
        ]
    
    def is_eoninfotech_reference(self, value: Any) -> bool:
        """Check if a value contains EONINFOTECH reference"""
        if not isinstance(value, str):
            return False
        
        return any(variant.lower() in value.lower() for variant in self.eoninfotech_variants)
    
    def is_eon_office_reference(self, value: Any) -> bool:
        """Check if a value contains EON OFFICE reference"""
        if not isinstance(value, str):
            return False
        
        return any(variant.lower() in value.lower() for variant in self.eon_office_variants)
    
    def mask_single_value(self, value: Any, column_name: str = None) -> Any:
        """Mask a single value if it contains EONINFOTECH"""
        if not self.is_eoninfotech_reference(value):
            return value
            
        # Determine appropriate replacement based on column type
        if column_name:
            column_lower = column_name.lower()
            
            if any(region_col in column_lower for region_col in self.region_columns):
                return 'Inactive Region'
            elif any(status_col in column_lower for status_col in self.status_columns):
                return 'Inactive'
        
        # Default replacement
        return 'Inactive'
    
    def mask_data_row(self, data_row: Dict) -> Dict:
        """Mask EONINFOTECH references in a single data row"""
        if not isinstance(data_row, dict):
            return data_row
            
        masked_row = data_row.copy()
        eoninfotech_detected = False
        eon_office_detected = False
        
        # First check if this is an EON OFFICE vehicle (special case)
        eon_office_detected = self.is_removed_vehicle(data_row)
        
        # Check and mask each field
        for key, value in masked_row.items():
            if self.is_eoninfotech_reference(value):
                eoninfotech_detected = True
                masked_row[key] = self.mask_single_value(value, key)
            elif self.is_eon_office_reference(value):
                eon_office_detected = True
                if any(plant_col in key.lower() for plant_col in self.plant_columns):
                    masked_row[key] = 'Removed Facility'
        
        # Apply appropriate status based on detection
        if eon_office_detected:
            # EON OFFICE vehicles: mark as REMOVED
            for status_col in self.status_columns:
                if status_col in masked_row:
                    masked_row[status_col] = 'Device Removed'
            
            # Add status if no status column exists
            if not any(col in masked_row for col in self.status_columns):
                masked_row['status'] = 'Device Removed'
                
        elif eoninfotech_detected:
            # Regular EONINFOTECH vehicles: mark as inactive
            for status_col in self.status_columns:
                if status_col in masked_row:
                    masked_row[status_col] = 'Inactive'
            
            # Add status if no status column exists
            if not any(col in masked_row for col in self.status_columns):
                masked_row['status'] = 'Inactive'
        
        return masked_row
    
    def mask_data_list(self, data_list: List[Dict]) -> List[Dict]:
        """Mask EONINFOTECH references in a list of data rows"""
        if not isinstance(data_list, list):
            return data_list
            
        return [self.mask_data_row(row) for row in data_list]
    
    def mask_sql_query(self, sql_query: str) -> str:
        """Add CASE statements to mask EONINFOTECH in SQL results"""
        if not sql_query or not isinstance(sql_query, str):
            return sql_query
            
        masked_sql = sql_query
        
        # Patterns for common column selections that need masking
        masking_patterns = [
            # District/Region names
            (r'(dm\.name\s+as\s+region_name)', 
             "CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as region_name"),
            (r'(dm\.name\s+as\s+district_name)', 
             "CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as district_name"),
            
            # Zone names  
            (r'(zm\.zone_name)', 
             "CASE WHEN zm.zone_name = 'EONINFOTECH' THEN 'Inactive Region' ELSE zm.zone_name END as zone_name"),
            
            # Plant names - special handling for EON OFFICE
            (r'(hm\.name\s+as\s+plant_name)', 
             "CASE WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Removed Facility' WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Facility' ELSE hm.name END as plant_name"),
            
            # Generic district/region references
            (r'(\bdm\.name\b)(?!\s+as|\')', 
             "CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END"),
        ]
        
        for pattern, replacement in masking_patterns:
            masked_sql = re.sub(pattern, replacement, masked_sql, flags=re.IGNORECASE)
        
        # Add status column if vehicle queries don't have it
        if 'vehicle_master vm' in masked_sql and 'SELECT' in masked_sql.upper():
            if not re.search(r'\bstatus\b', masked_sql, re.IGNORECASE):
                # Find the SELECT clause and add status with EON OFFICE handling
                select_match = re.search(r'SELECT\s+(.*?)\s+FROM', masked_sql, re.IGNORECASE | re.DOTALL)
                if select_match and 'vm.reg_no' in select_match.group(1):
                    select_part = select_match.group(1).strip()
                    new_select = select_part + """, 
                        CASE 
                            WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Device Removed'
                            WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' 
                            ELSE COALESCE(vm.status, 'Active') 
                        END as status"""
                    masked_sql = masked_sql.replace(select_part, new_select)
        
        return masked_sql
    
    def mask_query_result(self, query_result: Dict) -> Dict:
        """Mask EONINFOTECH references in a complete query result"""
        if not isinstance(query_result, dict):
            return query_result
            
        masked_result = query_result.copy()
        
        # Mask data rows
        if 'rows' in masked_result and isinstance(masked_result['rows'], list):
            masked_result['rows'] = self.mask_data_list(masked_result['rows'])
        
        # Mask column headers/metadata
        if 'columns' in masked_result:
            masked_columns = []
            for col in masked_result['columns']:
                if isinstance(col, dict) and 'name' in col:
                    col_copy = col.copy()
                    if self.is_eoninfotech_reference(col['name']):
                        col_copy['name'] = col['name'].replace('EONINFOTECH', 'Inactive_Region').replace('eoninfotech', 'inactive_region')
                    masked_columns.append(col_copy)
                else:
                    masked_columns.append(col)
            masked_result['columns'] = masked_columns
        
        return masked_result
    
    def mask_text_response(self, text_response: str) -> str:
        """Mask EONINFOTECH references in text responses"""
        if not isinstance(text_response, str):
            return text_response
            
        masked_text = text_response
        
        # Replace all variants with business-friendly terms
        for variant in self.eoninfotech_variants:
            # In context of regions/locations
            if 'region' in masked_text.lower() or 'zone' in masked_text.lower() or 'district' in masked_text.lower():
                masked_text = masked_text.replace(variant, 'Inactive Region')
            else:
                # General replacement
                masked_text = masked_text.replace(variant, 'inactive vehicles area')
        
        return masked_text
    
    def should_apply_masking(self, query_text: str = None, data: Any = None) -> bool:
        """Determine if EONINFOTECH masking should be applied"""
        # Check query text
        if query_text and self.contains_eoninfotech_reference(query_text):
            return True
        
        # Check data content
        if data:
            if isinstance(data, dict):
                return any(self.is_eoninfotech_reference(v) for v in data.values())
            elif isinstance(data, list):
                return any(self.should_apply_masking(data=item) for item in data)
            elif isinstance(data, str):
                return self.is_eoninfotech_reference(data)
        
        return False
    
    def contains_eoninfotech_reference(self, text: str) -> bool:
        """Check if text contains any EONINFOTECH reference"""
        if not isinstance(text, str):
            return False
        
        return any(variant.lower() in text.lower() for variant in self.eoninfotech_variants)
    
    def create_masked_where_clause(self, original_where: str) -> str:
        """Create WHERE clause that handles EONINFOTECH queries appropriately"""
        if not self.contains_eoninfotech_reference(original_where):
            return original_where
        
        # For EONINFOTECH queries, modify to search for the actual database value
        # but results will be masked in the output
        masked_where = original_where
        
        for variant in self.eoninfotech_variants:
            if variant.lower() in original_where.lower():
                # Add condition to include EONINFOTECH data but mark as inactive
                masked_where = f"({original_where} OR dm.name = 'EONINFOTECH')"
                break
        
        return masked_where
    
    def is_removed_vehicle(self, data_row: Dict) -> bool:
        """Check if a vehicle should be considered REMOVED (EON OFFICE)"""
        if not isinstance(data_row, dict):
            return False
        
        # Check if any plant/facility field contains EON OFFICE
        for key, value in data_row.items():
            if any(plant_col in key.lower() for plant_col in self.plant_columns):
                if self.is_eon_office_reference(value):
                    return True
                    
        # Also check if in EONINFOTECH region AND plant contains "office"
        has_eoninfotech_region = any(
            (any(region_col in key.lower() for region_col in self.region_columns) and 
             self.is_eoninfotech_reference(value))
            for key, value in data_row.items()
        )
        
        has_office_plant = any(
            (any(plant_col in key.lower() for plant_col in self.plant_columns) and 
             isinstance(value, str) and 'office' in value.lower())
            for key, value in data_row.items()
        )
        
        return has_eoninfotech_region and has_office_plant
    
    def should_hide_vehicle_details(self, vehicle_data: Dict) -> bool:
        """Check if vehicle details should be hidden (EON OFFICE vehicles)"""
        return self.is_removed_vehicle(vehicle_data)
    
    def get_vehicle_removed_message(self, vehicle_reg: str = None) -> str:
        """Get the standard message for removed vehicles"""
        if vehicle_reg:
            return f"Vehicle {vehicle_reg}'s device has been removed."
        else:
            return "This vehicle's device has been removed."
    
    def process_vehicle_query_result(self, query_result: Dict, hide_removed: bool = True) -> Dict:
        """
        Process vehicle query results to handle removed vehicles appropriately
        
        Args:
            query_result: The original query result
            hide_removed: If True, replace removed vehicle data with removal message
        
        Returns:
            Processed query result with appropriate handling for removed vehicles
        """
        if not isinstance(query_result, dict) or 'rows' not in query_result:
            return query_result
            
        processed_result = query_result.copy()
        processed_rows = []
        removal_messages = []
        
        for row in query_result['rows']:
            if self.should_hide_vehicle_details(row):
                if hide_removed:
                    # Instead of showing vehicle details, add a removal message
                    vehicle_reg = row.get('reg_no', row.get('vehicle_reg', 'Unknown'))
                    removal_messages.append(self.get_vehicle_removed_message(vehicle_reg))
                else:
                    # Mask the data but still show the row
                    processed_rows.append(self.mask_data_row(row))
            else:
                # Normal processing
                processed_rows.append(self.mask_data_row(row))
        
        processed_result['rows'] = processed_rows
        
        # If there are removal messages, add them to the result
        if removal_messages:
            processed_result['removal_messages'] = removal_messages
            
        return processed_result
    
    def get_masking_instructions(self) -> Dict:
        """Get instructions for implementing EONINFOTECH masking"""
        return {
            'purpose': 'Hide internal EONINFOTECH codes from user display',
            'rules': {
                'regions_zones': 'Replace EONINFOTECH with "Inactive Region"',
                'status_fields': 'Force status to "Inactive" for EONINFOTECH vehicles',
                'text_responses': 'Use business-friendly terms instead of EONINFOTECH',
                'sql_queries': 'Add CASE statements to mask at query level'
            },
            'implementation': {
                'data_rows': 'Use mask_data_row() or mask_data_list()',
                'sql_generation': 'Use mask_sql_query()',
                'query_results': 'Use mask_query_result()',
                'text_responses': 'Use mask_text_response()'
            }
        }

# Global instance for easy access
eoninfotech_masker = EoninfotechDataMasker()

def mask_eoninfotech_data(data: Any) -> Any:
    """Convenience function for masking EONINFOTECH data"""
    if isinstance(data, dict):
        return eoninfotech_masker.mask_data_row(data)
    elif isinstance(data, list):
        return eoninfotech_masker.mask_data_list(data)
    else:
        return data

def mask_eoninfotech_sql(sql: str) -> str:
    """Convenience function for masking SQL queries"""
    return eoninfotech_masker.mask_sql_query(sql)

def mask_eoninfotech_response(response: str) -> str:
    """Convenience function for masking text responses"""
    return eoninfotech_masker.mask_text_response(response)

if __name__ == "__main__":
    # Test the masking utility
    masker = EoninfotechDataMasker()
    
    print("🎭 EONINFOTECH Data Masking Utility Test")
    print("=" * 50)
    
    # Test data masking
    test_data = [
        {'reg_no': 'PB-01-1234', 'region_name': 'EONINFOTECH', 'status': 'active'},
        {'reg_no': 'PB-02-5678', 'zone_name': 'Gujarat', 'status': 'active'}
    ]
    
    print("Original data:", test_data)
    masked = masker.mask_data_list(test_data)
    print("Masked data:", masked)
    
    # Test SQL masking
    test_sql = "SELECT vm.reg_no, dm.name as region_name FROM vehicle_master vm JOIN district_master dm ON vm.district_id = dm.id_no"
    masked_sql = masker.mask_sql_query(test_sql)
    print(f"\nOriginal SQL: {test_sql}")
    print(f"Masked SQL: {masked_sql}")
    
    print("\n✅ Masking utility test complete!")

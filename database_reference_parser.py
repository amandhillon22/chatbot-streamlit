#!/usr/bin/env python3
"""
Database Reference Parser - Extracts structured intelligence from dat                'crm_complaint_dtls'           # Track complaint status (use 'Y' for Open, 'N' for Closed)base_reference.md
Integrates wit            "Store customer complaint details and status (active_status column: must use exact value 'Y' to find open complaints, 'N' for closed - NEVER use 'Open'/'Closed' words)",
            "Links complaints to categories and site visits",
            "CRITICAL: When filtering by status, always use exact values: active_status = 'Y' for open, active_status = 'N' for closed"existing embeddings system without disrupting workflow
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Any

class DatabaseReferenceParser:
    def __init__(self, reference_file='database_reference.md'):
        self.reference_file = reference_file
        self.table_metadata = {}
        self.business_context = {}
        self.transportation_keywords = self._load_transportation_keywords()
        
        # Query status value mappings
        self.status_values = {
            'crm_complaint_dtls': {
                'active': 'Y',  # CRITICAL: Use exact value 'Y' for active/open complaints
                'inactive': 'N', # CRITICAL: Use exact value 'N' for closed complaints
                'column': 'active_status'  
            }
        }
        
        # Import EONINFOTECH masker for consistent data masking
        try:
            from eoninfotech_masker import EoninfotechDataMasker
            self.data_masker = EoninfotechDataMasker()
        except ImportError:
            self.data_masker = None
            print("⚠️ EONINFOTECH masker not available - data will not be masked")
        
    def _load_transportation_keywords(self):
        """Transportation domain specific keywords mapping"""
        return {
            # Vehicle & Fleet
            'vehicle': ['vehicle_master', 'taxi_tm', 'bulker_trip_report', 'veh_report'],
            'vehicle_type': ['veh_type', 'vehicle_master'],
            'vehicle_category': ['veh_type', 'vehicle_master'],
            'fleet': ['vehicle_master', 'fleet_report', 'taxi_tm'],
            'truck': ['vehicle_master', 'bulker_trip_report', 'truck_master'],
            'taxi': ['taxi_tm', 'taxi_master', 'vehicle_master'],
            'bulker': ['bulker_trip_report', 'vehicle_master', 'veh_type'],
            
            # Vehicle Status & Activity
            'active': ['vehicle_master', 'veh_report', 'trip_report'],
            'inactive': ['vehicle_master', 'veh_report', 'maintenance_report'],
            'vehicle_status': ['vehicle_master', 'veh_report', 'maintenance_report'],
            'maintenance': ['maintenance_report', 'vehicle_master'],
            'accidental': ['vehicle_master', 'maintenance_report'],
            'device_missing': ['vehicle_master', 'gps_data'],
            'device_faulty': ['vehicle_master', 'gps_data'],
            'eoninfotech': ['vehicle_master', 'district_master', 'zone_master'],
            
            # Organizational Hierarchy (Zone → District → Plant → Vehicle)
            'zone': ['zone_master', 'district_master', 'hosp_master', 'vehicle_master'],
            'region': ['district_master', 'zone_master', 'hosp_master', 'vehicle_master'], 
            'district': ['district_master', 'zone_master', 'hosp_master', 'vehicle_master'],
            'plant': ['hosp_master', 'district_master', 'vehicle_master', 'plant_data'],
            'hierarchy': ['zone_master', 'district_master', 'hosp_master', 'vehicle_master'],
            'eoninfotech': ['district_master', 'vehicle_master', 'hosp_master'],  # Special inactive region
            
            # Trip & Journey
            'trip': ['trip_report', 'cur_trip_report', 'drum_trip_report', 'bulker_trip_report'],
            'journey': ['trip_report', 'route_master', 'route_detail'],
            'travel': ['trip_report', 'distance_report', 'route_master'],
            
            # Customer & Business
            'customer': ['customer_detail', 'site_master', 'customer_master', 'customer_ship_details'],
            'client': ['customer_detail', 'site_master', 'customer_ship_details'],
            'order': ['so_details', 'so_transferred_details', 'so_master'],
            'sales': ['so_details', 'so_master', 'sales_report'],
            
            # CRM & Complaint Management
            'complaint': [
                'crm_complaint_dtls',          # Main complaint table (active_status: use 'Y' for Open, 'N' for Closed)
                'crm_complaint_category',      # Categories like 'Delivery', 'Quality'
                'crm_complaint_category_type', # Specific types under each category
                'crm_site_visit_dtls',        # Site visit records
                'customer_ship_details'        # Customer shipping info
            ],
            'site_visit': [
                'crm_site_visit_dtls',
                'crm_complaint_dtls',          # Reference to complaints (active_status column: value must be 'Y' for Open or 'N' for Closed)
                'customer_ship_details'
            ],
            'feedback': [
                'crm_site_visit_dtls',
                'crm_complaint_dtls'           # Links to complaint status (Y=Open, N=Closed)
            ],
            'customer_complaint': [
                'crm_complaint_dtls',           # Main complaint table (active_status: Y=Open, N=Closed)
                'customer_ship_details',
                'crm_complaint_category',
                'crm_site_visit_dtls'
            ],
            'shipping': [
                'customer_ship_details',
                'ship_to_address'
            ],
            'complaint_tracking': [
                'crm_complaint_dtls',           # Track complaint status (active_status column accepts only 'Y' or 'N' values - not 'Open'/'Closed')
                'crm_site_visit_dtls',
                'crm_complaint_category',
                'crm_complaint_category_type'
            ],
            
            # Location & Geography  
            'plant': ['plant_data', 'plant_distance', 'plnt_report', 'hosp_master'],
            'plant': ['hosp_master', 'site_master', 'customer_detail'],
            'site': ['site_master', 'customer_detail', 'hosp_master', 'customer_ship_details', 'crm_site_visit_dtls'],
            'location': ['location_master', 'site_master', 'plant_data', 'ship_to_address'],
            'route': ['route_master', 'route_detail', 'link_master'],
            'distance': ['distance_report', 'distance_modify', 'plant_distance'],
            
            # Hierarchical relationships
            'hierarchy': ['hosp_master', 'site_master', 'customer_detail'],
            'organization': ['hosp_master', 'site_master', 'customer_detail'],
            'plant_site_customer': ['hosp_master', 'site_master', 'customer_detail'],
            'customer_complaint': ['customer_ship_details', 'crm_complaint_dtls', 'crm_site_visit_dtls'],
            'shipping_info': ['customer_ship_details', 'ship_to_address'],
            
            # Operations
            'fuel': ['fuel_report', 'fuel_master'],
            'maintenance': ['maintenance_report', 'vehicle_master'],
            'driver': ['driver_master', 'drv_veh_qr_assign'],
            'gps': ['gps_data', 'location_master'],
            
            # Time & Scheduling
            'schedule': ['route_master', 'schedule_master', 'trip_report'],
            'daily': ['daily_report', 'trip_report'],
            'monthly': ['monthly_report', 'performance_report']
        }
    
    def parse_reference_file(self):
        """Parse database_reference.md and extract structured information"""
        if not os.path.exists(self.reference_file):
            print(f"⚠️ {self.reference_file} not found, using basic keywords")
            return self._create_basic_metadata()
        
        try:
            with open(self.reference_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._extract_table_information(content)
        
        except Exception as e:
            print(f"⚠️ Error parsing database reference: {e}")
            return self._create_basic_metadata()
    
    def _extract_table_information(self, content):
        """Extract table structure and business context from markdown content"""
        tables = {}
        current_table = None
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Look for table headers
            if line.startswith('## 🗂️ Table:') or line.startswith('## Table:'):
                # Extract table name (handle different formats)
                table_match = re.search(r'`([^`]+)`', line)
                if table_match:
                    current_table = table_match.group(1)
                    tables[current_table] = {
                        'columns': [],
                        'business_context': '',
                        'relationships': [],
                        'key_columns': [],
                        'size_estimate': 'medium'
                    }
            
            # Extract column information from markdown tables
            elif current_table and '|' in line and 'Column' in line:
                # This is likely a table header, start collecting columns
                continue
                
            elif current_table and '|' in line and line.strip().startswith('|'):
                # Parse column data
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 2 and parts[0] and parts[1]:
                    column_info = {
                        'name': parts[0],
                        'type': parts[1] if len(parts) > 1 else 'unknown',
                        'nullable': 'YES' if len(parts) > 2 and 'null' in parts[2].lower() else 'NO',
                        'description': parts[3] if len(parts) > 3 else ''
                    }
                    tables[current_table]['columns'].append(column_info)
                    
                    # Identify key columns
                    col_name_lower = column_info['name'].lower()
                    if any(key in col_name_lower for key in ['id', 'key', 'no']):
                        tables[current_table]['key_columns'].append(column_info['name'])
        
        # Add business context based on table names
        for table_name, info in tables.items():
            info['business_context'] = self._infer_business_context(table_name)
            info['relationships'] = self._infer_relationships(table_name)
            info['size_estimate'] = self._estimate_table_size(table_name)
        
        print(f"✅ Parsed {len(tables)} tables from database reference")
        
        # Apply business rules to the parsed context
        context_data = {
            'tables': tables,
            'total_tables': len(tables)
        }
        business_rules = self.apply_business_rules(context_data)
        
        return {
            'tables': tables,
            'keywords': self._load_transportation_keywords(),
            'business_rules': business_rules,
            'parsing_metadata': {
                'file_path': self.reference_file,
                'total_tables': len(tables),
                'rules_applied': len(business_rules),
                'parsed_at': datetime.now().isoformat()
            }
        }
    
    def _infer_business_context(self, table_name):
        """Infer business context from table name"""
        table_lower = table_name.lower()
        contexts = []
        
        # CRM Complaint System Contexts
        crm_contexts = {
            'crm_complaint_dtls': [
                "Main complaint tracking and management system",
                "Stores customer complaint details and status (active_status column: must use exact value 'Y' to find open complaints, 'N' for closed - do not use 'Open'/'Closed' words)",
                "Links complaints to categories and site visits"
            ],
            'crm_complaint_category': [
                "Complaint categorization system",
                "Top-level complaint classification",
                "Organizes complaints by main categories (e.g., Delivery, Quality)"
            ],
            'crm_complaint_category_type': [
                "Detailed complaint type classification",
                "Sub-categories under main complaint categories",
                "Specific issue types for better tracking"
            ],
            'crm_site_visit_dtls': [
                "Site visit records for complaint resolution",
                "Tracks resolution attempts and outcomes",
                "Links complaints to on-site actions",
                "CRITICAL: product_correction column uses exact values 'Y' for done (not 'Yes') and 'N' for not done (not 'No')"
            ],
            'customer_ship_details': [
                "Customer shipping and delivery management",
                "Links customers to shipping addresses",
                "Used for complaint delivery context"
            ],
            'ship_to_address': [
                "Detailed shipping address information",
                "Delivery location management",
                "Address validation and verification"
            ]
        }
        
        # Add CRM-specific context if applicable
        if table_lower in crm_contexts:
            contexts.extend(crm_contexts[table_lower])
        
        # Core business entities
        if any(word in table_lower for word in ['trip', 'journey']):
            contexts.append("Vehicle trip and journey management")
        if any(word in table_lower for word in ['vehicle', 'taxi', 'truck']):
            contexts.append("Fleet and vehicle operations")
        if any(word in table_lower for word in ['customer', 'client']):
            contexts.append("Customer relationship management")
            if 'complaint' in table_lower:
                contexts.append("Complaint status tracking (active_status column requires exact values: use 'Y' to find open complaints, 'N' for closed)")
        if any(word in table_lower for word in ['route', 'distance']):
            contexts.append("Route planning and distance tracking")
        if any(word in table_lower for word in ['fuel', 'maintenance']):
            contexts.append("Vehicle maintenance and fuel management")
        if any(word in table_lower for word in ['plant', 'site', 'location']):
            contexts.append("Plant and location management")
        if any(word in table_lower for word in ['so_', 'order', 'sales']):
            contexts.append("Sales order and business operations")
            
        # Hierarchical context
        if 'zone_master' == table_lower:
            contexts.append("Top-level organizational hierarchy (Zone master)")
        if 'district_master' == table_lower:
            contexts.append("Second-level organizational hierarchy (District/Region master)")
        if 'hosp_master' == table_lower:
            contexts.append("Third-level organizational hierarchy (Plant/Facility master)")
        if 'vehicle_master' == table_lower:
            contexts.append("Bottom-level organizational hierarchy (Vehicle operations)")
        if 'plant_data' == table_lower:
            contexts.append("Plant operational metrics and readings")
        
        return "; ".join(contexts) if contexts else "General transportation data"
    
    def _infer_relationships(self, table_name):
        """Infer likely table relationships"""
        table_lower = table_name.lower()
        relationships = []
        
        # CRM Complaint System Relationships
        crm_relationships = {
            'crm_complaint_dtls': [
                'customer_ship_details',      # Links complaints to customer shipping info
                'crm_complaint_category',     # Categorizes complaints (active_status in main table: Y=Open, N=Closed)
                'crm_complaint_category_type',# Sub-categorizes complaints
                'crm_site_visit_dtls',       # Links to resolution visits
                'hosp_master'                # Links to plant/facility
            ],
            'crm_site_visit_dtls': [
                'crm_complaint_dtls',        # Links visits to complaints (complaint status: Y=Open, N=Closed)
                'customer_ship_details',     # Links to customer location
                'hosp_master'               # Links to plant/facility
            ],
            'crm_complaint_category': [
                'crm_complaint_category_type',# Parent-child category relationship
                'crm_complaint_dtls'        # Links categories to complaints (check active_status: Y=Open, N=Closed)
            ],
            'crm_complaint_category_type': [
                'crm_complaint_category',    # Child-parent category relationship
                'crm_complaint_dtls'        # Links types to complaints
            ],
            'customer_ship_details': [
                'ship_to_address',          # Links to detailed address info
                'crm_complaint_dtls',       # Links to complaints
                'crm_site_visit_dtls'      # Links to site visits
            ],
            'ship_to_address': [
                'customer_ship_details'     # Links back to shipping details
            ]
        }
        
        # Add CRM-specific relationships if applicable
        if table_lower in crm_relationships:
            relationships.extend(crm_relationships[table_lower])
            
        # Organizational hierarchy relationships (Zone → District → Plant → Vehicle)
        if 'zone_master' == table_lower:
            relationships.extend(['district_master'])
        if 'district_master' == table_lower:
            relationships.extend(['zone_master', 'hosp_master'])
        if 'hosp_master' == table_lower:
            relationships.extend(['district_master', 'vehicle_master', 'site_master', 'customer_detail', 'plant_data'])
        if 'vehicle_master' == table_lower:
            relationships.extend(['hosp_master', 'trip_report', 'driver_master', 'fuel_report', 'veh_type'])
        
        # Other site/customer relationships
        if 'site_master' == table_lower:
            relationships.extend(['hosp_master', 'customer_detail', 'customer_ship_details'])
        if 'customer_detail' == table_lower:
            relationships.extend(['site_master', 'hosp_master', 'customer_ship_details'])
        if 'plant_data' == table_lower:
            relationships.extend(['hosp_master'])
        
        # Vehicle type relationships
        if 'vehicle_master' == table_lower:
            relationships.extend(['trip_report', 'driver_master', 'fuel_report', 'veh_type'])
        elif 'vehicle' in table_lower:
            relationships.extend(['trip_report', 'driver_master', 'fuel_report'])
        if 'veh_type' == table_lower:
            relationships.extend(['vehicle_master'])
            
        # Common relationship patterns in transportation domain
        if 'trip' in table_lower:
            relationships.extend(['vehicle_master', 'route_master', 'customer_detail'])
        if 'customer' in table_lower and 'customer_detail' != table_lower:
            relationships.extend(['so_details', 'trip_report', 'site_master', 'crm_complaint_dtls'])
        if 'route' in table_lower:
            relationships.extend(['trip_report', 'distance_report'])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_relationships = []
        for rel in relationships:
            if rel not in seen:
                seen.add(rel)
                unique_relationships.append(rel)
                
        return unique_relationships
    
    def _estimate_table_size(self, table_name):
        """Estimate table size based on name patterns"""
        table_lower = table_name.lower()
        
        # Large tables (likely to have many records)
        if any(word in table_lower for word in ['trip_report', 'gps_data', 'log', 'history']):
            return 'large'
        # Medium tables (moderate records)
        elif any(word in table_lower for word in ['detail', 'report', 'data']):
            return 'medium'
        # Small tables (master/reference data)
        elif any(word in table_lower for word in ['master', 'config', 'setting']):
            return 'small'
        
        return 'medium'
    
    def _create_basic_metadata(self):
        """Create basic metadata when reference file is not available"""
        # Fallback to transportation keywords
        basic_tables = {}
        
        for keyword, table_list in self.transportation_keywords.items():
            for table in table_list:
                context = f"Transportation table related to {keyword}"
                if table == 'crm_complaint_dtls':
                    context = f"Complaint management table (active_status: use 'Y' for Open complaints, 'N' for Closed)"
                
                if table not in basic_tables:
                    basic_tables[table] = {
                        'columns': [],
                        'business_context': context,
                        'relationships': [],
                        'key_columns': ['id'],
                        'size_estimate': 'medium'
                    }
        
        return basic_tables
    
    def get_business_relevant_tables(self, query):
        """Find business-relevant tables for a given query"""
        query_lower = query.lower()
        relevant_tables = []
        
        # Direct keyword matching
        for keyword, tables in self.transportation_keywords.items():
            if keyword in query_lower:
                relevant_tables.extend(tables)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tables = []
        for table in relevant_tables:
            if table not in seen:
                seen.add(table)
                unique_tables.append(table)
        
        return unique_tables[:10]  # Limit to top 10 most relevant
    
    def get_table_context(self, table_name):
        """Get enhanced context for a specific table"""
        if not hasattr(self, '_parsed_data'):
            self._parsed_data = self.parse_reference_file()
        
        table_info = self._parsed_data.get(table_name, {})
        
        return {
            'business_context': table_info.get('business_context', ''),
            'relationships': table_info.get('relationships', []),
            'key_columns': table_info.get('key_columns', []),
            'size_estimate': table_info.get('size_estimate', 'medium'),
            'column_count': len(table_info.get('columns', []))
        }
    
    def enhance_query_context(self, query, existing_tables):
        """Enhance query context with database reference insights"""
        query_lower = query.lower()
        
        # Get business-relevant tables
        relevant_tables = self.get_business_relevant_tables(query)
        
        # Combine with existing tables and remove duplicates
        all_tables = list(set(existing_tables + relevant_tables))
        
        # Add context information
        context_info = {
            'business_relevant_tables': relevant_tables[:5],
            'query_intent': self._detect_query_intent(query),
            'suggested_relationships': self._suggest_relationships(relevant_tables),
            'performance_hints': self._get_performance_hints(relevant_tables)
        }
        
        return all_tables, context_info
    
    def _detect_query_intent(self, query):
        """Detect the business intent of the query"""
        query_lower = query.lower()
        
        intents = []
        
        # Reporting intents
        if any(word in query_lower for word in ['report', 'show', 'list', 'display']):
            intents.append('reporting')
        
        # Analysis intents
        if any(word in query_lower for word in ['analyze', 'compare', 'trend', 'average']):
            intents.append('analysis')
        
        # Operational intents (includes complaint status: Y=Open, N=Closed)
        if any(word in query_lower for word in ['status', 'current', 'active', 'pending']):
            intents.append('operational')
        
        # Time-based intents
        if any(word in query_lower for word in ['today', 'yesterday', 'month', 'weekly']):
            intents.append('time_based')
        
        return intents
    
    def _suggest_relationships(self, tables):
        """Suggest relationships between tables"""
        relationships = []
        
        for table in tables:
            table_context = self.get_table_context(table)
            relationships.extend(table_context.get('relationships', []))
        
        return list(set(relationships))
    
    def _get_performance_hints(self, tables):
        """Get performance hints for the tables"""
        hints = []
        
        for table in tables:
            context = self.get_table_context(table)
            size = context.get('size_estimate', 'medium')
            
            if size == 'large':
                hints.append(f"Consider adding LIMIT for {table} (large table)")
            elif 'trip' in table.lower():
                hints.append(f"Consider date filtering for {table}")
            elif 'crm_complaint_dtls' in table.lower():
                hints.append(f"For complaint status filters, active_status must be compared with exact value 'Y' (not 'Open') or 'N' (not 'Closed')")
            elif 'crm_site_visit_dtls' in table.lower():
                hints.append(f"For product correction filters, product_correction must use exact value 'Y' (not 'Yes') for done or 'N' (not 'No') for not done")
                hints.append(f"For action status filters (*_action_status columns like bh_action_status, cm_action_status), use 'A' for Approved/Active or 'R' for Rejected/Refused (NEVER use 'Y'/'N')")
        
        return hints
    
    def get_complaint_status_value(self, status_text):
        """Convert status text to correct database value for crm_complaint_dtls.active_status"""
        status_lower = status_text.lower().strip()
        
        # Direct value matches
        if status_lower in ['y', 'n']:
            return status_lower.upper()
        
        # Handle various forms of "open"
        if status_lower in ['open', 'active', 'ongoing', 'in progress', 'not closed']:
            return 'Y'  # CRITICAL: Use exact 'Y' value
        
        # Handle various forms of "closed"    
        if status_lower in ['closed', 'inactive', 'complete', 'completed', 'resolved']:
            return 'N'  # CRITICAL: Use exact 'N' value
        
        return None  # If no match found
    
    def apply_business_rules(self, context_data):
        """Apply domain-specific business rules to the parsed data"""
        business_rules = []
        
        # Rule 1: EONINFOTECH region vehicles are always inactive
        if any('eoninfotech' in str(context_data.get(field, '')).lower() 
               for field in ['zone', 'district', 'region', 'plant']):
            business_rules.append({
                'rule_type': 'vehicle_status_override',
                'condition': 'region_eoninfotech',
                'action': 'mark_all_vehicles_inactive',
                'description': 'Vehicles in EONINFOTECH region are considered inactive',
                'priority': 'high'
            })
            
        # Rule 2: Hierarchical relationships validation
        hierarchy_fields = ['zone', 'district', 'plant', 'vehicle']
        present_levels = [field for field in hierarchy_fields if field in context_data]
        if len(present_levels) > 1:
            business_rules.append({
                'rule_type': 'hierarchical_validation',
                'levels': present_levels,
                'description': f'Validate hierarchical relationship: {" → ".join(present_levels)}',
                'priority': 'medium'
            })
            
        # Rule 3: Vehicle status inference from maintenance/accident data
        if 'maintenance' in context_data or 'accidental' in context_data:
            business_rules.append({
                'rule_type': 'status_inference',
                'condition': 'maintenance_or_accident',
                'action': 'infer_inactive_status',
                'description': 'Vehicles under maintenance or accidental are likely inactive',
                'priority': 'medium'
            })
            
        return business_rules
    
    def check_eoninfotech_rule(self, query_text, context_data=None):
        """Check if EONINFOTECH region rule should be applied"""
        query_lower = query_text.lower()
        
        # Check for EONINFOTECH region mentions
        eoninfotech_indicators = [
            'eoninfotech',
            'eon info tech',
            'eon infotech'
        ]
        
        # Check for EON OFFICE mentions (special case - device removed)
        eon_office_indicators = [
            'eon office',
            'eon_office'
        ]
        
        is_eoninfotech_query = any(indicator in query_lower for indicator in eoninfotech_indicators)
        is_eon_office_query = any(indicator in query_lower for indicator in eon_office_indicators)
        
        if is_eon_office_query:
            return {
                'applies': True,
                'rule': 'eon_office_removed_vehicles',
                'description': 'Vehicles in EON OFFICE plant have had their devices removed',
                'query_modification': 'Show device removal message instead of vehicle details',
                'suggested_tables': ['vehicle_master', 'hosp_master', 'district_master'],
                'data_masking': {
                    'mask_eoninfotech_region': True,
                    'hide_vehicle_details': True,
                    'replace_with': 'Device Removed',
                    'removal_message': True
                }
            }
        elif is_eoninfotech_query:
            return {
                'applies': True,
                'rule': 'eoninfotech_inactive_vehicles',
                'description': 'All vehicles in EONINFOTECH region are considered inactive',
                'query_modification': 'Add vehicle status filter: inactive',
                'suggested_tables': ['vehicle_master', 'district_master', 'zone_master'],
                'data_masking': {
                    'mask_eoninfotech_region': True,
                    'replace_with': 'Inactive Region',
                    'force_inactive_status': True
                }
            }
            
        return {'applies': False}
    
    def mask_eoninfotech_data(self, data_row):
        """Mask EONINFOTECH references in data and show as inactive"""
        if self.data_masker:
            return self.data_masker.mask_data_row(data_row)
        else:
            # Fallback masking if masker not available
            if not isinstance(data_row, dict):
                return data_row
                
            masked_row = data_row.copy()
            
            # Check and mask EONINFOTECH in any column
            for key, value in masked_row.items():
                if isinstance(value, str) and value.upper() == 'EONINFOTECH':
                    if any(col in key.lower() for col in ['region', 'district', 'zone', 'area', 'location']):
                        masked_row[key] = 'Inactive Region'
                    else:
                        masked_row[key] = 'Inactive'
            
            return masked_row
    
    def mask_eoninfotech_in_list(self, data_list):
        """Mask EONINFOTECH references in a list of data rows"""
        if self.data_masker:
            return self.data_masker.mask_data_list(data_list)
        else:
            # Fallback
            if not isinstance(data_list, list):
                return data_list
            return [self.mask_eoninfotech_data(row) for row in data_list]
    
    def get_business_context_for_query(self, query_text):
        """Get relevant business context and rules for a specific query"""
        context = {
            'eoninfotech_rule': self.check_eoninfotech_rule(query_text),
            'keywords_matched': [],
            'suggested_tables': [],
            'business_rules': []
        }
        
        # Match keywords from transportation domain
        transportation_keywords = self._load_transportation_keywords()
        query_lower = query_text.lower()
        
        for keyword, tables in transportation_keywords.items():
            if keyword in query_lower:
                context['keywords_matched'].append(keyword)
                context['suggested_tables'].extend(tables)
                
        # Remove duplicates
        context['suggested_tables'] = list(set(context['suggested_tables']))
        
        # Add relevant business rules
        if context['eoninfotech_rule']['applies']:
            context['business_rules'].append(context['eoninfotech_rule'])
            
        return context
# Global instance
database_reference_parser = DatabaseReferenceParser()

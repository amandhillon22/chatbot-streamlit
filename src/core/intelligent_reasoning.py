#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Intelligent Contextual Reasoning Enhancement for Chatbot
"""

import re
import json
from typing import Dict, List, Optional, Tuple

class IntelligentReasoning:
    """
    Adds intelligent contextual reasoning to the chatbot
    to understand implicit requests and auto-resolve data relationships
    
    CRITICAL TABLE CLARIFICATIONS:
    - hosp_master = PLANT DATA (factories, facilities, sites) - NOT medical facilities!
    - district_master = REGIONS/DISTRICTS/STATES 
    - zone_master = ZONES (larger geographic areas)
    - vehicle_master = VEHICLES/TRUCKS/FLEET
    """
    
    def __init__(self):
        # CRITICAL: Define the core hierarchical relationships using exact ID columns
        # These ID relationships are MANDATORY and must NEVER be missed:
        # zone_master.id_no ← district_master.id_zone ← hosp_master.id_dist ← vehicle_master.id_hosp
        
        # IMPORTANT: hosp_master contains PLANT DATA, not medical data!
        
        # Import database reference parser for business rules
        try:
            from src.database.database_reference_parser import DatabaseReferenceParser
            self.db_parser = DatabaseReferenceParser()
        except ImportError:
            self.db_parser = None
            print("⚠️ DatabaseReferenceParser not available - business rules disabled")
        
        # Import EONINFOTECH masker for consistent data masking
        try:
            from src.database.eoninfotech_masker import EoninfotechDataMasker
            self.data_masker = EoninfotechDataMasker()
        except ImportError:
            self.data_masker = None
            print("⚠️ EONINFOTECH masker not available - data will not be masked")
        
        # DPR Master 1 (Daily Production Report) business context
        self.dpr_business_context = {
            'table_name': 'dpr_master1',
            'description': 'Daily Production Report for concrete orders and deliveries',
            'key_columns': {
                'id_no': 'Unique row identifier (DPR ID - NEVER confuse with vehicle registration)',
                'plant_id': 'Links to hosp_master.id_no for plant details',
                'pi_name': 'Plant incharge name',
                'cust_name': 'Customer name for delivery',
                'cust_id': 'Links to site_customer1.id_no for customer details',
                'site_name': 'Delivery site name',
                'site_id': 'Links to site_master1.id_no for site details',
                'fse_name': 'Sales person name (format: surname, firstname)',
                'site_distance': 'Distance from plant to site (km)',
                'tm_no': 'Transit Mixer registration (links to vehicle_master.reg_no - vehicle identifier, NOT DPR ID)',
                'vol_cum': 'Concrete volume in TM (out of 7 m³ total)',
                'grade': 'Concrete mixture grade',
                'smode': 'Service mode (with pump/without pump)',
                'bth_name': 'Batch/Batching order name',
                'tkt_no': 'Ticket number (links to drum_trip_report.tkt_no)',
                'pump_name': 'Pump name if smode = "with pump"',
                'challan_no': 'Challan number',
                'so_number': 'Sales order number',
                'cost_m3': 'Ready-mix cost per m³',
                'plant_code': 'Plant code',
                'batch_code': 'Batch code'
            },
            'relationships': {
                'plant_details': 'dpr_master1.plant_id = hosp_master.id_no',
                'customer_info': 'dpr_master1.cust_id = site_customer1.id_no',
                'site_details': 'dpr_master1.site_id = site_master1.id_no',
                'vehicle_info': 'dpr_master1.tm_no = vehicle_master.reg_no',
                'trip_tracking': 'dpr_master1.tkt_no = drum_trip_report.tkt_no'
            },
            'business_rules': {
                'tm_capacity': 'Total Transit Mixer capacity is 7 m³',
                'name_format': 'fse_name stored as "surname, firstname" → display as "firstname surname"',
                'service_modes': ['with pump', 'without pump'],
                'table_priority': 'Always use dpr_master1, never dpr_master'
            }
        }
        
        # Driver Master business context
        self.driver_business_context = {
            'table_name': 'driver_master',
            'description': 'Comprehensive driver information for transportation fleet management',
            'key_columns': {
                'id_no': 'Primary key - Driver unique identifier',
                'first_name': 'Driver first name',
                'last_name': 'Driver last name (surname)',
                'dt_of_birth': 'Date of birth for age calculation',
                'dt_of_joining': 'Employment start date for service duration',
                'gender': 'Driver gender (Male/Female)',
                'telephone': 'Mobile contact number (unique)',
                'lic_no': 'Driving license number (unique)',
                'lic_issue': 'License issue date',
                'lic_exp': 'License expiry date for renewal tracking',
                'd_code': 'Driver code (unique alphanumeric identifier)',
                'id_depo': 'Plant assignment (links to hosp_master.id_no)',
                'tshirt_size': 'Uniform size (S, M, L, XL)'
            },
            'relationships': {
                'plant_assignment': 'driver_master.id_depo = hosp_master.id_no',
                'referenced_by': 'Any table with drv_id, driver_id, or similar links to driver_master.id_no'
            },
            'business_rules': {
                'name_display': 'Display as "first_name + last_name" (firstname lastname format)',
                'unique_constraints': ['d_code', 'lic_no', 'telephone'],
                'license_monitoring': 'Track lic_exp for renewal alerts',
                'plant_hierarchy': 'id_depo determines plant assignment through hosp_master'
            }
        }
        
        # Driver query patterns
        self.driver_query_patterns = {
            'driver_lookup': [
                'driver details', 'driver information', 'driver profile',
                'find driver', 'driver search', 'driver by name',
                'about driver', 'driver info', 'tell me about'
            ],
            'license_management': [
                'license expiry', 'license renewal', 'driving license',
                'expired license', 'license status', 'lic_exp'
            ],
            'plant_assignment': [
                'driver assignment', 'plant drivers', 'drivers at plant',
                'depot drivers', 'driver location'
            ],
            'contact_info': [
                'driver contact', 'driver phone', 'driver mobile',
                'contact number', 'telephone number'
            ],
            'demographics': [
                'driver age', 'driver gender', 'driver statistics',
                'driver demographics', 'male drivers', 'female drivers',
                'birthday', 'birth date', 'date of birth', 'born',
                'when was born', 'birthday gift', 'age of driver'
            ],
            'service_duration': [
                'driver experience', 'years of service', 'joining date',
                'service period', 'employment duration'
            ],
            'uniform_management': [
                'tshirt size', 'uniform size', 'driver uniform',
                'shirt size', 'clothing size', 'size of', 'what size',
                't-shirt', 'tshirt', 'uniform'
            ],
            'driver_codes': [
                'driver code', 'd_code', 'driver identifier',
                'driver id', 'employee code'
            ],
            'driver_assignments': [
                'driver assignment', 'current assignment', 'assigned driver',
                'driver schedule', 'driver roster', 'assignment history',
                'driver allocation', 'assigned to', 'driver duty',
                'assignment status', 'active assignment', 'vehicle assignment',
                'plant assignment today', 'driver currently assigned',
                'assignment duration', 'assignment period', 'duty schedule',
                'driver availability', 'assignment conflict', 'overlap',
                'double assignment', 'scheduling conflict',
                'delivery assignment', 'concrete delivery', 'driver performance',
                'assignment efficiency', 'delivery performance',
                'driver plant mapping', 'plant drivers', 'depot assignment'
            ]
        }
        
        # DPR query patterns
        self.dpr_query_patterns = {
            'daily_production': [
                'daily production', 'production report', 'dpr', 'concrete orders',
                'concrete delivery', 'ready mix', 'readymix'
            ],
            'customer_orders': [
                'customer order', 'customer delivery', 'customer concrete',
                'delivery to customer', 'customer site'
            ],
            'transit_mixer': [
                'transit mixer', 'tm', 'concrete truck', 'mixer truck',
                'tm utilization', 'mixer capacity'
            ],
            'sales_person': [
                'sales person', 'fse', 'sales executive', 'sales performance'
            ],
            'concrete_grade': [
                'concrete grade', 'mixture grade', 'concrete type',
                'grade analysis'
            ],
            'pump_analysis': [
                'with pump', 'without pump', 'pump delivery',
                'pump vs non-pump', 'pump utilization'
            ],
            'site_distance': [
                'site distance', 'delivery distance', 'distance analysis',
                'distance optimization'
            ],
            'batch_orders': [
                'batch order', 'batching order', 'batch name',
                'batch code', 'production batch'
            ]
        }

        self.core_hierarchy = {
            'zone_master': {
                'primary_key': 'id_no',
                'child_table': 'district_master',
                'child_foreign_key': 'id_zone'
            },
            'district_master': {
                'primary_key': 'id_no',
                'parent_table': 'zone_master',
                'parent_foreign_key': 'id_zone',
                'child_table': 'hosp_master',
                'child_foreign_key': 'id_dist'
            },
            'hosp_master': {
                'primary_key': 'id_no',
                'parent_table': 'district_master',
                'parent_foreign_key': 'id_dist',
                'child_table': 'vehicle_master',
                'child_foreign_key': 'id_hosp'
            },
            'vehicle_master': {
                'primary_key': 'id_no',
                'parent_table': 'hosp_master',
                'parent_foreign_key': 'id_hosp'
            },
            
            # CRM Complaint System Hierarchy
            'customer_ship_details': {
                'primary_key': ['customer_id', 'ship_to_id'],
                'child_table': 'crm_complaint_dtls',
                'child_foreign_keys': ['cust_id', 'site_id']
            },
            'ship_to_address': {
                'primary_key': 'ship_to_id',
                'child_table': 'customer_ship_details',
                'child_foreign_key': 'ship_to_id'
            },
            'crm_complaint_category': {
                'primary_key': 'id_no',
                'child_table': 'crm_complaint_category_type',
                'child_foreign_key': 'category_id'
            },
            'crm_complaint_category_type': {
                'primary_key': 'id_no',
                'parent_table': 'crm_complaint_category',
                'parent_foreign_key': 'category_id',
                'child_table': 'crm_complaint_dtls',
                'child_foreign_key': 'complaint_type_id'
            },
            'crm_complaint_dtls': {
                'primary_key': 'id_no',
                'parent_tables': [
                    {'table': 'customer_ship_details', 'foreign_keys': ['cust_id', 'site_id']},
                    {'table': 'crm_complaint_category', 'foreign_key': 'complaint_category_id'},
                    {'table': 'crm_complaint_category_type', 'foreign_key': 'complaint_type_id'},
                    {'table': 'hosp_master', 'foreign_key': 'plant_id'}
                ],
                'child_table': 'crm_site_visit_dtls',
                'child_foreign_key': 'complaint_id'
            },
            'crm_site_visit_dtls': {
                'primary_key': 'id_no',
                'parent_tables': [
                    {'table': 'crm_complaint_dtls', 'foreign_key': 'complaint_id'},
                    {'table': 'customer_ship_details', 'foreign_keys': ['cust_id', 'site_id']},
                    {'table': 'hosp_master', 'foreign_key': 'plant_id'}
                ]
            }
        }
        
        # Enhanced CRM Complaint Status System
        self.complaint_status_mapping = {
            'P': {
                'description': 'Pending',
                'category_based': True,
                'assignments': {
                    '1': {'pending_with': 'Plant Incharge', 'category_name': 'Operations'},
                    '2': {'pending_with': 'Technical Manager/Incharge', 'category_name': 'Technical'}
                },
                'final_status': 'Open'
            },
            'QC': {'pending_with': 'HO QC', 'final_status': 'Open', 'description': 'Pending with HO QC'},
            'BH': {'pending_with': 'Business Head', 'final_status': 'Open', 'description': 'Pending with Business Head'},
            'TH': {'pending_with': 'Technical Head', 'final_status': 'Open', 'description': 'Pending with Technical Head'},
            'CF': {'pending_with': 'CFO', 'final_status': 'Open', 'description': 'Pending with CFO'},
            'MD': {'pending_with': 'MD', 'final_status': 'Open', 'description': 'Pending with MD'},
            'C': {'pending_with': 'Completed', 'final_status': 'Closed', 'description': 'Complaint Closed'}
        }

        # Action Status Values for approval workflow
        self.action_status_mapping = {
            'A': {'description': 'Approved', 'status': 'Approved'},
            'R': {'description': 'Rejected', 'status': 'Rejected'},
            'P': {'description': 'Pending', 'status': 'Pending'}  # Default for null/empty values
        }

        # Action status columns in crm_site_visit_dtls table
        self.action_status_columns = {
            'ho_qc_action_status': 'HO QC Action Status (A=Approved, R=Rejected)',
            'bh_action_status': 'Business Head Action Status (A=Approved, R=Rejected)', 
            'th_action_status': 'Technical Head Action Status (A=Approved, R=Rejected)',
            'cf_action_status': 'CFO Action Status (A=Approved, R=Rejected)',
            'md_action_status': 'MD Action Status (A=Approved, R=Rejected)'
        }

        # Overall complaint status workflow logic
        self.complaint_workflow_status = {
            'no_site_visit': 'Pending for Site Visit',
            'pending_rca': 'Pending for RCA',
            'pending_testing': 'Pending for Third Party Testing',
            'pending_execution': 'Pending for Execution/Rectification'
        }

        # Category mapping for business context
        self.complaint_categories = {
            '1': 'Operations',
            '2': 'Technical'
        }
        
        # Common data relationship patterns - ENHANCED HIERARCHICAL
        self.relationship_patterns = {
            'plant_name': {
                'from_plant_id': {
                    'source_tables': ['hosp_master'],
                    'key_column': 'id_no',
                    'target_column': 'name'
                },
                'from_vehicle': {
                    'source_tables': ['hosp_master', 'vehicle_master'],
                    'join_logic': 'JOIN hosp_master hm ON vm.id_hosp = hm.id_no',
                    'target_column': 'hm.name as plant_name'
                }
            },
            'zone_name': {
                'from_vehicle': {
                    'source_tables': ['zone_master', 'district_master', 'hosp_master', 'vehicle_master'],
                    'join_logic': '''
                        JOIN vehicle_master vm ON vm.id_hosp = hm.id_no 
                        JOIN hosp_master hm ON hm.id_no = vm.id_hosp
                        JOIN district_master dm ON dm.id_no = hm.id_dist 
                        JOIN zone_master zm ON zm.id_no = dm.id_zone
                    ''',
                    'target_column': 'zm.zone_name'
                },
                'from_region': {
                    'source_tables': ['zone_master', 'district_master'],
                    'join_logic': 'JOIN district_master dm ON dm.id_zone = zm.id_no',
                    'target_column': 'zm.zone_name'
                }
            },
            'region_name': {
                'from_vehicle': {
                    'source_tables': ['district_master', 'hosp_master', 'vehicle_master'],
                    'join_logic': '''
                        JOIN vehicle_master vm ON vm.id_hosp = hm.id_no
                        JOIN hosp_master hm ON hm.id_no = vm.id_hosp 
                        JOIN district_master dm ON dm.id_no = hm.id_dist
                    ''',
                    'target_column': 'dm.name as region_name'
                },
                'from_plant': {
                    'source_tables': ['district_master', 'hosp_master'],
                    'join_logic': 'JOIN hosp_master hm ON hm.id_dist = dm.id_no',
                    'target_column': 'dm.name as region_name'
                }
            },
            'customer_name': {
                'from_customer_id': {
                    'source_tables': ['customer_master', 'site_master'],
                    'key_column': 'customer_id', 
                    'target_column': 'customer_name'
                }
            },
            'complaint_status': {
                'from_complaint_id': {
                    'source_tables': ['crm_complaint_dtls'],
                    'key_column': 'id_no',
                    'target_column': "CASE status WHEN 'Y' THEN 'Open' WHEN 'N' THEN 'Closed' ELSE status END as status"
                }
            },
            'vehicle_details': {
                'from_reg_no': {
                    'source_tables': ['vehicle_master', 'mega_trips'],
                    'key_column': 'reg_no',
                    'target_column': '*'
                },
                'hierarchical_info': {
                    'source_tables': ['vehicle_master', 'hosp_master', 'district_master', 'zone_master'],
                    'join_logic': '''
                        LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no
                        LEFT JOIN district_master dm ON hm.id_dist = dm.id_no  
                        LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no
                    ''',
                    'target_column': 'vm.reg_no, hm.name as plant, dm.name as region, zm.zone_name'
                }
            },
            'driver_name': {
                'from_driver_id': {
                    'source_tables': ['driver_master'],
                    'key_column': 'driver_id',
                    'target_column': 'driver_name'
                }
            }
        }
        
        # Intent patterns for auto-resolution - ENHANCED HIERARCHICAL
        self.intent_patterns = [
            # Show all hierarchical entities patterns
            {
                'pattern': r'(?:show|list|all)\s+(?:all\s+)?(?:regions|districts)',
                'intent': 'show_all_regions',
                'extractor': self._extract_show_all_regions
            },
            {
                'pattern': r'(?:show|list|all)\s+(?:all\s+)?(?:zones|areas)',
                'intent': 'show_all_zones',
                'extractor': self._extract_show_all_zones
            },
            {
                'pattern': r'(?:show|list|all)\s+(?:all\s+)?(?:plants|facilities)',
                'intent': 'show_all_plants',
                'extractor': self._extract_show_all_plants
            },
            
            # Contextual patterns for "this vehicle" queries - PRIORITIZE THESE FIRST
            {
                'pattern': r'(?:which|what).*(?:plant|region|zone).*(?:this|that)\s+vehicle',
                'intent': 'get_vehicle_hierarchy_contextual',
                'extractor': self._extract_vehicle_from_context
            },
            {
                'pattern': r'(?:to|which|what).*(?:plant|region|zone).*(?:this|that)\s+vehicle\s+belong',
                'intent': 'get_vehicle_hierarchy_contextual',
                'extractor': self._extract_vehicle_from_context
            },
            # Zone hierarchy patterns with specific vehicle registration
            {
                'pattern': r'(?:zone|area).*(?:vehicle|truck)\s+([A-Z0-9-]+)(?!\s+belong)',
                'intent': 'get_zone_from_vehicle',
                'extractor': self._extract_zone_from_vehicle
            },
            {
                'pattern': r'(?:region|district).*(?:vehicle|truck)\s+([A-Z0-9-]+)(?!\s+belong)',
                'intent': 'get_region_from_vehicle',
                'extractor': self._extract_region_from_vehicle
            },
            {
                'pattern': r'(?:plant|facility).*(?:vehicle|truck)\s+([A-Z0-9-]+)(?!\s+belong)',
                'intent': 'get_plant_from_vehicle',
                'extractor': self._extract_plant_from_vehicle
            },
            {
                'pattern': r'(?:vehicles|trucks).*(?:zone|area)\s+([A-Z0-9\s]+)',
                'intent': 'get_vehicles_in_zone',
                'extractor': self._extract_vehicles_in_zone
            },
            {
                'pattern': r'(?:vehicles|trucks).*(?:region|district)\s+([A-Z0-9\s]+)',
                'intent': 'get_vehicles_in_region',
                'extractor': self._extract_vehicles_in_region
            },
            {
                'pattern': r'(?:vehicles|trucks).*(?:plant)\s+([A-Z0-9\s]+)',
                'intent': 'get_vehicles_in_plant',
                'extractor': self._extract_vehicles_in_plant
            },
            {
                'pattern': r'(?:vehicles|trucks).*(?:of|in|at)\s+([a-zA-Z0-9\s\-]+?)(?:\s+plant|$)',
                'intent': 'get_vehicles_of_plant',
                'extractor': self._extract_vehicles_of_plant_flexible
            },
            {
                'pattern': r'(?:hierarchy|structure|relationship).*(?:vehicle|truck)\s+([A-Z0-9-]+)',
                'intent': 'get_vehicle_hierarchy',
                'extractor': self._extract_vehicle_hierarchy
            },
            
            # Existing plant patterns
            {
                'pattern': r'(?:plant\s+name|name\s+of.*plant).*(?:plant\s+id|id)\s*(\d+)',
                'intent': 'get_plant_name_from_id',
                'extractor': self._extract_plant_id_direct
            },
            {
                'pattern': r'(?:plant\s+name|name\s+of.*plant).*(?:complaint.*(\d+)|mentioned.*(\d+))',
                'intent': 'get_plant_name_from_context',
                'extractor': self._extract_plant_from_complaint_context
            },
            {
                'pattern': r'(?:plant\s+id|id.*plant).*(\w+)',
                'intent': 'get_plant_id_from_name',
                'extractor': self._extract_plant_name_for_id
            },
            {
                'pattern': r'(?:site\s+visit.*details).*(\w+\s+plant|\w+)',
                'intent': 'get_site_visit_for_plant',
                'extractor': self._extract_plant_for_site_visit
            },
            {
                'pattern': r'(?:customer\s+name|name\s+of.*customer).*(?:customer\s+id|id)\s*(\d+)',
                'intent': 'get_customer_name_from_id', 
                'extractor': self._extract_customer_id_direct
            },
            {
                'pattern': r'(?:status|state).*(?:complaint|complaint\s+id)\s*(\d+)',
                'intent': 'get_complaint_status',
                'extractor': self._extract_complaint_id_direct
            },
            {
                'pattern': r'(?:show|list|get).*complaints.*(?:status\s+is|with\s+status)\s+(\w+)',
                'intent': 'get_complaints_by_status',
                'extractor': self._extract_complaint_status
            },
            {
                'pattern': r'(?:what|tell.*about|details.*of).*(?:that|the|this)\s+(?:plant|customer|vehicle)',
                'intent': 'get_details_from_last_context',
                'extractor': self._extract_from_last_context
            },
            
            # CRM Complaint Status Patterns
            {
                'pattern': r'(?:status|state).*(?:complaint|complaint\s+id)\s*(\d+)',
                'intent': 'get_complaint_status',
                'extractor': self._extract_complaint_id_direct
            },
            {
                'pattern': r'(?:show|list|get).*complaints.*(?:status\s+is|with\s+status)\s+(\w+)',
                'intent': 'get_complaints_by_status',
                'extractor': self._extract_complaint_status
            },
            {
                'pattern': r'(?:complaint.*(?:pending\s+with|assigned\s+to)|(?:who|which).*(?:handling|responsible).*complaint)\s*(\d+)',
                'intent': 'get_complaint_pending_with',
                'extractor': self._extract_complaint_id_for_pending
            },
            {
                'pattern': r'(?:overall\s+status|workflow\s+status|current\s+stage).*complaint\s*(\d+)',
                'intent': 'get_complaint_workflow_status',
                'extractor': self._extract_complaint_id_for_workflow
            },
            {
                'pattern': r'(?:show|list).*complaints.*(?:pending\s+with|assigned\s+to|with)\s+([a-zA-Z\s]+)',
                'intent': 'get_complaints_by_assignee',
                'extractor': self._extract_assignee_for_complaints
            },
            {
                'pattern': r'(?:complaints|complaint).*(?:pending\s+with|assigned\s+to|with)\s+([a-zA-Z\s]+)',
                'intent': 'get_complaints_by_assignee',
                'extractor': self._extract_assignee_for_complaints
            },
            {
                'pattern': r'(?:action\s+status|approval\s+status|approval).*complaint\s*(\d+)',
                'intent': 'get_complaint_action_status',
                'extractor': self._extract_complaint_id_for_action_status
            },
            {
                'pattern': r'(?:ho\s+qc|business\s+head|technical\s+head|cfo|md).*(?:approved|rejected|action).*complaint\s*(\d+)',
                'intent': 'get_specific_action_status',
                'extractor': self._extract_complaint_and_authority
            },
            {
                'pattern': r'(?:show|list).*complaints.*(?:approved|rejected).*(?:by|from)\s+(ho\s+qc|business\s+head|technical\s+head|cfo|md)',
                'intent': 'get_complaints_by_action_status',
                'extractor': self._extract_authority_and_action
            },
            
            # Product Correction Status Patterns
            {
                'pattern': r'(?:show|list|get).*complaints.*(?:product\s+correction|correction).*(?:done|completed|finished)',
                'intent': 'get_complaints_with_product_correction_done',
                'extractor': self._extract_product_correction_done
            },
            {
                'pattern': r'(?:show|list|get).*complaints.*(?:product\s+correction|correction).*(?:not\s+done|pending|incomplete|missing)',
                'intent': 'get_complaints_without_product_correction',
                'extractor': self._extract_product_correction_not_done
            },
            {
                'pattern': r'(?:show|list|get).*complaints.*(?:no|without|missing).*(?:product\s+correction|correction)',
                'intent': 'get_complaints_without_product_correction',
                'extractor': self._extract_product_correction_not_done
            },
            {
                'pattern': r'(?:show|list|get).*complaints.*(?:with|having).*(?:product\s+correction|correction)',
                'intent': 'get_complaints_with_product_correction_done',
                'extractor': self._extract_product_correction_done
            },
            {
                'pattern': r'(?:product\s+correction|correction).*(?:status|done|completed).*(?:complaint|complaint\s+id)\s*(\d+)',
                'intent': 'get_complaint_product_correction_status',
                'extractor': self._extract_complaint_id_for_product_correction
            },
            {
                'pattern': r'(?:complaint|complaint\s+id)\s*(\d+).*(?:product\s+correction|correction).*(?:status|done|completed)',
                'intent': 'get_complaint_product_correction_status',
                'extractor': self._extract_complaint_id_for_product_correction
            },
            
            # Category-based Complaint Patterns (Operation/Operations & Technical)
            {
                'pattern': r'(?:how\s+many|count|number\s+of).*complaints.*(?:of|in|from)\s+(?:operations?|operation)',
                'intent': 'get_complaints_count_by_category',
                'extractor': self._extract_operations_category_count
            },
            {
                'pattern': r'(?:how\s+many|count|number\s+of).*complaints.*(?:of|in|from)\s+(?:technical|tech)',
                'intent': 'get_complaints_count_by_category',
                'extractor': self._extract_technical_category_count
            },
            {
                'pattern': r'(?:show|list|get).*complaints.*(?:of|in|from)\s+(?:operations?|operation)',
                'intent': 'get_complaints_by_category',
                'extractor': self._extract_operations_category
            },
            {
                'pattern': r'(?:show|list|get).*complaints.*(?:of|in|from)\s+(?:technical|tech)',
                'intent': 'get_complaints_by_category',
                'extractor': self._extract_technical_category
            },
            {
                'pattern': r'(?:operations?|operation).*complaints',
                'intent': 'get_complaints_by_category',
                'extractor': self._extract_operations_category
            },
            {
                'pattern': r'(?:technical|tech).*complaints',
                'intent': 'get_complaints_by_category',
                'extractor': self._extract_technical_category
            },
            {
                'pattern': r'complaints.*(?:in|from)\s+(?:operations?|operation).*(?:category|dept|department)',
                'intent': 'get_complaints_by_category',
                'extractor': self._extract_operations_category
            },
            {
                'pattern': r'complaints.*(?:in|from)\s+(?:technical|tech).*(?:category|dept|department)',
                'intent': 'get_complaints_by_category',
                'extractor': self._extract_technical_category
            },
            {
                'pattern': r'complaints\s+(?:operations?|operation)(?:\s|$)',
                'intent': 'get_complaints_by_category',
                'extractor': self._extract_operations_category
            },
            {
                'pattern': r'complaints\s+(?:technical|tech)(?:\s|$)',
                'intent': 'get_complaints_by_category',
                'extractor': self._extract_technical_category
            },
            
            # Distance Report Patterns
            {
                'pattern': r'(?:show|display|get|find)\s+(?:distance|travel)\s+report',
                'intent': 'show_distance_report',
                'extractor': self._extract_distance_report_criteria
            },
            {
                'pattern': r'distance\s+(?:report|data)\s+(?:for|of)\s+vehicle\s+(\w+)',
                'intent': 'vehicle_distance_report',
                'extractor': self._extract_vehicle_distance_criteria
            },
            {
                'pattern': r'(?:show|get)\s+(?:drum\s+rotation|travel\s+time)\s+(?:for|of)\s+(\w+)',
                'intent': 'vehicle_drum_rotation',
                'extractor': self._extract_vehicle_distance_criteria  
            },
            {
                'pattern': r'(?:total|sum)\s+distance\s+(?:traveled|travelled|covered)',
                'intent': 'total_distance_traveled',
                'extractor': self._extract_distance_aggregation_criteria
            },
            {
                'pattern': r'(?:inter.*plant|plant.*to.*plant)\s+(?:distance|travel)',
                'intent': 'inter_plant_distance',
                'extractor': self._extract_inter_plant_criteria
            },
            {
                'pattern': r'(?:vehicle|truck)\s+travel\s+(?:between|from.*to)\s+(?:plants|facilities)',
                'intent': 'inter_plant_vehicle_travel',
                'extractor': self._extract_inter_plant_criteria
            },
            {
                'pattern': r'(?:daily|monthly|weekly)\s+distance\s+(?:report|analysis)',
                'intent': 'time_based_distance_report',
                'extractor': self._extract_time_distance_criteria
            }
        ]
    
    def analyze_query_intent(self, user_query: str, chat_context) -> Optional[Dict]:
        """
        Analyze user query to detect if it requires intelligent reasoning
        Returns enhanced query info if reasoning is needed, None otherwise
        """
        user_query_lower = user_query.lower().strip()
        print(f"🧠 [DEBUG] Analyzing query: '{user_query}'")
        
        # Check each intent pattern
        for i, intent_config in enumerate(self.intent_patterns):
            pattern = intent_config['pattern']
            intent = intent_config['intent']
            extractor = intent_config['extractor']
            
            match = re.search(pattern, user_query_lower, re.IGNORECASE)
            if match:
                print(f"🎯 [DEBUG] Pattern {i+1} matched! Intent: {intent}")
                print(f"📝 [DEBUG] Pattern: {pattern}")
                print(f"🔍 [DEBUG] Match groups: {match.groups()}")
                
                # Extract relevant data using the specific extractor
                extracted_data = extractor(user_query, match, chat_context)
                
                if extracted_data:
                    print(f"✅ [DEBUG] Data extracted: {extracted_data}")
                    return {
                        'original_query': user_query,
                        'intent': intent,
                        'extracted_data': extracted_data,
                        'reasoning_type': 'contextual_auto_resolve'
                    }
                else:
                    print(f"❌ [DEBUG] No data extracted from pattern match")
        
        print(f"🚫 [DEBUG] No intelligent reasoning patterns matched")
        return None
    
    def _extract_plant_id_direct(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract plant ID directly mentioned in query"""
        plant_id = match.group(1)
        if plant_id:
            return {
                'plant_id': plant_id,
                'target_info': 'plant_name',
                'source': 'direct_mention'
            }
        return None
    
    def _extract_plant_from_complaint_context(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract plant ID from complaint context in conversation"""
        complaint_id = match.group(1) or match.group(2)
        
        # Look for plant_id in recent conversation context
        if chat_context and chat_context.last_displayed_items:
            for item in chat_context.last_displayed_items:
                if ('complaint_id' in item and str(item['complaint_id']) == str(complaint_id)) or \
                   ('complaint' in str(item.get('_original_question', '')).lower() and complaint_id in str(item.get('_original_question', ''))):
                    
                    plant_id = item.get('plant_id')
                    if plant_id:
                        return {
                            'plant_id': plant_id,
                            'target_info': 'plant_name',
                            'source': 'conversation_context',
                            'context_item': item
                        }
        
        # If not found in displayed items, look in recent history
        if chat_context and chat_context.history:
            for interaction in reversed(chat_context.history[-3:]):  # Last 3 interactions
                response = interaction.get('response', '')
                if complaint_id and complaint_id in response.lower():
                    # Try to extract plant_id from the response text
                    plant_match = re.search(r'plant\s+id[:\s]*(\d+)', response.lower())
                    if plant_match:
                        return {
                            'plant_id': plant_match.group(1),
                            'target_info': 'plant_name',
                            'source': 'response_text_analysis',
                            'context_response': response
                        }
        
        return None
    
    def _extract_complaint_status(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract status value for complaint lookup"""
        status = match.group(1).lower() if match.groups() else None
        if status:
            # Map common status terms to Y/N
            if status in ['open', 'active', 'ongoing']:
                return {'status': 'Y'}
            elif status in ['closed', 'resolved', 'completed', 'done']:
                return {'status': 'N'}
        return None

    def _extract_complaint_id_direct(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract complaint ID for status lookup"""
        complaint_id = match.group(1) if match.groups() else None
        return {'complaint_id': complaint_id} if complaint_id else None

    def _extract_customer_id_direct(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract customer ID directly mentioned in query"""
        customer_id = match.group(1)
        if customer_id:
            return {
                'customer_id': customer_id,
                'target_info': 'customer_name',
                'source': 'direct_mention'
            }
        return None
    
    def _extract_from_last_context(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract information from the last conversation context"""
        if not chat_context or not chat_context.last_displayed_items:
            return None
        
        last_item = chat_context.last_displayed_items[-1] if chat_context.last_displayed_items else None
        if last_item:
            # Determine what kind of info the user wants
            if 'plant' in query.lower():
                plant_id = last_item.get('plant_id')
                if plant_id:
                    return {
                        'plant_id': plant_id,
                        'target_info': 'plant_name',
                        'source': 'last_context_item'
                    }
            elif 'customer' in query.lower():
                customer_id = last_item.get('customer_id')
                if customer_id:
                    return {
                        'customer_id': customer_id,
                        'target_info': 'customer_name',
                        'source': 'last_context_item'
                    }
        
        return None

    # CRM Complaint Status Extractor Methods
    def _extract_complaint_status(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract status value for complaint lookup"""
        print(f"🔍 [DEBUG] Extracting complaint status from: {query}")
        status = match.group(1).lower() if match.groups() else None
        if status:
            print(f"📊 [DEBUG] Found status: {status}")
            # Map common status terms to Y/N
            if status in ['open', 'active', 'ongoing']:
                return {'status': 'Y'}
            elif status in ['closed', 'resolved', 'completed', 'done']:
                return {'status': 'N'}
        return None

    def _extract_complaint_id_direct(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract complaint ID for status lookup"""
        print(f"🔍 [DEBUG] Extracting complaint ID from: {query}")
        complaint_id = match.group(1) if match.groups() else None
        print(f"📊 [DEBUG] Found complaint ID: {complaint_id}")
        return {'complaint_id': complaint_id} if complaint_id else None

    def _extract_complaint_id_for_pending(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract complaint ID for pending/assignee lookup"""
        print(f"🔍 [DEBUG] Extracting complaint ID for pending lookup from: {query}")
        complaint_id = match.group(1) if match.groups() else None
        print(f"📊 [DEBUG] Found complaint ID for pending: {complaint_id}")
        return {'complaint_id': complaint_id, 'query_type': 'pending_with'} if complaint_id else None

    def _extract_complaint_id_for_workflow(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract complaint ID for workflow status lookup"""
        print(f"🔍 [DEBUG] Extracting complaint ID for workflow lookup from: {query}")
        complaint_id = match.group(1) if match.groups() else None
        print(f"📊 [DEBUG] Found complaint ID for workflow: {complaint_id}")
        return {'complaint_id': complaint_id, 'query_type': 'workflow_status'} if complaint_id else None

    def _extract_assignee_for_complaints(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract assignee name for complaint lookup"""
        print(f"🔍 [DEBUG] Extracting assignee from: {query}")
        assignee = match.group(1).strip() if match.groups() else None
        if assignee:
            print(f"📊 [DEBUG] Found assignee: '{assignee}'")
            # Normalize assignee names
            assignee_mapping = {
                'plant incharge': 'Plant Incharge',
                'technical manager': 'Technical Manager/Incharge',
                'technical incharge': 'Technical Manager/Incharge',
                'ho qc': 'HO QC',
                'business head': 'Business Head',
                'technical head': 'Technical Head',
                'cfo': 'CFO',
                'md': 'MD'
            }
            normalized_assignee = assignee_mapping.get(assignee.lower(), assignee)
            print(f"📊 [DEBUG] Normalized assignee: '{normalized_assignee}'")
            return {'assignee': normalized_assignee, 'query_type': 'by_assignee'}
        return None

    def _extract_complaint_id_for_action_status(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract complaint ID for action status lookup"""
        print(f"🔍 [DEBUG] Extracting complaint ID for action status from: {query}")
        complaint_id = match.group(1) if match.groups() else None
        print(f"📊 [DEBUG] Found complaint ID for action status: {complaint_id}")
        return {'complaint_id': complaint_id, 'query_type': 'action_status'} if complaint_id else None

    def _extract_complaint_and_authority(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract complaint ID and authority from action status query"""
        print(f"🔍 [DEBUG] Extracting complaint and authority from: {query}")
        complaint_id = match.group(1) if match.groups() else None
        
        # Extract authority from query text
        query_lower = query.lower()
        authority_mapping = {
            'ho qc': 'ho_qc_action_status',
            'business head': 'bh_action_status', 
            'technical head': 'th_action_status',
            'cfo': 'cf_action_status',
            'md': 'md_action_status'
        }
        
        authority_column = None
        for authority, column in authority_mapping.items():
            if authority in query_lower:
                authority_column = column
                break
        
        print(f"📊 [DEBUG] Found complaint ID: {complaint_id}, authority column: {authority_column}")
        
        if complaint_id and authority_column:
            return {
                'complaint_id': complaint_id,
                'authority_column': authority_column,
                'query_type': 'specific_authority_action'
            }
        return None

    def _extract_authority_and_action(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract authority and action type for complaint lookup"""
        print(f"🔍 [DEBUG] Extracting authority and action from: {query}")
        authority = match.group(1).strip() if match.groups() else None
        
        # Determine action type from query
        action_type = None
        if 'approved' in query.lower():
            action_type = 'A'
        elif 'rejected' in query.lower():
            action_type = 'R'
        
        # Map authority to column name
        authority_mapping = {
            'ho qc': 'ho_qc_action_status',
            'business head': 'bh_action_status',
            'technical head': 'th_action_status', 
            'cfo': 'cf_action_status',
            'md': 'md_action_status'
        }
        
        authority_column = authority_mapping.get(authority.lower())
        
        print(f"📊 [DEBUG] Found authority: {authority}, column: {authority_column}, action: {action_type}")
        
        if authority_column and action_type:
            return {
                'authority_column': authority_column,
                'action_type': action_type,
                'authority_name': authority,
                'query_type': 'by_authority_action'
            }
        return None

    # Product Correction Extractor Methods
    def _extract_product_correction_done(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract intent for complaints with product correction done (Y)"""
        print(f"🔍 [DEBUG] Extracting product correction done from: {query}")
        return {'product_correction_status': 'Y', 'query_type': 'product_correction_done'}

    def _extract_product_correction_not_done(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract intent for complaints without product correction (N)"""
        print(f"🔍 [DEBUG] Extracting product correction not done from: {query}")
        return {'product_correction_status': 'N', 'query_type': 'product_correction_not_done'}

    def _extract_complaint_id_for_product_correction(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract complaint ID for product correction status lookup"""
        print(f"🔍 [DEBUG] Extracting complaint ID for product correction from: {query}")
        complaint_id = match.group(1) if match.groups() else None
        print(f"📊 [DEBUG] Found complaint ID for product correction: {complaint_id}")
        return {'complaint_id': complaint_id, 'query_type': 'product_correction_status'} if complaint_id else None

    # Category-based Complaint Extractor Methods
    def _extract_operations_category_count(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract intent for counting Operations category complaints"""
        print(f"🔍 [DEBUG] Extracting operations category count from: {query}")
        return {'category_id': '1', 'category_name': 'Operations', 'query_type': 'count_by_category'}

    def _extract_technical_category_count(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract intent for counting Technical category complaints"""
        print(f"🔍 [DEBUG] Extracting technical category count from: {query}")
        return {'category_id': '2', 'category_name': 'Technical', 'query_type': 'count_by_category'}

    def _extract_operations_category(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract intent for listing Operations category complaints"""
        print(f"🔍 [DEBUG] Extracting operations category from: {query}")
        return {'category_id': '1', 'category_name': 'Operations', 'query_type': 'list_by_category'}

    def _extract_technical_category(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract intent for listing Technical category complaints"""
        print(f"🔍 [DEBUG] Extracting technical category from: {query}")
        return {'category_id': '2', 'category_name': 'Technical', 'query_type': 'list_by_category'}
    
    def _extract_plant_name_for_id(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract plant name to find its ID"""
        plant_name = match.group(1)
        if plant_name:
            return {
                'plant_name': plant_name.strip(),
                'target_info': 'plant_id',
                'source': 'direct_mention'
            }
        return None
    
    def _extract_plant_for_site_visit(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract plant name for site visit queries"""
        plant_reference = match.group(1)
        if plant_reference:
            return {
                'plant_reference': plant_reference.strip(),
                'target_info': 'site_visit_details',
                'source': 'plant_site_visit_query'
            }
        return None
    
    def generate_intelligent_query(self, reasoning_result: Dict) -> Optional[str]:
        """
        Generate SQL query based on intelligent reasoning result - ENHANCED HIERARCHICAL
        """
        intent = reasoning_result['intent']
        extracted_data = reasoning_result['extracted_data']
        
        print(f"🔧 [DEBUG] Generating query for intent: {intent}")
        print(f"📊 [DEBUG] Using extracted data: {extracted_data}")

        # Handle complaint status queries
        if intent == 'get_complaints_by_status':
            status = extracted_data.get('status')
            if status:
                print(f"🎯 [DEBUG] Generating complaints by status query for: {status}")
                return f"""SELECT COUNT(T1.id_no)
                          FROM public.crm_complaint_dtls AS T1 
                          WHERE T1.active_status ILIKE '{status}'"""
        
        elif intent == 'get_complaint_status':
            complaint_id = extracted_data.get('complaint_id')
            if complaint_id:
                print(f"🎯 [DEBUG] Generating complaint status query for ID: {complaint_id}")
                return f"""
                    SELECT 
                        cd.id_no as complaint_id,
                        cd.complaint_date,
                        csv.complaint_status,
                        cd.complaint_category_id,
                        CASE 
                            WHEN csv.complaint_status = 'P' AND cd.complaint_category_id = '1' THEN 'Plant Incharge'
                            WHEN csv.complaint_status = 'P' AND cd.complaint_category_id = '2' THEN 'Technical Manager/Incharge'
                            WHEN csv.complaint_status = 'QC' THEN 'HO QC'
                            WHEN csv.complaint_status = 'BH' THEN 'Business Head'
                            WHEN csv.complaint_status = 'TH' THEN 'Technical Head'
                            WHEN csv.complaint_status = 'CF' THEN 'CFO'
                            WHEN csv.complaint_status = 'MD' THEN 'MD'
                            WHEN csv.complaint_status = 'C' THEN 'Completed'
                            ELSE 'Unknown'
                        END as pending_with,
                        CASE 
                            WHEN csv.complaint_status = 'C' THEN 'Closed'
                            ELSE 'Open'
                        END as final_status,
                        CASE 
                            WHEN cd.complaint_category_id = '1' THEN 'Operations'
                            WHEN cd.complaint_category_id = '2' THEN 'Technical'
                            ELSE 'Unknown'
                        END as category_type
                    FROM crm_complaint_dtls cd
                    LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                    WHERE cd.id_no = {complaint_id}
                    LIMIT 1;
                """
        
        elif intent == 'get_complaint_pending_with':
            complaint_id = extracted_data.get('complaint_id')
            if complaint_id:
                print(f"🎯 [DEBUG] Generating pending with query for complaint: {complaint_id}")
                return f"""
                    SELECT 
                        cd.id_no as complaint_id,
                        cd.complaint_date,
                        csv.complaint_status,
                        cd.complaint_category_id,
                        CASE 
                            WHEN csv.complaint_status = 'P' AND cd.complaint_category_id = '1' THEN 'Plant Incharge'
                            WHEN csv.complaint_status = 'P' AND cd.complaint_category_id = '2' THEN 'Technical Manager/Incharge'
                            WHEN csv.complaint_status = 'QC' THEN 'HO QC'
                            WHEN csv.complaint_status = 'BH' THEN 'Business Head'
                            WHEN csv.complaint_status = 'TH' THEN 'Technical Head'
                            WHEN csv.complaint_status = 'CF' THEN 'CFO'
                            WHEN csv.complaint_status = 'MD' THEN 'MD'
                            WHEN csv.complaint_status = 'C' THEN 'Completed'
                            ELSE 'Unknown'
                        END as pending_with,
                        CASE 
                            WHEN csv.complaint_status = 'C' THEN 'Closed'
                            ELSE 'Open'
                        END as final_status,
                        CASE 
                            WHEN cd.complaint_category_id = '1' THEN 'Operations'
                            WHEN cd.complaint_category_id = '2' THEN 'Technical'
                            ELSE 'Unknown'
                        END as category_type
                    FROM crm_complaint_dtls cd
                    LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                    WHERE cd.id_no = {complaint_id}
                    LIMIT 1;
                """
        
        elif intent == 'get_complaints_by_assignee':
            assignee = extracted_data.get('assignee')
            if assignee:
                print(f"🎯 [DEBUG] Generating complaints by assignee query for: {assignee}")
                
                # This is the key logic you mentioned!
                if assignee == 'Plant Incharge':
                    return f"""
                        SELECT 
                            cd.id_no as complaint_id,
                            cd.complaint_date,
                            csv.complaint_status,
                            cd.complaint_category_id,
                            'Plant Incharge' as pending_with,
                            'Operations' as category_type
                        FROM crm_complaint_dtls cd
                        LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                        WHERE csv.complaint_status = 'P' 
                          AND cd.complaint_category_id = '1'
                        ORDER BY cd.complaint_date DESC
                        LIMIT 50;
                    """
                elif assignee == 'Technical Manager/Incharge':
                    return f"""
                        SELECT 
                            cd.id_no as complaint_id,
                            cd.complaint_date,
                            csv.complaint_status,
                            cd.complaint_category_id,
                            'Technical Manager/Incharge' as pending_with,
                            'Technical' as category_type
                        FROM crm_complaint_dtls cd
                        LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                        WHERE csv.complaint_status = 'P' 
                          AND cd.complaint_category_id = '2'
                        ORDER BY cd.complaint_date DESC
                        LIMIT 50;
                    """
                else:
                    # For other assignees (QC, BH, TH, CF, MD)
                    status_mapping = {
                        'HO QC': 'QC',
                        'Business Head': 'BH',
                        'Technical Head': 'TH',
                        'CFO': 'CF',
                        'MD': 'MD'
                    }
                    status = status_mapping.get(assignee, assignee)
                    return f"""
                        SELECT 
                            cd.id_no as complaint_id,
                            cd.complaint_date,
                            csv.complaint_status,
                            cd.complaint_category_id,
                            '{assignee}' as pending_with,
                            CASE 
                                WHEN cd.complaint_category_id = '1' THEN 'Operations'
                                WHEN cd.complaint_category_id = '2' THEN 'Technical'
                                ELSE 'Unknown'
                            END as category_type
                        FROM crm_complaint_dtls cd
                        LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                        WHERE csv.complaint_status = '{status}'
                        ORDER BY cd.complaint_date DESC
                        LIMIT 50;
                    """
        
        elif intent == 'get_complaint_workflow_status':
            complaint_id = extracted_data.get('complaint_id')
            if complaint_id:
                print(f"🎯 [DEBUG] Generating workflow status query for complaint: {complaint_id}")
                return f"""
                    SELECT 
                        cd.id_no as complaint_id,
                        cd.complaint_date,
                        csv.complaint_status,
                        cd.complaint_category_id,
                        csv.ho_qc_action_status,
                        csv.bh_action_status,
                        csv.th_action_status,
                        csv.cf_action_status,
                        csv.md_action_status,
                        CASE 
                            WHEN csv.complaint_status = 'P' AND cd.complaint_category_id = '1' THEN 'Plant Incharge'
                            WHEN csv.complaint_status = 'P' AND cd.complaint_category_id = '2' THEN 'Technical Manager/Incharge'
                            WHEN csv.complaint_status = 'QC' THEN 'HO QC'
                            WHEN csv.complaint_status = 'BH' THEN 'Business Head'
                            WHEN csv.complaint_status = 'TH' THEN 'Technical Head'
                            WHEN csv.complaint_status = 'CF' THEN 'CFO'
                            WHEN csv.complaint_status = 'MD' THEN 'MD'
                            WHEN csv.complaint_status = 'C' THEN 'Completed'
                            ELSE 'Unknown'
                        END as current_stage,
                        CASE 
                            WHEN cd.complaint_category_id = '1' THEN 'Operations'
                            WHEN cd.complaint_category_id = '2' THEN 'Technical'
                            ELSE 'Unknown'
                        END as category_type
                    FROM crm_complaint_dtls cd
                    LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                    WHERE cd.id_no = {complaint_id}
                    LIMIT 1;
                """
        
        elif intent == 'get_specific_action_status':
            complaint_id = extracted_data.get('complaint_id')
            authority_column = extracted_data.get('authority_column')
            if complaint_id and authority_column:
                print(f"🎯 [DEBUG] Generating specific action status query for complaint {complaint_id}, authority: {authority_column}")
                return f"""
                    SELECT 
                        cd.id_no as complaint_id,
                        cd.complaint_date,
                        csv.{authority_column},
                        CASE csv.{authority_column}
                            WHEN 'A' THEN 'Approved'
                            WHEN 'R' THEN 'Rejected'
                            ELSE 'Pending'
                        END as action_status_description
                    FROM crm_complaint_dtls cd
                    LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                    WHERE cd.id_no = {complaint_id}
                    LIMIT 1;
                """
        
        elif intent == 'get_complaints_by_action_status':
            authority_column = extracted_data.get('authority_column')
            action_type = extracted_data.get('action_type')
            authority_name = extracted_data.get('authority_name')
            if authority_column and action_type:
                print(f"🎯 [DEBUG] Generating complaints by action status query for {authority_name}: {action_type}")
                return f"""
                    SELECT 
                        cd.id_no as complaint_id,
                        cd.complaint_date,
                        csv.{authority_column},
                        CASE csv.{authority_column}
                            WHEN 'A' THEN 'Approved'
                            WHEN 'R' THEN 'Rejected'
                            ELSE 'Pending'
                        END as action_status_description,
                        '{authority_name}' as authority
                    FROM crm_complaint_dtls cd
                    LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                    WHERE csv.{authority_column} = '{action_type}'
                    ORDER BY cd.complaint_date DESC
                    LIMIT 50;
                """
        
        # Product Correction Status Queries
        elif intent == 'get_complaints_with_product_correction_done':
            print(f"🎯 [DEBUG] Generating complaints with product correction done query")
            return f"""
                SELECT 
                    cd.id_no as complaint_id,
                    cd.complaint_date,
                    csv.product_correction,
                    csv.complaint_status,
                    cd.complaint_category_id,
                    CASE 
                        WHEN cd.complaint_category_id = '1' THEN 'Operations'
                        WHEN cd.complaint_category_id = '2' THEN 'Technical'
                        ELSE 'Unknown'
                    END as category_type,
                    'Product Correction Done' as correction_status
                FROM crm_complaint_dtls cd
                LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                WHERE csv.product_correction = 'Y'
                ORDER BY cd.complaint_date DESC
                LIMIT 50;
            """
        
        elif intent == 'get_complaints_without_product_correction':
            print(f"🎯 [DEBUG] Generating complaints without product correction query")
            return f"""
                SELECT 
                    cd.id_no as complaint_id,
                    cd.complaint_date,
                    csv.product_correction,
                    csv.complaint_status,
                    cd.complaint_category_id,
                    CASE 
                        WHEN cd.complaint_category_id = '1' THEN 'Operations'
                        WHEN cd.complaint_category_id = '2' THEN 'Technical'
                        ELSE 'Unknown'
                    END as category_type,
                    CASE 
                        WHEN csv.product_correction = 'N' THEN 'Product Correction Not Done'
                        WHEN csv.product_correction IS NULL OR csv.product_correction = '' THEN 'No Correction Status'
                        ELSE 'Unknown Status'
                    END as correction_status
                FROM crm_complaint_dtls cd
                LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                WHERE csv.product_correction = 'N' 
                   OR csv.product_correction IS NULL 
                   OR csv.product_correction = ''
                ORDER BY cd.complaint_date DESC
                LIMIT 50;
            """
        
        elif intent == 'get_complaint_product_correction_status':
            complaint_id = extracted_data.get('complaint_id')
            if complaint_id:
                print(f"🎯 [DEBUG] Generating product correction status query for complaint: {complaint_id}")
                return f"""
                    SELECT 
                        cd.id_no as complaint_id,
                        cd.complaint_date,
                        csv.product_correction,
                        csv.complaint_status,
                        cd.complaint_category_id,
                        CASE 
                            WHEN csv.product_correction = 'Y' THEN 'Product Correction Done'
                            WHEN csv.product_correction = 'N' THEN 'Product Correction Not Done'
                            WHEN csv.product_correction IS NULL OR csv.product_correction = '' THEN 'No Correction Status Recorded'
                            ELSE 'Unknown Status'
                        END as correction_status_description,
                        CASE 
                            WHEN cd.complaint_category_id = '1' THEN 'Operations'
                            WHEN cd.complaint_category_id = '2' THEN 'Technical'
                            ELSE 'Unknown'
                        END as category_type
                    FROM crm_complaint_dtls cd
                    LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                    WHERE cd.id_no = {complaint_id}
                    LIMIT 1;
                """
        
        # Category-based complaint queries
        elif intent == 'get_complaints_count_by_category':
            category_id = extracted_data.get('category_id')
            category_name = extracted_data.get('category_name')
            if category_id and category_name:
                print(f"🎯 [DEBUG] Generating complaints count by category query for: {category_name} (ID: {category_id})")
                return f"""
                    SELECT COUNT(cd.id_no) as complaint_count,
                           '{category_name}' as category_name,
                           '{category_id}' as category_id
                    FROM crm_complaint_dtls cd
                    WHERE cd.complaint_category_id = '{category_id}'
                    AND cd.active_status = 'Y';
                """
        
        elif intent == 'get_complaints_by_category':
            category_id = extracted_data.get('category_id')
            category_name = extracted_data.get('category_name')
            if category_id and category_name:
                print(f"🎯 [DEBUG] Generating complaints by category query for: {category_name} (ID: {category_id})")
                return f"""
                    SELECT 
                        cd.id_no as complaint_id,
                        cd.complaint_date,
                        cd.complaint_subject,
                        csv.complaint_status,
                        cd.complaint_category_id,
                        '{category_name}' as category_name,
                        CASE 
                            WHEN csv.complaint_status = 'P' AND cd.complaint_category_id = '1' THEN 'Plant Incharge'
                            WHEN csv.complaint_status = 'P' AND cd.complaint_category_id = '2' THEN 'Technical Manager/Incharge'
                            WHEN csv.complaint_status = 'QC' THEN 'HO QC'
                            WHEN csv.complaint_status = 'BH' THEN 'Business Head'
                            WHEN csv.complaint_status = 'TH' THEN 'Technical Head'
                            WHEN csv.complaint_status = 'CF' THEN 'CFO'
                            WHEN csv.complaint_status = 'MD' THEN 'MD'
                            WHEN csv.complaint_status = 'C' THEN 'Completed'
                            ELSE 'Unknown'
                        END as pending_with,
                        CASE 
                            WHEN csv.complaint_status = 'C' THEN 'Closed'
                            ELSE 'Open'
                        END as final_status
                    FROM crm_complaint_dtls cd
                    LEFT JOIN crm_site_visit_dtls csv ON cd.id_no = csv.complaint_id
                    WHERE cd.complaint_category_id = '{category_id}'
                    AND cd.active_status = 'Y'
                    ORDER BY cd.complaint_date DESC
                    LIMIT 50;
                """
        
        # Check for hierarchical queries first
        if intent.startswith(('get_zone_', 'get_region_', 'get_plant_', 'get_vehicles_', 'get_vehicle_hierarchy')):
            return self.generate_hierarchical_query(reasoning_result)
        
        # Existing query generation logic
        if intent == 'get_plant_name_from_id' or \
           intent == 'get_plant_name_from_context':
            
            plant_id = extracted_data.get('plant_id')
            if plant_id:
                # Use hosp_master for plant information - STRICT HIERARCHICAL
                return f"""SELECT DISTINCT hm.id_no as plant_id, hm.name as plant_name, hm.address
                          FROM hosp_master hm  
                          WHERE hm.id_no = {plant_id} 
                          LIMIT 5;"""
        
        elif intent == 'get_plant_id_from_name':
            plant_name = extracted_data.get('plant_name')
            if plant_name:
                return f"""SELECT DISTINCT hm.id_no as plant_id, hm.name as plant_name, hm.address
                          FROM hosp_master hm 
                          WHERE hm.name ILIKE '%{plant_name}%'
                          LIMIT 10;"""
        
        elif intent == 'get_site_visit_for_plant':
            plant_reference = extracted_data.get('plant_reference')
            if plant_reference:
                return f"""SELECT DISTINCT csv.*, hm.name as plant_name, hm.address
                          FROM public.crm_site_visit_dtls csv
                          JOIN hosp_master hm ON csv.plant_id = hm.id_no
                          WHERE hm.name ILIKE '%{plant_reference}%'
                          LIMIT 10;"""
        
        elif intent == 'get_customer_name_from_id':
            customer_id = extracted_data.get('customer_id') 
            if customer_id:
                return f"""SELECT DISTINCT customer_id, customer_name 
                          FROM public.customer_master 
                          WHERE customer_id = {customer_id} 
                          LIMIT 1;"""
        
        # Distance Report Queries
        elif intent == 'show_distance_report':
            return f"""
                SELECT dr.reg_no, dr.from_tm, dr.to_tm,
                       ROUND(dr.distance / 1000.0, 2) as distance_km,
                       CONCAT(LPAD((ROUND(dr.drum_rotation / 2.0)::integer / 60)::text, 2, '0'), ':', 
                              LPAD((ROUND(dr.drum_rotation / 2.0)::integer % 60)::text, 2, '0')) as drum_rotation_time,
                       hm.name as plant_name,
                       dm.name as region_name
                FROM public.distance_report dr
                JOIN public.vehicle_master vm ON dr.reg_no = vm.reg_no
                JOIN public.hosp_master hm ON vm.id_hosp = hm.id_no
                JOIN public.district_master dm ON hm.id_dist = dm.id_no
                ORDER BY dr.from_tm DESC
                LIMIT 50;
            """
        
        elif intent == 'vehicle_distance_report':
            vehicle_reg = extracted_data.get('vehicle_reg')
            if vehicle_reg:
                return f"""
                    SELECT dr.reg_no, dr.from_tm, dr.to_tm,
                           ROUND(dr.distance / 1000.0, 2) as distance_km,
                           CONCAT(LPAD((ROUND(dr.drum_rotation / 2.0)::integer / 60)::text, 2, '0'), ':', 
                                  LPAD((ROUND(dr.drum_rotation / 2.0)::integer % 60)::text, 2, '0')) as drum_rotation_time,
                           hm.name as plant_name,
                           dm.name as region_name
                    FROM public.distance_report dr
                    JOIN public.vehicle_master vm ON dr.reg_no = vm.reg_no
                    JOIN public.hosp_master hm ON vm.id_hosp = hm.id_no
                    JOIN public.district_master dm ON hm.id_dist = dm.id_no
                    WHERE dr.reg_no ILIKE '{vehicle_reg}'
                    ORDER BY dr.from_tm DESC
                    LIMIT 50;
                """
        
        elif intent == 'vehicle_drum_rotation':
            vehicle_reg = extracted_data.get('vehicle_reg')
            if vehicle_reg:
                return f"""
                    SELECT dr.reg_no, dr.from_tm, dr.to_tm,
                           CONCAT(LPAD((ROUND(dr.drum_rotation / 2.0)::integer / 60)::text, 2, '0'), ':', 
                                  LPAD((ROUND(dr.drum_rotation / 2.0)::integer % 60)::text, 2, '0')) as drum_rotation_time,
                           ROUND(dr.distance / 1000.0, 2) as distance_km
                    FROM public.distance_report dr
                    WHERE dr.reg_no ILIKE '{vehicle_reg}'
                    ORDER BY dr.from_tm DESC
                    LIMIT 20;
                """
        
        elif intent == 'total_distance_traveled':
            aggregation = extracted_data.get('aggregation', 'total')
            if aggregation == 'total':
                return f"""
                    SELECT dr.reg_no,
                           SUM(ROUND(dr.distance / 1000.0, 2)) as total_distance_km,
                           COUNT(*) as total_trips
                    FROM public.distance_report dr
                    GROUP BY dr.reg_no
                    ORDER BY total_distance_km DESC
                    LIMIT 20;
                """
            elif aggregation == 'average':
                return f"""
                    SELECT dr.reg_no,
                           AVG(ROUND(dr.distance / 1000.0, 2)) as avg_distance_km,
                           COUNT(*) as total_trips
                    FROM public.distance_report dr
                    GROUP BY dr.reg_no
                    ORDER BY avg_distance_km DESC
                    LIMIT 20;
                """
        
        elif intent == 'inter_plant_distance':
            return f"""
                SELECT hm.name as plant_name,
                       COUNT(*) as trips,
                       SUM(ROUND(dr.distance / 1000.0, 2)) as total_distance_km,
                       AVG(ROUND(dr.distance / 1000.0, 2)) as avg_distance_km,
                       dm.name as region_name
                FROM public.distance_report dr
                JOIN public.vehicle_master vm ON dr.reg_no = vm.reg_no
                JOIN public.hosp_master hm ON vm.id_hosp = hm.id_no
                JOIN public.district_master dm ON hm.id_dist = dm.id_no
                GROUP BY hm.name, dm.name
                ORDER BY total_distance_km DESC
                LIMIT 20;
            """
        
        elif intent == 'inter_plant_vehicle_travel':
            return f"""
                SELECT dr.reg_no,
                       hm.name as vehicle_plant,
                       dm.name as region,
                       COUNT(*) as inter_plant_trips,
                       SUM(ROUND(dr.distance / 1000.0, 2)) as total_travel_km
                FROM public.distance_report dr
                JOIN public.vehicle_master vm ON dr.reg_no = vm.reg_no
                JOIN public.hosp_master hm ON vm.id_hosp = hm.id_no
                JOIN public.district_master dm ON hm.id_dist = dm.id_no
                GROUP BY dr.reg_no, hm.name, dm.name
                HAVING COUNT(*) > 1
                ORDER BY total_travel_km DESC
                LIMIT 20;
            """
        
        elif intent == 'time_based_distance_report':
            time_period = extracted_data.get('time_period', 'daily')
            if time_period == 'daily':
                return f"""
                    SELECT DATE(dr.from_tm) as travel_date,
                           COUNT(*) as trips,
                           SUM(ROUND(dr.distance / 1000.0, 2)) as total_km,
                           COUNT(DISTINCT dr.reg_no) as vehicles_used
                    FROM public.distance_report dr
                    GROUP BY DATE(dr.from_tm)
                    ORDER BY travel_date DESC
                    LIMIT 30;
                """
            elif time_period == 'monthly':
                return f"""
                    SELECT EXTRACT(YEAR FROM dr.from_tm) as year,
                           EXTRACT(MONTH FROM dr.from_tm) as month,
                           COUNT(*) as trips,
                           SUM(ROUND(dr.distance / 1000.0, 2)) as total_km,
                           COUNT(DISTINCT dr.reg_no) as vehicles_used
                    FROM public.distance_report dr
                    GROUP BY EXTRACT(YEAR FROM dr.from_tm), EXTRACT(MONTH FROM dr.from_tm)
                    ORDER BY year DESC, month DESC
                    LIMIT 12;
                """
            elif time_period == 'weekly':
                return f"""
                    SELECT DATE_TRUNC('week', dr.from_tm) as week_start,
                           COUNT(*) as trips,
                           SUM(ROUND(dr.distance / 1000.0, 2)) as total_km,
                           COUNT(DISTINCT dr.reg_no) as vehicles_used
                    FROM public.distance_report dr
                    GROUP BY DATE_TRUNC('week', dr.from_tm)
                    ORDER BY week_start DESC
                    LIMIT 10;
                """
        
        print(f"❌ [DEBUG] No query generation logic found for intent: {intent}")
        return None
    
    def create_intelligent_response(self, reasoning_result: Dict, query_result: Dict) -> str:
        """
        Create a natural, intelligent response that explains the reasoning - ENHANCED HIERARCHICAL
        """
        extracted_data = reasoning_result['extracted_data']
        intent = reasoning_result['intent']
        source = extracted_data.get('source', 'unknown')
        
        print(f"💬 [DEBUG] Creating response for intent: {intent}")
        print(f"📊 [DEBUG] Query result type: {type(query_result)}")
        print(f"📝 [DEBUG] Query result keys: {query_result.keys() if isinstance(query_result, dict) else 'N/A'}")

        # Handle complaint status count responses
        if intent == 'get_complaints_by_status':
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = query_result['rows'][0].get('count', 0)
                status_display = 'open' if extracted_data.get('status') == 'Y' else 'closed'
                return f"Found {count} {status_display} complaints."
            return "Counting complaints with the specified status..."

        # Handle complaint status responses
        if intent == 'get_complaint_status':
            complaint_id = extracted_data.get('complaint_id')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                row = query_result['rows'][0]
                pending_with = row.get('pending_with', 'Unknown')
                final_status = row.get('final_status', 'Unknown')
                return f"Complaint ID {complaint_id} is currently with: {pending_with} (Status: {final_status})"
            return f"Checking status for complaint ID {complaint_id}..."
        
        # Handle pending with responses
        if intent == 'get_complaint_pending_with':
            complaint_id = extracted_data.get('complaint_id')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                row = query_result['rows'][0]
                pending_with = row.get('pending_with', 'Unknown')
                return f"Complaint ID {complaint_id} is currently pending with: {pending_with}"
            return f"Checking who is handling complaint ID {complaint_id}..."
        
        # Handle complaints by assignee responses
        if intent == 'get_complaints_by_assignee':
            assignee = extracted_data.get('assignee')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} complaints currently assigned to {assignee}."
            return f"Searching for complaints assigned to {assignee}..."
        
        # Handle workflow status responses
        if intent == 'get_complaint_workflow_status':
            complaint_id = extracted_data.get('complaint_id')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                row = query_result['rows'][0]
                current_stage = row.get('current_stage', 'Unknown')
                return f"Complaint ID {complaint_id} is currently at stage: {current_stage}"
            return f"Checking workflow status for complaint ID {complaint_id}..."
        
        # Handle specific action status responses
        if intent == 'get_specific_action_status':
            complaint_id = extracted_data.get('complaint_id')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                row = query_result['rows'][0]
                action_status = row.get('action_status_description', 'Unknown')
                return f"The action status for complaint ID {complaint_id} is: {action_status}"
            return f"Checking specific action status for complaint ID {complaint_id}..."
        
        # Handle complaints by action status responses
        if intent == 'get_complaints_by_action_status':
            authority_name = extracted_data.get('authority_name')
            action_type = 'approved' if extracted_data.get('action_type') == 'A' else 'rejected'
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} complaints {action_type} by {authority_name}."
            return f"Searching for complaints {action_type} by {authority_name}..."
        
        # Product Correction response templates
        if intent == 'get_complaints_with_product_correction_done':
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} complaints where product correction has been done."
            return "Searching for complaints with product correction completed..."
        
        if intent == 'get_complaints_without_product_correction':
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} complaints where product correction is not done or status is missing."
            return "Searching for complaints without product correction..."
        
        if intent == 'get_complaint_product_correction_status':
            complaint_id = extracted_data.get('complaint_id')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                row = query_result['rows'][0]
                correction_status = row.get('correction_status_description', 'Unknown')
                return f"Product correction status for complaint ID {complaint_id}: {correction_status}"
            return f"Checking product correction status for complaint ID {complaint_id}..."
        
        # Category-based complaint response templates
        if intent == 'get_complaints_count_by_category':
            category_name = extracted_data.get('category_name')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = query_result['rows'][0].get('complaint_count', 0)
                return f"Found {count} complaints in {category_name} category."
            return f"Counting complaints in {category_name} category..."
        
        if intent == 'get_complaints_by_category':
            category_name = extracted_data.get('category_name')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} complaints in {category_name} category."
            return f"Listing complaints in {category_name} category..."
        
        # Hierarchical response templates
        if intent.startswith(('get_zone_', 'get_region_', 'get_plant_', 'get_vehicles_', 'get_vehicle_hierarchy')):
            hierarchical_responses = {
                'get_zone_from_vehicle': f"Here's the zone information for vehicle {extracted_data.get('vehicle_reg', 'N/A')}:",
                'get_region_from_vehicle': f"Here's the region information for vehicle {extracted_data.get('vehicle_reg', 'N/A')}:",
                'get_plant_from_vehicle': f"Here's the plant information for vehicle {extracted_data.get('vehicle_reg', 'N/A')}:",
                'get_vehicles_in_zone': f"Here are the vehicles in zone '{extracted_data.get('zone_name', 'N/A')}':",
                'get_vehicles_in_region': f"Here are the vehicles in region '{extracted_data.get('region_name', 'N/A')}':",
                'get_vehicles_in_plant': f"Here are the vehicles in plant '{extracted_data.get('plant_name', 'N/A')}':",
                'get_vehicles_of_plant': f"Here are the vehicles assigned to '{extracted_data.get('plant_name', 'N/A')}' plant:",
                'get_vehicle_hierarchy': f"Here's the complete hierarchy for vehicle {extracted_data.get('vehicle_reg', 'N/A')}:",
                'get_vehicle_hierarchy_contextual': f"Here's the plant and region information for the vehicle:",
            }
            return hierarchical_responses.get(intent, "Here's the hierarchical information you requested:")
        
        # Existing plant responses
        if reasoning_result['intent'].startswith('get_plant_name'):
            plant_id = extracted_data.get('plant_id')
            
            response_parts = []
            
            if source == 'conversation_context':
                response_parts.append(f"I remember from our conversation that complaint ID mentioned had plant ID {plant_id}.")
            elif source == 'response_text_analysis':
                response_parts.append(f"Based on our previous discussion, I found that plant ID {plant_id} was mentioned.")
            else:
                response_parts.append(f"Looking up plant information for plant ID {plant_id}.")
            
            # Add the actual plant details from query result
            if query_result.get('sql') and 'rows' in query_result:
                response_parts.append("Here are the plant details:")
            
            return " ".join(response_parts)
        
        # Distance Report response templates
        if intent == 'show_distance_report':
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Here's the distance report showing {count} travel records with distance in KM and drum rotation time in HH:MM format."
            return "Retrieving vehicle distance report with travel distances and drum rotation data..."
        
        if intent == 'vehicle_distance_report':
            vehicle_reg = extracted_data.get('vehicle_reg')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} distance records for vehicle {vehicle_reg}. Distances are shown in KM and drum rotation in HH:MM format."
            return f"Searching for distance report data for vehicle {vehicle_reg}..."
        
        if intent == 'vehicle_drum_rotation':
            vehicle_reg = extracted_data.get('vehicle_reg')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} drum rotation records for vehicle {vehicle_reg}. Times are converted to HH:MM format."
            return f"Retrieving drum rotation data for vehicle {vehicle_reg}..."
        
        if intent == 'total_distance_traveled':
            aggregation = extracted_data.get('aggregation', 'total')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Here's the {aggregation} distance analysis for {count} vehicles, showing distances in KM."
            return f"Calculating {aggregation} distance traveled by vehicles..."
        
        if intent == 'inter_plant_distance':
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} plants with inter-plant travel data. Distances show vehicle movement between different plant facilities."
            return "Analyzing inter-plant vehicle travel distances..."
        
        if intent == 'inter_plant_vehicle_travel':
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Found {count} vehicles that travel between different plants. These vehicles handle inter-facility transportation."
            return "Identifying vehicles that travel between different plant facilities..."
        
        if intent == 'time_based_distance_report':
            time_period = extracted_data.get('time_period', 'daily')
            if query_result.get('sql') and 'rows' in query_result and query_result['rows']:
                count = len(query_result['rows'])
                return f"Here's the {time_period} distance analysis for {count} time periods, showing travel patterns and vehicle utilization."
            return f"Generating {time_period} distance report with travel patterns..."
        
        return "I found the information you were looking for based on our conversation context."

    # HIERARCHICAL EXTRACTOR METHODS
    def _extract_show_all_regions(self, query: str, match, chat_context):
        """Extract intent for showing all regions"""
        return {'list_type': 'regions'}

    def _extract_show_all_zones(self, query: str, match, chat_context):
        """Extract intent for showing all zones"""
        return {'list_type': 'zones'}

    def _extract_show_all_plants(self, query: str, match, chat_context):
        """Extract intent for showing all plants"""
        return {'list_type': 'plants'}

    def _extract_zone_from_vehicle(self, query: str, match, chat_context):
        """Extract vehicle registration for zone lookup"""
        vehicle_reg = match.group(1) if match.groups() else None
        return {'vehicle_reg': vehicle_reg} if vehicle_reg else None

    def _extract_region_from_vehicle(self, query: str, match, chat_context):
        """Extract vehicle registration for region lookup"""
        vehicle_reg = match.group(1) if match.groups() else None
        return {'vehicle_reg': vehicle_reg} if vehicle_reg else None

    def _extract_plant_from_vehicle(self, query: str, match, chat_context):
        """Extract vehicle registration for plant lookup"""
        vehicle_reg = match.group(1) if match.groups() else None
        return {'vehicle_reg': vehicle_reg} if vehicle_reg else None

    def _extract_vehicles_in_zone(self, query: str, match, chat_context):
        """Extract zone name for vehicle lookup"""
        zone_name = match.group(1).strip() if match.groups() else None
        return {'zone_name': zone_name} if zone_name else None

    def _extract_vehicles_in_region(self, query: str, match, chat_context):
        """Extract region name for vehicle lookup"""
        region_name = match.group(1).strip() if match.groups() else None
        return {'region_name': region_name} if region_name else None

    def _extract_vehicles_in_plant(self, query: str, match, chat_context):
        """Extract plant name for vehicle lookup"""
        plant_name = match.group(1).strip() if match.groups() else None
        return {'plant_name': plant_name} if plant_name else None

    def _extract_vehicle_hierarchy(self, query: str, match, chat_context):
        """Extract vehicle registration for complete hierarchy lookup"""
        vehicle_reg = match.group(1) if match.groups() else None
        return {'vehicle_reg': vehicle_reg} if vehicle_reg else None

    def _extract_vehicle_from_context(self, query: str, match, chat_context):
        """Extract vehicle registration from conversation context for 'this vehicle' queries"""
        print(f"🔍 [DEBUG] Extracting vehicle from context for query: '{query}'")
        
        if chat_context and hasattr(chat_context, 'last_displayed_items'):
            # Look for vehicle registration in recent context
            print(f"🔍 [DEBUG] Checking {len(chat_context.last_displayed_items)} context items...")
            for item in chat_context.last_displayed_items:
                if 'reg_no' in item:
                    vehicle_reg = item['reg_no']
                    print(f"✅ [DEBUG] Found vehicle reg from context: {vehicle_reg}")
                    return {'vehicle_reg': vehicle_reg}
        
        # If no context found, look for vehicle registration in the query itself
        # Try to find vehicle registration pattern in the query
        vehicle_match = re.search(r'\b([A-Z]{2}\d{2}[A-Z]{2}\d{4})\b', query)
        if vehicle_match:
            vehicle_reg = vehicle_match.group(1)
            print(f"✅ [DEBUG] Found vehicle reg in query: {vehicle_reg}")
            return {'vehicle_reg': vehicle_reg}
        
        print(f"❌ [DEBUG] No vehicle registration found in context or query")
        # If no context found, return None to fall back to normal processing
        return None

    def _extract_vehicles_of_plant_flexible(self, query: str, match, chat_context):
        """Extract plant name for vehicle lookup with flexible matching"""
        plant_name = match.group(1).strip() if match.groups() else None
        if plant_name:
            # Clean up the plant name - remove common words like "the"
            plant_name = re.sub(r'\b(?:the|plant)\b', '', plant_name, flags=re.IGNORECASE).strip()
            return {'plant_name': plant_name} if plant_name else None
        return None

    def generate_hierarchical_query(self, reasoning_result):
        """Generate SQL queries for hierarchical relationships"""
        intent = reasoning_result['intent']
        extracted_data = reasoning_result['extracted_data']
        
        hierarchical_queries = {
            'show_all_regions': lambda data: """
                SELECT DISTINCT dm.name as region_name, dm.id_no as region_id
                FROM district_master dm 
                WHERE dm.name IS NOT NULL AND dm.name != ''
                ORDER BY dm.name
            """,
            
            'show_all_zones': lambda data: """
                SELECT DISTINCT zm.zone_name, zm.id_no as zone_id
                FROM zone_master zm 
                WHERE zm.zone_name IS NOT NULL AND zm.zone_name != ''
                ORDER BY zm.zone_name
            """,
            
            'show_all_plants': lambda data: """
                SELECT DISTINCT hm.name as plant_name, hm.id_no as plant_id
                FROM hosp_master hm 
                WHERE hm.name IS NOT NULL AND hm.name != ''
                ORDER BY hm.name
            """,
            
            'get_zone_from_vehicle': lambda data: f"""
                SELECT 
                    CASE WHEN zm.zone_name = 'EONINFOTECH' THEN 'Inactive Region' ELSE zm.zone_name END as zone_name,
                    CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as district_name,
                    CASE WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Removed Facility' ELSE hm.name END as plant_name, 
                    vm.reg_no,
                    CASE 
                        WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Device Removed'
                        WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' 
                        ELSE 'Active' 
                    END as status
                FROM zone_master zm 
                JOIN district_master dm ON zm.id_no = dm.id_zone 
                JOIN hosp_master hm ON dm.id_no = hm.id_dist 
                JOIN vehicle_master vm ON hm.id_no = vm.id_hosp 
                WHERE vm.reg_no = '{data.get('vehicle_reg', '')}'
            """,
            
            'get_region_from_vehicle': lambda data: f"""
                SELECT 
                    CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as region_name,
                    CASE WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Removed Facility' ELSE hm.name END as plant_name, 
                    vm.reg_no,
                    CASE 
                        WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Device Removed'
                        WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' 
                        ELSE 'Active' 
                    END as status
                FROM district_master dm 
                JOIN hosp_master hm ON dm.id_no = hm.id_dist 
                JOIN vehicle_master vm ON hm.id_no = vm.id_hosp 
                WHERE vm.reg_no = '{data.get('vehicle_reg', '')}'
            """,
            
            'get_plant_from_vehicle': lambda data: f"""
                SELECT hm.name as plant_name, hm.address, vm.reg_no
                FROM hosp_master hm 
                JOIN vehicle_master vm ON hm.id_no = vm.id_hosp 
                WHERE vm.reg_no = '{data.get('vehicle_reg', '')}'
            """,
            
            'get_vehicles_in_zone': lambda data: f"""
                SELECT 
                    vm.reg_no, 
                    CASE WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Removed Facility' ELSE hm.name END as plant_name, 
                    CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as district_name,
                    CASE 
                        WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Device Removed'
                        WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' 
                        ELSE 'Active' 
                    END as status
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                JOIN district_master dm ON hm.id_dist = dm.id_no 
                JOIN zone_master zm ON dm.id_zone = zm.id_no 
                WHERE zm.zone_name ILIKE '%{data.get('zone_name', '')}%'
                   OR ('{data.get('zone_name', '').lower()}' IN ('eoninfotech', 'eon infotech') AND dm.name = 'EONINFOTECH')
                ORDER BY vm.reg_no
            """,
            
            'get_vehicles_in_region': lambda data: f"""
                SELECT 
                    vm.reg_no, 
                    CASE WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Removed Facility' ELSE hm.name END as plant_name,
                    CASE 
                        WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Device Removed'
                        WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' 
                        ELSE 'Active' 
                    END as status
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                JOIN district_master dm ON hm.id_dist = dm.id_no 
                WHERE dm.name ILIKE '%{data.get('region_name', '')}%'
                   OR ('{data.get('region_name', '').lower()}' IN ('eoninfotech', 'eon infotech') AND dm.name = 'EONINFOTECH')
                ORDER BY vm.reg_no
            """,
            
            'get_vehicles_in_plant': lambda data: f"""
                SELECT 
                    vm.reg_no, 
                    vm.regional_name,
                    CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' ELSE 'Active' END as status
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
                WHERE hm.name ILIKE '%{data.get('plant_name', '')}%'
                ORDER BY vm.reg_no
            """,
            
            'get_vehicles_of_plant': lambda data: f"""
                SELECT 
                    vm.reg_no, 
                    vm.bus_id, 
                    hm.name as plant_name,
                    CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' ELSE 'Active' END as status
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
                WHERE hm.name ILIKE '%{data.get('plant_name', '')}%'
                ORDER BY vm.reg_no
                LIMIT 50
            """,
            
            'get_vehicle_hierarchy': lambda data: f"""
                SELECT 
                    vm.reg_no, 
                    CASE WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Removed Facility' ELSE hm.name END as plant_name, 
                    CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as district_name,
                    CASE WHEN zm.zone_name = 'EONINFOTECH' THEN 'Inactive Region' ELSE zm.zone_name END as zone_name,
                    CASE 
                        WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Device Removed'
                        WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' 
                        ELSE 'Active' 
                    END as status
                FROM vehicle_master vm 
                LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no 
                LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no 
                WHERE vm.reg_no = '{data.get('vehicle_reg', '')}'
            """,
            
            'get_vehicle_hierarchy_contextual': lambda data: f"""
                SELECT 
                    vm.reg_no, 
                    CASE WHEN hm.name ILIKE '%EON OFFICE%' THEN 'Removed Facility' ELSE hm.name END as plant_name, 
                    CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as region_name
                FROM vehicle_master vm 
                LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no 
                WHERE vm.reg_no = '{data.get('vehicle_reg', '')}'
            """
        }
        
        query_generator = hierarchical_queries.get(intent)
        if query_generator:
            return query_generator(extracted_data).strip()
        
        return None

    def generate_hierarchical_sql(self, entity_type, target_entity, filters=None):
        """
        Generate SQL with complete hierarchical joins using the core ID relationships.
        
        Args:
            entity_type: The type of entity being queried ('vehicle', 'plant', 'region', 'zone')
            target_entity: What we want to show/filter on
            filters: Any additional filters
        
        Returns:
            Complete SQL with proper joins using id_dist, id_hosp relationships
        """
        
        # Define the complete join chain from bottom to top
        complete_join_chain = """
        FROM vehicle_master vm
        LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no
        LEFT JOIN district_master dm ON hm.id_dist = dm.id_no  
        LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no
        """
        
        sql_templates = {
            'vehicles_by_plant': {
                'select': 'vm.reg_no, vm.bus_id, hm.name as plant_name, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive\' ELSE \'Active\' END as status',
                'joins': complete_join_chain,
                'where_template': "hm.name ILIKE '%{plant_name}%'"
            },
            'vehicles_by_region': {
                'select': 'vm.reg_no, vm.bus_id, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE dm.name END as region_name, hm.name as plant_name, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive\' ELSE \'Active\' END as status',
                'joins': complete_join_chain,
                'where_template': "dm.name ILIKE '%{region_name}%' OR ('{region_name}' IN ('eoninfotech', 'eon infotech') AND dm.name = 'EONINFOTECH')"
            },
            'vehicles_by_zone': {
                'select': 'vm.reg_no, vm.bus_id, CASE WHEN zm.zone_name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE zm.zone_name END as zone_name, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE dm.name END as region_name, hm.name as plant_name, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive\' ELSE \'Active\' END as status',
                'joins': complete_join_chain,
                'where_template': "zm.zone_name ILIKE '%{zone_name}%' OR ('{zone_name}' IN ('eoninfotech', 'eon infotech') AND dm.name = 'EONINFOTECH')"
            },
            'plants_by_region': {
                'select': 'hm.name as plant_name, hm.id_no as plant_id, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE dm.name END as region_name',
                'joins': """
                FROM hosp_master hm
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
                """,
                'where_template': "dm.name ILIKE '%{region_name}%' OR ('{region_name}' IN ('eoninfotech', 'eon infotech') AND dm.name = 'EONINFOTECH')"
            },
            'plants_by_location_smart': {
                'select': 'hm.name as plant_name, hm.id_no as plant_id, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE dm.name END as region_name',
                'joins': """
                FROM hosp_master hm
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
                """,
                'where_template': "dm.name ILIKE '%{location_name}%' OR ('{location_name}' IN ('eoninfotech', 'eon infotech') AND dm.name = 'EONINFOTECH')",
                'note': 'Use this for most location queries (Gujarat, Maharashtra, etc.) - they are typically districts'
            },
            'plants_by_zone': {
                'select': 'hm.name as plant_name, hm.id_no as plant_id, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE dm.name END as region_name, CASE WHEN zm.zone_name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE zm.zone_name END as zone_name',
                'joins': """
                FROM hosp_master hm
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
                LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no
                """,
                'where_template': "zm.zone_name ILIKE '%{zone_name}%' OR ('{zone_name}' IN ('eoninfotech', 'eon infotech') AND dm.name = 'EONINFOTECH')",
                'note': 'Use this ONLY when specifically asking for zone data or when location is confirmed to be a zone'
            },
            'full_hierarchy_for_vehicle': {
                'select': 'vm.reg_no, vm.bus_id, hm.name as plant_name, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE dm.name END as region_name, CASE WHEN zm.zone_name = \'EONINFOTECH\' THEN \'Inactive Region\' ELSE zm.zone_name END as zone_name, CASE WHEN dm.name = \'EONINFOTECH\' THEN \'Inactive\' ELSE \'Active\' END as status',
                'joins': complete_join_chain,
                'where_template': "vm.reg_no = '{vehicle_reg}'"
            }
        }
        
        return sql_templates.get(f"{entity_type}_{target_entity}", None)
    
    def validate_hierarchical_query(self, query_text):
        """
        Validate that hierarchical queries use the correct ID relationships.
        Returns suggestions for fixing common mistakes.
        """
        issues = []
        suggestions = []
        
        # Check for common relationship mistakes
        if 'vehicle' in query_text.lower() and 'plant' in query_text.lower():
            if 'id_hosp' not in query_text:
                issues.append("Missing id_hosp relationship between vehicle_master and hosp_master")
                suggestions.append("Use: JOIN hosp_master hm ON vm.id_hosp = hm.id_no")
        
        if 'plant' in query_text.lower() and 'region' in query_text.lower():
            if 'id_dist' not in query_text:
                issues.append("Missing id_dist relationship between hosp_master and district_master")
                suggestions.append("Use: JOIN district_master dm ON hm.id_dist = dm.id_no")
        
        if 'region' in query_text.lower() and 'zone' in query_text.lower():
            if 'id_zone' not in query_text:
                issues.append("Missing id_zone relationship between district_master and zone_master")
                suggestions.append("Use: JOIN zone_master zm ON dm.id_zone = zm.id_no")
        
        return issues, suggestions
    
    def get_mandatory_joins_for_query(self, query_lower):
        """
        Return the mandatory JOIN statements needed for a hierarchical query.
        This ensures no relationships are missed.
        """
        mandatory_joins = []
        
        # Analyze what entities are mentioned to determine required joins
        entities_mentioned = {
            'vehicle': any(word in query_lower for word in ['vehicle', 'truck', 'bus', 'fleet', 'reg_no']),
            'plant': any(word in query_lower for word in ['plant', 'facility', 'hosp']),
            'region': any(word in query_lower for word in ['region', 'district']),
            'zone': any(word in query_lower for word in ['zone'])
        }
        
        # Build the join chain based on what's needed
        if entities_mentioned['vehicle']:
            # Vehicle is mentioned, start from vehicle_master
            base_table = 'vehicle_master vm'
            
            if entities_mentioned['plant']:
                mandatory_joins.append('LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no')
                
                if entities_mentioned['region']:
                    mandatory_joins.append('LEFT JOIN district_master dm ON hm.id_dist = dm.id_no')
                    
                    if entities_mentioned['zone']:
                        mandatory_joins.append('LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no')
                        
        elif entities_mentioned['plant']:
            # Plant is mentioned, start from hosp_master
            base_table = 'hosp_master hm'
            
            if entities_mentioned['region']:
                mandatory_joins.append('LEFT JOIN district_master dm ON hm.id_dist = dm.id_no')
                
                if entities_mentioned['zone']:
                    mandatory_joins.append('LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no')
                    
        elif entities_mentioned['region']:
            # Region is mentioned, start from district_master
            base_table = 'district_master dm'
            
            if entities_mentioned['zone']:
                mandatory_joins.append('LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no')
                
        else:
            # Default to zone_master if only zone is mentioned
            base_table = 'zone_master zm'
        
        return base_table, mandatory_joins

    def analyze_hierarchical_completeness(self, query_text, sql_result=None):
        """
        Analyze if a query properly handles the hierarchical relationships.
        Returns suggestions to ensure no data is missed due to incomplete joins.
        """
        query_lower = query_text.lower()
        issues = []
        recommendations = []
        
        # Check for vehicle-plant relationship completeness
        if ('vehicle' in query_lower and 'plant' in query_lower) or \
           ('vehicle' in query_lower and any(x in query_lower for x in ['mohali', 'chandigarh', 'ludhiana', 'amritsar'])):
            
            if sql_result and 'JOIN hosp_master' not in sql_result:
                issues.append("Vehicle-Plant query missing proper JOIN")
                recommendations.append("""
                CRITICAL: For vehicle-plant queries, ALWAYS use:
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no
                WHERE hm.name ILIKE '%plant_name%'
                """)
                
        # Check for region-based completeness  
        if ('vehicle' in query_lower and any(x in query_lower for x in ['region', 'district', 'punjab', 'haryana'])):
            
            if sql_result and 'district_master' not in sql_result:
                issues.append("Vehicle-Region query missing district hierarchy")
                recommendations.append("""
                CRITICAL: For vehicle-region queries, ALWAYS use complete hierarchy:
                FROM vehicle_master vm
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no  
                JOIN district_master dm ON hm.id_dist = dm.id_no
                WHERE dm.name ILIKE '%region_name%'
                """)
                
        # Check for zone-based completeness
        if ('vehicle' in query_lower and 'zone' in query_lower):
            
            if sql_result and 'zone_master' not in sql_result:
                issues.append("Vehicle-Zone query missing complete hierarchy")
                recommendations.append("""
                CRITICAL: For vehicle-zone queries, ALWAYS use full hierarchy:
                FROM vehicle_master vm
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no
                JOIN district_master dm ON hm.id_dist = dm.id_no  
                JOIN zone_master zm ON dm.id_zone = zm.id_no
                WHERE zm.zone_name ILIKE '%zone_name%'
                """)
        
        return {
            'has_issues': len(issues) > 0,
            'issues': issues,
            'recommendations': recommendations,
            'completeness_score': max(0, 100 - (len(issues) * 25))  # Deduct 25% per major issue
        }
    
    def get_hierarchical_sql_template(self, entity_from, entity_to, filter_value=None):
        """
        Get the correct SQL template for hierarchical queries.
        Ensures all ID relationships are properly maintained.
        """
        
        templates = {
            ('vehicle', 'plant'): {
                'sql': """
                SELECT vm.reg_no, vm.bus_id, hm.name as plant_name, hm.id_no as plant_id
                FROM vehicle_master vm
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no
                {where_clause}
                ORDER BY hm.name, vm.reg_no
                """,
                'where_template': "WHERE hm.name ILIKE '%{filter_value}%'" if filter_value else ""
            },
            
            ('vehicle', 'region'): {
                'sql': """
                SELECT vm.reg_no, vm.bus_id, hm.name as plant_name, dm.name as region_name
                FROM vehicle_master vm
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no
                JOIN district_master dm ON hm.id_dist = dm.id_no
                {where_clause}
                ORDER BY dm.name, hm.name, vm.reg_no
                """,
                'where_template': "WHERE dm.name ILIKE '%{filter_value}%'" if filter_value else ""
            },
            
            ('vehicle', 'zone'): {
                'sql': """
                SELECT vm.reg_no, vm.bus_id, hm.name as plant_name, dm.name as region_name, zm.zone_name
                FROM vehicle_master vm
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no
                JOIN district_master dm ON hm.id_dist = dm.id_no
                JOIN zone_master zm ON dm.id_zone = zm.id_no
                {where_clause}
                ORDER BY zm.zone_name, dm.name, hm.name, vm.reg_no
                """,
                'where_template': "WHERE zm.zone_name ILIKE '%{filter_value}%'" if filter_value else ""
            },
            
            ('plant', 'region'): {
                'sql': """
                SELECT hm.name as plant_name, hm.id_no as plant_id, dm.name as region_name
                FROM hosp_master hm
                JOIN district_master dm ON hm.id_dist = dm.id_no
                {where_clause}
                ORDER BY dm.name, hm.name
                """,
                'where_template': "WHERE dm.name ILIKE '%{filter_value}%'" if filter_value else ""
            },
            
            ('plant', 'zone'): {
                'sql': """
                SELECT hm.name as plant_name, hm.id_no as plant_id, dm.name as region_name, zm.zone_name
                FROM hosp_master hm
                JOIN district_master dm ON hm.id_dist = dm.id_no
                JOIN zone_master zm ON dm.id_zone = zm.id_no
                {where_clause}
                ORDER BY zm.zone_name, dm.name, hm.name
                """,
                'where_template': "WHERE zm.zone_name ILIKE '%{filter_value}%'" if filter_value else ""
            }
        }
        
        template = templates.get((entity_from, entity_to))
        if template and filter_value:
            where_clause = template['where_template'].format(filter_value=filter_value)
            return template['sql'].format(where_clause=where_clause)
        elif template:
            return template['sql'].format(where_clause="")
        
        return None
    
    def apply_business_rules(self, query, context):
        """Apply domain-specific business rules to queries"""
        business_context = {'rules_applied': [], 'query_modifications': [], 'data_masking': None}
        
        if not self.db_parser:
            return business_context
            
        try:
            # Check if this is a specific vehicle query first
            vehicle_check = self.check_for_removed_vehicle_query(query)
            
            # Get business context for the query
            query_context = self.db_parser.get_business_context_for_query(query)
            
            # Apply EONINFOTECH/EON OFFICE rules if applicable
            if query_context['eoninfotech_rule']['applies']:
                rule = query_context['eoninfotech_rule']
                
                if rule['rule'] == 'eon_office_removed_vehicles':
                    # Special handling for EON OFFICE vehicles
                    business_context['rules_applied'].append({
                        'rule_name': 'eon_office_removed_vehicles',
                        'description': rule['description'],
                        'impact': 'Vehicle device has been removed - show removal message instead of details'
                    })
                    
                    business_context['query_modifications'].append({
                        'type': 'device_removal',
                        'modification': 'Replace vehicle details with removal message',
                        'suggested_response': 'Show device removal message'
                    })
                    
                elif rule['rule'] == 'eoninfotech_inactive_vehicles':
                    # Regular EONINFOTECH handling
                    business_context['rules_applied'].append({
                        'rule_name': 'eoninfotech_inactive_vehicles',
                        'description': rule['description'],
                        'impact': 'All vehicles in this region are considered inactive'
                    })
                    
                    business_context['query_modifications'].append({
                        'type': 'status_filter',
                        'modification': 'Add inactive vehicle filter for EONINFOTECH region',
                        'suggested_where_clause': "AND (dm.name != 'EONINFOTECH' OR 'Active' = 'inactive')"
                    })
                
                # Add data masking instructions
                if 'data_masking' in rule:
                    business_context['data_masking'] = rule['data_masking']
                    
                # Store vehicle query info for later use
                if vehicle_check['is_vehicle_query']:
                    business_context['vehicle_query'] = vehicle_check
                
            return business_context
            
        except Exception as e:
            print(f"⚠️ Error applying business rules: {e}")
            return business_context
    
    def apply_data_masking(self, query_result, business_context):
        """Apply data masking based on business rules"""
        if not business_context.get('data_masking'):
            return query_result
            
        # Use centralized masker if available
        if self.data_masker:
            # Special handling for vehicle queries that should show removal message
            if (business_context.get('data_masking', {}).get('removal_message') and 
                business_context.get('vehicle_query', {}).get('is_vehicle_query')):
                
                return self.data_masker.process_vehicle_query_result(query_result, hide_removed=True)
            else:
                return self.data_masker.mask_query_result(query_result)
        
        # Fallback masking logic
        if business_context['data_masking'].get('mask_eoninfotech_region'):
            if isinstance(query_result, dict) and 'rows' in query_result:
                # Check for removal messages first
                if business_context['data_masking'].get('removal_message'):
                    # For EON OFFICE vehicles, replace with removal message
                    removal_messages = []
                    filtered_rows = []
                    
                    for row in query_result['rows']:
                        # Check if this is an EON OFFICE vehicle
                        is_eon_office = any(
                            ('plant' in str(key).lower() and 'eon office' in str(value).lower())
                            for key, value in row.items()
                        )
                        
                        if is_eon_office:
                            vehicle_reg = row.get('reg_no', row.get('vehicle_reg', 'Unknown'))
                            removal_messages.append(f"Vehicle {vehicle_reg}'s device has been removed.")
                        else:
                            if self.db_parser:
                                filtered_rows.append(self.db_parser.mask_eoninfotech_data(row))
                            else:
                                filtered_rows.append(row)
                    
                    query_result['rows'] = filtered_rows
                    if removal_messages:
                        query_result['removal_messages'] = removal_messages
                        
                else:
                    # Regular EONINFOTECH masking
                    if self.db_parser:
                        query_result['rows'] = self.db_parser.mask_eoninfotech_in_list(query_result['rows'])
                    
                # Update column headers if needed
                if 'columns' in query_result:
                    masked_columns = []
                    for col in query_result['columns']:
                        if isinstance(col, dict) and col.get('name'):
                            if 'eoninfotech' in col['name'].lower():
                                col['name'] = col['name'].replace('EONINFOTECH', 'Inactive Region').replace('eoninfotech', 'inactive_region')
                        masked_columns.append(col)
                    query_result['columns'] = masked_columns
                    
        return query_result
    
    def generate_masked_sql_for_eoninfotech(self, original_sql):
        """Generate SQL that masks EONINFOTECH data at query level"""
        if self.data_masker:
            return self.data_masker.mask_sql_query(original_sql)
        
        # Fallback SQL masking
        if not original_sql:
            return original_sql
            
        masked_sql = original_sql
        
        # Add CASE statements to mask EONINFOTECH in SELECT clauses
        region_patterns = [
            (r'(dm\.name\s+as\s+region_name)', "CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as region_name"),
            (r'(dm\.name\s+as\s+district_name)', "CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END as district_name"),
            (r'(zm\.zone_name)', "CASE WHEN zm.zone_name = 'EONINFOTECH' THEN 'Inactive Region' ELSE zm.zone_name END as zone_name"),
            (r'(dm\.name)(?!\s+as)', "CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive Region' ELSE dm.name END"),
        ]
        
        for pattern, replacement in region_patterns:
            masked_sql = re.sub(pattern, replacement, masked_sql, flags=re.IGNORECASE)
            
        # Add status indication for EONINFOTECH vehicles
        if 'vehicle_master vm' in masked_sql and 'SELECT' in masked_sql.upper():
            # Add status column if not present
            if 'Active' not in masked_sql and 'status' not in masked_sql.lower():
                # Insert status column after vehicle info
                select_match = re.search(r'SELECT\s+(.*?)\s+FROM', masked_sql, re.IGNORECASE | re.DOTALL)
                if select_match:
                    select_part = select_match.group(1)
                    if 'vm.reg_no' in select_part:
                        new_select = select_part + ", CASE WHEN dm.name = 'EONINFOTECH' THEN 'Inactive' ELSE 'Active' END as status"
                        masked_sql = masked_sql.replace(select_part, new_select)
                        
        return masked_sql

    def check_for_removed_vehicle_query(self, query_text):
        """Check if this is a query for a specific vehicle that might be removed"""
        query_lower = query_text.lower()
        
        # Patterns that indicate specific vehicle queries
        vehicle_query_patterns = [
            r'(?:vehicle|truck)\s+([A-Z0-9\-]+)',  # "vehicle ABC-123"
            r'(?:reg\s+no|registration)\s+([A-Z0-9\-]+)',  # "reg no ABC-123"
            r'(?:details|info|information).*(?:vehicle|truck)\s+([A-Z0-9\-]+)',  # "details of vehicle ABC-123"
            r'([A-Z0-9\-]+).*(?:vehicle|truck)',  # "ABC-123 vehicle"
        ]
        
        for pattern in vehicle_query_patterns:
            match = re.search(pattern, query_text, re.IGNORECASE)
            if match:
                vehicle_reg = match.group(1)
                return {
                    'is_vehicle_query': True,
                    'vehicle_reg': vehicle_reg,
                    'query_type': 'specific_vehicle_details'
                }
        
        return {'is_vehicle_query': False}
    
    def should_show_removal_message(self, vehicle_data):
        """Check if we should show removal message instead of vehicle details"""
        if self.data_masker:
            return self.data_masker.should_hide_vehicle_details(vehicle_data)
        return False
    
    def create_vehicle_removal_response(self, vehicle_reg, query_result=None):
        """Create a response for removed vehicles"""
        base_message = f"Vehicle {vehicle_reg}'s device has been removed."
        
        if query_result and query_result.get('removal_messages'):
            return query_result['removal_messages'][0]
        
        return base_message

    # Distance Report Extractor Methods
    def _extract_distance_report_criteria(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract criteria for general distance reports"""
        return {
            'report_type': 'distance_report',
            'table': 'distance_report',
            'vehicle_reg': None,
            'time_filter': None,
            'additional_joins': ['vehicle_master', 'hosp_master', 'district_master']
        }

    def _extract_vehicle_distance_criteria(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract vehicle-specific distance report criteria"""
        vehicle_reg = None
        if match and len(match.groups()) > 0:
            vehicle_reg = match.group(1).upper()
        else:
            # Try to extract vehicle registration from query
            vehicle_match = re.search(r'vehicle\s+(\w+)', query, re.IGNORECASE)
            if vehicle_match:
                vehicle_reg = vehicle_match.group(1).upper()
        
        return {
            'report_type': 'vehicle_distance_report',
            'table': 'distance_report',
            'vehicle_reg': vehicle_reg,
            'time_filter': None,
            'additional_joins': ['vehicle_master', 'hosp_master', 'district_master']
        }

    def _extract_distance_aggregation_criteria(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract criteria for distance aggregation queries"""
        aggregation_type = 'total'
        if re.search(r'average|avg', query, re.IGNORECASE):
            aggregation_type = 'average'
        elif re.search(r'maximum|max', query, re.IGNORECASE):
            aggregation_type = 'maximum'
        
        return {
            'report_type': 'distance_aggregation',
            'table': 'distance_report',
            'aggregation': aggregation_type,
        }

    def detect_dpr_query_type(self, user_input):
        """Detect Daily Production Report query patterns"""
        user_input_lower = user_input.lower()
        
        # Check for DPR-specific patterns
        for query_type, patterns in self.dpr_query_patterns.items():
            if any(pattern in user_input_lower for pattern in patterns):
                return query_type
        
        return None

    def generate_dpr_sql(self, user_input, entities):
        """Generate SQL for Daily Production Report queries"""
        query_type = self.detect_dpr_query_type(user_input)
        user_input_lower = user_input.lower()
        
        base_query = """
        SELECT 
            dpr.id_no,
            hm.name as plant_name,
            dpr.pi_name as plant_incharge,
            dpr.cust_name as customer_name,
            dpr.site_name,
            CASE 
                WHEN dpr.fse_name LIKE '%,%' 
                THEN TRIM(SUBSTRING(dpr.fse_name FROM POSITION(',' IN dpr.fse_name) + 1)) || ' ' || TRIM(SUBSTRING(dpr.fse_name FROM 1 FOR POSITION(',' IN dpr.fse_name) - 1))
                ELSE dpr.fse_name 
            END as sales_person,
            dpr.site_distance,
            dpr.tm_no as transit_mixer,
            dpr.vol_cum as volume_m3,
            dpr.grade as concrete_grade,
            dpr.smode as service_mode,
            dpr.bth_name as batch_name,
            dpr.tkt_no as ticket_number,
            dpr.pump_name,
            dpr.challan_no,
            dpr.so_number as sales_order,
            dpr.cost_m3 as cost_per_m3,
            dpr.plant_code,
            dpr.batch_code
        FROM dpr_master1 dpr
        LEFT JOIN hosp_master hm ON dpr.plant_id = hm.id_no
        """
        
        # Add specific conditions based on query type
        conditions = []
        
        if query_type == 'customer_orders':
            if any(term in user_input_lower for term in ['specific customer', 'customer name']):
                # Extract customer name if mentioned
                for entity in entities:
                    if entity.get('entity_type') == 'customer':
                        conditions.append(f"dpr.cust_name ILIKE '%{entity['value']}%'")
            
        elif query_type == 'transit_mixer':
            if 'utilization' in user_input_lower:
                base_query = """
                SELECT 
                    dpr.tm_no as transit_mixer,
                    COUNT(*) as delivery_count,
                    AVG(dpr.vol_cum) as avg_volume,
                    SUM(dpr.vol_cum) as total_volume,
                    AVG(dpr.site_distance) as avg_distance
                FROM dpr_master1 dpr
                """
                base_query += " GROUP BY dpr.tm_no ORDER BY delivery_count DESC"
                return base_query
            
        elif query_type == 'sales_person':
            base_query = """
            SELECT 
                CASE 
                    WHEN dpr.fse_name LIKE '%,%' 
                    THEN TRIM(SUBSTRING(dpr.fse_name FROM POSITION(',' IN dpr.fse_name) + 1)) || ' ' || TRIM(SUBSTRING(dpr.fse_name FROM 1 FOR POSITION(',' IN dpr.fse_name) - 1))
                    ELSE dpr.fse_name 
                END as sales_person,
                COUNT(*) as order_count,
                SUM(dpr.vol_cum) as total_volume,
                AVG(dpr.cost_m3) as avg_cost_per_m3,
                hm.name as plant_name
            FROM dpr_master1 dpr
            LEFT JOIN hosp_master hm ON dpr.plant_id = hm.id_no
            """
            base_query += " GROUP BY dpr.fse_name, hm.name ORDER BY order_count DESC"
            return base_query
            
        elif query_type == 'pump_analysis':
            if 'vs' in user_input_lower or 'comparison' in user_input_lower:
                base_query = """
                SELECT 
                    dpr.smode as service_mode,
                    COUNT(*) as delivery_count,
                    AVG(dpr.vol_cum) as avg_volume,
                    AVG(dpr.site_distance) as avg_distance,
                    AVG(dpr.cost_m3) as avg_cost_per_m3
                FROM dpr_master1 dpr
                """
                base_query += " GROUP BY dpr.smode ORDER BY delivery_count DESC"
                return base_query
        
        elif query_type == 'concrete_grade':
            if 'analysis' in user_input_lower or 'summary' in user_input_lower:
                base_query = """
                SELECT 
                    dpr.grade as concrete_grade,
                    COUNT(*) as order_count,
                    SUM(dpr.vol_cum) as total_volume,
                    AVG(dpr.cost_m3) as avg_cost_per_m3,
                    AVG(dpr.site_distance) as avg_delivery_distance
                FROM dpr_master1 dpr
                """
                base_query += " GROUP BY dpr.grade ORDER BY order_count DESC"
                return base_query
        
        # Add date filters if date entities are found
        for entity in entities:
            if entity.get('entity_type') == 'date':
                # Assuming there's a date column (you may need to adjust this)
                conditions.append(f"DATE(dpr.created_date) = '{entity['value']}'")
        
        # Add plant filter if plant entity is found
        for entity in entities:
            if entity.get('entity_type') == 'plant':
                conditions.append(f"hm.name ILIKE '%{entity['value']}%'")
        
        # Add vehicle filter if vehicle entity is found
        for entity in entities:
            if entity.get('entity_type') == 'vehicle':
                # FIXED: Use helper function to distinguish DPR IDs from vehicle registrations
                # dpr.tm_no should contain vehicle registration numbers (links to vehicle_master.reg_no)
                # Never confuse with dpr.id_no (which is internal DPR ID)
                vehicle_value = entity['value']
                
                # Use the new helper function to properly classify the identifier
                classification = self.distinguish_dpr_id_from_vehicle_reg(vehicle_value)
                
                if classification['type'] == 'dpr_id':
                    # This is a DPR ID - use direct lookup
                    conditions.append(f"dpr.id_no = {vehicle_value}")
                    print(f"🔧 [DPR FIX] Using DPR ID search: {classification['suggested_query']} (Reason: {classification['reasoning']})")
                else:
                    # This is a vehicle registration - use tm_no field
                    conditions.append(classification['suggested_query'])
                    print(f"🔧 [DPR FIX] Using vehicle registration search: {classification['suggested_query']} (Reason: {classification['reasoning']})")
        
        # Add WHERE clause if conditions exist
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        # Add default ordering
        base_query += " ORDER BY dpr.id_no DESC LIMIT 50"
        
        return base_query

    def distinguish_dpr_id_from_vehicle_reg(self, value):
        """
        Distinguish between DPR IDs and vehicle registration numbers to prevent identifier confusion.
        
        Args:
            value (str): The identifier value to classify
            
        Returns:
            dict: Classification result with type and recommended usage
        """
        if not value:
            return {'type': 'unknown', 'field': None, 'reasoning': 'Empty value'}
        
        value_str = str(value).strip()
        
        # DPR ID patterns (purely numeric)
        if value_str.isdigit():
            return {
                'type': 'dpr_id',
                'field': 'dpr.id_no',
                'reasoning': 'Purely numeric - likely internal DPR ID',
                'suggested_query': f"dpr.id_no = {value_str}"
            }
        
        # Vehicle registration patterns (alphanumeric with various formats)
        # Common vehicle registration formats: HR55AN1234, MH01AB1234, KA03MH6789, etc.
        vehicle_patterns = [
            r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$',  # Standard Indian format: HR55AN1234
            r'^[A-Z]{1,3}\d{1,4}[A-Z]{0,3}\d{0,4}$',  # Various state formats
            r'^[A-Z]+\d+[A-Z]*\d*$',  # General alphanumeric vehicle pattern
        ]
        
        import re
        for pattern in vehicle_patterns:
            if re.match(pattern, value_str.upper()):
                return {
                    'type': 'vehicle_registration',
                    'field': 'dpr.tm_no',
                    'reasoning': f'Matches vehicle registration pattern: {pattern}',
                    'suggested_query': f"dpr.tm_no ILIKE '%{value_str}%'"
                }
        
        # Mixed alphanumeric - likely vehicle registration
        if re.match(r'^[A-Z0-9]+$', value_str.upper()) and not value_str.isdigit():
            return {
                'type': 'vehicle_registration',
                'field': 'dpr.tm_no', 
                'reasoning': 'Mixed alphanumeric - likely vehicle registration',
                'suggested_query': f"dpr.tm_no ILIKE '%{value_str}%'"
            }
        
        # Default to vehicle registration for non-numeric values
        return {
            'type': 'vehicle_registration',
            'field': 'dpr.tm_no',
            'reasoning': 'Non-numeric value - defaulting to vehicle registration',
            'suggested_query': f"dpr.tm_no ILIKE '%{value_str}%'"
        }

    def is_dpr_related_query(self, user_input):
        """Check if the query is related to Daily Production Report"""
        dpr_keywords = [
            'dpr', 'daily production', 'production report', 'concrete order',
            'concrete delivery', 'ready mix', 'readymix', 'transit mixer',
            'tm', 'concrete truck', 'customer delivery', 'site delivery',
            'sales person', 'fse', 'concrete grade', 'batch order',
            'pump delivery', 'challan', 'sales order'
        ]
        
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in dpr_keywords)

    def detect_driver_query_type(self, user_input):
        """Detect the type of driver-related query"""
        user_input_lower = user_input.lower()
        
        # Check each driver query pattern
        for query_type, patterns in self.driver_query_patterns.items():
            if any(pattern in user_input_lower for pattern in patterns):
                return query_type
        
        # Additional specific driver detection
        driver_indicators = [
            'driver', 'drivers', 'drv_id', 'driver_id', 'd_code',
            'license', 'licence', 'mobile', 'phone', 'contact',
            'tshirt', 'uniform', 'assignment', 'depot'
        ]
        
        if any(indicator in user_input_lower for indicator in driver_indicators):
            return 'driver_lookup'  # Default driver query type
        
        return None

    def generate_driver_sql(self, query_type, user_input, entities=None):
        """Generate SQL for driver-related queries"""
        if entities is None:
            entities = []
        
        base_query = """
        SELECT 
            dm.id_no,
            CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
            dm.d_code AS driver_code,
            dm.telephone AS mobile_number,
            dm.lic_no AS license_number,
            dm.lic_exp AS license_expiry,
            dm.dt_of_birth,
            dm.dt_of_joining,
            dm.gender,
            dm.tshirt_size,
            hm.name AS assigned_plant,
            hm.hosp_code AS plant_code
        FROM driver_master dm
        LEFT JOIN hosp_master hm ON dm.id_depo = hm.id_no
        """
        
        conditions = []
        
        if query_type == 'license_management':
            # Focus on license-related information
            base_query = """
            SELECT 
                dm.id_no,
                CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                dm.d_code AS driver_code,
                dm.lic_no AS license_number,
                dm.lic_issue AS license_issued,
                dm.lic_exp AS license_expiry,
                CASE 
                    WHEN dm.lic_exp < CURRENT_DATE THEN 'EXPIRED'
                    WHEN dm.lic_exp <= CURRENT_DATE + INTERVAL '30 days' THEN 'EXPIRES_SOON'
                    ELSE 'VALID'
                END AS license_status,
                dm.telephone AS mobile_number,
                hm.name AS assigned_plant
            FROM driver_master dm
            LEFT JOIN hosp_master hm ON dm.id_depo = hm.id_no
            """
            
            # Check for expiry-related queries
            if any(word in user_input.lower() for word in ['expir', 'renew', 'expired']):
                conditions.append("dm.lic_exp <= CURRENT_DATE + INTERVAL '90 days'")
        
        elif query_type == 'plant_assignment':
            # Focus on plant assignment
            conditions.append("dm.id_depo IS NOT NULL")
        
        elif query_type == 'contact_info':
            # Focus on contact information
            base_query = """
            SELECT 
                dm.id_no,
                CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                dm.d_code AS driver_code,
                dm.telephone AS mobile_number,
                hm.name AS assigned_plant,
                hm.hosp_code AS plant_code
            FROM driver_master dm
            LEFT JOIN hosp_master hm ON dm.id_depo = hm.id_no
            """
            conditions.append("dm.telephone IS NOT NULL AND dm.telephone != ''")
        
        elif query_type == 'demographics':
            # Focus on demographic analysis
            if any(word in user_input.lower() for word in ['birthday', 'birth', 'born']):
                base_query = """
                SELECT 
                    dm.id_no,
                    CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                    dm.d_code AS driver_code,
                    dm.dt_of_birth AS birth_date,
                    TO_CHAR(dm.dt_of_birth, 'DD-MM-YYYY') AS formatted_birth_date,
                    TO_CHAR(dm.dt_of_birth, 'DD Month') AS birthday,
                    EXTRACT(YEAR FROM AGE(CURRENT_DATE, dm.dt_of_birth)) AS age,
                    dm.gender,
                    hm.name AS assigned_plant
                FROM driver_master dm
                LEFT JOIN hosp_master hm ON dm.id_depo = hm.id_no
                """
                conditions.append("dm.dt_of_birth IS NOT NULL")
            elif 'age' in user_input.lower():
                base_query = """
                SELECT 
                    dm.id_no,
                    CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                    dm.dt_of_birth,
                    EXTRACT(YEAR FROM AGE(CURRENT_DATE, dm.dt_of_birth)) AS age,
                    dm.gender,
                    hm.name AS assigned_plant
                FROM driver_master dm
                LEFT JOIN hosp_master hm ON dm.id_depo = hm.id_no
                """
                conditions.append("dm.dt_of_birth IS NOT NULL")
            else:
                # General demographics
                base_query = """
                SELECT 
                    dm.gender,
                    COUNT(*) AS driver_count,
                    AVG(EXTRACT(YEAR FROM AGE(CURRENT_DATE, dm.dt_of_birth))) AS average_age
                FROM driver_master dm
                WHERE dm.dt_of_birth IS NOT NULL
                GROUP BY dm.gender
                """
                return base_query  # Special case - already complete
        
        elif query_type == 'service_duration':
            # Focus on service duration
            base_query = """
            SELECT 
                dm.id_no,
                CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                dm.d_code AS driver_code,
                dm.dt_of_joining,
                EXTRACT(YEAR FROM AGE(CURRENT_DATE, dm.dt_of_joining)) AS years_of_service,
                hm.name AS assigned_plant
            FROM driver_master dm
            LEFT JOIN hosp_master hm ON dm.id_depo = hm.id_no
            """
            conditions.append("dm.dt_of_joining IS NOT NULL")
        
        elif query_type == 'uniform_management':
            # Check if asking about specific person's size vs. general distribution
            has_person_name = bool(re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', user_input))
            
            if has_person_name:
                # Individual driver size query
                base_query = """
                SELECT 
                    dm.id_no,
                    CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                    dm.d_code AS driver_code,
                    dm.tshirt_size AS uniform_size,
                    CASE 
                        WHEN dm.tshirt_size IS NULL OR dm.tshirt_size = '' THEN 'Size not recorded'
                        ELSE CONCAT('T-shirt size: ', dm.tshirt_size)
                    END AS size_info,
                    hm.name AS assigned_plant
                FROM driver_master dm
                LEFT JOIN hosp_master hm ON dm.id_depo = hm.id_no
                """
                # Don't add tshirt_size filter here - let it show even if size is not recorded
            else:
                # General uniform distribution
                base_query = """
                SELECT 
                    dm.tshirt_size,
                    COUNT(*) AS driver_count,
                    STRING_AGG(CONCAT(dm.first_name, ' ', dm.last_name), ', ') AS drivers
                FROM driver_master dm
                WHERE dm.tshirt_size IS NOT NULL AND dm.tshirt_size != ''
                GROUP BY dm.tshirt_size
                ORDER BY dm.tshirt_size
                """
                return base_query  # Special case - already complete
        
        elif query_type == 'driver_assignments':
            # Focus on driver assignments and scheduling
            if any(word in user_input.lower() for word in ['current', 'active', 'today', 'now']):
                # Current active assignments
                base_query = """
                SELECT 
                    da.id AS assignment_id,
                    CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                    da.d_code AS driver_code,
                    vm.vehicle_no,
                    vm.chassis_no,
                    hm.name AS plant_name,
                    da.date_from AS assignment_start,
                    da.date_to AS assignment_end,
                    CASE 
                        WHEN da.date_to IS NULL THEN 'ACTIVE'
                        WHEN da.date_to >= CURRENT_DATE THEN 'ACTIVE'
                        ELSE 'COMPLETED'
                    END AS assignment_status,
                    da.remarks
                FROM driver_assignment da
                LEFT JOIN driver_master dm ON da.d_code = dm.d_code
                LEFT JOIN vehicle_master vm ON da.vehicle_no = vm.vehicle_no
                LEFT JOIN hosp_master hm ON da.id_depo = hm.id_no
                """
                conditions.append("(da.date_to IS NULL OR da.date_to >= CURRENT_DATE)")
            
            elif any(word in user_input.lower() for word in ['history', 'past', 'previous', 'all']):
                # Assignment history
                base_query = """
                SELECT 
                    da.id AS assignment_id,
                    CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                    da.d_code AS driver_code,
                    vm.vehicle_no,
                    hm.name AS plant_name,
                    da.date_from AS assignment_start,
                    da.date_to AS assignment_end,
                    CASE 
                        WHEN da.date_to IS NULL THEN 'ACTIVE'
                        WHEN da.date_to >= CURRENT_DATE THEN 'ACTIVE'
                        ELSE 'COMPLETED'
                    END AS assignment_status,
                    EXTRACT(DAYS FROM (COALESCE(da.date_to, CURRENT_DATE) - da.date_from)) AS assignment_duration_days
                FROM driver_assignment da
                LEFT JOIN driver_master dm ON da.d_code = dm.d_code
                LEFT JOIN vehicle_master vm ON da.vehicle_no = vm.vehicle_no
                LEFT JOIN hosp_master hm ON da.id_depo = hm.id_no
                """
            
            elif any(word in user_input.lower() for word in ['conflict', 'overlap', 'double']):
                # Assignment conflicts
                base_query = """
                SELECT 
                    da1.d_code AS driver_code,
                    CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                    da1.vehicle_no AS vehicle1,
                    da2.vehicle_no AS vehicle2,
                    da1.date_from AS assignment1_start,
                    da1.date_to AS assignment1_end,
                    da2.date_from AS assignment2_start,
                    da2.date_to AS assignment2_end,
                    'ASSIGNMENT_CONFLICT' AS issue_type
                FROM driver_assignment da1
                JOIN driver_assignment da2 ON da1.d_code = da2.d_code AND da1.id != da2.id
                LEFT JOIN driver_master dm ON da1.d_code = dm.d_code
                WHERE da1.date_from <= COALESCE(da2.date_to, CURRENT_DATE)
                AND COALESCE(da1.date_to, CURRENT_DATE) >= da2.date_from
                """
            
            elif any(word in user_input.lower() for word in ['performance', 'efficiency', 'delivery']):
                # Performance analysis
                base_query = """
                SELECT 
                    da.d_code AS driver_code,
                    CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                    COUNT(da.id) AS total_assignments,
                    AVG(EXTRACT(DAYS FROM (COALESCE(da.date_to, CURRENT_DATE) - da.date_from))) AS avg_assignment_duration,
                    COUNT(CASE WHEN da.date_to IS NULL OR da.date_to >= CURRENT_DATE THEN 1 END) AS active_assignments,
                    hm.name AS primary_plant
                FROM driver_assignment da
                LEFT JOIN driver_master dm ON da.d_code = dm.d_code
                LEFT JOIN hosp_master hm ON da.id_depo = hm.id_no
                GROUP BY da.d_code, dm.first_name, dm.last_name, hm.name
                """
            
            else:
                # Default: Current assignments with basic info
                base_query = """
                SELECT 
                    da.id AS assignment_id,
                    CONCAT(dm.first_name, ' ', dm.last_name) AS driver_name,
                    da.d_code AS driver_code,
                    vm.vehicle_no,
                    hm.name AS plant_name,
                    da.date_from AS assignment_start,
                    da.date_to AS assignment_end,
                    CASE 
                        WHEN da.date_to IS NULL THEN 'ACTIVE'
                        WHEN da.date_to >= CURRENT_DATE THEN 'ACTIVE'
                        ELSE 'COMPLETED'
                    END AS assignment_status
                FROM driver_assignment da
                LEFT JOIN driver_master dm ON da.d_code = dm.d_code
                LEFT JOIN vehicle_master vm ON da.vehicle_no = vm.vehicle_no
                LEFT JOIN hosp_master hm ON da.id_depo = hm.id_no
                """
        
        # Add entity-based filters
        for entity in entities:
            if entity.get('entity_type') == 'driver_name':
                name_parts = entity['value'].split()
                if len(name_parts) == 1:
                    conditions.append(f"(dm.first_name ILIKE '%{name_parts[0]}%' OR dm.last_name ILIKE '%{name_parts[0]}%')")
                else:
                    conditions.append(f"dm.first_name ILIKE '%{name_parts[0]}%' AND dm.last_name ILIKE '%{name_parts[-1]}%'")
            
            elif entity.get('entity_type') == 'plant':
                conditions.append(f"hm.name ILIKE '%{entity['value']}%'")
            
            elif entity.get('entity_type') == 'driver_code':
                conditions.append(f"dm.d_code ILIKE '%{entity['value']}%'")
            
            elif entity.get('entity_type') == 'license_number':
                conditions.append(f"dm.lic_no ILIKE '%{entity['value']}%'")
            
            elif entity.get('entity_type') == 'vehicle_number':
                if query_type == 'driver_assignments':
                    conditions.append(f"da.vehicle_no ILIKE '%{entity['value']}%'")
            
            elif entity.get('entity_type') == 'assignment_status':
                if query_type == 'driver_assignments':
                    status = entity['value'].lower()
                    if status in ['active', 'current']:
                        conditions.append("(da.date_to IS NULL OR da.date_to >= CURRENT_DATE)")
                    elif status in ['completed', 'finished']:
                        conditions.append("da.date_to < CURRENT_DATE")
            
            elif entity.get('entity_type') == 'date':
                if query_type == 'driver_assignments':
                    conditions.append(f"da.date_from <= '{entity['value']}' AND (da.date_to IS NULL OR da.date_to >= '{entity['value']}')")
        
        # Add WHERE clause if conditions exist
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        # Add default ordering
        base_query += " ORDER BY dm.first_name, dm.last_name LIMIT 50"
        
        return base_query

    def is_driver_related_query(self, user_input):
        """Check if the query is related to driver management"""
        driver_keywords = [
            'driver', 'drivers', 'drv_id', 'driver_id', 'd_code',
            'license', 'licence', 'driving license', 'mobile number',
            'phone', 'contact', 'tshirt', 'uniform', 'assignment',
            'depot', 'plant assignment', 'driver details', 'employee',
            'birthday', 'birth date', 'date of birth', 'born', 'age',
            'driver assignment', 'current assignment', 'assigned driver',
            'driver schedule', 'driver roster', 'assignment history',
            'driver allocation', 'assigned to', 'driver duty',
            'assignment status', 'active assignment', 'vehicle assignment',
            'assignment duration', 'assignment conflict', 'duty schedule',
            'driver availability', 'scheduling conflict', 'delivery assignment'
        ]
        
        user_input_lower = user_input.lower()
        
        # Direct keyword matching
        has_driver_keyword = any(keyword in user_input_lower for keyword in driver_keywords)
        
        # Check for person name patterns with driver-related attributes
        # Look for both capitalized and lowercase name patterns
        has_person_name = (
            bool(re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', user_input)) or  # Capitalized names
            bool(re.search(r'\b[a-z]+\s+[a-z]+\b', user_input_lower))  # Lowercase names that could be names
        )
        
        person_with_driver_attributes = (
            # Pattern: "PersonName + driver_attribute" (e.g., "kailash mahto tshirt size")
            any(attr in user_input_lower for attr in ['tshirt', 'uniform', 'size', 'birthday', 'birth', 'age', 'mobile', 'phone']) and
            has_person_name
        )
        
        # Check for "size of PersonName" patterns
        size_of_person = (
            'size of' in user_input_lower and has_person_name
        )
        
        # Check for birthday/birth-related queries that might be about drivers
        birthday_queries = (
            any(word in user_input_lower for word in ['birthday', 'birth', 'born', 'age']) and has_person_name
        )
        
        # Check for "tell me about PersonName" patterns (could be driver info)
        tell_about_person = (
            any(phrase in user_input_lower for phrase in ['tell me about', 'about']) and has_person_name
        )
        
        return has_driver_keyword or person_with_driver_attributes or birthday_queries or size_of_person or tell_about_person

    def extract_entities(self, user_input, conversation_context=None):
        """Extract entities from user input for driver queries"""
        entities = []
        user_input_lower = user_input.lower()
        
        # Extract driver names (look for patterns like "driver John", "John Smith", etc.)
        import re
        
        # Pattern for driver names after keywords like "driver", "find", "show"
        name_patterns = [
            r'driver\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)',
            r'named?\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)',
            r'called\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)',
            r'about\s+([A-Za-z]+(?:\s+[A-Za-z]+))'  # Handle "tell me about john smith"
        ]
        
        for pattern in name_patterns:
            matches = re.finditer(pattern, user_input, re.IGNORECASE)
            for match in matches:
                name = match.group(1).strip()
                if len(name) > 1:  # Avoid single characters
                    entities.append({
                        'entity_type': 'driver_name',
                        'value': name,
                        'confidence': 0.8
                    })
        
        # Extract standalone person names (First Last format)
        # Look for capitalized words that appear to be names
        person_name_pattern = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
        name_matches = re.finditer(person_name_pattern, user_input)
        
        for match in name_matches:
            full_name = match.group(0).strip()
            first_name = match.group(1)
            last_name = match.group(2)
            
            # Skip common non-name patterns
            skip_patterns = ['When Was', 'What Size', 'Tell Me', 'Show Me', 'Find All']
            if full_name not in skip_patterns:
                entities.append({
                    'entity_type': 'driver_name',
                    'value': full_name,
                    'first_name': first_name,
                    'last_name': last_name,
                    'confidence': 0.9
                })
        
        # Also look for lowercase names that might be driver names
        # This handles cases like "kailash mahto"
        # Use a more specific approach to find names
        words = user_input_lower.split()
        skip_words = ['of', 'to', 'is', 'in', 'on', 'at', 'by', 'for', 'the', 'and', 'or', 'but', 'what', 'when', 'where', 'why', 'how', 'was', 'were', 'his', 'her', 'it', 'size', 'me', 'about', 'tell', 'give', 'want', 'birthday', 'gift', 'forgot']
        
        # Look for consecutive pairs of non-skip words that could be names
        for i in range(len(words) - 1):
            first_word = words[i]
            second_word = words[i + 1]
            
            if (len(first_word) > 2 and len(second_word) > 2 and 
                first_word not in skip_words and second_word not in skip_words and
                first_word.isalpha() and second_word.isalpha()):
                
                # Capitalize for display
                display_name = f"{first_word.title()} {second_word.title()}"
                
                # Check if we already have this name
                if not any(e['value'] == display_name for e in entities):
                    entities.append({
                        'entity_type': 'driver_name',
                        'value': display_name,
                        'first_name': first_word.title(),
                        'last_name': second_word.title(),
                        'confidence': 0.8
                    })
        
        # Extract plant names
        plant_patterns = [
            r'plant\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)',
            r'at\s+([A-Za-z]+(?:\s+plant)?)',
            r'depot\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)'
        ]
        
        for pattern in plant_patterns:
            matches = re.finditer(pattern, user_input, re.IGNORECASE)
            for match in matches:
                plant = match.group(1).strip()
                # Skip obvious non-plant words
                skip_plant_words = ['is', 'the', 'a', 'an', 'this', 'that', 'these', 'those']
                if len(plant) > 1 and plant.lower() not in skip_plant_words:
                    entities.append({
                        'entity_type': 'plant',
                        'value': plant,
                        'confidence': 0.7
                    })
        
        # Extract driver codes
        code_patterns = [
            r'd_code\s*[:=]?\s*([A-Za-z0-9]+)',
            r'driver code\s*[:=]?\s*([A-Za-z0-9]+)',
            r'code\s+([A-Za-z0-9]+)'
        ]
        
        for pattern in code_patterns:
            matches = re.finditer(pattern, user_input, re.IGNORECASE)
            for match in matches:
                code = match.group(1).strip()
                if len(code) > 1:
                    entities.append({
                        'entity_type': 'driver_code',
                        'value': code,
                        'confidence': 0.9
                    })
        
        # Extract license numbers
        license_patterns = [
            r'license\s*(?:number|no\.?)?\s*[:=]?\s*([A-Za-z0-9\-]+)',
            r'lic_no\s*[:=]?\s*([A-Za-z0-9\-]+)'
        ]
        
        for pattern in license_patterns:
            matches = re.finditer(pattern, user_input, re.IGNORECASE)
            for match in matches:
                license_no = match.group(1).strip()
                if len(license_no) > 3:  # License numbers are usually longer
                    entities.append({
                        'entity_type': 'license_number',
                        'value': license_no,
                        'confidence': 0.9
                    })
        
        # Extract vehicle numbers for assignment queries
        vehicle_patterns = [
            r'vehicle\s*(?:number|no\.?)?\s*[:=]?\s*([A-Za-z0-9\-]+)',
            r'vehicle_no\s*[:=]?\s*([A-Za-z0-9\-]+)',
            r'truck\s*(?:number|no\.?)?\s*[:=]?\s*([A-Za-z0-9\-]+)',
            r'\b([A-Z]{2}\d{2}[A-Z]{2}\d{4})\b',  # Pattern for vehicle registration numbers
            r'\b([A-Z]{2}\-\d{2}\-[A-Z]{2}\-\d{4})\b'  # Alternative format
        ]
        
        for pattern in vehicle_patterns:
            matches = re.finditer(pattern, user_input, re.IGNORECASE)
            for match in matches:
                vehicle_no = match.group(1).strip()
                if len(vehicle_no) > 3:
                    entities.append({
                        'entity_type': 'vehicle_number',
                        'value': vehicle_no,
                        'confidence': 0.8
                    })
        
        # Extract assignment status
        status_patterns = [
            (r'\b(active|current|ongoing)\b', 'active'),
            (r'\b(completed|finished|ended|past)\b', 'completed'),
            (r'\b(all|total)\b', 'all')
        ]
        
        for pattern, status_type in status_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                entities.append({
                    'entity_type': 'assignment_status',
                    'value': status_type,
                    'confidence': 0.7
                })
        
        # Extract dates for assignment queries
        date_patterns = [
            r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD
            r'\b(\d{2}-\d{2}-\d{4})\b',  # DD-MM-YYYY
            r'\b(\d{1,2}/\d{1,2}/\d{4})\b',  # M/D/YYYY or MM/DD/YYYY
            r'\btoday\b',
            r'\byesterday\b',
            r'\btomorrow\b'
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, user_input, re.IGNORECASE)
            for match in matches:
                date_value = match.group(0).strip()
                # Convert relative dates to actual dates
                if date_value.lower() == 'today':
                    from datetime import date
                    date_value = date.today().strftime('%Y-%m-%d')
                elif date_value.lower() == 'yesterday':
                    from datetime import date, timedelta
                    date_value = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
                elif date_value.lower() == 'tomorrow':
                    from datetime import date, timedelta
                    date_value = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
                
                entities.append({
                    'entity_type': 'date',
                    'value': date_value,
                    'confidence': 0.8
                })
        
        return entities

    def _extract_inter_plant_criteria(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract criteria for inter-plant distance queries"""
        return {
            'report_type': 'inter_plant_distance',
            'table': 'distance_report',
            'focus': 'plant_hierarchy',
            'additional_joins': ['vehicle_master', 'hosp_master', 'district_master']
        }

    def _extract_time_distance_criteria(self, query: str, match, chat_context) -> Optional[Dict]:
        """Extract criteria for time-based distance reports"""
        time_period = 'daily'
        if re.search(r'monthly', query, re.IGNORECASE):
            time_period = 'monthly'
        elif re.search(r'weekly', query, re.IGNORECASE):
            time_period = 'weekly'
        elif re.search(r'yearly|annual', query, re.IGNORECASE):
            time_period = 'yearly'
        
        return {
            'report_type': 'time_distance_report',
            'table': 'distance_report',
            'time_period': time_period,
            'additional_joins': ['vehicle_master', 'hosp_master', 'district_master']
        }

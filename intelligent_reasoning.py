#!/usr/bin/env python3
"""
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
    - hosp_master = PLANT DATA (factories, facilities, sites) - NOT hospitals!
    - district_master = REGIONS/DISTRICTS/STATES 
    - zone_master = ZONES (larger geographic areas)
    - vehicle_master = VEHICLES/TRUCKS/FLEET
    """
    
    def __init__(self):
        # CRITICAL: Define the core hierarchical relationships using exact ID columns
        # These ID relationships are MANDATORY and must NEVER be missed:
        # zone_master.id_no ← district_master.id_zone ← hosp_master.id_dist ← vehicle_master.id_hosp
        
        # IMPORTANT: hosp_master contains PLANT DATA, not hospital data!
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
            }
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
                'pattern': r'(?:show|list|all)\s+(?:all\s+)?(?:plants|hospitals|facilities)',
                'intent': 'show_all_plants',
                'extractor': self._extract_show_all_plants
            },
            
            # Zone hierarchy patterns
            {
                'pattern': r'(?:zone|area).*(?:vehicle|truck)\s+([A-Z0-9-]+)',
                'intent': 'get_zone_from_vehicle',
                'extractor': self._extract_zone_from_vehicle
            },
            {
                'pattern': r'(?:region|district).*(?:vehicle|truck)\s+([A-Z0-9-]+)',
                'intent': 'get_region_from_vehicle',
                'extractor': self._extract_region_from_vehicle
            },
            {
                'pattern': r'(?:plant|hospital|facility).*(?:vehicle|truck)\s+([A-Z0-9-]+)',
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
                'pattern': r'(?:vehicles|trucks).*(?:plant|hospital)\s+([A-Z0-9\s]+)',
                'intent': 'get_vehicles_in_plant',
                'extractor': self._extract_vehicles_in_plant
            },
            {
                'pattern': r'(?:vehicles|trucks).*(?:of|in|at)\s+([a-zA-Z0-9\s\-]+?)(?:\s+plant|\s+hospital|$)',
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
                'pattern': r'(?:what|tell.*about|details.*of).*(?:that|the|this)\s+(?:plant|customer|vehicle)',
                'intent': 'get_details_from_last_context',
                'extractor': self._extract_from_last_context
            }
        ]
    
    def analyze_query_intent(self, user_query: str, chat_context) -> Optional[Dict]:
        """
        Analyze user query to detect if it requires intelligent reasoning
        Returns enhanced query info if reasoning is needed, None otherwise
        """
        user_query_lower = user_query.lower().strip()
        
        # Check each intent pattern
        for intent_config in self.intent_patterns:
            pattern = intent_config['pattern']
            intent = intent_config['intent']
            extractor = intent_config['extractor']
            
            match = re.search(pattern, user_query_lower, re.IGNORECASE)
            if match:
                # Extract relevant data using the specific extractor
                extracted_data = extractor(user_query, match, chat_context)
                
                if extracted_data:
                    return {
                        'original_query': user_query,
                        'intent': intent,
                        'extracted_data': extracted_data,
                        'reasoning_type': 'contextual_auto_resolve'
                    }
        
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
        
        return None
    
    def create_intelligent_response(self, reasoning_result: Dict, query_result: Dict) -> str:
        """
        Create a natural, intelligent response that explains the reasoning - ENHANCED HIERARCHICAL
        """
        extracted_data = reasoning_result['extracted_data']
        intent = reasoning_result['intent']
        source = extracted_data.get('source', 'unknown')
        
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

    def _extract_vehicles_of_plant_flexible(self, query: str, match, chat_context):
        """Extract plant name for vehicle lookup with flexible matching"""
        plant_name = match.group(1).strip() if match.groups() else None
        if plant_name:
            # Clean up the plant name - remove common words like "the"
            plant_name = re.sub(r'\b(?:the|plant|hospital)\b', '', plant_name, flags=re.IGNORECASE).strip()
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
                SELECT zm.zone_name, dm.name as district_name, hm.name as plant_name, vm.reg_no
                FROM zone_master zm 
                JOIN district_master dm ON zm.id_no = dm.id_zone 
                JOIN hosp_master hm ON dm.id_no = hm.id_dist 
                JOIN vehicle_master vm ON hm.id_no = vm.id_hosp 
                WHERE vm.reg_no = '{data.get('vehicle_reg', '')}'
            """,
            
            'get_region_from_vehicle': lambda data: f"""
                SELECT dm.name as region_name, hm.name as plant_name, vm.reg_no
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
                SELECT vm.reg_no, hm.name as plant_name, dm.name as district_name
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                JOIN district_master dm ON hm.id_dist = dm.id_no 
                JOIN zone_master zm ON dm.id_zone = zm.id_no 
                WHERE zm.zone_name ILIKE '%{data.get('zone_name', '')}%'
                ORDER BY vm.reg_no
            """,
            
            'get_vehicles_in_region': lambda data: f"""
                SELECT vm.reg_no, hm.name as plant_name
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                JOIN district_master dm ON hm.id_dist = dm.id_no 
                WHERE dm.name ILIKE '%{data.get('region_name', '')}%'
                ORDER BY vm.reg_no
            """,
            
            'get_vehicles_in_plant': lambda data: f"""
                SELECT vm.reg_no, vm.regional_name
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                WHERE hm.name ILIKE '%{data.get('plant_name', '')}%'
                ORDER BY vm.reg_no
            """,
            
            'get_vehicles_of_plant': lambda data: f"""
                SELECT vm.reg_no, vm.bus_id, hm.name as plant_name
                FROM vehicle_master vm 
                JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                WHERE hm.name ILIKE '%{data.get('plant_name', '')}%'
                ORDER BY vm.reg_no
                LIMIT 50
            """,
            
            'get_vehicle_hierarchy': lambda data: f"""
                SELECT vm.reg_no, hm.name as plant_name, dm.name as district_name, zm.zone_name
                FROM vehicle_master vm 
                LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no 
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no 
                LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no 
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
                'select': 'vm.reg_no, vm.bus_id, hm.name as plant_name',
                'joins': complete_join_chain,
                'where_template': "hm.name ILIKE '%{plant_name}%'"
            },
            'vehicles_by_region': {
                'select': 'vm.reg_no, vm.bus_id, dm.name as region_name, hm.name as plant_name',
                'joins': complete_join_chain,
                'where_template': "dm.name ILIKE '%{region_name}%'"
            },
            'vehicles_by_zone': {
                'select': 'vm.reg_no, vm.bus_id, zm.zone_name, dm.name as region_name, hm.name as plant_name',
                'joins': complete_join_chain,
                'where_template': "zm.zone_name ILIKE '%{zone_name}%'"
            },
            'plants_by_region': {
                'select': 'hm.name as plant_name, hm.id_no as plant_id, dm.name as region_name',
                'joins': """
                FROM hosp_master hm
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
                """,
                'where_template': "dm.name ILIKE '%{region_name}%'"
            },
            'plants_by_location_smart': {
                'select': 'hm.name as plant_name, hm.id_no as plant_id, dm.name as region_name',
                'joins': """
                FROM hosp_master hm
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
                """,
                'where_template': "dm.name ILIKE '%{location_name}%'",
                'note': 'Use this for most location queries (Gujarat, Maharashtra, etc.) - they are typically districts'
            },
            'plants_by_zone': {
                'select': 'hm.name as plant_name, hm.id_no as plant_id, dm.name as region_name, zm.zone_name',
                'joins': """
                FROM hosp_master hm
                LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
                LEFT JOIN zone_master zm ON dm.id_zone = zm.id_no
                """,
                'where_template': "zm.zone_name ILIKE '%{zone_name}%'",
                'note': 'Use this ONLY when specifically asking for zone data or when location is confirmed to be a zone'
            },
            'full_hierarchy_for_vehicle': {
                'select': 'vm.reg_no, vm.bus_id, hm.name as plant_name, dm.name as region_name, zm.zone_name',
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
            'plant': any(word in query_lower for word in ['plant', 'hospital', 'facility', 'hosp']),
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

def test_intelligent_reasoning():
    """Test the intelligent reasoning system"""
    print("🧠 Testing Intelligent Reasoning System")
    print("=" * 50)
    
    reasoning = IntelligentReasoning()
    
    # Mock chat context with complaint data
    class MockChatContext:
        def __init__(self):
            self.last_displayed_items = [
                {
                    'complaint_id': 172,
                    'plant_id': 435,
                    'customer_id': 119898,
                    '_original_question': 'site visit details of complaint id 172'
                }
            ]
            self.history = []
    
    context = MockChatContext()
    
    # Test cases
    test_queries = [
        "can you tell me the plant name for complaint id 172",
        "what is the plant name for the one mentioned in complaint id 172", 
        "tell me the plant name if you have the plant id",
        "the plant name for that complaint"
    ]
    
    for query in test_queries:
        print(f"\n📝 Testing: '{query}'")
        
        result = reasoning.analyze_query_intent(query, context)
        if result:
            print(f"✅ Intent detected: {result['intent']}")
            print(f"📊 Extracted data: {result['extracted_data']}")
            
            sql = reasoning.generate_intelligent_query(result)
            if sql:
                print(f"🔧 Generated SQL: {sql.strip()}")
        else:
            print("❌ No intelligent reasoning needed")

if __name__ == "__main__":
    test_intelligent_reasoning()

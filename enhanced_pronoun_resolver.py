#!/usr/bin/env python3
"""
Enhanced Pronoun and Context Resolution System
Handles follow-up questions with pronouns like "their", "its", "those", etc.
"""

import re
from typing import Dict, List, Optional, Any

class EnhancedPronounResolver:
    """
    Enhanced system for resolving pronouns and contextual references
    in follow-up questions after displaying query results.
    """
    
    def __init__(self):
        # Comprehensive pronoun patterns for different contexts
        self.pronoun_patterns = {
            # Possessive pronouns referring to previous results (with typo handling)
            'possessive_pronouns': [
                r'\b(?:their|its|his|her|thier|thire)\s+(details?|information?|data|info|names?|addresses?|status|properties?)\b',
                r'\b(?:their|its|his|her|thier|thire)\s+(plant\s+names?|customer\s+names?|vehicle\s+details?)\b',
                r'\bshow\s+(?:their|its|his|her|thier|thire)\s+(\w+)\b',
                r'\b(?:what\s+(?:are|is))\s+(?:their|its|his|her|thier|thire)\s+(\w+)\b',
                r'\b(?:give|show|display)\s+(?:their|its|his|her|thier|thire)\s+(\w+)\b'
            ],
            
            # Demonstrative pronouns
            'demonstrative_pronouns': [
                r'\b(?:those|these|that|this)\s+(vehicles?|plants?|customers?|complaints?|items?)\b',
                r'\bfor\s+(?:those|these|that|this)\s+(\w+)\b',
                r'\bshow\s+(?:those|these|that|this)\s+(\w+)\b'
            ],
            
            # Generic references to previous results
            'generic_references': [
                r'\bshow\s+(?:me\s+)?(?:all\s+)?(?:the\s+)?details?\b',
                r'\b(?:what|tell\s+me)\s+about\s+(?:them|it|those)\b',
                r'\b(?:give\s+me\s+)?(?:more\s+)?information?\s+(?:about\s+)?(?:them|it|those)?\b',
                r'\blist\s+(?:all\s+)?(?:their|its)\s+(\w+)\b',
                r'\b(?:display|show)\s+(?:complete|full|all)\s+(?:details?|information?)\b'
            ],
            
            # Specific field requests
            'field_requests': [
                r'\b(?:what\s+(?:are|is)\s+)?(?:their|its)\s+(names?|addresses?|ids?|numbers?|types?|statuses?)\b',
                r'\bshow\s+(?:me\s+)?(?:their|its)\s+(plant\s+names?|customer\s+names?|registration\s+numbers?)\b',
                r'\b(?:list|display)\s+(?:all\s+)?(?:their|its)\s+(\w+)\b'
            ],
            
            # Clarification avoidance patterns
            'context_continuation': [
                r'\bfor\s+(?:those|these|them|it)\b',
                r'\bof\s+(?:those|these|them|it)\b',
                r'\bin\s+(?:those|these|them|it)\b',
                r'\babout\s+(?:those|these|them|it)\b'
            ]
        }
        
        # Entity type mapping for context resolution
        self.entity_mappings = {
            'vehicles': {
                'identifier_fields': ['reg_no', 'registration_number', 'vehicle_id', 'vehicle_registration_number', 'id_no'],
                'detail_fields': ['reg_no', 'vehicle_type', 'model', 'plant_name', 'region'],
                'table': 'crm_site_visit_dtls',
                'common_joins': [
                    'LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no',
                    'LEFT JOIN district_master dm ON hm.id_dist = dm.id_no'
                ]
            },
            'plants': {
                'identifier_fields': ['id_no', 'plant_id', 'plant_name', 'name'],
                'detail_fields': ['plant_name', 'address', 'id_no', 'region'],
                'table': 'mst_plant',
                'common_joins': [
                    'LEFT JOIN district_master dm ON mp.id_dist = dm.id_no'
                ]
            },
            'customers': {
                'identifier_fields': ['customer_id', 'cust_id', 'id_no'],
                'detail_fields': ['customer_name', 'customer_id', 'address', 'site_name'],
                'table': 'customer_ship_details',  # Updated to use the correct table
                'common_joins': [
                    'LEFT JOIN site_master sm ON csd.ship_to_id = sm.id_no'
                ]
            },
            'complaints': {
                'identifier_fields': ['id_no', 'complaint_id'],
                'detail_fields': ['id_no', 'complaint_date', 'active_status', 'description', 'plant_name'],
                'table': 'crm_complaint_dtls',
                'common_joins': [
                    'LEFT JOIN customer_ship_details csd ON cd.cust_id = csd.id_no'
                ]
            }
        }
    
    def detect_pronoun_reference(self, query: str) -> Dict[str, Any]:
        """
        Detect if the query contains pronoun references that should be resolved
        using previous conversation context.
        
        Returns:
            Dict with detection results and suggested resolution approach
        """
        query_lower = query.lower().strip()
        
        detection_result = {
            'has_pronoun_reference': False,
            'pronoun_type': None,
            'matched_pattern': None,
            'extracted_field': None,
            'confidence': 0.0,
            'needs_context_resolution': False
        }
        
        # Check each pronoun pattern category
        for category, patterns in self.pronoun_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, query_lower, re.IGNORECASE)
                if match:
                    detection_result['has_pronoun_reference'] = True
                    detection_result['pronoun_type'] = category
                    detection_result['matched_pattern'] = pattern
                    detection_result['needs_context_resolution'] = True
                    detection_result['confidence'] = 0.9
                    
                    # Extract specific field if captured
                    if match.groups():
                        detection_result['extracted_field'] = match.group(1)
                    
                    print(f"🎯 Pronoun reference detected: {category}")
                    print(f"📝 Pattern: {pattern}")
                    print(f"🔍 Field: {detection_result['extracted_field']}")
                    
                    return detection_result
        
        # Additional checks for subtle context continuation
        subtle_patterns = [
            r'\bshow\s+(?:me\s+)?(?:details?|information?)\b',
            r'\b(?:what|tell\s+me)\s+about\b',
            r'\b(?:more\s+)?information?\b',
            r'\bnames?\s+(?:of|for)?\b'
        ]
        
        for pattern in subtle_patterns:
            if re.search(pattern, query_lower):
                detection_result['has_pronoun_reference'] = True
                detection_result['pronoun_type'] = 'implicit_reference'
                detection_result['matched_pattern'] = pattern
                detection_result['needs_context_resolution'] = True
                detection_result['confidence'] = 0.7
                break
        
        return detection_result
    
    def resolve_context_reference(self, query: str, chat_context, detection_result: Dict) -> Optional[Dict]:
        """
        Resolve pronoun references using conversation context to generate
        appropriate follow-up queries.
        """
        if not chat_context or not chat_context.last_displayed_items:
            print("❌ No conversation context available for pronoun resolution")
            return None
        
        # Get the last displayed items
        last_items = chat_context.last_displayed_items
        if not last_items:
            print("❌ No items in last displayed results")
            return None
        
        # Determine the entity type from context
        entity_type = self._infer_entity_type(last_items)
        if not entity_type:
            print("❌ Could not infer entity type from context")
            return None
        
        print(f"🎯 Inferred entity type: {entity_type}")
        
        # Get the requested field/detail type
        requested_field = detection_result.get('extracted_field', 'details')
        
        # Generate context-aware SQL query
        sql_query = self._generate_context_aware_query(
            entity_type, 
            last_items, 
            requested_field,
            query
        )
        
        if sql_query:
            return {
                'sql': sql_query,
                'entity_type': entity_type,
                'requested_field': requested_field,
                'context_items_count': len(last_items),
                'reasoning': f"Resolved pronoun reference to show {requested_field} for {len(last_items)} {entity_type} from previous results"
            }
        
        return None
    
    def _infer_entity_type(self, last_items: List[Dict]) -> Optional[str]:
        """
        Infer the entity type (vehicles, plants, customers, etc.) 
        from the structure of last displayed items.
        """
        if not last_items:
            return None
        
        # Check first item's fields to determine type
        sample_item = last_items[0]
        fields = set(sample_item.keys())
        
        # Remove metadata fields
        fields.discard('_display_index')
        fields.discard('_original_question')
        fields.discard('_sql_query')
        
        # Check against known entity patterns - ORDER MATTERS!
        # Check most specific patterns first
        if any(field in fields for field in ['complaint_id', 'complaint_date', 'complaint_category_id']):
            return 'complaints'
        elif any(field in fields for field in ['customer_id', 'cust_id', 'customer_name']):
            return 'customers'
        elif any(field in fields for field in ['reg_no', 'registration_number', 'vehicle_id', 'vehicle_registration_number']):
            return 'vehicles'
        elif any(field in fields for field in ['plant_id', 'plant_name', 'hosp_id']) or ('name' in fields and any(field in fields for field in ['plant_id', 'plant_name'])):
            return 'plants'  
        elif 'name' in fields and any(field in fields for field in ['id_no', 'address']):
            # Could be plants if has name and id_no/address
            return 'plants'
        
        print(f"🔍 Available fields for type inference: {fields}")
        return None
    
    def _generate_context_aware_query(self, entity_type: str, last_items: List[Dict], 
                                    requested_field: str, original_query: str) -> Optional[str]:
        """
        Generate SQL query based on entity type and requested information.
        """
        if entity_type not in self.entity_mappings:
            print(f"❌ Unknown entity type: {entity_type}")
            return None
        
        entity_config = self.entity_mappings[entity_type]
        
        # Get identifiers from last items
        identifiers = []
        identifier_field = None
        
        for id_field in entity_config['identifier_fields']:
            sample_values = [item.get(id_field) for item in last_items if item.get(id_field)]
            if sample_values:
                identifier_field = id_field
                identifiers = [str(val) for val in sample_values if val]
                break
        
        if not identifiers or not identifier_field:
            print(f"❌ No identifiers found for {entity_type}")
            return None
        
        print(f"🔑 Using identifier field: {identifier_field}")
        print(f"📊 Found {len(identifiers)} identifiers")
        
        # Determine what fields to select based on request
        select_fields = self._determine_select_fields(
            entity_type, 
            entity_config, 
            requested_field, 
            original_query
        )
        
        # Build the SQL query with consistent table aliases
        base_table = entity_config['table']
        table_alias = self._get_consistent_alias(base_table)
        
        sql_parts = [
            f"SELECT {select_fields}",
            f"FROM {base_table} {table_alias}"
        ]
        
        # Add common joins if needed - fix aliases
        for join in entity_config.get('common_joins', []):
            # Fix join statements to use consistent aliases
            fixed_join = self._fix_join_aliases(join, entity_type)
            sql_parts.append(fixed_join)
        
        # Add WHERE clause for identifiers
        if len(identifiers) == 1:
            sql_parts.append(f"WHERE {table_alias}.{identifier_field} = '{identifiers[0]}'")
        else:
            identifiers_str = "', '".join(identifiers[:50])  # Limit to 50 for performance
            sql_parts.append(f"WHERE {table_alias}.{identifier_field} IN ('{identifiers_str}')")
        
        sql_query = "\n".join(sql_parts)
        
        print(f"🔧 Generated context-aware SQL:")
        print(f"   {sql_query}")
        
        return sql_query
    
    def _get_consistent_alias(self, table_name: str) -> str:
        """Get consistent table alias based on table name"""
        alias_map = {
            'vehicle_master': 'vm',
            'hosp_master': 'hm', 
            'customer_ship_details': 'csd',  # Updated alias
            'crm_complaint_dtls': 'cd',
            'crm_site_visit_dtls': 'csvd',
            'district_master': 'dm',
            'zone_master': 'zm',
            'site_master': 'sm'
        }
        return alias_map.get(table_name, table_name[:2])
    
    def _fix_join_aliases(self, join_statement: str, entity_type: str) -> str:
        """Fix join statements to use consistent aliases"""
        # Replace common alias issues
        fixes = {
            'LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no': 'LEFT JOIN hosp_master hm ON vm.id_hosp = hm.id_no',
            'LEFT JOIN district_master dm ON hm.id_dist = dm.id_no': 'LEFT JOIN district_master dm ON hm.id_dist = dm.id_no',
            'LEFT JOIN site_master sm ON csd.ship_to_id = sm.id_no': 'LEFT JOIN site_master sm ON csd.ship_to_id = sm.id_no'
        }
        
        return fixes.get(join_statement, join_statement)
    
    def _determine_select_fields(self, entity_type: str, entity_config: Dict, 
                               requested_field: str, original_query: str) -> str:
        """
        Determine what fields to select based on the user's request.
        """
        query_lower = original_query.lower()
        
        # Get consistent table alias
        base_table = entity_config['table']
        table_alias = self._get_consistent_alias(base_table)
        
        # If user asks for specific fields
        if requested_field and requested_field != 'details':
            if 'name' in requested_field:
                if entity_type == 'vehicles':
                    return f"{table_alias}.reg_no, hm.name as plant_name, dm.name as region_name"
                elif entity_type == 'plants':
                    return f"{table_alias}.name as plant_name, {table_alias}.address, dm.name as region_name"
                elif entity_type == 'customers':
                    return f"{table_alias}.customer_name, {table_alias}.customer_id"
            
            elif 'address' in requested_field:
                if entity_type == 'plants':
                    return f"{table_alias}.name as plant_name, {table_alias}.address"
                elif entity_type == 'customers':
                    return f"{table_alias}.customer_name, sm.site_name, sm.address"
            
            elif 'status' in requested_field:
                if entity_type == 'complaints':
                    return f"{table_alias}.id_no, {table_alias}.active_status, {table_alias}.complaint_date"
        
        # Check for specific requests in the query
        if 'plant name' in query_lower and entity_type == 'vehicles':
            return f"{table_alias}.reg_no, hm.name as plant_name"
        elif 'customer name' in query_lower and entity_type == 'complaints':
            # For complaints, get customer names from customer_ship_details via cust_id
            return f"{table_alias}.id_no, {table_alias}.complaint_date, csd.customer_name, {table_alias}.plant_name"
        elif 'region' in query_lower or 'district' in query_lower:
            if entity_type == 'vehicles':
                return f"{table_alias}.reg_no, hm.name as plant_name, dm.name as region_name"
            elif entity_type == 'plants':
                return f"{table_alias}.name as plant_name, dm.name as region_name"
        
        # Default comprehensive details
        if entity_type == 'vehicles':
            return f"{table_alias}.reg_no, {table_alias}.vehicle_type, hm.name as plant_name, dm.name as region_name"
        elif entity_type == 'plants':
            return f"{table_alias}.name as plant_name, {table_alias}.address, {table_alias}.id_no, dm.name as region_name"
        elif entity_type == 'customers':
            return f"{table_alias}.customer_name, {table_alias}.customer_id, sm.site_name as site_address"
        elif entity_type == 'complaints':
            return f"{table_alias}.id_no, {table_alias}.complaint_date, {table_alias}.active_status, {table_alias}.plant_name, csd.customer_name"
        
        return "*"
    
    def should_avoid_clarification(self, query: str, chat_context) -> bool:
        """
        Determine if we should avoid asking for clarification and instead
        use context resolution for this query.
        """
        if not chat_context or not chat_context.last_displayed_items:
            return False
        
        detection_result = self.detect_pronoun_reference(query)
        
        # High confidence pronoun references should use context
        if detection_result['has_pronoun_reference'] and detection_result['confidence'] >= 0.8:
            return True
        
        # Check if this is clearly a follow-up to previous results
        query_lower = query.lower()
        
        followup_indicators = [
            'show their',
            'what are their',
            'tell me about them',
            'show me details',
            'more information',
            'show all details',
            'list their',
            'display their'
        ]
        
        return any(indicator in query_lower for indicator in followup_indicators)


def test_enhanced_pronoun_resolver():
    """Test the enhanced pronoun resolution system"""
    print("🧪 Testing Enhanced Pronoun Resolution System")
    print("=" * 50)
    
    resolver = EnhancedPronounResolver()
    
    # Mock chat context with vehicle data
    class MockChatContext:
        def __init__(self):
            self.last_displayed_items = [
                {
                    'reg_no': 'UP16GT8409',
                    'vehicle_type': 'Truck',
                    'plant_id': 460,
                    '_display_index': 1,
                    '_original_question': 'show all vehicles'
                },
                {
                    'reg_no': 'KA01AK6654', 
                    'vehicle_type': 'Car',
                    'plant_id': 461,
                    '_display_index': 2,
                    '_original_question': 'show all vehicles'
                }
            ]
            self.history = []
    
    context = MockChatContext()
    
    # Test queries
    test_queries = [
        "show their details",
        "what are their plant names",
        "tell me more about them", 
        "show me information about those vehicles",
        "display their complete information",
        "list their registration numbers"
    ]
    
    for query in test_queries:
        print(f"\n📝 Testing: '{query}'")
        
        # Test pronoun detection
        detection = resolver.detect_pronoun_reference(query)
        print(f"   🎯 Detected: {detection['has_pronoun_reference']}")
        print(f"   📊 Type: {detection.get('pronoun_type')}")
        print(f"   🔍 Field: {detection.get('extracted_field')}")
        
        # Test context resolution
        if detection['needs_context_resolution']:
            resolution = resolver.resolve_context_reference(query, context, detection)
            if resolution:
                print(f"   ✅ Resolved SQL: {resolution['sql'][:100]}...")
                print(f"   🎯 Entity: {resolution['entity_type']}")
                print(f"   📊 Field: {resolution['requested_field']}")
            else:
                print(f"   ❌ Could not resolve context")
        
        # Test clarification avoidance
        should_avoid = resolver.should_avoid_clarification(query, context)
        print(f"   🚫 Avoid clarification: {should_avoid}")

if __name__ == "__main__":
    test_enhanced_pronoun_resolver()

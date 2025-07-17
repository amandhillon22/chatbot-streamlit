#!/usr/bin/env python3
"""
Enhanced Table Mapping System for Better Query Accuracy
"""

import re
from typing import List, Dict, Tuple, Set
from difflib import SequenceMatcher

class EnhancedTableMapper:
    """Advanced table mapping with multiple strategies"""
    
    def __init__(self):
        # High-priority keyword mappings - these should ALWAYS be preferred
        self.priority_mappings = {
            # CRM and Customer Management
            'site visit': ['crm_site_visit_dtls', 'site_visit_history', 'visit_details'],
            'customer complaint': ['customer_complaints', 'complaint_details', 'crm_complaints'],
            'complaint': ['customer_complaints', 'complaint_details', 'crm_complaints'],
            'site visit details': ['crm_site_visit_dtls'],
            'visit details': ['crm_site_visit_dtls', 'visit_history'],
            
            # Vehicle Management
            'vehicle': ['vehicle_master', 'mega_trips', 'drv_veh_qr_assign'],
            'truck': ['vehicle_master', 'mega_trips'],
            'fleet': ['vehicle_master', 'mega_trips'],
            
            # Plant and Location
            'plant': ['plant_schedule', 'plant_master', 'plant_data'],
            'location': ['vehicle_location_shifting', 'plant_schedule'],
            'region': ['vehicle_master', 'vehicle_location_shifting'],
            
            # Maintenance
            'maintenance': ['veh_maintain', 'tc_maintenances', 'maintenance_history'],
            'repair': ['veh_maintain', 'maintenance_history'],
            
            # Driver Management
            'driver': ['driver_master', 'drv_veh_qr_assign', 'driver_details'],
            
            # Trip and Route
            'trip': ['mega_trips', 'trip_details', 'route_master'],
            'route': ['route_master', 'mega_trips'],
            
            # Financial
            'billing': ['billing_master', 'customer_bill_details'],
            'payment': ['payment_history', 'billing_master'],
        }
        
        # Domain-specific table groups
        self.table_domains = {
            'crm': ['crm_site_visit_dtls', 'customer_complaints', 'crm_complaints'],
            'vehicle': ['vehicle_master', 'mega_trips', 'vehicle_breakdown'],
            'driver': ['driver_master', 'drv_veh_qr_assign'],
            'plant': ['plant_schedule', 'plant_master', 'plant_data'],
            'maintenance': ['veh_maintain', 'tc_maintenances'],
            'financial': ['billing_master', 'payment_history'],
        }
        
        # Exact table name aliases
        self.table_aliases = {
            'site_visit': 'crm_site_visit_dtls',
            'site_visits': 'crm_site_visit_dtls',
            'visit': 'crm_site_visit_dtls',
            'visits': 'crm_site_visit_dtls',
            'complaints': 'customer_complaints',
            'complaint': 'customer_complaints',
        }
    
    def extract_keywords(self, query: str) -> Set[str]:
        """Extract relevant keywords from query"""
        query_lower = query.lower()
        keywords = set()
        
        # Extract exact phrases first
        for phrase in self.priority_mappings.keys():
            if phrase in query_lower:
                keywords.add(phrase)
        
        # Extract individual words
        words = re.findall(r'\b\w+\b', query_lower)
        for word in words:
            if len(word) > 2:  # Skip very short words
                keywords.add(word)
        
        return keywords
    
    def get_priority_tables(self, query: str) -> List[str]:
        """Get high-priority tables based on keyword matching"""
        keywords = self.extract_keywords(query)
        priority_tables = []
        
        # Check for exact phrase matches first (highest priority)
        for phrase, tables in self.priority_mappings.items():
            if phrase in query.lower():
                priority_tables.extend(tables)
                print(f"🎯 PRIORITY MATCH: '{phrase}' → {tables}")
        
        # Check for individual keyword matches
        for keyword in keywords:
            if keyword in self.priority_mappings:
                priority_tables.extend(self.priority_mappings[keyword])
            
            # Check table aliases
            if keyword in self.table_aliases:
                priority_tables.append(self.table_aliases[keyword])
        
        return list(set(priority_tables))  # Remove duplicates
    
    def fuzzy_match_tables(self, query: str, available_tables: List[str], threshold: float = 0.6) -> List[Tuple[str, float]]:
        """Fuzzy match query terms with table names"""
        query_lower = query.lower()
        matches = []
        
        for table in available_tables:
            # Direct substring match
            if any(term in table.lower() for term in query_lower.split()):
                matches.append((table, 0.9))
            
            # Fuzzy string matching
            similarity = SequenceMatcher(None, query_lower, table.lower()).ratio()
            if similarity >= threshold:
                matches.append((table, similarity))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def rank_tables(self, query: str, embedding_results: List, available_tables: List[str]) -> List[Tuple[str, float, str]]:
        """Combine multiple strategies to rank tables"""
        
        # Strategy 1: Priority keyword matching (highest weight)
        priority_tables = self.get_priority_tables(query)
        
        # Strategy 2: Fuzzy matching
        fuzzy_matches = self.fuzzy_match_tables(query, available_tables)
        
        # Strategy 3: Embedding results (existing system)
        embedding_tables = [(table[0], table[1]) for table in embedding_results]
        
        # Combine and weight the results
        final_ranking = {}
        
        # Priority tables get highest scores
        for table in priority_tables:
            # Check both bare table name and with schema prefix
            matching_tables = []
            
            # Check exact match
            if table in available_tables:
                matching_tables.append(table)
            
            # Check with public schema prefix
            public_table = f'public.{table}'
            if public_table in available_tables:
                matching_tables.append(public_table)
            
            # Check if any available table ends with this table name
            for available_table in available_tables:
                if available_table.endswith(f'.{table}'):
                    matching_tables.append(available_table)
            
            # Add all matching tables with highest priority
            for matching_table in matching_tables:
                final_ranking[matching_table] = final_ranking.get(matching_table, 0) + 1.0  # Highest weight
                
        # Fuzzy matches get medium scores
        for table, score in fuzzy_matches:
            final_ranking[table] = final_ranking.get(table, 0) + (score * 0.7)
        
        # Embedding matches get lower scores
        for table, score in embedding_tables:
            final_ranking[table] = final_ranking.get(table, 0) + (score * 0.3)
        
        # Convert to list and sort
        ranked_tables = [(table, score, "combined") for table, score in final_ranking.items()]
        ranked_tables.sort(key=lambda x: x[1], reverse=True)
        
        return ranked_tables[:8]  # Return top 8

def test_enhanced_mapping():
    """Test the enhanced mapping system"""
    mapper = EnhancedTableMapper()
    
    test_queries = [
        "show me the site visit details",
        "customer complaint data",
        "vehicle maintenance records", 
        "plant information",
        "site visit for complaint id 130"
    ]
    
    # Mock available tables (you'd get this from your schema)
    available_tables = [
        'crm_site_visit_dtls', 'customer_complaints', 'vehicle_master',
        'mega_trips', 'plant_schedule', 'veh_maintain', 'non_sales_history'
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        priority_tables = mapper.get_priority_tables(query)
        print(f"   Priority tables: {priority_tables}")
        
        # Mock embedding results (what current system returns)
        mock_embedding = [('non_sales_history', 0.7), ('mega_trips', 0.6)]
        
        ranked = mapper.rank_tables(query, mock_embedding, available_tables)
        print(f"   Final ranking: {ranked}")

if __name__ == "__main__":
    test_enhanced_mapping()

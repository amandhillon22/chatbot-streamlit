#!/usr/bin/env python3
"""Analyze why Gujarat query uses zone_master unnecessarily"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

from src.core.query_agent import english_to_sql

def analyze_gujarat_query():
    """Analyze the Gujarat query to understand why it uses zone_master"""
    print("🔍 Analyzing Gujarat Query Logic...")
    print("=" * 60)
    
    test_query = "show me plants in Gujarat"
    print(f"📋 Query: '{test_query}'")
    
    result = english_to_sql(test_query)
    sql_query = result.get('sql', '')
    
    print(f"\n🔍 Generated SQL:")
    print(sql_query)
    
    print(f"\n📊 Analysis:")
    
    # Check what tables are being used
    if 'zone_master' in sql_query:
        print("❓ QUESTION: Why is zone_master being used?")
        print("   Gujarat could be a state/district name, not necessarily a zone")
    
    if 'district_master' in sql_query:
        print("✅ GOOD: district_master is used (correct for regions/states)")
        
    if 'hosp_master' in sql_query:
        print("✅ GOOD: hosp_master is used (correct for plants)")
    
    # Check the WHERE clause
    if 'zm.zone_name' in sql_query:
        print("❓ ISSUE: Filtering by zone_name when Gujarat might be a district/state")
        print("   Should we check if Gujarat exists in district_master.name first?")
    
    print(f"\n🤔 Better approach might be:")
    print("1. First check if 'Gujarat' exists in district_master.name")
    print("2. Only use zone_master if it's actually a zone name")
    print("3. For this query, likely only need: hosp_master + district_master")
    
    # Test alternative query
    alternative_sql = """
    SELECT hm.name 
    FROM public.hosp_master hm 
    JOIN public.district_master dm ON hm.id_dist = dm.id_no 
    WHERE dm.name ILIKE '%Gujarat%' 
    LIMIT 50;
    """
    
    print(f"\n💡 Alternative SQL (without zone_master):")
    print(alternative_sql.strip())

if __name__ == "__main__":
    analyze_gujarat_query()

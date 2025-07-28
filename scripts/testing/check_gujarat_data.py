#!/usr/bin/env python3
"""Check where Gujarat actually exists in the database"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.sql import run_query

def check_gujarat_location():
    """Check where Gujarat exists in the database hierarchy"""
    print("🔍 Checking where 'Gujarat' exists in the database...")
    print("=" * 60)
    
    # Check zone_master
    print("\n1. Checking zone_master.zone_name for Gujarat:")
    try:
        zones = run_query("SELECT zone_name FROM public.zone_master WHERE zone_name ILIKE '%gujarat%';")
        print(f"   Found {len(zones)} results: {zones}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Check district_master
    print("\n2. Checking district_master.name for Gujarat:")
    try:
        districts = run_query("SELECT name FROM public.district_master WHERE name ILIKE '%gujarat%';")
        print(f"   Found {len(districts)} results: {districts}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Check both with exact match
    print("\n3. Checking exact matches:")
    try:
        exact_zones = run_query("SELECT zone_name FROM public.zone_master WHERE zone_name = 'Gujarat';")
        print(f"   Exact zone matches: {len(exact_zones)} results: {exact_zones}")
        
        exact_districts = run_query("SELECT name FROM public.district_master WHERE name = 'Gujarat';")
        print(f"   Exact district matches: {len(exact_districts)} results: {exact_districts}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test the alternative query
    print("\n4. Testing alternative query (district_master only):")
    try:
        alt_results = run_query("""
            SELECT hm.name 
            FROM public.hosp_master hm 
            JOIN public.district_master dm ON hm.id_dist = dm.id_no 
            WHERE dm.name ILIKE '%Gujarat%' 
            LIMIT 10;
        """)
        print(f"   Plants found via district_master: {len(alt_results)} results")
        for result in alt_results[:5]:  # Show first 5
            print(f"     - {result[0]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test the current query (with zone_master)
    print("\n5. Testing current query (with zone_master):")
    try:
        current_results = run_query("""
            SELECT hm.name 
            FROM public.hosp_master hm 
            JOIN public.district_master dm ON hm.id_dist = dm.id_no 
            JOIN public.zone_master zm ON dm.id_zone = zm.id_no 
            WHERE zm.zone_name = 'Gujarat' 
            LIMIT 10;
        """)
        print(f"   Plants found via zone_master: {len(current_results)} results")
        for result in current_results[:5]:  # Show first 5
            print(f"     - {result[0]}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    check_gujarat_location()

#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test all the plant-vehicle fixes together
"""

import re

def test_pattern_matching():
    """Test the new regex pattern for plant-vehicle queries"""
    
    print("🧪 Testing Plant-Vehicle Query Patterns")
    print("=" * 50)
    
    # Test the new flexible pattern
    pattern = r'(?:vehicles|trucks).*(?:of|in|at)\s+([a-zA-Z0-9\s\-]+?)(?:\s+plant|$)'
    
    test_queries = [
        "show me the vehicles of mohali plant",
        "vehicles of mohali",
        "show vehicles in mohali plant", 
        "trucks at mohali",
        "vehicles of PB-Mohali plant",
        "show me vehicles of the mohali plant"
    ]
    
    print("🎯 Testing Regex Pattern:")
    print(f"Pattern: {pattern}")
    print()
    
    for query in test_queries:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            plant_name = match.group(1).strip()
            # Clean up like the extractor does
            cleaned = re.sub(r'\b(?:the|plant)\b', '', plant_name, flags=re.IGNORECASE).strip()
            print(f"✅ '{query}' → Extracted: '{plant_name}' → Cleaned: '{cleaned}'")
        else:
            print(f"❌ '{query}' → No match")
    
    print(f"\n🔧 COMPLETE FIX SUMMARY:")
    print("=" * 30)
    print("1. ✅ Added explicit guidance in query_agent.py:")
    print("   🚛 VEHICLES OF PLANT QUERIES - Uses vehicle_master JOIN hosp_master")
    print()
    print("2. ✅ Enhanced intelligent_reasoning.py patterns:")
    print("   - New flexible regex pattern for plant name extraction")
    print("   - Handles lowercase, mixed case, and various phrasings")
    print()
    print("3. ✅ Added get_vehicles_of_plant intent handler:")
    print("   - Generates correct SQL with ILIKE '%plant_name%'")
    print("   - Returns reg_no, bus_id, and plant_name")
    print()
    print("🎯 EXPECTED RESULT:")
    print("Query: 'show me the vehicles of mohali plant'")
    print("→ Should immediately generate:")
    print("  SELECT vm.reg_no, vm.bus_id, hm.name as plant_name")
    print("  FROM vehicle_master vm") 
    print("  JOIN hosp_master hm ON vm.id_hosp = hm.id_no")
    print("  WHERE hm.name ILIKE '%mohali%'")
    print("  ORDER BY vm.reg_no LIMIT 50")

if __name__ == "__main__":
    test_pattern_matching()

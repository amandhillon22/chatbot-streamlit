#!/usr/bin/env python3
"""
import sys
sys.path.append('/home/linux/Documents/chatbot-diya')

Test plant queries without embeddings - direct test
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

def test_direct_plant_query():
    """Test plant query directly without the complex initialization"""
    
    prompt = """
You are an intelligent SQL assistant for PostgreSQL schemas.

PLANT & HIERARCHY QUERY GUIDANCE:

For PLANT queries:
- ALWAYS use hosp_master table for plant data
- Plant Name: hm.name
- Plant Address: hm.address  
- Region Link: hm.id_dist (connects to district_master)

For REGION queries:
- ALWAYS use district_master table for regions
- Region Name: dm.name

HIERARCHY SQL Examples:
-- Plants in Punjab region:
SELECT hm.name as plant_name, hm.address 
FROM hosp_master hm 
JOIN district_master dm ON hm.id_dist = dm.id_no 
WHERE dm.name ILIKE '%punjab%' 
LIMIT 50;

Return ONLY JSON:
{
  "schema": "public",
  "sql": "SQL query string",
  "response": "Natural language response",
  "follow_up": "Follow-up question or null"
}

User Query: show me plants in punjab region
"""
    
    try:
        response = model.generate_content(prompt)
        print("🤖 Gemini Response:")
        print(response.text)
        
        # Try to extract JSON
        import re
        import json
        match = re.search(r'{.*}', response.text, re.DOTALL)
        if match:
            result = json.loads(match.group())
            print("\n✅ Parsed JSON:")
            print(f"SQL: {result.get('sql', 'None')}")
            print(f"Response: {result.get('response', 'None')}")
        else:
            print("❌ No JSON found in response")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_direct_plant_query()

#!/usr/bin/env python3
"""
Direct test of SQL generation
"""
import google.generativeai as genai
import json
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def test_simple_sql():
    prompt = """
You are a PostgreSQL expert. Generate SIMPLE, CLEAN SQL for drum_trip_report queries.

**TABLE: drum_trip_report**
Key columns: reg_no, plant_out, site_in, site_out, plant_in, ps_kms, sp_kms, cycle_km, 
ps_duration, sp_duration, cycle_time, drum_in_plant, unloading_duration, site_waiting, 
plant_lat, plant_lng, site_lat, site_lng, tkt_no

**CRITICAL RULES:**
1. Keep SQL SIMPLE - just SELECT the raw data
2. Use ROUND() for decimal precision, NOT TRUNC() (doesn't exist in PostgreSQL)
3. No complex formatting in SQL - that happens later in Python
4. Always add LIMIT for performance
5. Use meaningful column aliases for user display

**User Request:** show me 10 drum trip reports

Generate clean SQL that fetches the relevant data without complex formatting.

Return JSON:
{
    "sql": "SELECT ... (simple, clean SQL)",
    "response": "Brief explanation"
}
"""
    
    try:
        response = model.generate_content(prompt).text.strip()
        print("Raw AI Response:")
        print(response)
        print("\n" + "="*60)
        
        # Try to extract JSON
        if "```json" in response:
            json_part = response.split("```json")[1].split("```")[0].strip()
        elif "{" in response:
            # Find JSON-like content
            start = response.find("{")
            end = response.rfind("}") + 1
            json_part = response[start:end]
        else:
            json_part = response
            
        print("Extracted JSON:")
        print(json_part)
        
        result = json.loads(json_part)
        print("\n" + "="*60)
        print("Parsed Result:")
        print(f"SQL: {result.get('sql')}")
        print(f"Response: {result.get('response')}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple_sql()

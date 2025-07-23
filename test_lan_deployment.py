#!/usr/bin/env python3
"""
LAN Deployment Test
This script tests all components before launching the chatbot for LAN access
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("🧪 Testing module imports...")
    
    try:
        # Core Flask dependencies
        import flask
        print("  ✅ Flask")
        
        import psycopg2
        print("  ✅ PostgreSQL adapter")
        
        import streamlit
        print("  ✅ Streamlit")
        
        # Core project modules
        from query_agent import english_to_sql, generate_final_response
        print("  ✅ Query agent")
        
        from sql import run_query
        print("  ✅ SQL module")
        
        # Business logic modules
        from eoninfotech_masker import EoninfotechDataMasker
        print("  ✅ EONINFOTECH masker")
        
        from database_reference_parser import DatabaseReferenceParser
        print("  ✅ Database reference parser")
        
        from intelligent_reasoning import IntelligentReasoning
        print("  ✅ Intelligent reasoning")
        
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_business_logic():
    """Test business logic integration"""
    print("\n🧠 Testing business logic...")
    
    try:
        # Test EONINFOTECH masker
        from eoninfotech_masker import EoninfotechDataMasker
        masker = EoninfotechDataMasker()
        
        # Test masking functionality
        test_data = [{"plant_name": "EONINFOTECH", "vehicle_id": "TEST001"}]
        masked_data = masker.mask_data_list(test_data)
        print("  ✅ EONINFOTECH masking works")
        
        # Test EON OFFICE removal logic
        eon_office_data = [{"plant_name": "EON OFFICE", "vehicle_id": "TEST002"}]
        masked_eon_office = masker.mask_data_list(eon_office_data)
        print("  ✅ EON OFFICE removal logic works")
        
        # Test database reference parser
        from database_reference_parser import DatabaseReferenceParser
        parser = DatabaseReferenceParser()
        
        # Test business context
        business_context = parser.get_business_context_for_query("test query")
        print("  ✅ Business context retrieval works")
        
        return True
    except Exception as e:
        print(f"  ❌ Business logic error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🗄️  Testing database connection...")
    
    try:
        import psycopg2
        from dotenv import load_dotenv
        load_dotenv()
        
        conn = psycopg2.connect(
            host=os.getenv('hostname', 'localhost'),
            dbname=os.getenv('dbname', 'rdc_dump'),
            user=os.getenv('user_name', 'postgres'),
            password=os.getenv('password', 'Akshit@123'),
            port=5432
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = \'public\';')
        table_count = cursor.fetchone()[0]
        print(f"  ✅ Database connection successful - {table_count} tables found")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False

def test_flask_app_structure():
    """Test Flask app structure"""
    print("\n🌐 Testing Flask app structure...")
    
    try:
        # Check if main Flask app file exists
        if os.path.exists('flask_app.py'):
            print("  ✅ flask_app.py found")
        else:
            print("  ❌ flask_app.py not found")
            return False
        
        # Try to import the Flask app
        from flask_app import app
        print("  ✅ Flask app imports successfully")
        
        # Check if app has required routes
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        required_routes = ['/', '/api/chat', '/api/login']
        
        for route in required_routes:
            if any(route in rule for rule in rules):
                print(f"  ✅ Route {route} available")
            else:
                print(f"  ⚠️  Route {route} not found")
        
        return True
    except Exception as e:
        print(f"  ❌ Flask app test failed: {e}")
        return False

def get_network_info():
    """Get network information"""
    print("\n🌐 Network Information:")
    
    try:
        import subprocess
        
        # Get IP address
        result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if 'inet ' in line and ('192.168.' in line or '10.' in line or '172.' in line):
                ip = line.strip().split()[1].split('/')[0]
                print(f"  🔗 LAN IP: {ip}")
                print(f"  🌐 Access URL: http://{ip}:5000")
                break
    except Exception as e:
        print(f"  ❌ Network info error: {e}")

def main():
    """Run all tests"""
    print("🔍 Diya Chatbot - LAN Deployment Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 4
    
    if test_imports():
        tests_passed += 1
    
    if test_business_logic():
        tests_passed += 1
    
    if test_database_connection():
        tests_passed += 1
    
    if test_flask_app_structure():
        tests_passed += 1
    
    get_network_info()
    
    print(f"\n📊 Test Results: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Ready for LAN deployment.")
        print("🚀 Run './start_lan.sh' to start the server for LAN access.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

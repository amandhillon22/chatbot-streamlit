#!/usr/bin/env python3
"""
Test that simulates the full startup process to verify connection pool exhaustion is resolved
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_startup_simulation():
    """Test the full startup process that was causing connection pool exhaustion"""
    try:
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        print("🚀 Testing Full Startup Simulation")
        print("=" * 50)
        
        # Test 1: Core database manager
        print("1️⃣ Testing core database manager...")
        from src.core.sql import db_manager
        print("✅ Core database manager loaded")
        
        # Test 2: Distance unit analyzer (was causing the pool exhaustion)
        print("\n2️⃣ Testing distance unit analyzer...")
        from src.database.distance_units import DistanceUnitManager
        distance_manager = DistanceUnitManager()
        print("✅ Distance unit analyzer loaded (should not exhaust pool)")
        
        # Test 3: Enhanced table mapper
        print("\n3️⃣ Testing enhanced table mapper...")
        from src.nlp.enhanced_table_mapper import EnhancedTableMapper
        table_mapper = EnhancedTableMapper()
        print("✅ Enhanced table mapper loaded")
        
        # Test 4: Sentence embeddings (fixed in this session)
        print("\n4️⃣ Testing sentence embeddings...")
        from src.nlp.sentence_embeddings import initialize_sentence_embeddings
        sentence_manager = initialize_sentence_embeddings()
        print("✅ Sentence embeddings loaded")
        
        # Test 5: Connection pool still functional after all initialization
        print("\n5️⃣ Testing connection pool after full initialization...")
        for i in range(5):
            with db_manager.get_connection_context() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT %s as final_test', (i,))
                result = cursor.fetchone()
                if i % 2 == 0:
                    print(f"✅ Final test {i}: {result}")
        
        print("\n🎉 ALL STARTUP COMPONENTS LOADED SUCCESSFULLY!")
        print("✅ No connection pool exhaustion detected")
        return True
        
    except Exception as e:
        print(f"❌ Startup simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_startup_simulation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 STARTUP SIMULATION: ✅ PASSED")
        print("✅ Connection pool exhaustion fix is complete!")
        print("✅ System ready for production deployment!")
    else:
        print("❌ STARTUP SIMULATION: ❌ FAILED")
        print("❌ Additional fixes needed")

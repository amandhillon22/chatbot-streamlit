#!/usr/bin/env python3
"""
Test CRM Complaint System Integration
Verifies that the CRM complaint tracking system is properly integrated
"""

import os
import sys
import json
from database_reference_parser import DatabaseReferenceParser

def test_crm_keywords():
    """Test if CRM complaint keywords are properly integrated"""
    parser = DatabaseReferenceParser()
    
    # Check if CRM-related keywords exist
    keywords = parser._load_transportation_keywords()
    
    # Check for complaint keywords
    assert 'complaint' in keywords, "Complaint keyword missing"
    assert 'crm' in keywords, "CRM keyword missing"
    assert 'site_visit' in keywords, "Site visit keyword missing"
    assert 'feedback' in keywords, "Feedback keyword missing"
    
    # Check if the right tables are associated
    assert 'crm_complaint_dtls' in keywords['complaint'], "crm_complaint_dtls missing from complaint keyword"
    assert 'crm_complaint_category' in keywords['complaint'], "crm_complaint_category missing from complaint keyword"
    assert 'crm_site_visit_dtls' in keywords['site_visit'], "crm_site_visit_dtls missing from site_visit keyword"
    assert 'customer_ship_details' in keywords['customer'], "customer_ship_details missing from customer keyword"
    
    print("✅ CRM complaint keywords are properly integrated")
    return True

def test_crm_tables_relationship():
    """Test if CRM complaint tables relationships are properly defined"""
    parser = DatabaseReferenceParser()
    
    # Test relationships for crm_complaint_dtls
    complaint_rels = parser._infer_relationships('crm_complaint_dtls')
    
    # Check if required relationships exist
    assert 'customer_ship_details' in complaint_rels, "customer_ship_details relationship missing"
    assert 'crm_complaint_category' in complaint_rels, "crm_complaint_category relationship missing"
    assert 'crm_site_visit_dtls' in complaint_rels, "crm_site_visit_dtls relationship missing"
    
    # Test relationships for customer_ship_details
    ship_rels = parser._infer_relationships('customer_ship_details')
    assert 'ship_to_address' in ship_rels, "ship_to_address relationship missing"
    assert 'crm_complaint_dtls' in ship_rels, "crm_complaint_dtls relationship missing"
    
    # Test relationships for crm_site_visit_dtls
    visit_rels = parser._infer_relationships('crm_site_visit_dtls')
    assert 'crm_complaint_dtls' in visit_rels, "crm_complaint_dtls relationship missing"
    assert 'customer_ship_details' in visit_rels, "customer_ship_details relationship missing"
    
    print("✅ CRM complaint table relationships are properly defined")
    return True

def test_crm_business_context():
    """Test if CRM complaint business context is properly defined"""
    parser = DatabaseReferenceParser()
    
    # Test business context for crm_complaint_dtls
    complaint_context = parser._infer_business_context('crm_complaint_dtls')
    assert "complaint" in complaint_context.lower(), "Complaint context missing from crm_complaint_dtls"
    
    # Test business context for crm_site_visit_dtls
    visit_context = parser._infer_business_context('crm_site_visit_dtls')
    assert "site visit" in visit_context.lower(), "Site visit context missing from crm_site_visit_dtls"
    
    # Test business context for customer_ship_details
    ship_context = parser._infer_business_context('customer_ship_details')
    assert "shipping" in ship_context.lower(), "Shipping context missing from customer_ship_details"
    
    print("✅ CRM complaint business context is properly defined")
    return True

def test_query_resolution():
    """Test if CRM complaint queries can be properly resolved"""
    parser = DatabaseReferenceParser()
    
    # Test query about complaints
    complaint_query = "Show all customer complaints"
    relevant_tables = parser.get_business_relevant_tables(complaint_query)
    
    assert 'crm_complaint_dtls' in relevant_tables, "crm_complaint_dtls missing from complaint query"
    
    # Test query about site visits
    visit_query = "List recent site visits for complaints"
    relevant_tables = parser.get_business_relevant_tables(visit_query)
    
    assert 'crm_site_visit_dtls' in relevant_tables, "crm_site_visit_dtls missing from site visit query"
    
    # Test query about shipping addresses
    ship_query = "Show customer shipping information"
    relevant_tables = parser.get_business_relevant_tables(ship_query)
    
    assert any('ship' in table for table in relevant_tables), "Shipping tables missing from shipping query"
    
    print("✅ CRM complaint queries can be properly resolved")
    return True

def main():
    """Run all tests"""
    print("🧪 Testing CRM Complaint System Integration")
    print("=" * 50)
    
    test_functions = [
        test_crm_keywords,
        test_crm_tables_relationship,
        test_crm_business_context,
        test_query_resolution
    ]
    
    passed = 0
    for test_func in test_functions:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"❌ {test_func.__name__} failed: {e}")
        except Exception as e:
            print(f"❌ {test_func.__name__} error: {e}")
    
    print(f"📊 Test results: {passed}/{len(test_functions)} tests passed")
    
    if passed == len(test_functions):
        print("🎉 All tests passed! CRM complaint system is fully integrated.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

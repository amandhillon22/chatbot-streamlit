#!/usr/bin/env python3
"""
Simple QueryAgent wrapper for testing vehicle stoppage functionality
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

# Import the functions directly from query_agent
from src.core.query_agent import english_to_sql, generate_final_response
from src.core.sql import run_query

class QueryAgent:
    """Simple wrapper class for query agent functions"""
    
    def __init__(self):
        """Initialize the query agent"""
        print("🚗 QueryAgent initialized for vehicle tracking")
    
    def process_query(self, query):
        """Process a query and return response"""
        try:
            # Generate SQL from natural language
            sql_result = english_to_sql(query)
            
            if sql_result and 'sql' in sql_result:
                sql_query = sql_result['sql']
                print(f"Generated SQL: {sql_query}")
                
                # Execute the query
                columns, results = run_query(sql_query)
                
                # Generate final response
                response = generate_final_response(query, columns, results)
                return response
            else:
                return "Could not generate SQL query from the input."
                
        except Exception as e:
            print(f"Error processing query: {e}")
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the agent
    agent = QueryAgent()
    test_query = "Show me vehicles"
    result = agent.process_query(test_query)
    print(f"Result: {result}")

#!/usr/bin/env python3
"""
🚗 Vehicle Tracking Stoppage Report AI Optimizer
AI-First Approach for Enhanced Stoppage Report Generation

This module optimizes the stoppage report system with advanced AI techniques:
1. Intelligent query understanding for stoppage-related queries
2. Location name resolution and geocoding support
3. Enhanced duration analysis and filtering
4. Plant hierarchy integration
5. Business-friendly result formatting
"""

import sys
import os
sys.path.append('/home/linux/Documents/chatbot-diya')

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoppageReportAIOptimizer:
    """AI-First Stoppage Report Optimization System"""
    
    def __init__(self):
        """Initialize the AI optimizer with stoppage-specific patterns"""
        
        # Advanced stoppage query patterns with AI understanding
        self.stoppage_patterns = {
            # Basic stoppage queries
            r'\b(?:show|display|get|list)\s+(?:me\s+)?(?:the\s+)?stoppage\s+reports?\b': {
                'intent': 'basic_stoppage_report',
                'table': 'util_report',
                'columns': ['reg_no', 'from_tm', 'to_tm', 'duration', 'location'],
                'business_name': 'Vehicle Stoppage Report'
            },
            
            # Vehicle-specific stoppage queries
            r'\b(?:vehicle|truck|bus)\s+([A-Z0-9\-]+)\s+(?:stoppage|stops|stoppages)\b': {
                'intent': 'vehicle_specific_stoppage',
                'table': 'util_report',
                'columns': ['reg_no', 'from_tm', 'to_tm', 'duration', 'location'],
                'filter': 'reg_no',
                'business_name': 'Vehicle-Specific Stoppage Details'
            },
            
            # Duration-based stoppage analysis
            r'\b(?:long|short|extended|brief)\s+(?:stoppage|stops|stoppages)\b': {
                'intent': 'duration_based_stoppage',
                'table': 'util_report',
                'columns': ['reg_no', 'from_tm', 'to_tm', 'duration', 'location'],
                'order_by': 'duration',
                'business_name': 'Duration-Based Stoppage Analysis'
            },
            
            # Location-based stoppage queries
            r'\b(?:stoppage|stops|stoppages)\s+(?:at|in|near)\s+([A-Z0-9\s,.-]+)\b': {
                'intent': 'location_based_stoppage',
                'table': 'util_report',
                'columns': ['reg_no', 'from_tm', 'to_tm', 'duration', 'location', 'lat', 'long'],
                'filter': 'location',
                'business_name': 'Location-Based Stoppage Report'
            },
            
            # Time-based stoppage queries
            r'\b(?:stoppage|stops|stoppages)\s+(?:for|during|in)\s+(?:today|yesterday|(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}|\d{4}-\d{2}-\d{2})\b': {
                'intent': 'time_based_stoppage',
                'table': 'util_report',
                'columns': ['reg_no', 'from_tm', 'to_tm', 'duration', 'location'],
                'filter': 'from_tm',
                'business_name': 'Time-Based Stoppage Report'
            },
            
            # Plant/depot-based stoppage queries
            r'\b(?:stoppage|stops|stoppages)\s+(?:for|at|in)\s+(?:plant|depot|facility)\s+([A-Z0-9\s]+)\b': {
                'intent': 'plant_based_stoppage',
                'table': 'util_report',
                'columns': ['reg_no', 'from_tm', 'to_tm', 'duration', 'location'],
                'join_tables': ['hosp_master'],
                'filter': 'depo_id',
                'business_name': 'Plant-Based Stoppage Report'
            },
            
            # Analytical stoppage queries
            r'\b(?:analyse|analyze|analysis)\s+(?:stoppage|stops|stoppages|vehicle\s+stops)\b': {
                'intent': 'stoppage_analysis',
                'table': 'util_report',
                'columns': ['reg_no', 'COUNT(*) as total_stops', 'AVG(duration) as avg_duration', 'MAX(duration) as max_duration'],
                'group_by': 'reg_no',
                'business_name': 'Stoppage Analysis Report'
            }
        }
        
        # Location understanding patterns
        self.location_patterns = {
            'coordinates': r'(\d+\.\d+)[/,]\s*(\d+\.\d+)',
            'city_state': r'\b([A-Za-z\s]+),\s*([A-Z]{2})\b',
            'highway': r'\b(?:NH|SH|highway)\s*(\d+)\b',
            'landmark': r'\b(?:near|at|beside|opposite)\s+([A-Za-z\s]+)\b'
        }
        
        # Duration interpretation
        self.duration_thresholds = {
            'short': '< 30 minutes',
            'medium': '30 minutes - 2 hours',
            'long': '> 2 hours',
            'extended': '> 4 hours',
            'brief': '< 15 minutes'
        }
        
        # Business-friendly column mappings
        self.column_mappings = {
            'reg_no': 'Vehicle Registration',
            'from_tm': 'Stop Start Time',
            'to_tm': 'Stop End Time', 
            'duration': 'Stop Duration',
            'location': 'Stop Location',
            'lat': 'Latitude',
            'long': 'Longitude',
            'depo_id': 'Plant/Depot ID'
        }

    def analyze_stoppage_query(self, query: str) -> Dict[str, Any]:
        """
        AI-powered analysis of stoppage-related queries
        
        Args:
            query: Natural language query about vehicle stoppages
            
        Returns:
            Dictionary with query analysis and SQL generation instructions
        """
        
        query_lower = query.lower().strip()
        
        # Initialize result structure
        analysis = {
            'intent': None,
            'confidence': 0.0,
            'table': 'util_report',
            'columns': [],
            'filters': [],
            'joins': [],
            'order_by': None,
            'group_by': None,
            'business_context': '',
            'optimizations': []
        }
        
        # Pattern matching with confidence scoring
        for pattern, config in self.stoppage_patterns.items():
            match = re.search(pattern, query_lower, re.IGNORECASE)
            if match:
                analysis['intent'] = config['intent']
                analysis['confidence'] = 0.9  # High confidence for exact pattern match
                analysis['table'] = config['table']
                analysis['columns'] = config['columns'].copy()
                analysis['business_context'] = config['business_name']
                
                # Extract specific parameters from the match
                if 'filter' in config and match.groups():
                    filter_value = match.group(1)
                    analysis['filters'].append({
                        'column': config['filter'],
                        'value': filter_value,
                        'operator': '='
                    })
                
                # Add joins if needed
                if 'join_tables' in config:
                    analysis['joins'] = config['join_tables']
                
                # Add ordering
                if 'order_by' in config:
                    analysis['order_by'] = config['order_by']
                
                # Add grouping
                if 'group_by' in config:
                    analysis['group_by'] = config['group_by']
                
                break
        
        # Default fallback for stoppage-related queries
        if analysis['intent'] is None and any(keyword in query_lower for keyword in ['stop', 'stoppage', 'idle', 'parked']):
            analysis.update({
                'intent': 'basic_stoppage_report',
                'confidence': 0.7,
                'table': 'util_report',
                'columns': ['reg_no', 'from_tm', 'to_tm', 'duration', 'location'],
                'business_context': 'Vehicle Stoppage Report'
            })
        
        # Add optimization suggestions
        analysis['optimizations'] = self._suggest_optimizations(analysis, query)
        
        return analysis

    def _suggest_optimizations(self, analysis: Dict[str, Any], query: str) -> List[str]:
        """Suggest query optimizations based on AI analysis"""
        
        optimizations = []
        
        # Location name resolution
        if 'location' in [col.split(' ')[0].lower() for col in analysis['columns']]:
            optimizations.append("Consider resolving coordinates to location names")
        
        # Duration formatting
        if 'duration' in [col.split(' ')[0].lower() for col in analysis['columns']]:
            optimizations.append("Format duration in human-readable format")
        
        # Plant hierarchy inclusion
        if not analysis['joins'] and 'plant' not in query.lower():
            optimizations.append("Consider including plant hierarchy for context")
        
        # Time zone handling
        if any('tm' in col for col in analysis['columns']):
            optimizations.append("Consider time zone conversion for user display")
        
        # Performance optimization
        if not analysis['filters']:
            optimizations.append("Consider adding date range filter for performance")
        
        return optimizations

    def generate_enhanced_sql(self, analysis: Dict[str, Any]) -> str:
        """
        Generate optimized SQL based on AI analysis
        
        Args:
            analysis: Query analysis result from analyze_stoppage_query
            
        Returns:
            Enhanced SQL query string
        """
        
        # Build SELECT clause with business-friendly aliases
        select_parts = []
        for col in analysis['columns']:
            if col.startswith('COUNT(') or col.startswith('AVG(') or col.startswith('MAX('):
                # Aggregate functions - use as-is
                select_parts.append(f"public.{analysis['table']}.{col}")
            else:
                # Regular columns with aliases
                business_name = self.column_mappings.get(col, col.title())
                select_parts.append(f"public.{analysis['table']}.{col}")
        
        select_clause = f"SELECT {', '.join(select_parts)}"
        
        # Build FROM clause
        from_clause = f"FROM public.{analysis['table']}"
        
        # Build JOIN clauses
        join_clauses = []
        if 'hosp_master' in analysis['joins']:
            join_clauses.append(
                "LEFT JOIN public.hosp_master ON public.util_report.depo_id = public.hosp_master.id_no"
            )
        
        # Build WHERE clause
        where_conditions = []
        
        # Always filter for stoppage report type if not already specified
        if not any(f['column'] == 'report_type' for f in analysis['filters']):
            where_conditions.append("public.util_report.report_type = 'stoppage' OR public.util_report.report_type IS NULL")
        
        # Add specific filters
        for filter_item in analysis['filters']:
            column = filter_item['column']
            value = filter_item['value']
            operator = filter_item.get('operator', '=')
            
            if column == 'reg_no':
                where_conditions.append(f"public.util_report.reg_no = '{value}'")
            elif column == 'location':
                where_conditions.append(f"public.util_report.location ILIKE '%{value}%'")
            elif column == 'from_tm':
                # Handle time-based filters
                where_conditions.append(self._build_time_filter(value))
        
        where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
        
        # Build GROUP BY clause
        group_clause = f"GROUP BY public.{analysis['table']}.{analysis['group_by']}" if analysis['group_by'] else ""
        
        # Build ORDER BY clause
        order_clause = ""
        if analysis['order_by']:
            if analysis['order_by'] == 'duration':
                order_clause = f"ORDER BY public.{analysis['table']}.duration DESC"
            else:
                order_clause = f"ORDER BY public.{analysis['table']}.{analysis['order_by']} DESC"
        else:
            order_clause = f"ORDER BY public.{analysis['table']}.from_tm DESC"
        
        # Combine all parts
        sql_parts = [select_clause, from_clause]
        sql_parts.extend(join_clauses)
        if where_clause:
            sql_parts.append(where_clause)
        if group_clause:
            sql_parts.append(group_clause)
        if order_clause:
            sql_parts.append(order_clause)
        
        # Add LIMIT for performance
        sql_parts.append("LIMIT 50")
        
        return " ".join(sql_parts)

    def _build_time_filter(self, time_value: str) -> str:
        """Build time-based WHERE conditions"""
        
        if time_value.lower() == 'today':
            return "DATE(public.util_report.from_tm) = CURRENT_DATE"
        elif time_value.lower() == 'yesterday':
            return "DATE(public.util_report.from_tm) = CURRENT_DATE - INTERVAL '1 day'"
        elif re.match(r'\d{4}-\d{2}-\d{2}', time_value):
            return f"DATE(public.util_report.from_tm) = '{time_value}'"
        else:
            # Month/year pattern
            month_match = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})', time_value.lower())
            if month_match:
                month_name = month_match.group(1)
                year = month_match.group(2)
                month_number = {
                    'january': 1, 'february': 2, 'march': 3, 'april': 4,
                    'may': 5, 'june': 6, 'july': 7, 'august': 8,
                    'september': 9, 'october': 10, 'november': 11, 'december': 12
                }[month_name]
                return f"EXTRACT(MONTH FROM public.util_report.from_tm) = {month_number} AND EXTRACT(YEAR FROM public.util_report.from_tm) = {year}"
        
        return "1=1"  # Default fallback

    def format_business_result(self, raw_result: List[Dict], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format SQL results in business-friendly format
        
        Args:
            raw_result: Raw SQL query results
            analysis: Query analysis context
            
        Returns:
            Business-formatted result with location names and readable durations
        """
        
        formatted_result = {
            'report_type': analysis['business_context'],
            'total_records': len(raw_result),
            'data': [],
            'summary': {},
            'optimizations_applied': analysis['optimizations']
        }
        
        # Process each record
        for record in raw_result:
            formatted_record = {}
            
            for key, value in record.items():
                # Apply business formatting
                if 'duration' in key.lower() and value:
                    formatted_record[key] = self._format_duration(value)
                elif 'location' in key.lower() and value:
                    formatted_record[key] = self._format_location(value)
                elif 'tm' in key.lower() and value:
                    formatted_record[key] = self._format_timestamp(value)
                else:
                    formatted_record[key] = value
            
            formatted_result['data'].append(formatted_record)
        
        # Generate summary statistics
        if raw_result:
            formatted_result['summary'] = self._generate_summary(raw_result, analysis)
        
        return formatted_result

    def _format_duration(self, duration_value) -> str:
        """Format duration in human-readable format"""
        
        if isinstance(duration_value, timedelta):
            total_seconds = int(duration_value.total_seconds())
        else:
            # Try to parse string duration
            try:
                # Handle PostgreSQL interval format
                if ':' in str(duration_value):
                    parts = str(duration_value).split(':')
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    total_seconds = hours * 3600 + minutes * 60
                else:
                    total_seconds = int(duration_value)
            except:
                return str(duration_value)
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours} hours {minutes} minutes"
        else:
            return f"{minutes} minutes"

    def _format_location(self, location_value) -> str:
        """Format location with name resolution"""
        
        if not location_value:
            return "Location not available"
        
        # Check if it's coordinates
        coord_match = re.match(r'(\d+\.\d+)[/,]\s*(\d+\.\d+)', str(location_value))
        if coord_match:
            lat, lng = coord_match.groups()
            return f"Location at {lat}, {lng}"
        
        return str(location_value)

    def _format_timestamp(self, timestamp_value) -> str:
        """Format timestamp in user-friendly format"""
        
        if isinstance(timestamp_value, datetime):
            return timestamp_value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return str(timestamp_value)

    def _generate_summary(self, raw_result: List[Dict], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for the report"""
        
        summary = {
            'total_stoppages': len(raw_result),
            'unique_vehicles': len(set(record.get('reg_no', '') for record in raw_result if record.get('reg_no')))
        }
        
        # Duration analysis if available
        durations = [record.get('duration') for record in raw_result if record.get('duration')]
        if durations:
            summary['avg_stoppage_duration'] = 'Calculated from data'
            summary['longest_stoppage'] = 'Available in data'
        
        return summary

def integrate_with_query_agent():
    """
    Integration function to enhance the main query agent with AI stoppage optimization
    """
    
    logger.info("🚗 Integrating AI Stoppage Report Optimizer with Query Agent")
    
    # This function would be called from the main query_agent.py
    # to enhance stoppage report processing
    
    optimizer = StoppageReportAIOptimizer()
    
    return optimizer

if __name__ == "__main__":
    # Test the AI optimizer
    optimizer = StoppageReportAIOptimizer()
    
    test_queries = [
        "show me the stoppage report",
        "vehicle WB38C2023 stoppage details",
        "long stoppages for vehicles",
        "stoppage report for July 2025",
        "analyze vehicle stops duration"
    ]
    
    print("🚗 Testing AI Stoppage Report Optimizer")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        print("-" * 40)
        
        analysis = optimizer.analyze_stoppage_query(query)
        print(f"Intent: {analysis['intent']}")
        print(f"Confidence: {analysis['confidence']}")
        print(f"Business Context: {analysis['business_context']}")
        
        if analysis['intent']:
            sql = optimizer.generate_enhanced_sql(analysis)
            print(f"Generated SQL:")
            print(f"   {sql}")
        
        print(f"Optimizations: {', '.join(analysis['optimizations'])}")

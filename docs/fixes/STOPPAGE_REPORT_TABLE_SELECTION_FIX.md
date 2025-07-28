# Stoppage Report Table Selection Fix Summary

## Problem Identified
The query for "show me the stoppage report for the month of july 2025" was incorrectly generating:
```sql
SELECT MIN(public.driver_stop_report.date_time) AS earliest_date, MAX(public.driver_stop_report.date_time) AS latest_date FROM public.driver_stop_report;
```

Instead of the correct query:
```sql
SELECT public.util_report.reg_no, public.util_report.location, public.util_report.from_tm, public.util_report.to_tm, public.util_report.duration FROM public.util_report WHERE EXTRACT(MONTH FROM public.util_report.from_tm) = 7 AND EXTRACT(YEAR FROM public.util_report.from_tm) = 2025 LIMIT 50;
```

## Root Cause
The enhanced table mapping system was incorrectly suggesting `driver_stop_report` instead of the correct `util_report` table for vehicle stoppage queries.

## Solutions Implemented

### 1. Added Explicit Stoppage Report Guidance
Added specific guidance in multiple places in the query prompt:

**In Table Meanings Section:**
- Added `util_report`: VEHICLE STOPPAGE/UTILIZATION REPORTS - Use for all stoppage queries (NOT driver_stop_report)

**In Query Interpretation Rules:**
- Added "Stoppage report" → SELECT FROM util_report (NOT driver_stop_report!)
- Added "Vehicle stoppage" → SELECT FROM util_report WHERE reg_no conditions
- Added "NEVER use driver_stop_report for vehicle stoppage queries"

**In Hierarchical Guidance:**
- Added comprehensive stoppage report section with regex pattern matching
- Pattern: `r'\b(stoppage|util_report|stop|idle|parked)\b'`
- Explicit examples showing correct util_report usage
- Clear warnings against using driver_stop_report

### 2. Fixed JSON Serialization
Also fixed the `datetime.time` serialization issue in `generate_final_response()` by adding proper handling for time objects:

```python
elif isinstance(val, datetime.time):
    # Handle datetime.time objects (like duration columns)
    hours = val.hour
    minutes = val.minute
    seconds = val.second
    if hours > 0:
        row_dict[col] = f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        row_dict[col] = f"{minutes}m {seconds}s"
    else:
        row_dict[col] = f"{seconds}s"
```

## Expected Outcome
- "Stoppage report" queries should now correctly use the `util_report` table
- JSON serialization errors for time objects should be resolved
- The system should generate the correct SQL query for stoppage reports

## Testing
The Flask server has been restarted with the updated code. Test the same query:
"show me the stoppage report for the month of july 2025"

Expected SQL output:
```sql
SELECT public.util_report.reg_no, public.util_report.location, public.util_report.from_tm, public.util_report.to_tm, public.util_report.duration FROM public.util_report WHERE EXTRACT(MONTH FROM public.util_report.from_tm) = 7 AND EXTRACT(YEAR FROM public.util_report.from_tm) = 2025 LIMIT 50;
```

## Files Modified
- `/home/linux/Documents/chatbot-diya/src/core/query_agent.py`
  - Added stoppage report table guidance
  - Fixed datetime.time JSON serialization
  - Enhanced prompt with explicit table selection rules

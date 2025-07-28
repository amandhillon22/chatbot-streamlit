# Vehicle Tracking Report System Enhancement

## 🚗 Vehicle Tracking Dataset Optimization

This document outlines the implementation of a comprehensive vehicle tracking report system supporting four main report types:

1. **Overspeeding Report**
2. **Distance Report** 
3. **Stoppage Report**
4. **Trip Report**

## 📊 Stoppage Report Implementation

### Table: `util_report`

The `util_report` table stores stoppage data for vehicles during their journeys.

#### Column Specifications:

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `id_no` | integer | Primary key, auto-increment |
| `reg_no` | character varying(50) | Vehicle registration number |
| `from_tm` | timestamp without time zone | Start time of the stop |
| `to_tm` | timestamp without time zone | End time of the stop |
| `location` | text | Formatted as "latitude/longitude" |
| `lat` | numeric(10,8) | Latitude coordinate |
| `long` | numeric(11,8) | Longitude coordinate |
| `duration` | interval | Duration of the stop |
| `depo_id` | integer | References hosp_master.id_no (plant/depot info) |
| `report_type` | character varying(20) | Type of report ('stoppage', 'overspeeding', 'distance', 'trip') |
| `created_at` | timestamp without time zone | Record creation timestamp |

#### Relationships:
- `util_report.depo_id` → `hosp_master.id_no` (Plant/Depot information)
- `hosp_master.id_dist` → `district_master.id_no` (Regional hierarchy)
- `district_master.id_zone` → `zone_master.id_no` (Zone hierarchy)

#### Business Logic:
- Location data available in two formats: combined (`location` column) and separate (`lat`, `long` columns)
- Duration shows time period of vehicle stops
- Connection to plant hierarchy through `depo_id` for regional reporting
- Location names should be displayed to users (not raw coordinates)

### SQL Examples:

#### Basic Stoppage Report:
```sql
SELECT 
    ur.reg_no,
    ur.from_tm,
    ur.to_tm,
    ur.duration,
    hm.name as plant_name,
    dm.name as region_name
FROM util_report ur
LEFT JOIN hosp_master hm ON ur.depo_id = hm.id_no
LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
WHERE ur.report_type = 'stoppage'
ORDER BY ur.from_tm DESC;
```

#### Stoppage Report with Location Resolution:
```sql
SELECT 
    ur.reg_no,
    ur.from_tm,
    ur.to_tm,
    ur.duration,
    -- Convert coordinates to location name (placeholder for geocoding)
    CASE 
        WHEN ur.location IS NOT NULL THEN 'Location at ' || ur.location
        WHEN ur.lat IS NOT NULL AND ur.long IS NOT NULL THEN 'Location at ' || ur.lat || ',' || ur.long
        ELSE 'Location not available'
    END as stop_location,
    hm.name as plant_name,
    dm.name as region_name
FROM util_report ur
LEFT JOIN hosp_master hm ON ur.depo_id = hm.id_no
LEFT JOIN district_master dm ON hm.id_dist = dm.id_no
WHERE ur.report_type = 'stoppage'
ORDER BY ur.from_tm DESC;
```

## 🎯 Implementation Notes:

1. **Location Display**: Always show location names to users, never raw coordinates
2. **Duration Format**: Present duration in human-readable format (e.g., "2 hours 30 minutes")
3. **Hierarchical Context**: Include plant and region information for business context
4. **Time Formatting**: Display timestamps in user-friendly format
5. **Filtering Options**: Support filtering by vehicle, date range, duration, and location

## 🚀 Next Steps:

This implementation provides the foundation for stoppage report queries. The system will be enhanced to:
- Parse natural language queries about vehicle stops
- Generate appropriate SQL queries with location resolution
- Present results in business-friendly format
- Support filtering and aggregation operations

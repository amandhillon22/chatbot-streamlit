## 🗂️ Table: `crm_complaint_category`

**📊 Rows:** 2

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| category | character varying | YES |
| status | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `crm_complaint_category_pkey`: CREATE UNIQUE INDEX crm_complaint_category_pkey ON public.crm_complaint_category USING btree (id_no)

### 📝 Description
Contains complaint categories for the Customer Relationship Management system. This is the parent table for complaint categorization.

## 🗂️ Table: `crm_complaint_category_type`

**📊 Rows:** 22

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| category_id | integer | NO |
| category_type | character varying | YES |
| status | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- category_id → crm_complaint_category.id_no (Parent complaint category)

### 🧭 Indexes
- `crm_complaint_category_type_pkey`: CREATE UNIQUE INDEX crm_complaint_category_type_pkey ON public.crm_complaint_category_type USING btree (id_no)

### 📝 Description
Contains specific types of complaints under each category. This is a child table of crm_complaint_category that allows for sub-categorization of complaints.

## 🗂️ Table: `crm_complaint_dtls`

**📊 Rows:** 100

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_name | character varying | YES |
| cust_id | integer | YES |
| site_id | integer | YES |
| complaint_date | date | YES |
| contact_name | character varying | YES |
| designation | character varying | YES |
| contact_no | bigint | YES |
| complaint_category_id | integer | YES |
| complaint_type_id | integer | YES |
| description | text | YES |
| complaint_raised_by | character varying | YES |
| complaint_raised_at | timestamp without time zone | YES |
| pour_date | date | YES |
| concrete_grade | integer | YES |
| pour_volume | double precision | YES |
| plant_id | integer | YES |
| customer_email | text | YES |
| active_status | character varying | YES |
| complaint_deleted_by | character varying | YES |
| complaint_deleted_at | timestamp without time zone | YES |
| complaint_deleted_by_role | character varying | YES |
| complaint_updated_at | timestamp without time zone | YES |
| complaint_updated_by | character varying | YES |
| comp_image | text | YES |
| comp_image_1 | text | YES |
| comp_image_2 | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- cust_id, site_id → customer_ship_details.customer_id, customer_ship_details.site_id (Customer and site information)
- complaint_category_id → crm_complaint_category.id_no (Complaint category)
- complaint_type_id → crm_complaint_category_type.id_no (Complaint type)
- plant_id → hosp_master.id_no (Plant/facility details)

### 🧭 Indexes
- `crm_complaint_dtls_pkey`: CREATE UNIQUE INDEX crm_complaint_dtls_pkey ON public.crm_complaint_dtls USING btree (id_no)

### 📝 Description
The main complaint tracking table that contains all details about customer complaints. It links customers, sites, complaint categories, and types to track and manage customer issues effectively.

## 🗂️ Table: `crm_site_visit_dtls`

**📊 Rows:** 90

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_id | integer | YES |
| cust_id | integer | YES |
| site_id | integer | YES |
| date_of_visit | date | YES |
| contact_no | character varying | YES |
| liability | double precision | YES |
| reason_for_visit | text | YES |
| supply_date | date | YES |
| concrete_grade | integer | YES |
| pour_volume | bigint | YES |
| supply_plant | integer | YES |
| site_visit_by | character varying | YES |
| feedback | text | YES |
| site_image | text | YES |
| site_image_1 | text | YES |
| site_image_2 | text | YES |
| rca_image | text | YES |
| time_stamp | timestamp without time zone | YES |
| created_by | character varying | YES |
| product_correction | character varying | YES |
| correction_image | text | YES |
| complaint_id | integer | YES |
| third_party_testing | character varying | YES |
| test_status | character varying | YES |
| liability_amount | double precision | YES |
| test_image | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- complaint_id → crm_complaint_dtls.id_no (Associated complaint)
- cust_id, site_id → customer_ship_details.customer_id, customer_ship_details.site_id (Customer and site information)
- plant_id → hosp_master.id_no (Plant/facility details)

### 🧭 Indexes
- `crm_site_visit_dtls_pkey`: CREATE UNIQUE INDEX crm_site_visit_dtls_pkey ON public.crm_site_visit_dtls USING btree (id_no)

### 📝 Description
Contains site visit details related to customer complaints. This table tracks visits to customer sites for complaint resolution, including feedback, images, and resolution status.

## 🗂️ Table: `customer_ship_details`

**📊 Rows:** 61274

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_id | integer | NO |
| customer_name | character varying | YES |
| ship_to_id | integer | NO |
| ship_to_address | text | YES |
| ship_to_pincode | integer | YES |
| ship_to_state | character varying | YES |
| ship_to_gst | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| salesrep_id | character varying | YES |

### 🔐 Primary Keys
- customer_id, ship_to_id

### 🔗 Foreign Keys
- ship_to_id → ship_to_address.ship_to_id (Shipping address details)

### 🧭 Indexes
- `customer_ship_details_pkey`: CREATE UNIQUE INDEX customer_ship_details_pkey ON public.customer_ship_details USING btree (customer_id, ship_to_id)
- `csh1`: CREATE INDEX csh1 ON public.customer_ship_details USING btree (customer_id)

### 📝 Description
Contains customer shipping information, linking customers to their shipping addresses. This table is referenced by the CRM complaint system to track customer-related complaints.

## 🗂️ Table: `ship_to_address`

**📊 Rows:** Unknown

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| ship_to_id | integer | NO |
| address_line1 | character varying | YES |
| address_line2 | character varying | YES |
| city | character varying | YES |
| state | character varying | YES |
| pincode | integer | YES |
| country | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- ship_to_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `ship_to_address_pkey`: CREATE UNIQUE INDEX ship_to_address_pkey ON public.ship_to_address USING btree (ship_to_id)

### 📝 Description
Contains detailed shipping address information referenced by customer_ship_details. This table stores the physical locations for customer shipments and site visits.

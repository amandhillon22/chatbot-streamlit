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
The `ship_to_address` table contains customer shipping addresses referenced by `customer_ship_details.ship_to_id`.

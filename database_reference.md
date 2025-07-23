# 📘 PostgreSQL Database Documentation (With Full Data)

## 🗂️ Table: `adv_assignment`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_id | integer | NO |
| adv_id | integer | NO |
| adv_enable | character | YES |
| adv_priority | integer | YES |
| send_flag | character | YES |

### 🔐 Primary Keys
- box_id, adv_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_adv_assignment`: CREATE UNIQUE INDEX pk_adv_assignment ON public.adv_assignment USING btree (box_id, adv_id)
## 🗂️ Table: `adv_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| advertisement | text | YES |
| eng_name | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_adv_master`: CREATE UNIQUE INDEX pk_adv_master ON public.adv_master USING btree (id_no)
## 🗂️ Table: `ain_data`

**📊 Rows:** 39

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_id | integer | NO |
| ain_ref | real | YES |
| ain_0_c | character varying | YES |
| ain_0_m | real | YES |
| ain_0_vdio | real | YES |
| ain_1_c | character varying | YES |
| ain_1_m | real | YES |
| ain_1_vdio | real | YES |
| remarks | text | YES |
| box_sno | integer | YES |
| ain_2_c | character varying | YES |
| ain_2_m | real | YES |
| ain_2_vdio | real | YES |
| ain_3_c | character varying | YES |
| ain_3_m | real | YES |
| ain_3_vdio | real | YES |

### 🔐 Primary Keys
- box_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `ain_data_pkey`: CREATE UNIQUE INDEX ain_data_pkey ON public.ain_data USING btree (box_id)
## 🗂️ Table: `alarm2veh`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| alarm2veh_id | integer | NO |
| alarm2veh_alarm_trigger_id | integer | YES |
| reg_no | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `alarm_trigger`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| alarm_id | integer | NO |
| alarm_a2v_id | integer | YES |

### 🔐 Primary Keys
- alarm_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `alarm_trigger_pkey`: CREATE UNIQUE INDEX alarm_trigger_pkey ON public.alarm_trigger USING btree (alarm_id)
## 🗂️ Table: `alert_ign`

**📊 Rows:** 21464

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | YES |
| latitude | double precision | YES |
| longitude | double precision | YES |
| addrs | text | YES |
| date_time | timestamp without time zone | YES |
| status | character varying | YES |
| speed | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `ai1`: CREATE INDEX ai1 ON public.alert_ign USING btree (reg_no)
- `ai2`: CREATE INDEX ai2 ON public.alert_ign USING btree (date_time)
## 🗂️ Table: `all_eta_string`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_id | integer | YES |
| stop_id | integer | YES |
| fe_string | text | YES |
| disp_string | text | YES |
| genration_time_stamp | timestamp without time zone | YES |
| transmision_time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `api_limit`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| api_code | character varying | YES |
| cur_limit | integer | YES |
| max_limit | integer | YES |
| time_stamp | timestamp without time zone | YES |
| ip_allowed | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `app_customers`

**📊 Rows:** 1458

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| cust_id | character varying | YES |
| type | integer | YES |
| plant_id | integer | YES |
| name | character varying | YES |
| contact | bigint | YES |
| email | character varying | YES |
| id_proof | text | YES |
| address | text | YES |
| city | character varying | YES |
| state | character varying | YES |
| pincode | integer | YES |
| address_proof | text | YES |
| gst_registration | character varying | YES |
| gst_no | character varying | YES |
| gst_proof | text | YES |
| status | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `app_customers_pkey`: CREATE UNIQUE INDEX app_customers_pkey ON public.app_customers USING btree (id)
## 🗂️ Table: `app_orders`

**📊 Rows:** 94812

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| cust_id | integer | YES |
| site | character varying | YES |
| site_id | integer | YES |
| site_name | character varying | YES |
| address | text | YES |
| city | character varying | YES |
| state | character varying | YES |
| pincode | integer | YES |
| sch_date | date | YES |
| sch_time | time without time zone | YES |
| grade | character varying | YES |
| quantity | double precision | YES |
| pump | character varying | YES |
| status | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| remarks | text | YES |
| grade2 | character varying | YES |
| quantity2 | double precision | YES |
| pump2 | character varying | YES |
| structure | character varying | YES |
| pour_rate | double precision | YES |
| structure2 | character varying | YES |
| pour_rate2 | double precision | YES |
| fd_status | character | YES |
| acc_status | text | YES |
| schd_timestamp | timestamp without time zone | YES |
| order_placed_by | text | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `app_orders_pkey`: CREATE UNIQUE INDEX app_orders_pkey ON public.app_orders USING btree (id)
- `app1`: CREATE INDEX app1 ON public.app_orders USING btree (cust_id)
- `app11`: CREATE INDEX app11 ON public.app_orders USING btree (sch_date)
## 🗂️ Table: `app_regions`

**📊 Rows:** 19

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| region_name | character varying | YES |
| employee_name | character varying | YES |
| contact_no | character varying | YES |
| email_id | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `app_regions_pkey`: CREATE UNIQUE INDEX app_regions_pkey ON public.app_regions USING btree (id)
## 🗂️ Table: `assign_alert_info`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| rt_id | integer | NO |
| alert_sno | integer | NO |
| stop_id | integer | YES |
| stop_type | character | YES |
| refer_id | bigint | YES |
| conv_lat | double precision | YES |
| conv_long | double precision | YES |
| assign_ts | timestamp without time zone | YES |
| assigned | character | YES |
| ack_ts | timestamp without time zone | YES |
| err_code | ARRAY | YES |
| remarks | text | YES |
| alert_type_id | integer | YES |
| wnd_m | integer | YES |

### 🔐 Primary Keys
- rt_id, alert_sno

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `assign_alert_info_pkey`: CREATE UNIQUE INDEX assign_alert_info_pkey ON public.assign_alert_info USING btree (rt_id, alert_sno)
- `assign_alert_info_rt_id_alert_sno_idx`: CREATE INDEX assign_alert_info_rt_id_alert_sno_idx ON public.assign_alert_info USING btree (rt_id, alert_sno)
## 🗂️ Table: `assign_geoz`

**📊 Rows:** 36883

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | NO |
| geoz_id | integer | NO |
| geoz_sno | integer | NO |
| status | "char" | YES |
| assigned_ts | timestamp without time zone | YES |
| ack_ts | timestamp without time zone | YES |
| err_code | character varying | YES |
| remarks | character varying | YES |

### 🔐 Primary Keys
- bus_id, geoz_id, geoz_sno

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `assign_geo_pkey`: CREATE UNIQUE INDEX assign_geo_pkey ON public.assign_geoz USING btree (bus_id, geoz_id, geoz_sno)
- `assign_geoz_bus_id_geoz_sno_key`: CREATE UNIQUE INDEX assign_geoz_bus_id_geoz_sno_key ON public.assign_geoz USING btree (bus_id, geoz_sno)
- `ndx_assign_geoz_bus_id_sno`: CREATE INDEX ndx_assign_geoz_bus_id_sno ON public.assign_geoz USING btree (bus_id, geoz_sno)
## 🗂️ Table: `assign_plant`

**📊 Rows:** 85

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| user_id | integer | YES |
| id_no | integer | NO |
| region_id | text | YES |
| plantid | text | YES |
| zone_id | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `attd_logs`

**📊 Rows:** 5595

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| time_stamp | timestamp without time zone | YES |
| status | character varying | YES |
| inout | character varying | YES |
| data_cnt | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `attd_master`

**📊 Rows:** 18

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| image_link | character varying | YES |
| fse_name | character varying | NO |
| plant_id | integer | YES |
| time_in | timestamp without time zone | YES |
| time_out | timestamp without time zone | YES |
| date_entry | date | NO |
| lati_in | double precision | YES |
| longi_in | double precision | YES |
| lati_out | double precision | YES |
| longi_out | double precision | YES |
| in_addr | text | YES |
| out_addr | text | YES |

### 🔐 Primary Keys
- fse_name, date_entry

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `attd_master_pkey`: CREATE UNIQUE INDEX attd_master_pkey ON public.attd_master USING btree (date_entry, fse_name)
## 🗂️ Table: `auto_fuel_add`

**📊 Rows:** 5251

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| reg_no | character varying | YES |
| plant_name | integer | YES |
| fuel_added | double precision | YES |
| from_date | timestamp without time zone | YES |
| latitude | double precision | YES |
| longitude | double precision | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `auto_mileage_add_pkey`: CREATE UNIQUE INDEX auto_mileage_add_pkey ON public.auto_fuel_add USING btree (id)
## 🗂️ Table: `auto_fuel_theft`

**📊 Rows:** 14996

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| reg_no | character varying | YES |
| plant_name | integer | YES |
| from_date | timestamp without time zone | YES |
| latitude | double precision | YES |
| longitude | double precision | YES |
| fuel_before_drop | double precision | YES |
| fuel_after_drop | double precision | YES |
| drop_difference | double precision | YES |
| status | character | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `auto_mileage_theft_pkey`: CREATE UNIQUE INDEX auto_mileage_theft_pkey ON public.auto_fuel_theft USING btree (id)
## 🗂️ Table: `available_seats`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| etm_id | integer | NO |
| bus_id | integer | NO |
| regn_no | character varying | YES |
| stop_id | integer | NO |
| stop_name | character varying | YES |
| total_seats | integer | YES |
| seats_available | integer | YES |
| etm_time_stamp | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- etm_id, bus_id, stop_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_etm_table`: CREATE UNIQUE INDEX pk_etm_table ON public.available_seats USING btree (bus_id, stop_id, etm_id)
## 🗂️ Table: `battery_sms_update`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| regno | character varying | NO |
| battery | character varying | YES |
| update_battery | integer | YES |
| date_time | timestamp without time zone | YES |
| hosp_name | character varying | YES |

### 🔐 Primary Keys
- regno

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `battery_sms_update_pkey`: CREATE UNIQUE INDEX battery_sms_update_pkey ON public.battery_sms_update USING btree (regno)
## 🗂️ Table: `bdown_reason`

**📊 Rows:** 14

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| bd_reason | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `bdown_reason_pkey`: CREATE UNIQUE INDEX bdown_reason_pkey ON public.bdown_reason USING btree (id_no)
## 🗂️ Table: `bill_manage`

**📊 Rows:** 6357

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| bill_date | date | YES |
| region_id | integer | YES |
| region_name | character varying | YES |
| plant_id | integer | YES |
| plant_name | character varying | YES |
| bus_id | integer | YES |
| reg_no | character varying | YES |
| installed_date | date | YES |
| drs_status | character varying | YES |
| billing_days | integer | YES |
| rate | double precision | YES |
| shifting_remarks | text | YES |
| flag | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| type | character varying | YES |
| veh_type | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `billing_cycle`

**📊 Rows:** 13

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| billing_cycle | character varying | YES |
| from_month_day | character varying | YES |
| to_month_day | character varying | YES |
| chkdate | date | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `billing_cycle_pkey`: CREATE UNIQUE INDEX billing_cycle_pkey ON public.billing_cycle USING btree (id_no)
## 🗂️ Table: `bookmark`

**📊 Rows:** 84

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| username | character varying | YES |
| id_dist | integer | YES |
| reg_no | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `bookmark_pkey`: CREATE UNIQUE INDEX bookmark_pkey ON public.bookmark USING btree (id)
## 🗂️ Table: `bth_master`

**📊 Rows:** 139

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| bth_name | character varying | NO |
| bth_email | text | YES |
| bth_no | character varying | YES |
| plant_id | integer | NO |

### 🔐 Primary Keys
- bth_name, plant_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `bth_master_pkey`: CREATE UNIQUE INDEX bth_master_pkey ON public.bth_master USING btree (bth_name, plant_id)
## 🗂️ Table: `bulker_trip_report`

**📊 Rows:** 4060

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| depo_id | integer | YES |
| plant_out | timestamp without time zone | NO |
| site_in | timestamp without time zone | YES |
| ps_duration | time without time zone | YES |
| ps_kms | double precision | YES |
| ps_max_speed | double precision | YES |
| ps_avg_speed | double precision | YES |
| unloading_time | text | YES |
| unloading_duration | time without time zone | YES |
| site_waiting | time without time zone | YES |
| site_out | timestamp without time zone | YES |
| plant_in | timestamp without time zone | YES |
| sp_duration | time without time zone | YES |
| sp_kms | double precision | YES |
| sp_max_speed | double precision | YES |
| sp_avg_speed | double precision | YES |
| plant_lat | character varying | YES |
| plant_lng | character varying | YES |
| site_lat | character varying | YES |
| site_lng | character varying | YES |
| cycle_km | double precision | YES |
| cycle_time | time without time zone | YES |
| tkt_no | integer | YES |

### 🔐 Primary Keys
- reg_no, plant_out

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `bulker_trip_report_pkey`: CREATE UNIQUE INDEX bulker_trip_report_pkey ON public.bulker_trip_report USING btree (reg_no, plant_out)
## 🗂️ Table: `bus_configuration`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| veh_view_time | integer | YES |
| min_stoppage_time | integer | YES |
| min_speed | integer | YES |
| min_disconnect_time | integer | YES |
| speed_violation | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `bus_rt_status`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| status | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `busid_ts`: CREATE INDEX busid_ts ON public.bus_rt_status USING btree (bus_id, time_stamp)
## 🗂️ Table: `chat_messages`

**📊 Rows:** 40

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| session_id | integer | YES |
| message_type | character varying | NO |
| content | text | NO |
| sql_query | text | YES |
| created_at | timestamp without time zone | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- `session_id` → `chat_sessions.id`

### 🧭 Indexes
- `chat_messages_pkey`: CREATE UNIQUE INDEX chat_messages_pkey ON public.chat_messages USING btree (id)
- `idx_chat_messages_session_id`: CREATE INDEX idx_chat_messages_session_id ON public.chat_messages USING btree (session_id)
## 🗂️ Table: `chat_sessions`

**📊 Rows:** 3

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| user_id | integer | YES |
| session_id | character varying | NO |
| title | character varying | YES |
| created_at | timestamp without time zone | YES |
| updated_at | timestamp without time zone | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- `user_id` → `users.id`

### 🧭 Indexes
- `chat_sessions_pkey`: CREATE UNIQUE INDEX chat_sessions_pkey ON public.chat_sessions USING btree (id)
- `chat_sessions_session_id_key`: CREATE UNIQUE INDEX chat_sessions_session_id_key ON public.chat_sessions USING btree (session_id)
- `idx_chat_sessions_user_id`: CREATE INDEX idx_chat_sessions_user_id ON public.chat_sessions USING btree (user_id)
- `idx_chat_sessions_created_at`: CREATE INDEX idx_chat_sessions_created_at ON public.chat_sessions USING btree (created_at DESC)
## 🗂️ Table: `checkdpr`

**📊 Rows:** 541125

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| stringval | text | YES |
| time_stamp | timestamp without time zone | YES |
| challanno | text | YES |
| invoicedate | date | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `checker_master`

**📊 Rows:** 21

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| checker_name | character varying | YES |
| checker_email | text | YES |
| checker_no | character varying | YES |
| id_dist | integer | YES |
| assign_cfo_status | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `checkpoint_master`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | character varying | YES |
| s_lat | double precision | YES |
| s_long | double precision | YES |
| covt_lat | double precision | YES |
| covt_long | double precision | YES |
| remarks | text | YES |
| window_range | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `refer_master_pkey`: CREATE UNIQUE INDEX refer_master_pkey ON public.checkpoint_master USING btree (id_no)
- `id_no3`: CREATE INDEX id_no3 ON public.checkpoint_master USING btree (id_no)
## 🗂️ Table: `child_menu`

**📊 Rows:** 120

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| menu_id | integer | YES |
| sub_menu_id | integer | YES |
| child_menu | character | YES |
| child_menu_url | character | YES |
| status | integer | YES |
| create_date | date | YES |
| update_date | date | YES |
| id | integer | NO |
| order_no | integer | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `child_menu_pkey`: CREATE UNIQUE INDEX child_menu_pkey ON public.child_menu USING btree (id)
## 🗂️ Table: `cluster_master`

**📊 Rows:** 4

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| cluster_name | character varying | YES |
| cluster_code | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `comp_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| site_name | character varying | YES |
| covt_lat | character varying | YES |
| covt_long | character varying | YES |
| capacity | character varying | YES |
| tm_no | integer | YES |
| pump_no | integer | YES |
| mon_qty | character varying | YES |
| company | integer | NO |
| remarks | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `comp_master_pkey`: CREATE UNIQUE INDEX comp_master_pkey ON public.comp_master USING btree (id_no)
## 🗂️ Table: `conductor_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | bigint | NO |
| first_name | character varying | NO |
| last_name | character varying | NO |
| father_name | character varying | YES |
| dt_of_birth | date | YES |
| dt_of_joining | date | YES |
| gender | character varying | YES |
| blood | character varying | YES |
| street1 | character varying | YES |
| street2 | character varying | YES |
| city | character varying | YES |
| state | character varying | YES |
| zip | character varying | YES |
| telephone | character varying | YES |
| lic_no | character varying | YES |
| lic_issue | character varying | YES |
| lic_date | date | YES |
| lic_exp | date | YES |
| lic_token | character varying | YES |
| acc_no | character varying | YES |
| ret_dead | character varying | YES |
| c_code | text | YES |
| id_depo | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `conductor_main_pkey`: CREATE UNIQUE INDEX conductor_main_pkey ON public.conductor_master USING btree (id_no)
## 🗂️ Table: `consig_master`

**📊 Rows:** 32079

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| consig_id_no | bigint | NO |
| cust_no | character varying | YES |
| name | character varying | YES |
| city | character varying | YES |
| region | character varying | YES |
| consig_conv_lat | double precision | YES |
| consig_conv_long | double precision | YES |
| loc_time_stamp | timestamp without time zone | YES |
| remarks | text | YES |

### 🔐 Primary Keys
- consig_id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `consig_master_cust_no_key`: CREATE UNIQUE INDEX consig_master_cust_no_key ON public.consig_master USING btree (cust_no)
- `consig_master_pkey`: CREATE UNIQUE INDEX consig_master_pkey ON public.consig_master USING btree (consig_id_no)
## 🗂️ Table: `console_login`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| ip_addr | character varying | YES |
| time | timestamp without time zone | YES |
| users | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `control_station_config`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| port_number | integer | YES |
| ip_addr | inet | YES |
| configuration_delay | integer | YES |
| status | character varying | YES |
| xxx_allowed | integer | YES |
| data_timer | integer | YES |
| id_no | integer | NO |
| eta_limit | integer | YES |
| w_msg_eng | text | YES |
| w_msg_reg | text | YES |
| latest_eta_time_sec | integer | YES |
| ota_file_format | character varying | YES |
| ota_directory_loc | character varying | YES |
| etd_limit | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_contol_station_config`: CREATE UNIQUE INDEX pk_contol_station_config ON public.control_station_config USING btree (id_no)
## 🗂️ Table: `credit_inv_detail`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| invoice_no | character varying | YES |
| credit_note | character varying | YES |
| credit_date | character varying | YES |
| credit_qty | double precision | YES |
| comments | text | YES |
| reason_code | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `credit_limit`

**📊 Rows:** 34408

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_code | integer | YES |
| payment_term | integer | YES |
| credit_limit | double precision | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `credit_limit_pkey`: CREATE UNIQUE INDEX credit_limit_pkey ON public.credit_limit USING btree (id_no)
## 🗂️ Table: `crm_blocked_users`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| cust_id | integer | YES |
| blocked_by | character varying | YES |
| blocked_at | timestamp without time zone | YES |
| complaint_id | integer | YES |
| unblocked_at | timestamp without time zone | YES |
| status | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `crm_blocked_users_pkey`: CREATE UNIQUE INDEX crm_blocked_users_pkey ON public.crm_blocked_users USING btree (id_no)
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
- None

### 🧭 Indexes
- `crm_complaint_category_type_pkey`: CREATE UNIQUE INDEX crm_complaint_category_type_pkey ON public.crm_complaint_category_type USING btree (id_no)
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
- None

### 🧭 Indexes
- `crm_complaint_dtls_pkey`: CREATE UNIQUE INDEX crm_complaint_dtls_pkey ON public.crm_complaint_dtls USING btree (id_no)
## 🗂️ Table: `crm_complaint_work_status_logs`

**📊 Rows:** 8

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| complaint_id | integer | YES |
| work_status | text | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `crm_complaint_work_status_logs_pkey`: CREATE UNIQUE INDEX crm_complaint_work_status_logs_pkey ON public.crm_complaint_work_status_logs USING btree (id_no)
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
| test_approved_by | character varying | YES |
| complaint_status | character varying | YES |
| final_approved_liablilty | double precision | YES |
| bh_approved_liability | double precision | YES |
| bh_action_at | timestamp without time zone | YES |
| bh_action_by | character varying | YES |
| bh_remarks | text | YES |
| bh_action_status | character varying | YES |
| bh_action_remarks | text | YES |
| test_action_at | timestamp without time zone | YES |
| th_approved_liability | double precision | YES |
| th_action_status | character varying | YES |
| th_action_at | timestamp without time zone | YES |
| th_action_by | character varying | YES |
| th_remarks | text | YES |
| th_action_remarks | text | YES |
| cf_approved_liability | double precision | YES |
| cf_action_status | character varying | YES |
| cf_action_at | timestamp without time zone | YES |
| cf_action_by | character varying | YES |
| md_approved_liability | double precision | YES |
| md_action_status | character varying | YES |
| md_action_at | timestamp without time zone | YES |
| md_action_by | character varying | YES |
| md_remarks | text | YES |
| md_action_remarks | text | YES |
| cf_remarks | text | YES |
| cf_action_remarks | text | YES |
| acct_approved_liability | double precision | YES |
| acct_action_status | character varying | YES |
| acct_action_at | timestamp without time zone | YES |
| acct_action_by | character varying | YES |
| acct_remarks | text | YES |
| acct_action_remarks | text | YES |
| correction_description | text | YES |
| execution_remarks | text | YES |
| exec_pdf_q1 | text | YES |
| exec_pdf_q2 | text | YES |
| exec_pdf_q3 | text | YES |
| exec_done_at | timestamp without time zone | YES |
| exec_done_by | character varying | YES |
| ho_qc_action_at | timestamp without time zone | YES |
| ho_qc_action_by | character varying | YES |
| rca_submission_by | text | YES |
| rca_submit_at | timestamp without time zone | YES |
| ho_qc_remarks | text | YES |
| ho_qc_action_status | character varying | YES |
| correction_done_at | timestamp without time zone | YES |
| correction_done_by | character varying | YES |
| customer_user_name | text | YES |
| outstanding_amt | double precision | YES |
| exec_repair_cost_1 | double precision | YES |
| exec_methodology_1 | text | YES |
| exec_repair_cost_2 | double precision | YES |
| exec_methodology_2 | text | YES |
| exec_repair_cost_3 | double precision | YES |
| exec_methodology_3 | text | YES |
| exec_vendor_name_1 | character varying | YES |
| exec_vendor_name_2 | character varying | YES |
| exec_vendor_name_3 | character varying | YES |
| exec_pdf_m1 | text | YES |
| exec_pdf_m2 | text | YES |
| exec_pdf_m3 | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `crm_site_visit_dtls_pkey`: CREATE UNIQUE INDEX crm_site_visit_dtls_pkey ON public.crm_site_visit_dtls USING btree (id_no)
## 🗂️ Table: `cro_master`

**📊 Rows:** 1172

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| cro_name | character varying | NO |
| cro_email | text | YES |
| cro_no | character varying | YES |
| plant_id | integer | NO |
| cro_desg | character varying | YES |

### 🔐 Primary Keys
- cro_name, plant_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `cro_master_pkey`: CREATE UNIQUE INDEX cro_master_pkey ON public.cro_master USING btree (cro_name, plant_id)
## 🗂️ Table: `cur_trip_report`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | NO |
| total_time_taken | integer | YES |
| total_distance_travelled | integer | YES |
| maximum_speed | integer | YES |
| number_of_match | integer | YES |
| referral_ids | character varying | YES |
| start_time | timestamp without time zone | NO |
| end_time | timestamp without time zone | YES |
| id_route | integer | YES |
| time_stamp | timestamp without time zone | YES |
| rs_string | character varying | YES |
| repo_string | character varying | YES |
| remarks | text | YES |
| reg_no | character varying | NO |

### 🔐 Primary Keys
- start_time, reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `cur_trip_report_pkey`: CREATE UNIQUE INDEX cur_trip_report_pkey ON public.cur_trip_report USING btree (reg_no, start_time)
- `cur_date6`: CREATE INDEX cur_date6 ON public.cur_trip_report USING btree (bus_id, start_time)
- `cur_trip2`: CREATE INDEX cur_trip2 ON public.cur_trip_report USING btree (reg_no)
## 🗂️ Table: `customer_bill_details`

**📊 Rows:** 41072

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_id | integer | YES |
| bill_to_id | integer | YES |
| bill_to_address | text | YES |
| bill_to_state | character varying | YES |
| salesrep_id | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| bill_to_pincode | integer | YES |
| bill_to_gst | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `customer_bill_details_customer_id_bill_to_id_key`: CREATE UNIQUE INDEX customer_bill_details_customer_id_bill_to_id_key ON public.customer_bill_details USING btree (customer_id, bill_to_id)
- `customer_bill_details_pkey`: CREATE UNIQUE INDEX customer_bill_details_pkey ON public.customer_bill_details USING btree (id_no)
- `cbl1`: CREATE INDEX cbl1 ON public.customer_bill_details USING btree (customer_id)
## 🗂️ Table: `customer_connect_login_status`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| user_name | text | NO |
| reg_no | character varying | YES |
| login_status | character varying | NO |
| login_time | timestamp without time zone | YES |
| logout_time | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |
| user_login_token | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `customer_connect_login_status_pkey`: CREATE UNIQUE INDEX customer_connect_login_status_pkey ON public.customer_connect_login_status USING btree (id_no)
## 🗂️ Table: `customer_connect_logs`

**📊 Rows:** 83791

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| username | character varying | YES |
| login_time | timestamp without time zone | YES |
| ver_no | character varying | YES |
| cust_id | integer | YES |
| cust_name | character varying | YES |
| plant_id | integer | YES |
| tag | character varying | YES |
| imeino | character varying | YES |
| deviceid | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `customer_connect_user_tokens`

**📊 Rows:** 65779

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| username | character varying | NO |
| auth_token | text | NO |
| refresh_token | text | NO |
| expiry_time | timestamp without time zone | NO |
| time_stamp | timestamp without time zone | NO |
| version | character varying | NO |
| cust_id | integer | YES |
| last_update_refresh | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `customer_connect_user_tokens_pkey`: CREATE UNIQUE INDEX customer_connect_user_tokens_pkey ON public.customer_connect_user_tokens USING btree (id_no)
## 🗂️ Table: `customer_detail`

**📊 Rows:** 1259457

**👥 Business Context:** Customer detail table - bottom level in the organizational hierarchy. Contains detailed customer visit records, linking to both sites and plants. This is the transactional level where actual business activities are recorded.

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| cust_type | integer | YES |
| cust_id | integer | YES |
| project_name | character varying | YES |
| site_id | integer | YES |
| visit_purpose | integer | YES |
| dt_of_visit | timestamp without time zone | YES |
| dist_visit | double precision | YES |
| segment_id | integer | YES |
| grade | character varying | YES |
| duration | integer | YES |
| mix_type | character varying | YES |
| current_supplier | character varying | YES |
| created_by | character varying | YES |
| insert_ts | timestamp without time zone | YES |
| requirement | character varying | YES |
| lati | double precision | YES |
| longi | double precision | YES |
| loc_addr | text | YES |
| outcome | integer | YES |
| next_visit | date | YES |
| total_require | text | YES |
| cont_name | character varying | YES |
| cont_no | character varying | YES |
| cont_email | character varying | YES |
| cust_type_other | character varying | YES |
| purpose_of_visit_other | character varying | YES |
| segment_other | character varying | YES |
| outcome_other | character varying | YES |
| fse_id | integer | YES |
| plant_id | integer | YES |
| dist_calc | double precision | YES |
| payment_status | character varying | YES |
| payment_issue | character varying | YES |
| written_issue | text | YES |
| image | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys (Hierarchical Parents)
- site_id → site_master.id_no (Parent site location)
- plant_id → hosp_master.id_no (Parent plant)
- cust_id → [Customer master reference]

### 🧭 Indexes
- `customer_detail_pkey`: CREATE UNIQUE INDEX customer_detail_pkey ON public.customer_detail USING btree (id_no)
- `cd1`: CREATE INDEX cd1 ON public.customer_detail USING btree (created_by)
- `cd2`: CREATE INDEX cd2 ON public.customer_detail USING btree (cust_id)
- `cd3`: CREATE INDEX cd3 ON public.customer_detail USING btree (site_id)
- `cd4`: CREATE INDEX cd4 ON public.customer_detail USING btree (dt_of_visit)
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
- None

### 🧭 Indexes
- `customer_ship_details_pkey`: CREATE UNIQUE INDEX customer_ship_details_pkey ON public.customer_ship_details USING btree (customer_id, ship_to_id)
- `csh1`: CREATE INDEX csh1 ON public.customer_ship_details USING btree (customer_id)
## 🗂️ Table: `customer_type`

**📊 Rows:** 6

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| cust_type | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `customer_type_pkey`: CREATE UNIQUE INDEX customer_type_pkey ON public.customer_type USING btree (id_no)
## 🗂️ Table: `customer_user`

**📊 Rows:** 1047

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| username | character varying | YES |
| password | character varying | YES |
| designation | character varying | YES |
| mobile_no | character varying | YES |
| email_id | character varying | YES |
| customer_id | integer | YES |
| full_name | character varying | YES |
| status | character | YES |
| otp_code | character varying | YES |
| plant_id | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `customer_user_email_id_key`: CREATE UNIQUE INDEX customer_user_email_id_key ON public.customer_user USING btree (email_id)
- `customer_user_mobile_no_key`: CREATE UNIQUE INDEX customer_user_mobile_no_key ON public.customer_user USING btree (mobile_no)
- `customer_user_pkey`: CREATE UNIQUE INDEX customer_user_pkey ON public.customer_user USING btree (id_no)
- `customer_user_username_key`: CREATE UNIQUE INDEX customer_user_username_key ON public.customer_user USING btree (username)
## 🗂️ Table: `customer_user_deleted`

**📊 Rows:** 21

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| username | character varying | YES |
| password | character varying | YES |
| designation | character varying | YES |
| mobile_no | character varying | YES |
| email_id | character varying | YES |
| customer_id | integer | YES |
| full_name | character varying | YES |
| status | character | YES |
| otp_code | character varying | YES |
| plant_id | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `daily_dist`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| reg_no | character varying | NO |
| dist_calc | bigint | YES |
| last_calc_ts | timestamp without time zone | YES |

### 🔐 Primary Keys
- reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `daily_dist_pkey`: CREATE UNIQUE INDEX daily_dist_pkey ON public.daily_dist USING btree (reg_no)
## 🗂️ Table: `daily_report`

**📊 Rows:** 7318

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| bus_id | integer | YES |
| reg_no | character varying | NO |
| depo_id | integer | YES |
| date_time | timestamp without time zone | NO |
| insert_date_time | timestamp without time zone | YES |
| lat | numeric | YES |
| lon | numeric | YES |
| distance_m | integer | YES |
| ign_on_mins | integer | YES |
| idle_ign_on_mins | integer | YES |
| veh_moving_mins | integer | YES |
| drum_cw_mins | integer | YES |
| drum_ccw_mins | integer | YES |
| drum_cw_cnt | integer | YES |
| drum_ccw_cnt | integer | YES |
| imsi_1 | character varying | YES |
| imsi_2 | character varying | YES |
| remarks | character varying | YES |

### 🔐 Primary Keys
- reg_no, date_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `daily_report_pkey`: CREATE UNIQUE INDEX daily_report_pkey ON public.daily_report USING btree (reg_no, date_time)
## 🗂️ Table: `databasechangelog`

**📊 Rows:** 28

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | character varying | NO |
| author | character varying | NO |
| filename | character varying | NO |
| dateexecuted | timestamp without time zone | NO |
| orderexecuted | integer | NO |
| exectype | character varying | NO |
| md5sum | character varying | YES |
| description | character varying | YES |
| comments | character varying | YES |
| tag | character varying | YES |
| liquibase | character varying | YES |
| contexts | character varying | YES |
| labels | character varying | YES |
| deployment_id | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `databasechangeloglock`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| locked | boolean | NO |
| lockgranted | timestamp without time zone | YES |
| lockedby | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `databasechangeloglock_pkey`: CREATE UNIQUE INDEX databasechangeloglock_pkey ON public.databasechangeloglock USING btree (id)
## 🗂️ Table: `depo_stop_relation`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| depo_id | integer | YES |
| stop_id | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `descriptor_table`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| descriptor_no | bigint | YES |
| ip_address | inet | YES |
| time_of_connectivity | timestamp without time zone | YES |
| type | character varying | YES |
| bus_id | integer | YES |
| thread_id | bigint | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `device_master`

**📊 Rows:** 4

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| description | character varying | YES |
| part_no | character varying | YES |
| remarks | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `display_ip_table`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| ip_address | character varying | YES |
| interface_name | character varying | YES |
| memory_total | bigint | YES |
| memory_used | double precision | YES |
| memory_free | double precision | YES |
| cpu_used | double precision | YES |
| time_stamp | timestamp without time zone | YES |
| connected_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `distance_modify`

**📊 Rows:** 28730

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| site_id | integer | YES |
| ear_distance | double precision | YES |
| mod_distance | double precision | YES |
| time_stamp | timestamp without time zone | YES |
| created_by | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `distance_report`

**📊 Rows:** 2185376

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| amb_id | integer | NO |
| from_tm | timestamp without time zone | NO |
| to_tm | timestamp without time zone | YES |
| distance | integer | YES |
| reg_no | character varying | YES |
| drum_rotation | integer | YES |

### 🔐 Primary Keys
- amb_id, from_tm

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `distance_report_pkey`: CREATE UNIQUE INDEX distance_report_pkey ON public.distance_report USING btree (amb_id, from_tm)
- `id`: CREATE UNIQUE INDEX id ON public.distance_report USING btree (amb_id, from_tm)
## 🗂️ Table: `district_master`

**📊 Rows:** 34

**🏢 Business Context:** District/Region master table - second level in the organizational hierarchy (Zone → District → Plant → Vehicle). Contains district/region information and links to parent zones. Each district contains multiple plants.

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | character varying | YES |
| address | text | YES |
| user_code | character varying | YES |
| login_id | character varying | YES |
| common_email | text | YES |
| id_zone | integer | YES |
| remarks | text | YES |
| contact_no | character varying | YES |
| email_id | text | YES |
| cont_no | character varying | YES |
| bill_status | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys (Hierarchical Parents)
- id_zone → zone_master.id_no (Parent zone)

### 🔗 Referenced By (Hierarchical Children)
- hosp_master.id_dist → district_master.id_no (Plants under this district)

### 🧭 Indexes
- `district_master_pkey`: CREATE UNIQUE INDEX district_master_pkey ON public.district_master USING btree (id_no)
- `id_no1`: CREATE INDEX id_no1 ON public.district_master USING btree (id_no)
## 🗂️ Table: `download_report`

**📊 Rows:** 13

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| roport_name | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `download_report_pkey`: CREATE UNIQUE INDEX download_report_pkey ON public.download_report USING btree (id_no)
## 🗂️ Table: `dpr_master`

**📊 Rows:** 653805

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_id | integer | YES |
| pi_name | character varying | YES |
| cust_name | character varying | YES |
| cust_id | integer | YES |
| site_name | character varying | YES |
| site_id | integer | YES |
| fse_name | character varying | YES |
| site_distance | double precision | YES |
| tm_no | character varying | YES |
| vol_cum | double precision | YES |
| grade | character varying | YES |
| smode | character varying | YES |
| bth_name | character varying | YES |
| insert_ts | timestamp without time zone | YES |
| tkt_no | integer | YES |
| pump_name | character varying | YES |
| remarks | text | YES |
| vol_status | character | YES |
| d_status | character varying | YES |
| prv_dt_time | timestamp without time zone | YES |
| rej_vol | double precision | YES |
| challan_no | character varying | YES |
| so_no | character varying | YES |
| rej_reason | integer | YES |
| cost_m3 | double precision | YES |
| rej_grade | character varying | YES |
| cost_dvr_m3 | double precision | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `dpr_master_pkey`: CREATE UNIQUE INDEX dpr_master_pkey ON public.dpr_master USING btree (id_no)
- `dpr_master_tkt_no_key`: CREATE UNIQUE INDEX dpr_master_tkt_no_key ON public.dpr_master USING btree (tkt_no)
- `dpr1`: CREATE INDEX dpr1 ON public.dpr_master USING btree (insert_ts, tm_no)
## 🗂️ Table: `dpr_master1`

**📊 Rows:** 3259577

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_id | integer | YES |
| pi_name | character varying | YES |
| cust_name | character varying | YES |
| cust_id | integer | YES |
| site_name | character varying | YES |
| site_id | integer | YES |
| fse_name | character varying | YES |
| site_distance | double precision | YES |
| tm_no | character varying | YES |
| vol_cum | double precision | YES |
| grade | character varying | YES |
| smode | character varying | YES |
| bth_name | character varying | YES |
| insert_ts | timestamp without time zone | YES |
| tkt_no | integer | YES |
| pump_name | character varying | YES |
| remarks | text | YES |
| vol_status | character | YES |
| d_status | character varying | YES |
| prv_dt_time | timestamp without time zone | YES |
| rej_vol | double precision | YES |
| challan_no | character varying | YES |
| so_no | character varying | YES |
| rej_reason | integer | YES |
| cost_m3 | double precision | YES |
| rej_grade | character varying | YES |
| cost_dvr_m3 | double precision | YES |
| plant_code | character varying | YES |
| batch_code | character varying | YES |
| invoice_date | date | YES |
| man_inv | character varying | YES |
| man_cost | character varying | YES |
| man_div | character varying | YES |
| man_qty | character varying | YES |
| qr_code | text | YES |
| irn | character varying | YES |
| acknumber | character varying | YES |
| ack_datetime | character varying | YES |
| fd_status | character varying | YES |
| prod_time | time without time zone | YES |
| pn_kms | double precision | YES |
| pn_drum | double precision | YES |
| milg_cum | double precision | YES |
| milg_vol | double precision | YES |
| extra_status | character | YES |
| extra_status_timestamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `dpr_master1_batch_code_key`: CREATE UNIQUE INDEX dpr_master1_batch_code_key ON public.dpr_master1 USING btree (batch_code)
- `dpr_master1_pkey`: CREATE UNIQUE INDEX dpr_master1_pkey ON public.dpr_master1 USING btree (id_no)
- `dpr_master1_tkt_no_key`: CREATE UNIQUE INDEX dpr_master1_tkt_no_key ON public.dpr_master1 USING btree (tkt_no)
- `dpr11`: CREATE INDEX dpr11 ON public.dpr_master1 USING btree (insert_ts)
- `dpr12`: CREATE INDEX dpr12 ON public.dpr_master1 USING btree (tm_no)
- `dpr13`: CREATE INDEX dpr13 ON public.dpr_master1 USING btree (invoice_date)
- `dpr14`: CREATE INDEX dpr14 ON public.dpr_master1 USING btree (vol_cum)
- `dpr15`: CREATE INDEX dpr15 ON public.dpr_master1 USING btree (prv_dt_time)
- `dpr16`: CREATE INDEX dpr16 ON public.dpr_master1 USING btree (challan_no)
## 🗂️ Table: `driver_assignment`

**📊 Rows:** 360001

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_depo | integer | YES |
| reg_no | character varying | YES |
| driver_id | integer | YES |
| from_dt | date | YES |
| from_tm | time without time zone | YES |
| to_dt | date | YES |
| to_tm | time without time zone | YES |
| shift | integer | YES |
| created_by_user | text | YES |
| link_id | integer | YES |
| driver_id2 | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `driver_assignment_pkey`: CREATE UNIQUE INDEX driver_assignment_pkey ON public.driver_assignment USING btree (id_no)
- `dasn1`: CREATE INDEX dasn1 ON public.driver_assignment USING btree (driver_id)
- `dasn2`: CREATE INDEX dasn2 ON public.driver_assignment USING btree (from_dt DESC)
- `dasn3`: CREATE INDEX dasn3 ON public.driver_assignment USING btree (reg_no)
- `dasn4`: CREATE INDEX dasn4 ON public.driver_assignment USING btree (driver_id2)
## 🗂️ Table: `driver_master`

**📊 Rows:** 3522

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | bigint | NO |
| first_name | character varying | NO |
| last_name | character varying | NO |
| father_name | character varying | YES |
| dt_of_birth | date | YES |
| dt_of_joining | date | YES |
| gender | character varying | YES |
| blood | character varying | YES |
| street1 | character varying | YES |
| street2 | character varying | YES |
| city | character varying | YES |
| state | character varying | YES |
| zip | character varying | YES |
| telephone | character varying | YES |
| lic_no | character varying | YES |
| lic_issue | character varying | YES |
| lic_date | date | YES |
| lic_exp | date | YES |
| lic_token | character varying | YES |
| acc_no | character varying | YES |
| ret_dead | character varying | YES |
| d_code | text | YES |
| id_depo | integer | YES |
| status | character varying | YES |
| mother_plant | character varying | YES |
| lic_pic | text | YES |
| qr_created | timestamp without time zone | YES |
| vendor_id | integer | YES |
| last_code | character varying | YES |
| truein_response | text | YES |
| tshirt_size | character | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `driver_main_pkey`: CREATE UNIQUE INDEX driver_main_pkey ON public.driver_master USING btree (id_no)
- `driver_master_d_code_key`: CREATE UNIQUE INDEX driver_master_d_code_key ON public.driver_master USING btree (d_code)
- `driver_master_lic_no_key`: CREATE UNIQUE INDEX driver_master_lic_no_key ON public.driver_master USING btree (lic_no)
- `driver_master_telephone_key`: CREATE UNIQUE INDEX driver_master_telephone_key ON public.driver_master USING btree (telephone)
- `drvind`: CREATE INDEX drvind ON public.driver_master USING btree (id_no)
## 🗂️ Table: `driver_report`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| depo_code | integer | YES |
| driver_code | character varying | YES |
| bus_id | integer | YES |
| reg_no | character varying | NO |
| route_name | character varying | YES |
| route_time | time without time zone | NO |
| no_speed | integer | YES |
| date_time | date | NO |
| dt_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- reg_no, route_time, date_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `driver_report_pkey`: CREATE UNIQUE INDEX driver_report_pkey ON public.driver_report USING btree (reg_no, date_time, route_time)
## 🗂️ Table: `driver_stop_report`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| depo_code | integer | YES |
| driver_code | character varying | YES |
| bus_id | integer | YES |
| reg_no | character varying | NO |
| route_name | character varying | YES |
| route_time | time without time zone | NO |
| no_stoppage | integer | YES |
| date_time | date | NO |
| dt_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- reg_no, route_time, date_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `driver_stop_report_pkey`: CREATE UNIQUE INDEX driver_stop_report_pkey ON public.driver_stop_report USING btree (reg_no, date_time, route_time)
## 🗂️ Table: `drs_status`

**📊 Rows:** 17148

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reg_no | character varying | YES |
| depo_id | integer | YES |
| load_cnt | integer | YES |
| unload_cnt | integer | YES |
| distance | integer | YES |
| date_entry | date | YES |
| unknown_cnt | integer | YES |
| last_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `drum_trip_report`

**📊 Rows:** 3590193

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| depo_id | integer | YES |
| plant_out | timestamp without time zone | NO |
| site_in | timestamp without time zone | YES |
| ps_duration | time without time zone | YES |
| ps_kms | double precision | YES |
| ps_max_speed | double precision | YES |
| ps_avg_speed | double precision | YES |
| unloading_time | text | YES |
| unloading_duration | time without time zone | YES |
| site_waiting | time without time zone | YES |
| site_out | timestamp without time zone | YES |
| plant_in | timestamp without time zone | YES |
| sp_duration | time without time zone | YES |
| sp_kms | double precision | YES |
| sp_max_speed | double precision | YES |
| sp_avg_speed | double precision | YES |
| plant_lat | character varying | YES |
| plant_lng | character varying | YES |
| site_lat | character varying | YES |
| site_lng | character varying | YES |
| cycle_km | double precision | YES |
| cycle_time | time without time zone | YES |
| tkt_no | integer | YES |
| drum_in_plant | double precision | YES |
| unloading_cnt | integer | YES |
| loading_cnt | integer | YES |

### 🔐 Primary Keys
- reg_no, plant_out

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `drum_trip_report_pkey`: CREATE UNIQUE INDEX drum_trip_report_pkey ON public.drum_trip_report USING btree (reg_no, plant_out)
- `dtrind`: CREATE INDEX dtrind ON public.drum_trip_report USING btree (tkt_no)
## 🗂️ Table: `drv_qr_shift_hrs`

**📊 Rows:** 2

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| shift_hrs | integer | NO |
| status | character varying | NO |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `drv_qr_shift_hrs_pkey`: CREATE UNIQUE INDEX drv_qr_shift_hrs_pkey ON public.drv_qr_shift_hrs USING btree (id_no)
## 🗂️ Table: `drv_veh_qr_assign`

**📊 Rows:** 54251

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| drv_id | integer | YES |
| reg_no | text | YES |
| shift_hrs | character varying | YES |
| from_date | timestamp without time zone | YES |
| to_date | timestamp without time zone | YES |
| created_by_user | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `drv_veh_qr_assign_pkey`: CREATE UNIQUE INDEX drv_veh_qr_assign_pkey ON public.drv_veh_qr_assign USING btree (id_no)
## 🗂️ Table: `email_action`

**📊 Rows:** 15

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reason_type | character varying | YES |
| description | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `email_logs`

**📊 Rows:** 244149

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| email_to | character varying | YES |
| email_cc | character varying | YES |
| email_sub | text | YES |
| time_stamp | timestamp without time zone | YES |
| reason_id | integer | YES |
| remarks | text | YES |
| email_body | text | YES |
| hosp_id | integer | YES |
| emailreason_id | integer | YES |
| emailremarks | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `email_reason`

**📊 Rows:** 13

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reason_type | character varying | YES |
| description | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `eon_logs`

**📊 Rows:** 171965

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| bus_id | integer | YES |
| id_hosp | integer | YES |
| veh_type | integer | YES |
| frm_tm | timestamp without time zone | NO |
| gps_cnt | integer | YES |
| to_tm | timestamp without time zone | YES |
| duration | character varying | YES |
| old_speed | integer | YES |
| new_speed | integer | YES |
| old_sats | integer | YES |
| new_sats | integer | YES |
| old_power | character varying | YES |
| new_power | character varying | YES |

### 🔐 Primary Keys
- reg_no, frm_tm

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `eon_logs_pkey`: CREATE UNIQUE INDEX eon_logs_pkey ON public.eon_logs USING btree (reg_no, frm_tm)
## 🗂️ Table: `eta_checks`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| stop_id | integer | YES |
| route_id | integer | YES |
| last_max_eta | integer | YES |
| arrival_counter | integer | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `eta_etd_sms_detail`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | bigint | NO |
| modem_id | integer | YES |
| req_sender | bigint | YES |
| req_receiver | bigint | YES |
| request | text | YES |
| sim_number | bigint | YES |
| reply | text | YES |
| request_time | timestamp without time zone | YES |
| reply_time | timestamp without time zone | YES |
| status | character | YES |
| remark | text | YES |
| no_of_sms | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_eta_etd_sms_detail`: CREATE UNIQUE INDEX pk_eta_etd_sms_detail ON public.eta_etd_sms_detail USING btree (id_no)
## 🗂️ Table: `eta_etd_sms_thread`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| thread_type | character varying | YES |
| thread_start_time | timestamp without time zone | YES |
| current_time_stamp | timestamp without time zone | YES |
| id_no | integer | NO |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_eta_etd_sms_thread`: CREATE UNIQUE INDEX pk_eta_etd_sms_thread ON public.eta_etd_sms_thread USING btree (id_no)
## 🗂️ Table: `eta_etd_themes`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| stop_id | integer | NO |
| theme_id | integer | YES |
| lcd_id | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `eta_etd_vtype_assign`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_id | integer | NO |
| vtype_id | integer | NO |

### 🔐 Primary Keys
- box_id, vtype_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_eta_etd_vtype_assign`: CREATE UNIQUE INDEX pk_eta_etd_vtype_assign ON public.eta_etd_vtype_assign USING btree (box_id, vtype_id)
## 🗂️ Table: `eta_information`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| lstation | character varying | YES |
| st_id | character varying | YES |
| eta | character varying | YES |
| speed | character varying | YES |
| dst_cov | character varying | YES |
| mode | character varying | YES |
| tdist | character varying | YES |
| route | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| bus_id | integer | YES |
| reg_no | character varying | YES |
| eta_int | integer | YES |
| dest | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `bus_stid_idx`: CREATE INDEX bus_stid_idx ON public.eta_information USING btree (bus_id, st_id)
- `st_id_idx`: CREATE INDEX st_id_idx ON public.eta_information USING btree (st_id)
## 🗂️ Table: `eta_removal_analysis`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| analysis_date | date | YES |
| bus_id | integer | YES |
| stop_id | integer | YES |
| current_stop_match | integer | YES |
| less_300_match | integer | YES |
| sync_mode | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `eta_string`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| fe_string | text | YES |
| genration_time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `eta_string_pkey`: CREATE UNIQUE INDEX eta_string_pkey ON public.eta_string USING btree (id_no)
## 🗂️ Table: `eta_table`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| stop_id | integer | YES |
| eta | character varying | YES |
| bus_id | integer | YES |
| route_name | character varying | YES |
| bus_destination | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| p_check | character | YES |
| reg_no | character varying | YES |
| counter | integer | YES |
| last_st_status | integer | YES |
| eta_int | integer | YES |
| dist_cov | integer | YES |
| id_stop_from | integer | YES |
| id_stop_to | integer | YES |
| route_id | integer | YES |
| stop_sr_no | integer | YES |
| eta_err_code | integer | YES |
| eta_err_code_time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `busid_stopid_rtid_stopsrno`: CREATE INDEX busid_stopid_rtid_stopsrno ON public.eta_table USING btree (bus_id, stop_id, route_id, stop_sr_no)
- `combined_eta_idx`: CREATE INDEX combined_eta_idx ON public.eta_table USING btree (stop_id, p_check, time_stamp, eta_int)
- `eta_improve`: CREATE INDEX eta_improve ON public.eta_table USING btree (stop_id)
- `idx_busid`: CREATE INDEX idx_busid ON public.eta_table USING btree (bus_id)
- `improve_eta_time_ind`: CREATE INDEX improve_eta_time_ind ON public.eta_table USING btree (stop_id)
- `time_stamp_idx`: CREATE INDEX time_stamp_idx ON public.eta_table USING btree (time_stamp)
## 🗂️ Table: `etd_string`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| fe_string | text | YES |
| genration_time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `etd_string_pkey`: CREATE UNIQUE INDEX etd_string_pkey ON public.etd_string USING btree (id_no)
## 🗂️ Table: `etm_string`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| string | text | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `event`

**📊 Rows:** 582815

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| srno | integer | YES |
| event_time | timestamp without time zone | YES |
| bus_id | integer | YES |
| msg | text | YES |
| send_time | timestamp without time zone | YES |
| send_status | "char" | YES |
| retry_count | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `event_notification`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| srno | bigint | NO |
| event_no | bigint | YES |
| no_to | bigint | YES |
| no_from | bigint | YES |
| send_time | timestamp without time zone | YES |
| send_status | character | YES |
| retry_count | integer | YES |

### 🔐 Primary Keys
- srno

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_event_notification`: CREATE UNIQUE INDEX pk_event_notification ON public.event_notification USING btree (srno)
## 🗂️ Table: `fasttag_details`

**📊 Rows:** 132572

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| fetchdata | text | YES |
| time_stamp | timestamp without time zone | YES |
| status | character | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `fasttag_history`

**📊 Rows:** 28230

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reader_id | bigint | YES |
| fasttag_id | text | YES |
| v_no | character varying | YES |
| in_time | timestamp without time zone | YES |
| out_time | timestamp without time zone | YES |
| status | integer | YES |
| pwr_status | integer | YES |
| batt_volt | double precision | YES |
| server_timestamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `fasttag_master`

**📊 Rows:** 32

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reg_no | character varying | YES |
| fasttag_id | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `fasttag_master_pkey`: CREATE UNIQUE INDEX fasttag_master_pkey ON public.fasttag_master USING btree (id_no)
## 🗂️ Table: `fasttag_reader`

**📊 Rows:** 5

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reader_id | bigint | YES |
| loc_id | integer | YES |
| plant_id | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `fixed_asset_category_master`

**📊 Rows:** 42

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| category_id | integer | YES |
| category_name | character varying | YES |
| status | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `category_id`: CREATE UNIQUE INDEX category_id ON public.fixed_asset_category_master USING btree (category_id)
- `fixed_asset_category_master_pkey`: CREATE UNIQUE INDEX fixed_asset_category_master_pkey ON public.fixed_asset_category_master USING btree (id_no)
## 🗂️ Table: `fixed_asset_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_code | character varying | YES |
| plant_id | integer | YES |
| asset_number | character varying | NO |
| description | text | YES |
| unit | integer | YES |
| time_stamp | timestamp without time zone | YES |
| category_id | integer | YES |

### 🔐 Primary Keys
- id_no, asset_number

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `fixed_asset_master_pkey`: CREATE UNIQUE INDEX fixed_asset_master_pkey ON public.fixed_asset_master USING btree (id_no, asset_number)
## 🗂️ Table: `fixed_asset_qr_submission`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| submission_date | date | NO |
| asset_number | character varying | NO |
| scan_dt | timestamp without time zone | NO |
| scanned_asset | text | NO |
| time_stamp | timestamp without time zone | NO |
| scanned_by | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `fixed_asset_qr_submission_pkey`: CREATE UNIQUE INDEX fixed_asset_qr_submission_pkey ON public.fixed_asset_qr_submission USING btree (id_no)
## 🗂️ Table: `fixed_asset_quarters`

**📊 Rows:** 4

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| quarter | character varying | YES |
| period | character varying | YES |
| scanning_period | text | YES |
| status | character varying | YES |
| scanning_months | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `fixed_asset_quarters_pkey`: CREATE UNIQUE INDEX fixed_asset_quarters_pkey ON public.fixed_asset_quarters USING btree (id_no)
## 🗂️ Table: `fse_master`

**📊 Rows:** 393

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| fse_name | character varying | NO |
| fse_email | text | YES |
| fse_no | character varying | YES |
| plant_id | integer | NO |
| salesrep_id | bigint | YES |
| employee_id | character varying | YES |

### 🔐 Primary Keys
- fse_name, plant_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `fse_master_pkey`: CREATE UNIQUE INDEX fse_master_pkey ON public.fse_master USING btree (fse_name, plant_id)
## 🗂️ Table: `fse_master1`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| fse_name | character varying | NO |
| fse_email | text | YES |
| fse_no | character varying | YES |
| plant_id | integer | NO |

### 🔐 Primary Keys
- fse_name, plant_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `fse_master1_pkey`: CREATE UNIQUE INDEX fse_master1_pkey ON public.fse_master1 USING btree (fse_name, plant_id)
## 🗂️ Table: `fuel_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | YES |
| datetime_entry | timestamp without time zone | YES |
| fuel | integer | YES |
| remarks | character varying | YES |
| id | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `fuel_report`

**📊 Rows:** 485305

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reg_no | character varying | YES |
| from_date | timestamp without time zone | YES |
| to_date | timestamp without time zone | YES |
| ob_fuel | double precision | YES |
| cb_fuel | double precision | YES |
| fuel_added | double precision | YES |
| consumed | double precision | YES |
| dist_covered | double precision | YES |
| plant_name | integer | YES |
| mileage | double precision | YES |
| veh_type | integer | YES |
| fuel_pilferage | double precision | YES |
| ign_hrs | double precision | YES |
| ign_detail | text | YES |
| ign1_hrs | double precision | YES |
| ign1_detail | text | YES |
| ign2_hrs | double precision | YES |
| ign2_detail | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `fuel_report_pkey`: CREATE UNIQUE INDEX fuel_report_pkey ON public.fuel_report USING btree (id_no)
- `fuel1`: CREATE INDEX fuel1 ON public.fuel_report USING btree (reg_no)
- `fuel2`: CREATE INDEX fuel2 ON public.fuel_report USING btree (from_date)
## 🗂️ Table: `geo2veh`

**📊 Rows:** 2834

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| noti2veh_id | integer | NO |
| noti2veh_fence_id | integer | YES |
| reg_no | character varying | YES |
| noti2veh_geofence_control_id | integer | YES |

### 🔐 Primary Keys
- noti2veh_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `noti2veh_pkey`: CREATE UNIQUE INDEX noti2veh_pkey ON public.geo2veh USING btree (noti2veh_id)
## 🗂️ Table: `geo_type`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| geo_type_id | integer | NO |
| geo_type_name | character varying | YES |

### 🔐 Primary Keys
- geo_type_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `geo_type_pkey`: CREATE UNIQUE INDEX geo_type_pkey ON public.geo_type USING btree (geo_type_id)
## 🗂️ Table: `geofence`

**📊 Rows:** 594

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| geo_id | integer | NO |
| geo_name | character varying | NO |
| geo_type | integer | YES |
| geo_coord | character varying | YES |
| geo_enable | integer | YES |
| created_by | character varying | YES |

### 🔐 Primary Keys
- geo_name

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `geofence_pkey`: CREATE UNIQUE INDEX geofence_pkey ON public.geofence USING btree (geo_name)
## 🗂️ Table: `geofence_control`

**📊 Rows:** 100

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| geofence_control_id | integer | NO |
| geofence_control_check | integer | YES |
| geofence_control_sensor_id | integer | YES |
| geofence_control_speed_chk | character varying | YES |
| geofence_control_speed_min | integer | YES |
| geofence_control_speed_max | integer | YES |

### 🔐 Primary Keys
- geofence_control_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `geofence_control_pkey`: CREATE UNIQUE INDEX geofence_control_pkey ON public.geofence_control USING btree (geofence_control_id)
## 🗂️ Table: `geofence_last_pos`

**📊 Rows:** 1151

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| latitude | numeric | YES |
| longitude | numeric | YES |
| speed | integer | YES |
| date_time_entry | timestamp without time zone | YES |
| sensor3 | character | YES |
| bus_id | integer | YES |
| sensor2b3 | character | YES |

### 🔐 Primary Keys
- reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `geofence_last_pos_pkey`: CREATE UNIQUE INDEX geofence_last_pos_pkey ON public.geofence_last_pos USING btree (reg_no)
- `date_reg`: CREATE INDEX date_reg ON public.geofence_last_pos USING btree (reg_no, date_time_entry)
- `geofence_1`: CREATE INDEX geofence_1 ON public.geofence_last_pos USING btree (reg_no)
## 🗂️ Table: `geofence_outbox`

**📊 Rows:** 187996

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| updatedindb | timestamp without time zone | NO |
| insertintodb | timestamp without time zone | NO |
| sendingdatetime | timestamp without time zone | NO |
| text | text | YES |
| destinationnumber | character varying | NO |
| coding | character varying | NO |
| udh | text | YES |
| class | integer | YES |
| textdecoded | text | NO |
| id | integer | NO |
| multipart | boolean | NO |
| relativevalidity | integer | YES |
| senderid | character varying | YES |
| sendingtimeout | timestamp without time zone | NO |
| deliveryreport | character varying | YES |
| creatorid | text | NO |
| sent_sms | character | YES |

### 🔐 Primary Keys
- destinationnumber, textdecoded

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `geofence_outbox_pkey`: CREATE UNIQUE INDEX geofence_outbox_pkey ON public.geofence_outbox USING btree (destinationnumber, textdecoded)
## 🗂️ Table: `gps_status`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| time_stamp | timestamp without time zone | NO |
| bus_id | integer | YES |

### 🔐 Primary Keys
- reg_no, time_stamp

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `gps_status_pkey`: CREATE UNIQUE INDEX gps_status_pkey ON public.gps_status USING btree (reg_no, time_stamp)
- `gps1`: CREATE INDEX gps1 ON public.gps_status USING btree (reg_no)
- `gps2`: CREATE INDEX gps2 ON public.gps_status USING btree (time_stamp)
## 🗂️ Table: `grades`

**📊 Rows:** 124

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| grade | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `grades_grade_key`: CREATE UNIQUE INDEX grades_grade_key ON public.grades USING btree (grade)
- `grades_pkey`: CREATE UNIQUE INDEX grades_pkey ON public.grades USING btree (id)
- `grade1`: CREATE INDEX grade1 ON public.grades USING btree (grade)
- `grade2`: CREATE INDEX grade2 ON public.grades USING btree (id)
## 🗂️ Table: `h_leg`

**📊 Rows:** 2746

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| route_id | integer | YES |
| start_stn_id | integer | YES |
| end_stn_id | integer | YES |
| time_taken_secs | integer | YES |
| time_stamp_end | timestamp without time zone | YES |
| time_stamp_start | timestamp without time zone | YES |
| reg_no | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `ssid_esid_regno_rtid_tss`: CREATE INDEX ssid_esid_regno_rtid_tss ON public.h_leg USING btree (start_stn_id, end_stn_id, reg_no, route_id, time_taken_secs)
- `tss_busid_rtid`: CREATE INDEX tss_busid_rtid ON public.h_leg USING btree (time_stamp_start, bus_id, route_id)
- `tss_regno_rtid`: CREATE INDEX tss_regno_rtid ON public.h_leg USING btree (time_stamp_start, reg_no, route_id)
## 🗂️ Table: `h_table`

**📊 Rows:** 2349

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| rt_id | integer | YES |
| stop_id | integer | YES |
| stop_sr_no | integer | YES |
| stop_entry_time | integer | YES |
| time_stamp | timestamp without time zone | YES |
| dist_left_next_stn | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `hosp_master`

**📊 Rows:** 205

**🏭 Business Context:** Plant master table - third level in the organizational hierarchy (Zone → District → Plant → Vehicle). Contains plant/facility details, contact information, and location data. **Note: 'hosp' refers to plants/facilities, not medical facilities.** Links to parent districts and serves as the operational base for vehicles.

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | character varying | YES |
| cont_person | character varying | YES |
| address | text | YES |
| cont_no | character varying | YES |
| id_dist | integer | YES |
| s_lat | double precision | YES |
| s_long | double precision | YES |
| covt_lat | double precision | YES |
| covt_long | double precision | YES |
| tm_no | integer | YES |
| pl_email | text | YES |
| order_by | integer | YES |
| bh_name | character varying | YES |
| bh_no | character varying | YES |
| bh_email | text | YES |
| bm_name | character varying | YES |
| bm_no | character varying | YES |
| bm_email | text | YES |
| loc_code | character varying | YES |
| order_by1 | integer | YES |
| tc_name | character varying | YES |
| tc_no | character varying | YES |
| tc_email | text | YES |
| tc_name1 | character varying | YES |
| tc_no1 | character varying | YES |
| tc_email1 | text | YES |
| gst_no | character varying | YES |
| cin_no | character varying | YES |
| pan_no | character varying | YES |
| cluster_id | integer | YES |
| alert_number | character varying | YES |
| plant_type | integer | YES |
| plt_capacity | double precision | YES |
| id_zone | integer | YES |
| loader_card_no | character varying | YES |
| def_mileage | double precision | YES |
| site_code | character varying | YES |
| bill_status | character varying | YES |
| batching_email | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys (Hierarchical Parents)
- id_dist → district_master.id_no (Parent district/region)

### 🔗 Referenced By (Hierarchical Children)
- vehicle_master.id_hosp → hosp_master.id_no (Vehicles assigned to this plant)
- site_master.plant_id → hosp_master.id_no (Sites under this plant)
- customer_detail.plant_id → hosp_master.id_no (Customer visits to this plant)
- plant_data.plant_id → hosp_master.id_no (Plant operational data)

### 🧭 Indexes
- `hosp_master_pkey`: CREATE UNIQUE INDEX hosp_master_pkey ON public.hosp_master USING btree (id_no)
- `id_no2`: CREATE INDEX id_no2 ON public.hosp_master USING btree (id_no)
## 🗂️ Table: `idle_time_status`

**📊 Rows:** 5335

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| date_time | timestamp without time zone | YES |
| eng_hrs | integer | YES |
| eng_detail | text | YES |
| date_time_stop | timestamp without time zone | YES |
| silo_time | timestamp without time zone | YES |
| normal_time | timestamp without time zone | YES |
| unload_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `idle_time_status_pkey`: CREATE UNIQUE INDEX idle_time_status_pkey ON public.idle_time_status USING btree (reg_no)
- `idle1`: CREATE INDEX idle1 ON public.idle_time_status USING btree (reg_no)
## 🗂️ Table: `imp_stop_times`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| stop_id | integer | NO |

### 🔐 Primary Keys
- stop_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `imp_st`: CREATE UNIQUE INDEX imp_st ON public.imp_stop_times USING btree (stop_id)
## 🗂️ Table: `inv_details`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| invoice_no | character varying | YES |
| image_text | text | YES |
| fetch_status | character | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `invoice_upload`

**📊 Rows:** 39868

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| invoice_no | character varying | YES |
| invoice_img | text | YES |
| time_stamp | timestamp without time zone | YES |
| invoice_status | text | YES |
| pdf_size | text | YES |
| status | character varying | YES |
| upload_start_time | timestamp without time zone | YES |
| upload_end_time | timestamp without time zone | YES |
| username | character varying | YES |
| version | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `iocl_data`

**📊 Rows:** 118943

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| mid | bigint | YES |
| merchant_name | character varying | YES |
| location | character varying | YES |
| card_no | bigint | YES |
| txn_date | timestamp without time zone | YES |
| txn_type | character varying | YES |
| txn_mode | character varying | YES |
| product | character varying | YES |
| rsp | character varying | YES |
| quantity | character varying | YES |
| amount | double precision | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `iocl_data_pkey`: CREATE UNIQUE INDEX iocl_data_pkey ON public.iocl_data USING btree (id_no)
- `iocl1`: CREATE INDEX iocl1 ON public.iocl_data USING btree (card_no)
- `iocl2`: CREATE INDEX iocl2 ON public.iocl_data USING btree (txn_date)
## 🗂️ Table: `iocl_recharge`

**📊 Rows:** 8

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| region_id | integer | YES |
| vendor_id | integer | YES |
| iocl_card | character varying | YES |
| date_entry | date | YES |
| amount | double precision | YES |
| created_by | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| remarks | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `iocl_recharge_pkey`: CREATE UNIQUE INDEX iocl_recharge_pkey ON public.iocl_recharge USING btree (id_no)
## 🗂️ Table: `jcb_details`

**📊 Rows:** 126

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_depo | integer | YES |
| reg_no | character varying | NO |
| vendor_id | integer | YES |
| var_mlg | double precision | YES |
| fixed_cost | character varying | YES |
| contract_type | integer | YES |
| var_mlg_hrs | double precision | YES |

### 🔐 Primary Keys
- reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `jcb_details_pkey`: CREATE UNIQUE INDEX jcb_details_pkey ON public.jcb_details USING btree (reg_no)
## 🗂️ Table: `known_stops`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| stop_id | integer | YES |
| au_stops | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk2`: CREATE UNIQUE INDEX pk2 ON public.known_stops USING btree (id_no)
- `uid`: CREATE UNIQUE INDEX uid ON public.known_stops USING btree (stop_id)
## 🗂️ Table: `last_geo_loc`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| addrs | text | YES |
| date_time | timestamp without time zone | YES |
| geo_frm | character | YES |

### 🔐 Primary Keys
- reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `last_geo_loc_pkey`: CREATE UNIQUE INDEX last_geo_loc_pkey ON public.last_geo_loc USING btree (reg_no)
## 🗂️ Table: `line_diagram_routes`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| s_no | integer | NO |
| route_id | integer | YES |

### 🔐 Primary Keys
- s_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk1`: CREATE UNIQUE INDEX pk1 ON public.line_diagram_routes USING btree (s_no)
## 🗂️ Table: `link_master`

**📊 Rows:** 178

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_link | bigint | NO |
| start_stop_id | bigint | NO |
| end_stop_id | bigint | NO |
| distance | integer | YES |
| time | bigint | YES |
| angle | integer | YES |
| window_range | integer | YES |
| id_checkpoint | integer | NO |
| pattern | text | YES |
| remark | text | YES |

### 🔐 Primary Keys
- id_link, start_stop_id, end_stop_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `PK2`: CREATE UNIQUE INDEX "PK2" ON public.link_master USING btree (id_link, start_stop_id, end_stop_id)
- `link_master_id_link_key`: CREATE UNIQUE INDEX link_master_id_link_key ON public.link_master USING btree (id_link)
- `link1`: CREATE INDEX link1 ON public.link_master USING btree (id_link)
- `link3`: CREATE INDEX link3 ON public.link_master USING btree (start_stop_id)
## 🗂️ Table: `loader_report`

**📊 Rows:** 13761

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| tot_mins | double precision | YES |
| ign_detail | text | YES |
| date_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `loader2`: CREATE INDEX loader2 ON public.loader_report USING btree (reg_no)
## 🗂️ Table: `login_master`

**📊 Rows:** 128

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | character varying | YES |
| pl_email | character varying | YES |
| cont_no | character varying | YES |
| state_id | integer | YES |
| id_dist | integer | YES |
| pincode | integer | YES |
| address | text | YES |
| status | integer | YES |
| role_id | integer | YES |
| head_title | text | YES |
| foot_title | text | YES |
| favi_title | text | YES |
| logo | text | YES |
| change_ver | character | YES |
| tm_track_head | text | YES |
| tm_track_foot | text | YES |
| months | text | YES |
| map_logo | integer | YES |
| setting_id | integer | YES |
| created_by | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `login_master_pkey`: CREATE UNIQUE INDEX login_master_pkey ON public.login_master USING btree (id_no)
## 🗂️ Table: `logs`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | YES |
| date_time | timestamp without time zone | YES |
| alert | character varying | YES |
| remarks | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `master_admin`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | smallint | NO |
| user_name | character varying | NO |
| pass_word | character varying | NO |
| full_name | character varying | YES |
| id_dist | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `mega_trips`

**📊 Rows:** 13903

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| reg_no | character varying | YES |
| plant_id | integer | YES |
| t1_time | timestamp without time zone | YES |
| t2_time | timestamp without time zone | YES |
| t3_time | timestamp without time zone | YES |
| id_no | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `menu`

**📊 Rows:** 21

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| name | character | YES |
| url | character | YES |
| status | integer | YES |
| create_at | character | YES |
| update_date | character | YES |
| icons | character varying | YES |
| order_list | integer | YES |
| roleuser | integer | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `menu_pkey`: CREATE UNIQUE INDEX menu_pkey ON public.menu USING btree (id)
## 🗂️ Table: `mixcode_master`

**📊 Rows:** 81889

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| mix_code | character varying | YES |
| plant_code | character varying | YES |
| time_updated | timestamp without time zone | YES |
| grade_id | integer | YES |
| status | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `mixcode_master_mix_code_plant_code_key`: CREATE UNIQUE INDEX mixcode_master_mix_code_plant_code_key ON public.mixcode_master USING btree (mix_code, plant_code)
- `mixcode_master_pkey`: CREATE UNIQUE INDEX mixcode_master_pkey ON public.mixcode_master USING btree (id_no)
- `mixcode1`: CREATE INDEX mixcode1 ON public.mixcode_master USING btree (plant_code)
## 🗂️ Table: `modem_admin`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | character varying | YES |
| mobile_number | bigint | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_modem_admin`: CREATE UNIQUE INDEX pk_modem_admin ON public.modem_admin USING btree (id_no)
## 🗂️ Table: `modem_configuration`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| serial_port | character varying | YES |
| baud_rate | bigint | YES |
| modem_type | character varying | YES |
| sim_number | bigint | YES |
| sms_counter | integer | YES |
| sms_limit | integer | YES |
| modem_status | character varying | YES |
| priority | integer | YES |
| time_stamp | timestamp without time zone | YES |
| sms_pack_expiry_date | timestamp without time zone | YES |
| active | character | YES |
| sms_counter_day | integer | YES |
| active_day | character | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_modem_configuration`: CREATE UNIQUE INDEX pk_modem_configuration ON public.modem_configuration USING btree (id_no)
## 🗂️ Table: `monthly_bill_details`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| bill_date | date | YES |
| region_id | integer | YES |
| plant_id | integer | YES |
| region_name | character varying | YES |
| plant_name | character varying | YES |
| reg_no | character varying | YES |
| installation_dt | date | YES |
| drs_status | character varying | YES |
| billing_days | integer | YES |
| rate | double precision | YES |
| amount | double precision | YES |
| shifting_remarks | text | YES |
| flag | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `monthly_diesel_upload`

**📊 Rows:** 301

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_code | character varying | YES |
| start_date | date | YES |
| end_date | date | YES |
| diesel_rate | double precision | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `monthly_upload`

**📊 Rows:** 1036

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| plant_code | character | NO |
| diesel_price | double precision | YES |
| opr_cost | double precision | YES |
| target_value | double precision | YES |
| plant_name | character varying | YES |
| entry_date | date | NO |

### 🔐 Primary Keys
- plant_code, entry_date

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `monthly_upload_pkey`: CREATE UNIQUE INDEX monthly_upload_pkey ON public.monthly_upload USING btree (entry_date, plant_code)
## 🗂️ Table: `multiple_display`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_id | integer | YES |
| sub_box_id | integer | YES |
| id_route | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `multiple_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_id | integer | YES |
| sub_box_id | integer | NO |

### 🔐 Primary Keys
- sub_box_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `multiple_master_pkey`: CREATE UNIQUE INDEX multiple_master_pkey ON public.multiple_master USING btree (sub_box_id)
## 🗂️ Table: `night_halt`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| route_id | integer | NO |
| stop_id | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `no_free_sms_dates`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reason | text | YES |
| total_sms_to_send | integer | YES |
| date | date | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_no_free_sms_dates`: CREATE UNIQUE INDEX pk_no_free_sms_dates ON public.no_free_sms_dates USING btree (id_no)
## 🗂️ Table: `non_sales_history`

**📊 Rows:** 452115

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| s_name | character varying | YES |
| cust_name | character varying | YES |
| site_name | character varying | YES |
| cont_person | character varying | YES |
| cont_no | character varying | YES |
| lat | double precision | YES |
| lng | double precision | YES |
| addr | text | YES |
| remarks | text | YES |
| dist_calc | double precision | YES |
| plant_id | integer | YES |
| time_stamp | timestamp without time zone | YES |
| cro_id | integer | YES |
| image | text | YES |
| app_timestamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `non_sales_history_pkey`: CREATE UNIQUE INDEX non_sales_history_pkey ON public.non_sales_history USING btree (id_no)
- `non1`: CREATE INDEX non1 ON public.non_sales_history USING btree (s_name)
- `non2`: CREATE INDEX non2 ON public.non_sales_history USING btree (time_stamp)
## 🗂️ Table: `notification_generated`

**📊 Rows:** 284954

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| noti_gen_id | integer | NO |
| noti_gen_noti_id | integer | YES |
| noti_gen_insertdb_time | timestamp without time zone | YES |
| noti_gen_noti_text | character varying | NO |
| noti_gen_noti_sms | character varying | YES |
| noti_gen_noti_email | character varying | YES |
| noti_gen_sms_no | character varying | NO |
| noti_gen_noti_emailid | character varying | YES |
| noti_gen_generatedtime | timestamp without time zone | YES |
| noti_gen_sped_violate | integer | YES |
| noti_gen_reg_no | character varying | YES |

### 🔐 Primary Keys
- noti_gen_noti_text, noti_gen_sms_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `notificication_generated_pkey`: CREATE UNIQUE INDEX notificication_generated_pkey ON public.notification_generated USING btree (noti_gen_noti_text, noti_gen_sms_no)
## 🗂️ Table: `notification_type`

**📊 Rows:** 3

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| noti_type_id | integer | NO |
| noti_type_name | character varying | YES |

### 🔐 Primary Keys
- noti_type_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `notification_type_pkey`: CREATE UNIQUE INDEX notification_type_pkey ON public.notification_type USING btree (noti_type_id)
## 🗂️ Table: `notifications`

**📊 Rows:** 170

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| noti_id | integer | NO |
| noti_name | character varying | NO |
| time_interval_from | date | YES |
| time_interval_to | date | YES |
| time_diff_msg | character varying | YES |
| noti_text | text | YES |
| noti_control_type | integer | NO |
| noti_control_type_id | integer | YES |
| noti_enable | integer | YES |
| noti_email_chk | character varying | YES |
| noti_email | character varying | YES |
| noti_sms_chk | character varying | YES |
| noti_sms_no | character varying | YES |
| noti_sms_no1 | character varying | YES |
| noti_sms_no2 | character varying | YES |
| noti_sms_no3 | character varying | YES |
| noti_sms_no4 | character varying | YES |
| noti_email1 | character varying | YES |
| noti_email2 | character varying | YES |
| noti_email3 | character varying | YES |
| noti_email4 | character varying | YES |

### 🔐 Primary Keys
- noti_name, noti_control_type

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `notifications_pkey`: CREATE UNIQUE INDEX notifications_pkey ON public.notifications USING btree (noti_name, noti_control_type)
## 🗂️ Table: `order_invoice`

**📊 Rows:** 2519390

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| invoice_no | character varying | YES |
| invoice_date | date | YES |
| plant_id | integer | YES |
| cust_id | integer | YES |
| party_name | character varying | YES |
| party_address | text | YES |
| ship_address | text | YES |
| gst_no | character varying | YES |
| term_of_payment | character varying | YES |
| transport_mode | character varying | YES |
| state | character varying | YES |
| veh_no | character varying | YES |
| dc_no | character varying | YES |
| dc_date | timestamp without time zone | YES |
| place_of_supply | character varying | YES |
| date_of_supply | date | YES |
| sales_order | character varying | YES |
| po_no | character varying | YES |
| description | text | YES |
| hsn_code | character varying | YES |
| uom | character varying | YES |
| qty | double precision | YES |
| unit_price | double precision | YES |
| basic_amt | double precision | YES |
| cgst | integer | YES |
| cgst_amt | double precision | YES |
| sgst | integer | YES |
| sgst_amt | double precision | YES |
| igst | integer | YES |
| igst_amt | double precision | YES |
| gross_amt | double precision | YES |
| cementitious_type | character varying | YES |
| max_agg_size | character varying | YES |
| admixure_type | character varying | YES |
| slump | character varying | YES |
| min_cementitious_content | character varying | YES |
| batch_no | character varying | YES |
| order_qty | double precision | YES |
| qty_with_this_load | double precision | YES |
| cumulative_qty | double precision | YES |
| pouring_location | character varying | YES |
| pumped_by_rdc | character varying | YES |
| time_arrival_onsite | character varying | YES |
| time_discharged_completed | character varying | YES |
| time_released_from_site | character varying | YES |
| remarks | text | YES |
| customer_status | character varying | YES |
| rejection_reason | text | YES |
| sms_status | character varying | YES |
| otp_code | character varying | YES |
| customer_signature | text | YES |
| time_stamp | timestamp without time zone | YES |
| acknowledger_id | character varying | YES |
| driver_contact | bigint | YES |
| customer_contact | bigint | YES |
| pdf_path | text | YES |
| signature_by | character varying | YES |
| pdf_status | character varying | YES |
| payment_status | character | YES |
| state_code | character varying | YES |
| siteid | integer | YES |
| comments | text | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `order_invoice_pkey`: CREATE UNIQUE INDEX order_invoice_pkey ON public.order_invoice USING btree (id)
## 🗂️ Table: `order_invoice1`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| invoice_no | character varying | YES |
| invoice_date | date | YES |
| plant_id | integer | YES |
| cust_id | integer | YES |
| party_name | character varying | YES |
| party_address | text | YES |
| ship_address | text | YES |
| gst_no | character varying | YES |
| term_of_payment | character varying | YES |
| transport_mode | character varying | YES |
| state | character varying | YES |
| veh_no | character varying | YES |
| dc_no | character varying | YES |
| dc_date | timestamp without time zone | YES |
| place_of_supply | character varying | YES |
| date_of_supply | date | YES |
| sales_order | character varying | YES |
| po_no | character varying | YES |
| description | text | YES |
| hsn_code | character varying | YES |
| uom | character varying | YES |
| qty | double precision | YES |
| unit_price | double precision | YES |
| basic_amt | double precision | YES |
| cgst | integer | YES |
| cgst_amt | double precision | YES |
| sgst | integer | YES |
| sgst_amt | double precision | YES |
| igst | integer | YES |
| igst_amt | double precision | YES |
| gross_amt | double precision | YES |
| cementitious_type | character varying | YES |
| max_agg_size | character varying | YES |
| admixure_type | character varying | YES |
| slump | character varying | YES |
| min_cementitious_content | character varying | YES |
| batch_no | character varying | YES |
| order_qty | double precision | YES |
| qty_with_this_load | double precision | YES |
| cumulative_qty | double precision | YES |
| pouring_location | character varying | YES |
| pumped_by_rdc | character varying | YES |
| time_arrival_onsite | character varying | YES |
| time_discharged_completed | character varying | YES |
| time_released_from_site | character varying | YES |
| remarks | text | YES |
| customer_status | character varying | YES |
| rejection_reason | text | YES |
| sms_status | character varying | YES |
| otp_code | character varying | YES |
| customer_signature | text | YES |
| time_stamp | timestamp without time zone | YES |
| acknowledger_id | character varying | YES |
| driver_contact | bigint | YES |
| customer_contact | bigint | YES |
| pdf_path | text | YES |
| signature_by | character varying | YES |
| pdf_status | character varying | YES |
| payment_status | character | YES |
| state_code | character varying | YES |
| siteid | integer | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `order_invoice1_pkey`: CREATE UNIQUE INDEX order_invoice1_pkey ON public.order_invoice1 USING btree (id)
## 🗂️ Table: `order_master`

**📊 Rows:** 196

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| order_type | character varying | YES |
| plant_code | character varying | YES |
| time_updated | timestamp without time zone | YES |
| gst_state | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `order1`: CREATE INDEX order1 ON public.order_master USING btree (plant_code)
## 🗂️ Table: `ota_bus`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_no | integer | NO |
| ota_flag | character | YES |
| ota_type | character varying | YES |
| fw_version | integer | YES |
| total_packet | integer | YES |
| current_packet | integer | YES |
| status | character varying | YES |
| req_time_stamp | timestamp without time zone | YES |
| upd_time_stamp | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- box_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_ota_bus`: CREATE UNIQUE INDEX pk_ota_bus ON public.ota_bus USING btree (box_no)
## 🗂️ Table: `ota_stop`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_no | integer | NO |
| ota_flag | character | YES |
| ota_type | character varying | YES |
| fw_version | integer | YES |
| total_packet | integer | YES |
| current_packet | integer | YES |
| status | character varying | YES |
| req_time_stamp | timestamp without time zone | YES |
| upd_time_stamp | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- box_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_ota`: CREATE UNIQUE INDEX pk_ota ON public.ota_stop USING btree (box_no)
## 🗂️ Table: `ota_stop_history`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_no | integer | YES |
| ota_type | character varying | YES |
| fw_version | integer | YES |
| status | character varying | YES |
| req_time_stamp | timestamp without time zone | YES |
| upd_time_stamp | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `outcome_master`

**📊 Rows:** 5

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| outcome_type | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `outcome_master_pkey`: CREATE UNIQUE INDEX outcome_master_pkey ON public.outcome_master USING btree (id_no)
## 🗂️ Table: `overdue_invoice`

**📊 Rows:** 10143

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_code | integer | YES |
| invoice_no | character varying | YES |
| balance_amt | double precision | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `overdue_invoice_pkey`: CREATE UNIQUE INDEX overdue_invoice_pkey ON public.overdue_invoice USING btree (id_no)
## 🗂️ Table: `pattern_detail`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_route | integer | YES |
| pattern | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `payment_history`

**📊 Rows:** 384

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| order_id | character varying | YES |
| tracking_id | character varying | YES |
| bank_ref_no | character varying | YES |
| order_status | character varying | YES |
| failure_message | character varying | YES |
| payment_mode | character varying | YES |
| card_name | character varying | YES |
| currency | character varying | YES |
| amount | double precision | YES |
| trans_date | timestamp without time zone | YES |
| db_timestamp | timestamp without time zone | YES |
| inv_id | bigint | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `payment_issue`

**📊 Rows:** 8

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| issue_name | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `payment_pending`

**📊 Rows:** 3

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| cust_name | character varying | YES |
| fse_name | character varying | YES |
| pending_amt | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `payment_request`

**📊 Rows:** 867

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| tag | character varying | YES |
| order_id | character varying | NO |
| invoice_no | character varying | YES |
| invoice_date | date | YES |
| gross_amt | double precision | YES |
| order_qty | double precision | YES |
| time_stamp | timestamp without time zone | YES |
| gateway_request_time | timestamp without time zone | YES |
| status | character | YES |
| confirm_payment_status | character varying | YES |
| confirm_payment_time | timestamp without time zone | YES |
| gateway_request_status | character varying | YES |
| reason | text | YES |

### 🔐 Primary Keys
- order_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `payment_request_pkey`: CREATE UNIQUE INDEX payment_request_pkey ON public.payment_request USING btree (order_id)
## 🗂️ Table: `permission`

**📊 Rows:** 12

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| user_role | integer | YES |
| menu_id | text | YES |
| sub_menu_id | text | YES |
| child_id | text | YES |
| role | integer | YES |
| child_menu_edit | text | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `permission_pkey`: CREATE UNIQUE INDEX permission_pkey ON public.permission USING btree (id)
## 🗂️ Table: `pl_daily_data`

**📊 Rows:** 6370

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_name | character varying | YES |
| loc_code | character varying | YES |
| mix_hrs | double precision | YES |
| diesel_issued | double precision | YES |
| maint_cost | double precision | YES |
| water_purchased | double precision | YES |
| time_stamp | timestamp without time zone | YES |
| date_entry | date | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pl_daily_data_loc_code_date_entry_key`: CREATE UNIQUE INDEX pl_daily_data_loc_code_date_entry_key ON public.pl_daily_data USING btree (loc_code, date_entry)
- `pl_daily_data_pkey`: CREATE UNIQUE INDEX pl_daily_data_pkey ON public.pl_daily_data USING btree (id_no)
- `ddata1`: CREATE INDEX ddata1 ON public.pl_daily_data USING btree (date_entry)
## 🗂️ Table: `pl_rmcost`

**📊 Rows:** 1172786

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_name | character varying | YES |
| loc_code | character varying | YES |
| invoice_no | character varying | YES |
| rm_cost | double precision | YES |
| time_stamp | timestamp without time zone | YES |
| invoice_date | date | YES |
| batch_no | character varying | YES |
| batching_start | timestamp without time zone | YES |
| batching_end | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pl_rmcost_invoice_no_key`: CREATE UNIQUE INDEX pl_rmcost_invoice_no_key ON public.pl_rmcost USING btree (invoice_no)
- `pl_rmcost_pkey`: CREATE UNIQUE INDEX pl_rmcost_pkey ON public.pl_rmcost USING btree (id_no)
- `rmcost1`: CREATE INDEX rmcost1 ON public.pl_rmcost USING btree (invoice_date)
## 🗂️ Table: `plant_data`

**📊 Rows:** 41

**📊 Business Context:** Plant operational data table. Contains daily operational readings and metrics for plants. Links to hosp_master for plant identification and hierarchy.

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| date_entry | date | YES |
| plant_id | integer | YES |
| eb_read | double precision | YES |
| tmrh_read | double precision | YES |
| mrhodg_read | double precision | YES |
| dgrh_read | double precision | YES |
| cpodg_read | double precision | YES |
| pbh_read | double precision | YES |
| time_updated | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- plant_id → hosp_master.id_no (Parent plant)

### 🧭 Indexes
- `plant_data_pkey`: CREATE UNIQUE INDEX plant_data_pkey ON public.plant_data USING btree (id_no)
## 🗂️ Table: `plant_distance`

**📊 Rows:** 170

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| src_id | integer | YES |
| dest_id | integer | YES |
| distance | double precision | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `plant_schedule`

**📊 Rows:** 5220

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_id | integer | YES |
| cust_name | character varying | YES |
| cust_id | integer | YES |
| site_name | character varying | YES |
| site_id | integer | YES |
| fse_name | character varying | YES |
| vol_cum | double precision | YES |
| grade | character varying | YES |
| smode | character varying | YES |
| mix_code | character varying | YES |
| assign_ft_name | character varying | YES |
| insert_ts | timestamp without time zone | YES |
| cont_person | character varying | YES |
| cont_no | bigint | YES |
| p_date | date | YES |
| p_time | time without time zone | YES |
| pump_name | character varying | YES |
| so_no | character varying | YES |
| plant_code | character varying | YES |
| remarks | text | YES |
| pour_rate | double precision | YES |
| structure | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `plant_schedule_pkey`: CREATE UNIQUE INDEX plant_schedule_pkey ON public.plant_schedule USING btree (id_no)
- `plant1`: CREATE INDEX plant1 ON public.plant_schedule USING btree (plant_id)
- `plnt2`: CREATE INDEX plnt2 ON public.plant_schedule USING btree (p_date)
## 🗂️ Table: `plant_site_distance`

**📊 Rows:** 6469

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| cust_id | integer | NO |
| site_id | integer | NO |
| plant_id | integer | NO |
| distance | double precision | YES |
| site_loc | character varying | YES |
| plant_loc | character varying | YES |
| id_no | integer | NO |

### 🔐 Primary Keys
- cust_id, site_id, plant_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `plant_site_distance_pkey`: CREATE UNIQUE INDEX plant_site_distance_pkey ON public.plant_site_distance USING btree (cust_id, site_id, plant_id)
## 🗂️ Table: `plnt_report`

**📊 Rows:** 50185

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| plant_id | integer | YES |
| from_tm | timestamp without time zone | NO |
| to_tm | timestamp without time zone | YES |
| distance | double precision | YES |
| start_loc | character varying | YES |
| end_loc | character varying | YES |
| start_id | integer | YES |
| end_id | integer | YES |
| drum_cnt | double precision | YES |

### 🔐 Primary Keys
- reg_no, from_tm

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `plnt_report_pkey`: CREATE UNIQUE INDEX plnt_report_pkey ON public.plnt_report USING btree (reg_no, from_tm)
- `pnt1`: CREATE INDEX pnt1 ON public.plnt_report USING btree (reg_no)
- `pnt2`: CREATE INDEX pnt2 ON public.plnt_report USING btree (from_tm)
- `pnt3`: CREATE INDEX pnt3 ON public.plnt_report USING btree (plant_id)
## 🗂️ Table: `pour_feedback`

**📊 Rows:** 178

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| username | character varying | YES |
| distid | integer | YES |
| supply_plant | character varying | YES |
| contact_name | character varying | YES |
| contact_mob | character varying | YES |
| mode | character varying | YES |
| pour_quantity | character varying | YES |
| delivery_schedule | character varying | YES |
| product_quality | character varying | YES |
| site_supervisor | integer | YES |
| tm_driver | integer | YES |
| fse | integer | YES |
| pumping_staff | integer | YES |
| order_taken | integer | YES |
| plant_staff | integer | YES |
| safety | integer | YES |
| overall_performance | integer | YES |
| suggestion | text | YES |
| recommend | character varying | YES |
| filled_time | timestamp without time zone | YES |
| update_time | timestamp without time zone | YES |
| status | character varying | YES |
| plant_id | integer | YES |
| pour_id | integer | YES |
| cube_rating | integer | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pour_feedback_pkey`: CREATE UNIQUE INDEX pour_feedback_pkey ON public.pour_feedback USING btree (id)
- `feedback2`: CREATE INDEX feedback2 ON public.pour_feedback USING btree (distid)
## 🗂️ Table: `pump_bill`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plantid | integer | YES |
| vendorid | integer | YES |
| fdate | date | YES |
| edate | date | YES |
| fixed_amt | double precision | YES |
| var_amt | double precision | YES |
| grdtot | double precision | YES |
| created_at | timestamp without time zone | NO |
| fixed_bill_no | character varying | YES |
| var_bill_no | character varying | YES |
| fixed_url | character varying | YES |
| var_url | character varying | YES |
| fixed_agree | integer | YES |
| var_agree | integer | YES |
| fixed_cost_amt | double precision | YES |
| var_cost_amt | double precision | YES |
| grdtot_cost | double precision | YES |
| iocl_amt | double precision | YES |
| status | integer | YES |
| iocl_status | integer | YES |
| fxd_invoice | date | YES |
| var_invoice | date | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pump_bill_pkey`: CREATE UNIQUE INDEX pump_bill_pkey ON public.pump_bill USING btree (id_no)
## 🗂️ Table: `pump_details`

**📊 Rows:** 427

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_depo | integer | YES |
| reg_no | character varying | NO |
| vendor_id | integer | YES |
| p_t_no | character varying | YES |
| p_t_deplyoed | character varying | YES |
| m_y_mfg | character varying | YES |
| cont_duration | integer | YES |
| from_dt | date | YES |
| to_dt | date | YES |
| fixed_cost | character varying | YES |
| p_d_avghrs | character varying | YES |
| p_d_avgcum | character varying | YES |
| t_van_dmil | character varying | YES |
| comm_qty_mnt | double precision | YES |
| pu_qty_rt | double precision | YES |
| unpu_qty_rt | double precision | YES |
| extra_qty_rt | double precision | YES |
| contract_type | integer | YES |

### 🔐 Primary Keys
- reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pump_details_pkey`: CREATE UNIQUE INDEX pump_details_pkey ON public.pump_details USING btree (reg_no)
## 🗂️ Table: `pump_trip_report`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| depo_id | integer | YES |
| plant_out | timestamp without time zone | NO |
| site_in | timestamp without time zone | YES |
| ps_duration | time without time zone | YES |
| ps_kms | double precision | YES |
| unloading_time | text | YES |
| unloading_duration | time without time zone | YES |
| site_waiting | time without time zone | YES |
| site_out | timestamp without time zone | YES |
| plant_in | timestamp without time zone | YES |
| sp_duration | time without time zone | YES |
| sp_kms | double precision | YES |
| plant_lat | character varying | YES |
| plant_lng | character varying | YES |
| site_lat | character varying | YES |
| site_lng | character varying | YES |
| cycle_km | double precision | YES |
| cycle_time | time without time zone | YES |

### 🔐 Primary Keys
- reg_no, plant_out

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pump_trip_report_pkey`: CREATE UNIQUE INDEX pump_trip_report_pkey ON public.pump_trip_report USING btree (reg_no, plant_out)
## 🗂️ Table: `pumpdpr_master`

**📊 Rows:** 165

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_id | integer | YES |
| vendor_name | character varying | YES |
| cust_name | character varying | YES |
| cust_id | integer | YES |
| site_name | character varying | YES |
| site_id | integer | YES |
| vol_cum | double precision | YES |
| grade | character varying | YES |
| vol_cum1 | double precision | YES |
| grade1 | character varying | YES |
| vol_cum2 | double precision | YES |
| grade3 | character varying | YES |
| bth_name | character varying | YES |
| insert_ts | timestamp without time zone | YES |
| from_dt | timestamp without time zone | YES |
| to_dt | timestamp without time zone | YES |
| pump_name | character varying | YES |
| remarks | text | YES |
| plant_start | timestamp without time zone | YES |
| site_reach | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pumpdpr_master_pkey`: CREATE UNIQUE INDEX pumpdpr_master_pkey ON public.pumpdpr_master USING btree (id_no)
## 🗂️ Table: `purpose_visit`

**📊 Rows:** 6

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| purpose_type | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `purpose_visit_pkey`: CREATE UNIQUE INDEX purpose_visit_pkey ON public.purpose_visit USING btree (id_no)
## 🗂️ Table: `pvt_cluster`

**📊 Rows:** 12

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| cust_id | integer | NO |
| cust_name | character varying | NO |
| zone | character varying | YES |

### 🔐 Primary Keys
- cust_id, cust_name

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pvt_cluster_pkey`: CREATE UNIQUE INDEX pvt_cluster_pkey ON public.pvt_cluster USING btree (cust_id, cust_name)
## 🗂️ Table: `qr_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| qr_user | character varying | YES |
| qr_email | text | YES |
| qr_no | character varying | YES |
| plant_id | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `qr_master_pkey`: CREATE UNIQUE INDEX qr_master_pkey ON public.qr_master USING btree (id_no)
## 🗂️ Table: `query_patterns`

**📊 Rows:** 22

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| user_query | text | NO |
| sql_query | text | NO |
| embedding_json | text | NO |
| success | boolean | YES |
| created_at | timestamp without time zone | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `query_patterns_pkey`: CREATE UNIQUE INDEX query_patterns_pkey ON public.query_patterns USING btree (id)
- `query_patterns_created_idx`: CREATE INDEX query_patterns_created_idx ON public.query_patterns USING btree (created_at)
## 🗂️ Table: `rdc_cluster`

**📊 Rows:** 13

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| cust_id | integer | NO |
| cust_name | character varying | NO |
| zone | character varying | YES |

### 🔐 Primary Keys
- cust_id, cust_name

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `rdc_cluster_pkey`: CREATE UNIQUE INDEX rdc_cluster_pkey ON public.rdc_cluster USING btree (cust_id, cust_name)
## 🗂️ Table: `regional_translation`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| word | text | YES |
| regional_code | text | YES |
| english_code | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_reginal_translation`: CREATE UNIQUE INDEX pk_reginal_translation ON public.regional_translation USING btree (id_no)
## 🗂️ Table: `rejection_reason`

**📊 Rows:** 7

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| rej_reason | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `report_logs`

**📊 Rows:** 33161

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| rep_name | character varying | YES |
| s_time | timestamp without time zone | YES |
| e_time | timestamp without time zone | YES |
| user_name | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `request_and_intimation`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| srno | bigint | NO |
| mobile_no | bigint | YES |
| msg | text | YES |
| msg_type | character | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- srno

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_request_and_intimation`: CREATE UNIQUE INDEX pk_request_and_intimation ON public.request_and_intimation USING btree (srno)
## 🗂️ Table: `role_detail`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| sr_no | integer | NO |
| role_name | character varying | YES |
| role_type | integer | YES |
| view | character varying | YES |
| create_modify | character varying | YES |
| delete | character varying | YES |
| assign | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `role_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| sr_no | integer | NO |
| name | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `roles`

**📊 Rows:** 12

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| role_name | character | YES |
| remarks | text | YES |
| status | integer | YES |
| create_at | date | YES |
| user_type | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `roles_pkey`: CREATE UNIQUE INDEX roles_pkey ON public.roles USING btree (id_no)
## 🗂️ Table: `route_detail`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_route | bigint | NO |
| stop_id | bigint | NO |
| stop_serial_no | bigint | NO |
| distance | integer | YES |
| time | bigint | YES |
| angle | integer | YES |
| window_range | integer | YES |
| id_checkpoint | integer | NO |
| display_report | "char" | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `rt_in1`: CREATE INDEX rt_in1 ON public.route_detail USING btree (stop_serial_no)
- `rt_index`: CREATE INDEX rt_index ON public.route_detail USING btree (id_route, stop_serial_no)
## 🗂️ Table: `route_detail_link`

**📊 Rows:** 169

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_route | integer | YES |
| link_serial_no | integer | YES |
| id_link | integer | YES |
| waiting_time | integer | YES |
| display_report | "char" | YES |
| stop_inter | "char" | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `rt_link1`: CREATE INDEX rt_link1 ON public.route_detail_link USING btree (id_route)
- `rt_link2`: CREATE INDEX rt_link2 ON public.route_detail_link USING btree (id_link, id_route)
## 🗂️ Table: `route_master`

**📊 Rows:** 28

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | character varying | YES |
| remark | text | YES |
| id_intermediate | integer | YES |
| id_source | integer | YES |
| regional_name | text | YES |
| english_name | text | YES |
| id_dist | integer | YES |
| full_name | character varying | YES |
| intermediate_serial_no | integer | YES |
| sch_km | integer | YES |
| sch_km_dest | integer | YES |
| multi_inter_rt | "char" | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `route_master_pkey`: CREATE UNIQUE INDEX route_master_pkey ON public.route_master USING btree (id_no)
- `rt_index1`: CREATE INDEX rt_index1 ON public.route_master USING btree (name)
- `rtm_index`: CREATE INDEX rtm_index ON public.route_master USING btree (id_no)
## 🗂️ Table: `route_schedule`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| s_no | integer | YES |
| d_id | bigint | YES |
| c_id | bigint | YES |
| route_id | integer | NO |
| s_time | time without time zone | NO |
| d_time | time without time zone | YES |
| veh_id | integer | NO |
| date_entry | date | NO |
| time_stamp | timestamp without time zone | YES |
| reg_no | character varying | YES |
| depo_id | integer | YES |
| trip_id | integer | YES |

### 🔐 Primary Keys
- route_id, s_time, veh_id, date_entry

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk3`: CREATE UNIQUE INDEX pk3 ON public.route_schedule USING btree (route_id, s_time, veh_id, date_entry)
- `rt_shd1`: CREATE INDEX rt_shd1 ON public.route_schedule USING btree (veh_id, date_entry, route_id)
## 🗂️ Table: `sales_app_config`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| gps_interval | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `sales_temp`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| username | character varying | YES |
| in_time | timestamp without time zone | YES |
| out_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `sales_temp_pkey`: CREATE UNIQUE INDEX sales_temp_pkey ON public.sales_temp USING btree (id)
## 🗂️ Table: `sap_doticket`

**📊 Rows:** 3693898

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| do_id_no | bigint | YES |
| ticket_number | character varying | NO |
| ship_to | character varying | YES |
| name1 | character varying | YES |
| orto1 | character varying | YES |
| pstlz | character varying | YES |
| regio | character varying | YES |
| telf1 | character varying | YES |
| driver_no | character varying | YES |
| driver_name | character varying | YES |
| licence_number | character varying | YES |
| persl_mob_numb | character varying | YES |
| delivery_qty | double precision | YES |
| truck_number | character varying | YES |
| from_distance | double precision | YES |
| actual_lod_date | date | YES |
| actual_lod_time | time without time zone | YES |
| actual_leave_date | date | YES |
| actual_leave_time | time without time zone | YES |
| consig_loc | character varying | YES |
| assigned_ts | timestamp without time zone | YES |
| assigned | character | YES |
| ack_ts | timestamp without time zone | YES |
| err_code | character varying | YES |
| assigned_conv_lat | double precision | YES |
| assigned_conv_long | double precision | YES |
| consig_wnd | integer | YES |
| consig_stop_id | integer | NO |
| consig_dist | integer | YES |
| tm_reg_no | character varying | YES |
| driver_id | integer | YES |
| remarks | text | YES |

### 🔐 Primary Keys
- ticket_number

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `sap_doticket_do_id_no_key`: CREATE UNIQUE INDEX sap_doticket_do_id_no_key ON public.sap_doticket USING btree (do_id_no)
- `sap_doticket_pkey`: CREATE UNIQUE INDEX sap_doticket_pkey ON public.sap_doticket USING btree (ticket_number)
- `sapd2`: CREATE INDEX sapd2 ON public.sap_doticket USING btree (assigned_ts)
- `sapd3`: CREATE INDEX sapd3 ON public.sap_doticket USING btree (ship_to)
- `sapr1`: CREATE INDEX sapr1 ON public.sap_doticket USING btree (tm_reg_no)
## 🗂️ Table: `sap_live2`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| do_id_no | character varying | NO |
| ev | integer | YES |
| insert_ts | timestamp without time zone | YES |
| sent_ts | timestamp without time zone | YES |
| sent_status | character | YES |
| date_time_entry | timestamp without time zone | YES |
| reg_no | character varying | YES |
| leave_timestamp | timestamp without time zone | YES |
| leave_stop_id | integer | YES |
| arrive_timestamp | timestamp without time zone | YES |
| arrive_stop_id | integer | YES |
| unload_first_time_stamp | timestamp without time zone | YES |
| return_timestamp | timestamp without time zone | YES |
| available_timestamp | timestamp without time zone | YES |
| available_stop_id | integer | YES |
| interval_T1 | time without time zone | YES |
| interval_T2 | time without time zone | YES |
| interval_T3 | time without time zone | YES |
| norm_cnt | integer | YES |
| unload_cnt | integer | YES |
| max_speed | integer | YES |
| remarks | text | YES |
| total_distance_travelled | integer | YES |
| conv_lat | double precision | YES |
| conv_long | double precision | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `sap1`: CREATE INDEX sap1 ON public.sap_live2 USING btree (ev)
- `sap2`: CREATE INDEX sap2 ON public.sap_live2 USING btree (reg_no)
- `sap3`: CREATE INDEX sap3 ON public.sap_live2 USING btree (insert_ts)
- `sap4`: CREATE INDEX sap4 ON public.sap_live2 USING btree (sent_status)
## 🗂️ Table: `schedule_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| exec_day | integer | YES |
| district | integer | YES |
| email | character varying | YES |
| reports | integer | YES |
| exec_time | time without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `schedule_master_pkey`: CREATE UNIQUE INDEX schedule_master_pkey ON public.schedule_master USING btree (id_no)
## 🗂️ Table: `schema_embeddings`

**📊 Rows:** 336

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| table_key | character varying | NO |
| description | text | NO |
| embedding_json | text | NO |
| created_at | timestamp without time zone | YES |
| updated_at | timestamp without time zone | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `schema_embeddings_pkey`: CREATE UNIQUE INDEX schema_embeddings_pkey ON public.schema_embeddings USING btree (id)
- `schema_embeddings_table_key_key`: CREATE UNIQUE INDEX schema_embeddings_table_key_key ON public.schema_embeddings USING btree (table_key)
- `schema_embeddings_table_key_idx`: CREATE INDEX schema_embeddings_table_key_idx ON public.schema_embeddings USING btree (table_key)
## 🗂️ Table: `seats_available`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| etm_id | integer | YES |
| veh_id | integer | YES |
| regn_no | character varying | YES |
| stop_id | integer | YES |
| stop_name | text | YES |
| total_seats | integer | YES |
| available_seats | integer | YES |
| etm_time_stamp | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `sensor2veh`

**📊 Rows:** 1060

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| sensor2veh_id | integer | NO |
| sensor2veh_sensor_id | integer | YES |
| sensor2veh_regno | character varying | YES |

### 🔐 Primary Keys
- sensor2veh_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `sensor2veh_pkey`: CREATE UNIQUE INDEX sensor2veh_pkey ON public.sensor2veh USING btree (sensor2veh_id)
## 🗂️ Table: `sensor_control`

**📊 Rows:** 39

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| sensor_control_id | integer | NO |
| sensor_type | integer | YES |
| sensor_geofence_control | integer | YES |
| sensor_geofence_control_check | character varying | YES |

### 🔐 Primary Keys
- sensor_control_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `sensor_control_pkey`: CREATE UNIQUE INDEX sensor_control_pkey ON public.sensor_control USING btree (sensor_control_id)
## 🗂️ Table: `sensor_type`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| sensor_type_id | integer | NO |
| sensor_type_name | character varying | YES |

### 🔐 Primary Keys
- sensor_type_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `sensor_type_pkey`: CREATE UNIQUE INDEX sensor_type_pkey ON public.sensor_type USING btree (sensor_type_id)
## 🗂️ Table: `silo_data`

**📊 Rows:** 40

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| silo_name | character varying | YES |
| silo_shape | character | YES |
| material_type | integer | YES |
| tank_capacity | double precision | YES |
| alert_vol | double precision | YES |
| silo_ht | double precision | YES |
| silo_dia | double precision | YES |
| offset_ht | double precision | YES |
| cone_ht | double precision | YES |
| silo_material | integer | YES |
| silo_density | integer | YES |
| silo_kfact | double precision | YES |
| silo_ht1 | double precision | YES |
| silo_ht2 | double precision | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `silo_data_pkey`: CREATE UNIQUE INDEX silo_data_pkey ON public.silo_data USING btree (id_no)
- `silo_data_silo_name_key`: CREATE UNIQUE INDEX silo_data_silo_name_key ON public.silo_data USING btree (silo_name)
## 🗂️ Table: `silo_history`

**📊 Rows:** 6472

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_id | integer | YES |
| reg_no | character varying | NO |
| date_entry | date | NO |
| qty | double precision | YES |
| silo_ht | double precision | YES |
| silo_tm | time without time zone | NO |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- reg_no, date_entry, silo_tm

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `silo_history_pkey`: CREATE UNIQUE INDEX silo_history_pkey ON public.silo_history USING btree (reg_no, date_entry, silo_tm)
- `sh1`: CREATE INDEX sh1 ON public.silo_history USING btree (reg_no)
- `sh2`: CREATE INDEX sh2 ON public.silo_history USING btree (date_entry)
## 🗂️ Table: `silo_hourly`

**📊 Rows:** 21937

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_id | integer | YES |
| reg_no | character varying | NO |
| date_entry | date | NO |
| qty | double precision | YES |
| silo_ht | double precision | YES |
| silo_tm | time without time zone | NO |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- reg_no, date_entry, silo_tm

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `silo_hourly_pkey`: CREATE UNIQUE INDEX silo_hourly_pkey ON public.silo_hourly USING btree (reg_no, date_entry, silo_tm)
- `shl1`: CREATE INDEX shl1 ON public.silo_hourly USING btree (reg_no)
- `shl2`: CREATE INDEX shl2 ON public.silo_hourly USING btree (date_entry)
## 🗂️ Table: `silo_sms`

**📊 Rows:** 48502

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| mobile_no | character varying | YES |
| status | character | YES |
| time_stamp | timestamp without time zone | YES |
| silo_name | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `silo_stock`

**📊 Rows:** 211591

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_code | character varying | YES |
| item_category | character varying | YES |
| stock_timestamp | timestamp without time zone | YES |
| time_updated | timestamp without time zone | YES |
| quantity | double precision | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `site_customer`

**📊 Rows:** 173141

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_name | character varying | YES |
| plant_id | integer | YES |
| created_by | character varying | YES |
| contact_no | character varying | YES |
| email_id | text | YES |
| remarks | text | YES |
| cont_name | character varying | YES |
| cust_type | integer | YES |
| site_status | integer | YES |
| status_time | timestamp without time zone | YES |
| fse_id | integer | YES |
| cust_status | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `site_customer_customer_name_key`: CREATE UNIQUE INDEX site_customer_customer_name_key ON public.site_customer USING btree (customer_name, plant_id)
- `site_customer_pkey`: CREATE UNIQUE INDEX site_customer_pkey ON public.site_customer USING btree (id_no)
- `sc1`: CREATE INDEX sc1 ON public.site_customer USING btree (id_no)
- `sc2`: CREATE INDEX sc2 ON public.site_customer USING btree (created_by)
- `sc3`: CREATE INDEX sc3 ON public.site_customer USING btree (customer_name)
## 🗂️ Table: `site_customer1`

**📊 Rows:** 32342

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_name | character varying | YES |
| plant_id | integer | YES |
| created_by | character varying | NO |
| contact_no | character varying | YES |
| email_id | text | YES |
| remarks | text | YES |
| cont_name | character varying | YES |
| cust_type | integer | YES |
| site_status | integer | YES |
| status_time | timestamp without time zone | YES |
| username | character varying | YES |
| password | character varying | YES |
| designation | character varying | YES |
| otp_code | character varying | YES |
| salesrep_id | bigint | YES |
| bill_to_id | integer | YES |
| bill_to_state | character varying | YES |

### 🔐 Primary Keys
- id_no, created_by

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `site_customer1_id_no_created_by_key`: CREATE UNIQUE INDEX site_customer1_id_no_created_by_key ON public.site_customer1 USING btree (id_no, created_by)
- `site_customer1_pkey`: CREATE UNIQUE INDEX site_customer1_pkey ON public.site_customer1 USING btree (id_no, created_by)
- `sc11`: CREATE INDEX sc11 ON public.site_customer1 USING btree (id_no)
- `sc21`: CREATE INDEX sc21 ON public.site_customer1 USING btree (created_by)
## 🗂️ Table: `site_customer1_deleted`

**📊 Rows:** 21

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_name | character varying | YES |
| plant_id | integer | YES |
| created_by | character varying | NO |
| contact_no | character varying | YES |
| email_id | text | YES |
| remarks | text | YES |
| cont_name | character varying | YES |
| cust_type | integer | YES |
| site_status | integer | YES |
| status_time | timestamp without time zone | YES |
| username | character varying | YES |
| password | character varying | YES |
| designation | character varying | YES |
| otp_code | character varying | YES |
| salesrep_id | bigint | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `site_customer2`

**📊 Rows:** 39926

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | bigint | NO |
| customer_name | character varying | YES |
| remarks | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `site_customer2_pkey`: CREATE UNIQUE INDEX site_customer2_pkey ON public.site_customer2 USING btree (id_no)
## 🗂️ Table: `site_master`

**📊 Rows:** 218926

**📍 Business Context:** Site master table - middle level in the organizational hierarchy. Contains customer sites/locations under specific plants. Links customers to plants and serves as the location reference for business operations.

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| site_name | character varying | YES |
| customer_id | integer | YES |
| plant_id | integer | YES |
| site_dist | double precision | YES |
| created_by | character varying | YES |
| contact_no | character varying | YES |
| email_id | text | YES |
| remarks | text | YES |
| gps_dist | double precision | YES |
| very_dist | double precision | YES |
| fse_id | integer | YES |
| fse_name | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys (Hierarchical Parents)
- plant_id → hosp_master.id_no (Parent plant)
- customer_id → [Customer master reference]

### 🔗 Referenced By (Hierarchical Children)  
- customer_detail.site_id → site_master.id_no (Customer visits to this site)

### 🧭 Indexes
- `site_master_pkey`: CREATE UNIQUE INDEX site_master_pkey ON public.site_master USING btree (id_no)
- `site_master_site_name_key`: CREATE UNIQUE INDEX site_master_site_name_key ON public.site_master USING btree (site_name, customer_id)
- `sm1`: CREATE INDEX sm1 ON public.site_master USING btree (id_no)
- `sm2`: CREATE INDEX sm2 ON public.site_master USING btree (created_by)
- `sm3`: CREATE INDEX sm3 ON public.site_master USING btree (customer_id)
- `sm4`: CREATE INDEX sm4 ON public.site_master USING btree (plant_id)
## 🗂️ Table: `site_master1`

**📊 Rows:** 45735

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| site_name | character varying | YES |
| customer_id | integer | YES |
| plant_id | integer | YES |
| site_dist | double precision | YES |
| created_by | character varying | NO |
| contact_no | character varying | YES |
| email_id | text | YES |
| remarks | text | YES |
| gps_dist | double precision | YES |
| very_dist | double precision | YES |
| fse_id | integer | YES |
| fse_name | character varying | YES |
| userid | integer | YES |
| ship_to_id | bigint | YES |
| milg_7 | double precision | YES |
| milg_8 | double precision | YES |
| milg_9 | double precision | YES |
| milg_10 | double precision | YES |
| cumperl | double precision | YES |
| bill_type | integer | YES |

### 🔐 Primary Keys
- id_no, created_by

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `site_master1_id_no_created_by_key`: CREATE UNIQUE INDEX site_master1_id_no_created_by_key ON public.site_master1 USING btree (id_no, created_by)
- `site_master1_pkey`: CREATE UNIQUE INDEX site_master1_pkey ON public.site_master1 USING btree (id_no, created_by)
- `sm11`: CREATE INDEX sm11 ON public.site_master1 USING btree (id_no)
- `sm21`: CREATE INDEX sm21 ON public.site_master1 USING btree (created_by)
## 🗂️ Table: `site_master2`

**📊 Rows:** 101093

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | bigint | NO |
| site_name | character varying | YES |
| customer_id | bigint | NO |
| remarks | character varying | YES |
| contact_no | character varying | YES |
| fse_name | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no, customer_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `site_master2_pkey`: CREATE UNIQUE INDEX site_master2_pkey ON public.site_master2 USING btree (id_no, customer_id)
## 🗂️ Table: `site_segment`

**📊 Rows:** 9

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| segment_name | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `site_segment_pkey`: CREATE UNIQUE INDEX site_segment_pkey ON public.site_segment USING btree (id_no)
## 🗂️ Table: `sms_server`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_hosp | integer | YES |
| mobile_no | bigint | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `sms_server_pkey`: CREATE UNIQUE INDEX sms_server_pkey ON public.sms_server USING btree (id_no)
## 🗂️ Table: `sms_server_configuration`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| time_stamp | timestamp without time zone | YES |
| modem_status | character varying | YES |
| retry_limit | integer | YES |
| interval | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `so_closure_status`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| so_number | character varying | YES |
| trans_id | integer | YES |
| status | character varying | YES |
| remark | text | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `so_details`

**📊 Rows:** 728

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_id | bigint | YES |
| site_id | bigint | YES |
| supply_plant_id | bigint | YES |
| distance | character varying | YES |
| mode | character varying | YES |
| quantity | character varying | YES |
| base_price | character varying | YES |
| gst | bigint | YES |
| total_price | character varying | YES |
| po_number | character varying | YES |
| total_so_value | character varying | YES |
| sez | text | YES |
| existing_so_available | character varying | YES |
| so_number | text | YES |
| bill_to_id | text | YES |
| so_status | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| created_by | text | YES |
| upload_po_copy | bytea | YES |
| site_mob_no | text | YES |
| salesrep_id | text | YES |
| order_type | integer | YES |
| mix_code | integer | YES |
| grade | integer | YES |
| fetch_status | character varying | YES |
| updated_at | timestamp without time zone | YES |
| updated_by | character varying | YES |
| so_accepted_time | timestamp without time zone | YES |
| so_accepted_by | character varying | YES |
| so_rejected_time | timestamp without time zone | YES |
| so_rejected_by | character varying | YES |
| remarks | text | YES |
| image_text | text | YES |
| mime_type | text | NO |
| so_remarks | text | YES |
| expected_payment_date | date | YES |
| expected_amount | bigint | YES |
| short_note | text | YES |
| forwarded_to_manager_at | timestamp without time zone | YES |
| forwarded_to_manager_by | character varying | YES |
| forwarded_to_head_at | timestamp without time zone | YES |
| forwarded_to_head_by | character varying | YES |
| forward_to_bh_remarks | text | YES |
| forwarded_to_cfo_at | timestamp without time zone | YES |
| forwarded_to_cfo_by | character varying | YES |
| forward_to_cfo_remarks | text | YES |
| approve_by_bm_at | timestamp without time zone | YES |
| approve_by_bh_at | timestamp without time zone | YES |
| approve_by_cfo_at | timestamp without time zone | YES |
| approve_by_cfo | character varying | YES |
| approve_cfo_remarks | text | YES |
| approve_by_night_accnt | character varying | YES |
| approve_by_night_accnt_at | timestamp without time zone | YES |
| old_supply_plant | bigint | YES |
| plant_transfer_at | timestamp without time zone | YES |
| transfer_remarks | text | YES |
| cu_remarks | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `so_details_pkey`: CREATE UNIQUE INDEX so_details_pkey ON public.so_details USING btree (id_no)
## 🗂️ Table: `so_details_temp`

**📊 Rows:** 6

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_id | bigint | YES |
| site_id | bigint | YES |
| supply_plant_id | bigint | YES |
| distance | character varying | YES |
| mode | character varying | YES |
| quantity | character varying | YES |
| base_price | character varying | YES |
| gst | bigint | YES |
| total_price | character varying | YES |
| po_number | character varying | YES |
| total_so_value | character varying | YES |
| sez | text | YES |
| existing_so_available | character varying | YES |
| so_number | text | YES |
| bill_to_id | text | YES |
| so_status | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| created_by | text | YES |
| upload_po_copy | bytea | YES |
| site_mob_no | text | YES |
| salesrep_id | text | YES |
| order_type | integer | YES |
| mix_code | integer | YES |
| grade | integer | YES |
| fetch_status | character varying | YES |
| updated_at | timestamp without time zone | YES |
| updated_by | character varying | YES |
| so_accepted_time | timestamp without time zone | YES |
| so_accepted_by | character varying | YES |
| so_rejected_time | timestamp without time zone | YES |
| so_rejected_by | character varying | YES |
| remarks | text | YES |
| image_text | text | YES |
| mime_type | text | NO |
| so_remarks | text | YES |
| expected_payment_date | date | YES |
| expected_amount | bigint | YES |
| short_note | text | YES |
| forwarded_to_manager_at | timestamp without time zone | YES |
| forwarded_to_manager_by | character varying | YES |
| forwarded_to_head_at | timestamp without time zone | YES |
| forwarded_to_head_by | character varying | YES |
| forward_to_bh_remarks | text | YES |
| forwarded_to_cfo_at | timestamp without time zone | YES |
| forwarded_to_cfo_by | character varying | YES |
| forward_to_cfo_remarks | text | YES |
| approve_by_bm_at | timestamp without time zone | YES |
| approve_by_bh_at | timestamp without time zone | YES |
| approve_by_cfo_at | timestamp without time zone | YES |
| approve_by_cfo | character varying | YES |
| approve_cfo_remarks | text | YES |
| approve_by_night_accnt | character varying | YES |
| approve_by_night_accnt_at | timestamp without time zone | YES |
| old_supply_plant | bigint | YES |
| plant_transfer_at | timestamp without time zone | YES |
| transfer_remarks | text | YES |
| cu_remarks | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `so_details_temp_pkey`: CREATE UNIQUE INDEX so_details_temp_pkey ON public.so_details_temp USING btree (id_no)
## 🗂️ Table: `so_health_configurations`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| exception_amt | bigint | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `so_health_configurations_pkey`: CREATE UNIQUE INDEX so_health_configurations_pkey ON public.so_health_configurations USING btree (id_no)
## 🗂️ Table: `so_status`

**📊 Rows:** 425

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| order_id | integer | NO |
| so_number | bigint | YES |
| error_message | text | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- order_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `so_status_pkey`: CREATE UNIQUE INDEX so_status_pkey ON public.so_status USING btree (order_id)
## 🗂️ Table: `so_transferred_details`

**📊 Rows:** 28

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_id | bigint | YES |
| site_id | bigint | YES |
| supply_plant_id | bigint | YES |
| distance | character varying | YES |
| mode | character varying | YES |
| quantity | character varying | YES |
| base_price | character varying | YES |
| gst | bigint | YES |
| total_price | character varying | YES |
| po_number | character varying | YES |
| total_so_value | character varying | YES |
| sez | text | YES |
| existing_so_available | character varying | YES |
| so_number | text | YES |
| bill_to_id | text | YES |
| so_status | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| created_by | text | YES |
| upload_po_copy | bytea | YES |
| site_mob_no | text | YES |
| salesrep_id | text | YES |
| order_type | integer | YES |
| mix_code | integer | YES |
| grade | integer | YES |
| fetch_status | character varying | YES |
| updated_at | timestamp without time zone | YES |
| updated_by | character varying | YES |
| so_accepted_time | timestamp without time zone | YES |
| so_accepted_by | character varying | YES |
| so_rejected_time | timestamp without time zone | YES |
| so_rejected_by | character varying | YES |
| remarks | text | YES |
| image_text | text | YES |
| mime_type | text | NO |
| so_remarks | text | YES |
| expected_payment_date | date | YES |
| expected_amount | bigint | YES |
| short_note | text | YES |
| forwarded_to_manager_at | timestamp without time zone | YES |
| forwarded_to_manager_by | character varying | YES |
| forwarded_to_head_at | timestamp without time zone | YES |
| forwarded_to_head_by | character varying | YES |
| forward_to_bh_remarks | text | YES |
| forwarded_to_cfo_at | timestamp without time zone | YES |
| forwarded_to_cfo_by | character varying | YES |
| forward_to_cfo_remarks | text | YES |
| approve_by_bm_at | timestamp without time zone | YES |
| approve_by_bh_at | timestamp without time zone | YES |
| approve_by_cfo_at | timestamp without time zone | YES |
| approve_by_cfo | character varying | YES |
| approve_cfo_remarks | text | YES |
| approve_by_night_accnt | character varying | YES |
| approve_by_night_accnt_at | timestamp without time zone | YES |
| old_supply_plant | bigint | YES |
| plant_transfer_at | timestamp without time zone | YES |
| transfer_remarks | text | YES |
| cu_remarks | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `transfered_so_pkey`: CREATE UNIQUE INDEX transfered_so_pkey ON public.so_transferred_details USING btree (id_no)
## 🗂️ Table: `so_transferred_details_temp`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_id | bigint | YES |
| site_id | bigint | YES |
| supply_plant_id | bigint | YES |
| distance | character varying | YES |
| mode | character varying | YES |
| quantity | character varying | YES |
| base_price | character varying | YES |
| gst | bigint | YES |
| total_price | character varying | YES |
| po_number | character varying | YES |
| total_so_value | character varying | YES |
| sez | text | YES |
| existing_so_available | character varying | YES |
| so_number | text | YES |
| bill_to_id | text | YES |
| so_status | character varying | YES |
| time_stamp | timestamp without time zone | YES |
| created_by | text | YES |
| upload_po_copy | bytea | YES |
| site_mob_no | text | YES |
| salesrep_id | text | YES |
| order_type | integer | YES |
| mix_code | integer | YES |
| grade | integer | YES |
| fetch_status | character varying | YES |
| updated_at | timestamp without time zone | YES |
| updated_by | character varying | YES |
| so_accepted_time | timestamp without time zone | YES |
| so_accepted_by | character varying | YES |
| so_rejected_time | timestamp without time zone | YES |
| so_rejected_by | character varying | YES |
| remarks | text | YES |
| image_text | text | YES |
| mime_type | text | NO |
| so_remarks | text | YES |
| expected_payment_date | date | YES |
| expected_amount | bigint | YES |
| short_note | text | YES |
| forwarded_to_manager_at | timestamp without time zone | YES |
| forwarded_to_manager_by | character varying | YES |
| forwarded_to_head_at | timestamp without time zone | YES |
| forwarded_to_head_by | character varying | YES |
| forward_to_bh_remarks | text | YES |
| forwarded_to_cfo_at | timestamp without time zone | YES |
| forwarded_to_cfo_by | character varying | YES |
| forward_to_cfo_remarks | text | YES |
| approve_by_bm_at | timestamp without time zone | YES |
| approve_by_bh_at | timestamp without time zone | YES |
| approve_by_cfo_at | timestamp without time zone | YES |
| approve_by_cfo | character varying | YES |
| approve_cfo_remarks | text | YES |
| approve_by_night_accnt | character varying | YES |
| approve_by_night_accnt_at | timestamp without time zone | YES |
| old_supply_plant | bigint | YES |
| plant_transfer_at | timestamp without time zone | YES |
| transfer_remarks | text | YES |
| cu_remarks | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `transfered_so_temp_pkey`: CREATE UNIQUE INDEX transfered_so_temp_pkey ON public.so_transferred_details_temp USING btree (id_no)
## 🗂️ Table: `speed2veh`

**📊 Rows:** 346

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| speed2veh_id | integer | NO |
| speed2veh_speed_control_id | integer | YES |
| reg_no | character varying | YES |

### 🔐 Primary Keys
- speed2veh_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `speed2veh_pkey`: CREATE UNIQUE INDEX speed2veh_pkey ON public.speed2veh USING btree (speed2veh_id)
## 🗂️ Table: `speed_control`

**📊 Rows:** 67

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| speed_control_id | integer | NO |
| speed_control_speed_min | integer | YES |
| speed_control_speed_max | integer | YES |

### 🔐 Primary Keys
- speed_control_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `speed_control_pkey`: CREATE UNIQUE INDEX speed_control_pkey ON public.speed_control USING btree (speed_control_id)
## 🗂️ Table: `status`

**📊 Rows:** 3

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| status | character varying | YES |
| code | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `status_pkey`: CREATE UNIQUE INDEX status_pkey ON public.status USING btree (id)
## 🗂️ Table: `stop_code`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| stop_no | integer | YES |
| stop_code | text | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `stop_status`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_no | integer | NO |
| stop_no | integer | YES |
| battery_status | character | YES |
| display_status | character | YES |
| sd_card_fault | character | YES |
| mains_removed | character | YES |
| tamper_alert | character | YES |
| connected | character | YES |
| gsm_sig_strength | integer | YES |
| battery_voltage | integer | YES |
| temperature | integer | YES |
| disp_fw_ver | integer | YES |
| disp_boot_loader_fw_ver | integer | YES |
| gsm_fw_ver | integer | YES |
| gsm_boot_loader_fw_ver | integer | YES |
| protocol_ver | integer | YES |
| reg_pkt_time_stamp | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |
| reset_flag | integer | YES |
| reset_cause | integer | YES |

### 🔐 Primary Keys
- box_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_stop_status`: CREATE UNIQUE INDEX pk_stop_status ON public.stop_status USING btree (box_no)
## 🗂️ Table: `stop_times`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| route_id | integer | YES |
| link_id | integer | YES |
| link_serial_no | integer | YES |
| trip_id | integer | YES |
| bay_no | integer | YES |
| dep_time | time without time zone | YES |
| waiting_time | integer | YES |
| arr_time | time without time zone | YES |
| end_day | integer | YES |
| valid_time | "char" | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `stopid`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| stop_id_match | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `stopidmatch`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| stop_id | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `structure_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| structure_name | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `sub_menu`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| menu_id | integer | YES |
| sub_menu | character | YES |
| sub_menu_url | character | YES |
| status | integer | YES |
| create_date | date | YES |
| update_date | date | YES |
| order_list | integer | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `sub_menu_pkey`: CREATE UNIQUE INDEX sub_menu_pkey ON public.sub_menu USING btree (id)
## 🗂️ Table: `tamper_sms_update`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| regno | character varying | NO |
| tamper | character varying | YES |
| update_tamper | integer | YES |
| date_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- regno

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tamper_sms_update_pkey`: CREATE UNIQUE INDEX tamper_sms_update_pkey ON public.tamper_sms_update USING btree (regno)
## 🗂️ Table: `tank_data`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| regn_no | character varying | NO |
| tank_type | character | YES |
| tank_vol | real | YES |
| tank_dia | real | YES |
| tank_len | real | YES |
| tank_c | character varying | YES |
| tank_c_type | character | YES |
| tank_width | real | YES |
| tank_ht | real | YES |
| gauge_r_bt | real | YES |
| gauge_r_tg | real | YES |
| float_h | real | YES |
| float_ht | real | YES |
| float_c | character varying | YES |
| float_r_min | real | YES |
| float_r_max | real | YES |
| float_v_disconn | real | YES |
| float_v_e_e | real | YES |
| float_pivot_off | real | YES |
| float_c_type | character | YES |
| remarks | text | YES |
| fuel_ad_type | character | YES |
| fuel_ad_max | real | YES |
| fuel_ad_min | real | YES |
| cal_pr_offset | double precision | YES |
| fuel_drop_add | double precision | YES |

### 🔐 Primary Keys
- regn_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tank_data_pkey`: CREATE UNIQUE INDEX tank_data_pkey ON public.tank_data USING btree (regn_no)
## 🗂️ Table: `tax_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| tax_type | character varying | YES |
| tax_value | double precision | YES |
| time_updated | timestamp without time zone | YES |
| description | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `taxi_tm`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| zone_id | integer | YES |
| region_id | integer | YES |
| plant_id | integer | YES |
| vend_id | integer | YES |
| created_at | timestamp without time zone | NO |
| taxi_tm | character varying | YES |
| stand_weight | double precision | YES |
| capacity | double precision | YES |
| vendor_id | integer | YES |
| fixed_cost | double precision | YES |
| per_kms_amount | double precision | YES |
| tm_mileage | double precision | YES |
| dry_mileage | double precision | YES |
| assetid | character varying | YES |
| mfg_year | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `taxi_tm_pkey`: CREATE UNIQUE INDEX taxi_tm_pkey ON public.taxi_tm USING btree (id_no)
## 🗂️ Table: `tc_attributes`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| description | character varying | NO |
| type | character varying | NO |
| attribute | character varying | NO |
| expression | character varying | NO |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tc_attributes_pkey`: CREATE UNIQUE INDEX tc_attributes_pkey ON public.tc_attributes USING btree (id)
## 🗂️ Table: `tc_calendars`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| name | character varying | NO |
| data | bytea | NO |
| attributes | character varying | NO |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tc_calendars_pkey`: CREATE UNIQUE INDEX tc_calendars_pkey ON public.tc_calendars USING btree (id)
## 🗂️ Table: `tc_commands`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| description | character varying | NO |
| type | character varying | NO |
| textchannel | boolean | NO |
| attributes | character varying | NO |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tc_commands_pkey`: CREATE UNIQUE INDEX tc_commands_pkey ON public.tc_commands USING btree (id)
## 🗂️ Table: `tc_device_attribute`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| deviceid | integer | NO |
| attributeid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `attributeid` → `tc_attributes.id`
- `deviceid` → `tc_devices.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_device_command`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| deviceid | integer | NO |
| commandid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `commandid` → `tc_commands.id`
- `deviceid` → `tc_devices.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_device_driver`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| deviceid | integer | NO |
| driverid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `deviceid` → `tc_devices.id`
- `driverid` → `tc_drivers.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_device_geofence`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| deviceid | integer | NO |
| geofenceid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `deviceid` → `tc_devices.id`
- `geofenceid` → `tc_geofences.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_device_maintenance`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| deviceid | integer | NO |
| maintenanceid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `deviceid` → `tc_devices.id`
- `maintenanceid` → `tc_maintenances.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_device_notification`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| deviceid | integer | NO |
| notificationid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `deviceid` → `tc_devices.id`
- `notificationid` → `tc_notifications.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_devices`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| name | character varying | NO |
| uniqueid | character varying | NO |
| lastupdate | timestamp without time zone | YES |
| positionid | integer | YES |
| groupid | integer | YES |
| attributes | character varying | YES |
| phone | character varying | YES |
| model | character varying | YES |
| contact | character varying | YES |
| category | character varying | YES |
| disabled | boolean | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- `groupid` → `tc_groups.id`

### 🧭 Indexes
- `tc_devices_pkey`: CREATE UNIQUE INDEX tc_devices_pkey ON public.tc_devices USING btree (id)
- `tc_devices_uniqueid_key`: CREATE UNIQUE INDEX tc_devices_uniqueid_key ON public.tc_devices USING btree (uniqueid)
- `tcde`: CREATE INDEX tcde ON public.tc_devices USING btree (id)
## 🗂️ Table: `tc_drivers`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| name | character varying | NO |
| uniqueid | character varying | NO |
| attributes | character varying | NO |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tc_drivers_pkey`: CREATE UNIQUE INDEX tc_drivers_pkey ON public.tc_drivers USING btree (id)
- `tc_drivers_uniqueid_key`: CREATE UNIQUE INDEX tc_drivers_uniqueid_key ON public.tc_drivers USING btree (uniqueid)
## 🗂️ Table: `tc_geofences`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| name | character varying | NO |
| description | character varying | YES |
| area | character varying | NO |
| attributes | character varying | YES |
| calendarid | integer | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- `calendarid` → `tc_calendars.id`

### 🧭 Indexes
- `tc_geofences_pkey`: CREATE UNIQUE INDEX tc_geofences_pkey ON public.tc_geofences USING btree (id)
## 🗂️ Table: `tc_group_attribute`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| groupid | integer | NO |
| attributeid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `attributeid` → `tc_attributes.id`
- `groupid` → `tc_groups.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_group_command`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| groupid | integer | NO |
| commandid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `commandid` → `tc_commands.id`
- `groupid` → `tc_groups.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_group_driver`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| groupid | integer | NO |
| driverid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `driverid` → `tc_drivers.id`
- `groupid` → `tc_groups.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_group_geofence`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| groupid | integer | NO |
| geofenceid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `geofenceid` → `tc_geofences.id`
- `groupid` → `tc_groups.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_group_maintenance`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| groupid | integer | NO |
| maintenanceid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `groupid` → `tc_groups.id`
- `maintenanceid` → `tc_maintenances.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_group_notification`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| groupid | integer | NO |
| notificationid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `groupid` → `tc_groups.id`
- `notificationid` → `tc_notifications.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_groups`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| name | character varying | NO |
| groupid | integer | YES |
| attributes | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- `groupid` → `tc_groups.id`

### 🧭 Indexes
- `tc_groups_pkey`: CREATE UNIQUE INDEX tc_groups_pkey ON public.tc_groups USING btree (id)
## 🗂️ Table: `tc_maintenances`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| name | character varying | NO |
| type | character varying | NO |
| start | double precision | NO |
| period | double precision | NO |
| attributes | character varying | NO |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tc_maintenances_pkey`: CREATE UNIQUE INDEX tc_maintenances_pkey ON public.tc_maintenances USING btree (id)
## 🗂️ Table: `tc_notifications`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| type | character varying | NO |
| attributes | character varying | YES |
| always | boolean | NO |
| calendarid | integer | YES |
| notificators | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- `calendarid` → `tc_calendars.id`

### 🧭 Indexes
- `tc_notifications_pkey`: CREATE UNIQUE INDEX tc_notifications_pkey ON public.tc_notifications USING btree (id)
## 🗂️ Table: `tc_servers`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| registration | boolean | NO |
| latitude | double precision | NO |
| longitude | double precision | NO |
| zoom | integer | NO |
| map | character varying | YES |
| bingkey | character varying | YES |
| mapurl | character varying | YES |
| readonly | boolean | NO |
| twelvehourformat | boolean | NO |
| attributes | character varying | YES |
| forcesettings | boolean | NO |
| coordinateformat | character varying | YES |
| devicereadonly | boolean | YES |
| limitcommands | boolean | YES |
| poilayer | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tc_servers_pkey`: CREATE UNIQUE INDEX tc_servers_pkey ON public.tc_servers USING btree (id)
## 🗂️ Table: `tc_statistics`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| capturetime | timestamp without time zone | NO |
| activeusers | integer | NO |
| activedevices | integer | NO |
| requests | integer | NO |
| messagesreceived | integer | NO |
| messagesstored | integer | NO |
| attributes | character varying | NO |
| mailsent | integer | NO |
| smssent | integer | NO |
| geocoderrequests | integer | NO |
| geolocationrequests | integer | NO |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tc_statistics_pkey`: CREATE UNIQUE INDEX tc_statistics_pkey ON public.tc_statistics USING btree (id)
## 🗂️ Table: `tc_user_attribute`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| attributeid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `attributeid` → `tc_attributes.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_calendar`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| calendarid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `calendarid` → `tc_calendars.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_command`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| commandid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `commandid` → `tc_commands.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_device`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| deviceid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `deviceid` → `tc_devices.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_driver`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| driverid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `driverid` → `tc_drivers.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_geofence`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| geofenceid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `geofenceid` → `tc_geofences.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_group`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| groupid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `groupid` → `tc_groups.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_maintenance`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| maintenanceid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `maintenanceid` → `tc_maintenances.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_notification`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| notificationid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `notificationid` → `tc_notifications.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_user_user`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| userid | integer | NO |
| manageduserid | integer | NO |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- `manageduserid` → `tc_users.id`
- `userid` → `tc_users.id`

### 🧭 Indexes
- None
## 🗂️ Table: `tc_users`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| name | character varying | NO |
| email | character varying | NO |
| hashedpassword | character varying | YES |
| salt | character varying | YES |
| readonly | boolean | NO |
| administrator | boolean | YES |
| map | character varying | YES |
| latitude | double precision | NO |
| longitude | double precision | NO |
| zoom | integer | NO |
| twelvehourformat | boolean | NO |
| attributes | character varying | YES |
| coordinateformat | character varying | YES |
| disabled | boolean | YES |
| expirationtime | timestamp without time zone | YES |
| devicelimit | integer | YES |
| token | character varying | YES |
| userlimit | integer | YES |
| devicereadonly | boolean | YES |
| phone | character varying | YES |
| limitcommands | boolean | YES |
| login | character varying | YES |
| poilayer | character varying | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tc_users_email_key`: CREATE UNIQUE INDEX tc_users_email_key ON public.tc_users USING btree (email)
- `tc_users_pkey`: CREATE UNIQUE INDEX tc_users_pkey ON public.tc_users USING btree (id)
## 🗂️ Table: `temp_invoice_upload`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| invoice_no | character varying | YES |
| invoice_img | text | YES |
| time_stamp | timestamp without time zone | YES |
| invoice_status | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `temp_sales`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| rep_id | bigint | YES |
| name | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `theme_color`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | character | YES |
| color_one | character | YES |
| color_two | character | YES |
| color_three | character | YES |
| role | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `theme_color_pkey`: CREATE UNIQUE INDEX theme_color_pkey ON public.theme_color USING btree (id_no)
## 🗂️ Table: `theme_setting`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| setting_name | character varying | YES |
| head_title | text | YES |
| foot_title | text | YES |
| favi_title | text | YES |
| logo | character varying | YES |
| change_ver | character varying | YES |
| tm_track_head | text | YES |
| tm_track_foot | text | YES |
| map_logo | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `theme_setting_pkey`: CREATE UNIQUE INDEX theme_setting_pkey ON public.theme_setting USING btree (id_no)
## 🗂️ Table: `tipper_trip_report`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| reg_no | character varying | NO |
| depo_id | integer | YES |
| plant_in | timestamp without time zone | NO |
| unload_start | timestamp without time zone | YES |
| pu_duration | time without time zone | YES |
| unload_end | timestamp without time zone | YES |
| unload_duration | time without time zone | YES |
| plant_out | timestamp without time zone | YES |
| up_duration | time without time zone | YES |
| cycle_time | time without time zone | YES |
| bus_id | integer | YES |

### 🔐 Primary Keys
- reg_no, plant_in

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tipper_trip_report_pkey`: CREATE UNIQUE INDEX tipper_trip_report_pkey ON public.tipper_trip_report USING btree (reg_no, plant_in)
## 🗂️ Table: `tm_documents`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| plant_id | integer | YES |
| reg_no | character varying | YES |
| registration_certificate | text | YES |
| registration_exp_dt | date | YES |
| fitness_certificate | text | YES |
| fitness_exp_dt | date | YES |
| permit_certificate | text | YES |
| permit_exp_dt | date | YES |
| insurance_copy | text | YES |
| insurance_exp_dt | date | YES |
| puc | text | YES |
| puc_exp_dt | date | YES |
| model_no | text | YES |
| chas_no | text | YES |
| eng_no | text | YES |
| nt_permit_exp_date | date | YES |
| tax_rcpt_exp_date | date | YES |
| nt_permit_file | text | YES |
| tax_rcpt_file | text | YES |
| vendor_id | integer | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tm_documents_pkey`: CREATE UNIQUE INDEX tm_documents_pkey ON public.tm_documents USING btree (id)
## 🗂️ Table: `tm_dry_run`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| from_plt | integer | NO |
| to_plt | integer | YES |
| reg_no | character varying | NO |
| dt_entry | date | YES |
| kms_plt | double precision | YES |
| created_by | character varying | YES |
| time_stamp | timestamp without time zone | NO |
| remarks | text | YES |

### 🔐 Primary Keys
- from_plt, reg_no, time_stamp

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tm_dry_run_pkey`: CREATE UNIQUE INDEX tm_dry_run_pkey ON public.tm_dry_run USING btree (from_plt, reg_no, time_stamp)
- `dry1`: CREATE INDEX dry1 ON public.tm_dry_run USING btree (dt_entry)
## 🗂️ Table: `tm_status`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| plant_name | character varying | NO |
| tm_no | integer | YES |
| date_time | timestamp without time zone | NO |
| plant_id | integer | YES |

### 🔐 Primary Keys
- plant_name, date_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tm_status_pkey`: CREATE UNIQUE INDEX tm_status_pkey ON public.tm_status USING btree (plant_name, date_time)
- `tms1`: CREATE INDEX tms1 ON public.tm_status USING btree (plant_id)
- `tms2`: CREATE INDEX tms2 ON public.tm_status USING btree (date_time)
## 🗂️ Table: `tm_status_sms`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_dist | integer | YES |
| plant_id | integer | YES |
| sms1 | character varying | YES |
| sms2 | character varying | YES |
| email1 | character varying | YES |
| email2 | character varying | YES |
| daily_rpt1 | character varying | YES |
| daily_rpt2 | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `tm_status_sms_pkey`: CREATE UNIQUE INDEX tm_status_sms_pkey ON public.tm_status_sms USING btree (id_no)
## 🗂️ Table: `tm_trip_zero`

**📊 Rows:** 34494

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plant_id | integer | YES |
| date_entry | date | YES |
| tot_tms | integer | YES |
| zero_tms | integer | YES |
| volume | double precision | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `zero1`: CREATE INDEX zero1 ON public.tm_trip_zero USING btree (date_entry)
- `zero2`: CREATE INDEX zero2 ON public.tm_trip_zero USING btree (plant_id)
## 🗂️ Table: `trip_live`

**📊 Rows:** 218199

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| date_time_entry | timestamp without time zone | YES |
| latitude | numeric | YES |
| longitude | numeric | YES |
| speed | integer | YES |
| time_stamp | timestamp without time zone | YES |
| stop_id_match | integer | YES |
| reg_no | character varying | YES |
| pkt_type | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `trip_live1`: CREATE INDEX trip_live1 ON public.trip_live USING btree (reg_no)
- `trip_live2`: CREATE INDEX trip_live2 ON public.trip_live USING btree (date_time_entry)
## 🗂️ Table: `trip_live_pos`

**📊 Rows:** 4327

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| date_time_entry | timestamp without time zone | YES |
| latitude | numeric | YES |
| longitude | numeric | YES |
| speed | integer | YES |
| time_stamp | timestamp without time zone | YES |
| stop_id_match | integer | YES |
| reg_no | character varying | YES |
| pkt_type | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `livepos`: CREATE INDEX livepos ON public.trip_live_pos USING btree (reg_no)
## 🗂️ Table: `trip_live_pos_91`

**📊 Rows:** 4127

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| date_time_entry | timestamp without time zone | YES |
| latitude | numeric | YES |
| longitude | numeric | YES |
| speed | integer | YES |
| time_stamp | timestamp without time zone | YES |
| stop_id_match | integer | YES |
| reg_no | character varying | YES |
| pkt_type | integer | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `livepos91`: CREATE INDEX livepos91 ON public.trip_live_pos_91 USING btree (reg_no)
## 🗂️ Table: `trip_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| route_id | integer | NO |
| src_dep_timings | time without time zone | NO |
| dest_dep_timings | time without time zone | NO |
| trip_id | integer | NO |
| depo_id | integer | YES |
| trip_days | integer | YES |

### 🔐 Primary Keys
- route_id, src_dep_timings, dest_dep_timings, trip_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk_trip`: CREATE UNIQUE INDEX pk_trip ON public.trip_master USING btree (trip_id, route_id, src_dep_timings, dest_dep_timings)
- `trip_master_trip_id_key`: CREATE UNIQUE INDEX trip_master_trip_id_key ON public.trip_master USING btree (trip_id)
## 🗂️ Table: `trip_report`

**📊 Rows:** 8738827

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | NO |
| total_time_taken | integer | YES |
| total_distance_travelled | integer | YES |
| maximum_speed | integer | YES |
| number_of_match | integer | YES |
| referral_ids | character varying | YES |
| start_time | timestamp without time zone | NO |
| end_time | timestamp without time zone | YES |
| id_route | integer | YES |
| time_stamp | timestamp without time zone | NO |
| rs_string | character varying | YES |
| repo_string | character varying | YES |
| remarks | text | YES |
| reg_no | character varying | NO |
| driver_id | integer | YES |

### 🔐 Primary Keys
- start_time, time_stamp, reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `trip_report_pkey`: CREATE UNIQUE INDEX trip_report_pkey ON public.trip_report USING btree (reg_no, start_time, time_stamp)
- `date6`: CREATE INDEX date6 ON public.trip_report USING btree (bus_id, start_time)
- `trip2`: CREATE INDEX trip2 ON public.trip_report USING btree (reg_no)
- `trip3`: CREATE INDEX trip3 ON public.trip_report USING btree (start_time)
## 🗂️ Table: `truein_data`

**📊 Rows:** 410297

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| drv_code | character varying | YES |
| log_date_time | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |
| latitude | double precision | YES |
| longitude | double precision | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `truein1`: CREATE INDEX truein1 ON public.truein_data USING btree (log_date_time)
- `truein2`: CREATE INDEX truein2 ON public.truein_data USING btree (drv_code)
## 🗂️ Table: `ul_driver_master`

**📊 Rows:** 3

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | text | YES |
| username | text | YES |
| password | text | YES |
| contact_no | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `ul_driver_master_pkey`: CREATE UNIQUE INDEX ul_driver_master_pkey ON public.ul_driver_master USING btree (id_no)
## 🗂️ Table: `ul_drv_app_token`

**📊 Rows:** 120

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| username | character varying | NO |
| auth_token | text | NO |
| refresh_token | text | YES |
| expiry_time | timestamp without time zone | YES |
| time_stamp | timestamp without time zone | YES |
| version | character varying | YES |
| cust_id | integer | YES |
| last_update_refresh | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `drv_app_token_pkey`: CREATE UNIQUE INDEX drv_app_token_pkey ON public.ul_drv_app_token USING btree (id_no)
## 🗂️ Table: `ul_drv_trip_details`

**📊 Rows:** 101

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| trip_id | integer | NO |
| drv_id | integer | YES |
| trip_start_at | timestamp without time zone | YES |
| lat | text | YES |
| lng | text | YES |
| trip_end_at | timestamp without time zone | YES |

### 🔐 Primary Keys
- trip_id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `ul_drv_trip_details_pkey`: CREATE UNIQUE INDEX ul_drv_trip_details_pkey ON public.ul_drv_trip_details USING btree (trip_id)
## 🗂️ Table: `ul_drv_trip_images`

**📊 Rows:** 116

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| trip_id | integer | YES |
| drv_id | integer | YES |
| trip_image | text | YES |
| time_stamp | timestamp without time zone | YES |
| lat | text | YES |
| lng | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `ul_drv_trip_images_pkey`: CREATE UNIQUE INDEX ul_drv_trip_images_pkey ON public.ul_drv_trip_images USING btree (id_no)
## 🗂️ Table: `unapplied_amount`

**📊 Rows:** 5614

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| customer_code | integer | YES |
| unapplied_amount | double precision | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `Unapplied_amount_pkey`: CREATE UNIQUE INDEX "Unapplied_amount_pkey" ON public.unapplied_amount USING btree (id_no)
## 🗂️ Table: `url_reg`

**📊 Rows:** 2411

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| site_id | integer | NO |
| reg_no | character varying | NO |
| plant_id | integer | YES |
| exp_time | timestamp without time zone | YES |

### 🔐 Primary Keys
- site_id, reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `url_reg_pkey`: CREATE UNIQUE INDEX url_reg_pkey ON public.url_reg USING btree (site_id, reg_no)
## 🗂️ Table: `user_feedback`

**📊 Rows:** 147793

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| username | character varying | YES |
| distid | integer | YES |
| email | character varying | YES |
| supply_plant | character varying | YES |
| cust_name | character varying | YES |
| cust_id | integer | YES |
| site_id | integer | YES |
| site_name | character varying | YES |
| contact_name | character varying | YES |
| contact_mob | character varying | YES |
| concrete_date | date | YES |
| start_time | time without time zone | YES |
| end_time | time without time zone | YES |
| mode | character varying | YES |
| pour_quantity | character varying | YES |
| grade | character varying | YES |
| delivery_schedule | character varying | YES |
| product_quality | character varying | YES |
| site_supervisor | integer | YES |
| tm_driver | integer | YES |
| fse | integer | YES |
| pumping_staff | integer | YES |
| order_taken | integer | YES |
| plant_staff | integer | YES |
| safety | integer | YES |
| overall_performance | integer | YES |
| suggestion | text | YES |
| recommend | character varying | YES |
| filled_by_email | character varying | YES |
| filled_time | timestamp without time zone | YES |
| update_time | timestamp without time zone | YES |
| status | character varying | YES |
| cc_emails | character varying | YES |
| plant_id | integer | YES |
| mobile_no | bigint | YES |
| otp | integer | YES |
| otp_status | character varying | YES |
| otp_time | timestamp without time zone | YES |
| non_sales_id | integer | YES |
| telerate | integer | YES |
| telerate_remarks | text | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `user_feedback_pkey`: CREATE UNIQUE INDEX user_feedback_pkey ON public.user_feedback USING btree (id)
- `feedback1`: CREATE INDEX feedback1 ON public.user_feedback USING btree (distid)
## 🗂️ Table: `user_type_master`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| user_type | integer | YES |
| name | character varying | YES |
| app_used | character varying | YES |
| linked_with | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `user_type_master_pkey`: CREATE UNIQUE INDEX user_type_master_pkey ON public.user_type_master USING btree (id_no)
## 🗂️ Table: `users`

**📊 Rows:** 1

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| username | character varying | NO |
| password_hash | character varying | NO |
| created_at | timestamp without time zone | YES |
| last_login | timestamp without time zone | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `users_pkey`: CREATE UNIQUE INDEX users_pkey ON public.users USING btree (id)
- `users_username_key`: CREATE UNIQUE INDEX users_username_key ON public.users USING btree (username)
## 🗂️ Table: `van_details`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_depo | integer | YES |
| reg_no | character varying | NO |
| vendor_id | integer | YES |
| var_mlg | double precision | YES |
| fixed_cost | character varying | YES |
| contract_type | integer | YES |
| var_mlg_hrs | double precision | YES |

### 🔐 Primary Keys
- reg_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `van_details_pkey`: CREATE UNIQUE INDEX van_details_pkey ON public.van_details USING btree (reg_no)
## 🗂️ Table: `veh_assigned_status`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| cur_status | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `pk`: CREATE UNIQUE INDEX pk ON public.veh_assigned_status USING btree (id_no)
## 🗂️ Table: `veh_maintain`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| veh_no | character varying | YES |
| from | date | YES |
| to | date | YES |
| purpose | text | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `veh_maintain_pkey`: CREATE UNIQUE INDEX veh_maintain_pkey ON public.veh_maintain USING btree (id)
## 🗂️ Table: `veh_stoppage_sms`

**📊 Rows:** 497

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| reg_no | character varying | NO |
| created_by | character varying | NO |
| mobile11 | character varying | NO |
| stop_time1 | integer | YES |
| stop_intr | integer | YES |
| mobile12 | character varying | YES |
| mobile13 | character varying | YES |
| mobile14 | character varying | YES |
| mobile15 | character varying | YES |
| stop_time2 | integer | YES |
| mobile21 | character varying | YES |
| mobile22 | character varying | YES |
| mobile23 | character varying | YES |
| mobile24 | character varying | YES |
| mobile25 | character varying | YES |
| stop_time3 | integer | YES |
| mobile31 | character varying | YES |
| mobile32 | character varying | YES |
| mobile33 | character varying | YES |
| mobile34 | character varying | YES |
| mobile35 | character varying | YES |
| plant_id | integer | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `veh_stoppage_sms_pkey`: CREATE UNIQUE INDEX veh_stoppage_sms_pkey ON public.veh_stoppage_sms USING btree (id)
## 🗂️ Table: `veh_type`

**📊 Rows:** 11

**🚗 Business Context:** Vehicle type lookup table defining different categories of vehicles (trucks, taxis, bulkers, etc.). Referenced by `vehicle_master.dept_no` for vehicle categorization.

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| name | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `veh_type_pkey`: CREATE UNIQUE INDEX veh_type_pkey ON public.veh_type USING btree (id_no)
## 🗂️ Table: `veh_volume`

**📊 Rows:** 6646

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| reg_no | character varying | NO |
| plant_id | integer | YES |
| date_tm | date | NO |
| tm_vol | double precision | YES |
| created_by | character varying | YES |
| tm_kms | double precision | YES |
| tm_trips | double precision | YES |
| tm_dry | double precision | YES |

### 🔐 Primary Keys
- reg_no, date_tm

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `veh_volume_pkey`: CREATE UNIQUE INDEX veh_volume_pkey ON public.veh_volume USING btree (reg_no, date_tm)
## 🗂️ Table: `vehicle_breakdown`

**📊 Rows:** 1312596

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_depo | integer | YES |
| reg_no | character varying | YES |
| from_dt | date | YES |
| from_tm | time without time zone | YES |
| to_dt | date | YES |
| to_tm | time without time zone | YES |
| bdown_reason | text | YES |
| bdown_hrs | bigint | YES |
| bdown_option | text | YES |
| time_stamp | timestamp without time zone | YES |
| veh_type | integer | YES |
| created_by | character varying | YES |
| vendor_id | integer | YES |
| status | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vehicle_breakdown_pkey`: CREATE UNIQUE INDEX vehicle_breakdown_pkey ON public.vehicle_breakdown USING btree (id_no)
- `vbd1`: CREATE INDEX vbd1 ON public.vehicle_breakdown USING btree (from_dt)
- `vbd2`: CREATE INDEX vbd2 ON public.vehicle_breakdown USING btree (reg_no)
## 🗂️ Table: `vehicle_breakdown_deleted`

**📊 Rows:** 71192

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_depo | integer | YES |
| reg_no | character varying | YES |
| from_dt | date | YES |
| from_tm | time without time zone | YES |
| to_dt | date | YES |
| to_tm | time without time zone | YES |
| bdown_reason | text | YES |
| bdown_hrs | bigint | YES |
| bdown_option | text | YES |
| time_stamp | timestamp without time zone | YES |
| veh_type | integer | YES |
| created_by | character varying | YES |
| vendor_id | integer | YES |
| status | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vehicle_breakdown_deleted_pkey`: CREATE UNIQUE INDEX vehicle_breakdown_deleted_pkey ON public.vehicle_breakdown_deleted USING btree (id_no)
- `vbd3`: CREATE INDEX vbd3 ON public.vehicle_breakdown_deleted USING btree (from_dt)
- `vbd4`: CREATE INDEX vbd4 ON public.vehicle_breakdown_deleted USING btree (reg_no)
## 🗂️ Table: `vehicle_breakdown_test`

**📊 Rows:** 73

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_depo | integer | YES |
| reg_no | character varying | YES |
| from_dt | date | YES |
| from_tm | time without time zone | YES |
| to_dt | date | YES |
| to_tm | time without time zone | YES |
| bdown_reason | text | YES |
| bdown_hrs | bigint | YES |
| bdown_option | text | YES |
| time_stamp | timestamp without time zone | YES |
| veh_type | integer | YES |
| created_by | character varying | YES |
| vendor_id | integer | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vehicle_breakdown_test_pkey`: CREATE UNIQUE INDEX vehicle_breakdown_test_pkey ON public.vehicle_breakdown_test USING btree (id_no)
## 🗂️ Table: `vehicle_location_shifting`

**📊 Rows:** 93

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| reg_no | character varying | YES |
| region | integer | YES |
| old_plant | integer | YES |
| shifting_date | date | YES |
| remarks | text | YES |
| billing_days | integer | YES |
| vts_id | integer | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vehicle_location_shifting_pkey`: CREATE UNIQUE INDEX vehicle_location_shifting_pkey ON public.vehicle_location_shifting USING btree (id_no)
## 🗂️ Table: `vehicle_master`

**📊 Rows:** 2234

**🚗 Business Context:** Vehicle master table - bottom level in the organizational hierarchy (Zone → District → Plant → Vehicle). Contains fleet management, device details, and vehicle categorization. Links to parent plants via `id_hosp`. The `dept_no` column links to `veh_type.id_no` to categorize vehicles by type (truck, taxi, bulker, etc.).

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| bus_id | integer | YES |
| reg_no | character varying | YES |
| gsm_no | bigint | YES |
| ip_addr | inet | YES |
| breakdown | character | YES |
| alarm_status | integer | YES |
| data_status | integer | YES |
| conn_status | integer | YES |
| disconnection_reason | character varying | YES |
| id_hosp | integer | YES |
| ver_no | character varying | YES |
| installed_date | date | YES |
| cha_no | character varying | YES |
| eng_no | character varying | YES |
| manufacture | character varying | YES |
| dept_no | integer | YES |
| model_no | integer | YES |
| remarks | text | YES |
| id_route | integer | YES |
| sms_enable | "char" | YES |
| master_update_flag | "char" | YES |
| master_updated_time | timestamp without time zone | YES |
| route_update_flag | "char" | YES |
| route_updated_time | timestamp without time zone | YES |
| veh_track_enable | "char" | YES |
| ack_no | integer | YES |
| install_status | "char" | YES |
| english_name | text | YES |
| regional_name | text | YES |
| cp_update_flag | "char" | YES |
| cp_updated_time | timestamp without time zone | YES |
| contact_name | character varying | YES |
| contact_no | bigint | YES |
| eta_generate | "char" | YES |
| reload_flag | "char" | YES |
| current_status | integer | YES |
| d_id | bigint | YES |
| c_id | bigint | YES |
| trip_id | integer | YES |
| trip_start_date | date | YES |
| fuel_installed | integer | YES |
| overspeed | integer | YES |
| batt_volt | integer | YES |
| generate_report | integer | YES |
| drum_sensor | integer | YES |
| vendor_id | integer | YES |
| drum_direction | integer | YES |
| device_id | integer | YES |
| fixed_cost | double precision | YES |
| tm_mileage | double precision | YES |
| dry_mileage | double precision | YES |
| ignition_status | integer | YES |
| capacity | double precision | YES |
| stand_weight | double precision | YES |
| time_stamp | timestamp without time zone | YES |
| last_installed_date | date | YES |
| expiry_date | date | YES |
| imei | character varying | YES |
| serial_no | character varying | YES |
| mfg_year | character varying | YES |
| assetid | character varying | YES |
| fasttag_id | text | YES |
| silo_sensor | integer | YES |
| drs_chk | character | YES |
| per_kms_amount | double precision | YES |
| mob_no | integer | YES |
| start_date | date | YES |
| end_date | date | YES |
| bill_stop_date | date | YES |
| shifting_remarks | text | YES |
| billing_type | character | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- dept_no → veh_type.id_no (Vehicle Type Category)
- id_hosp → hosp_master.id_no (Parent plant/facility in hierarchy)

### 🧭 Indexes
- `vehicle_master_bus_id_key`: CREATE UNIQUE INDEX vehicle_master_bus_id_key ON public.vehicle_master USING btree (bus_id)
- `vehicle_master_pkey`: CREATE UNIQUE INDEX vehicle_master_pkey ON public.vehicle_master USING btree (id_no)
- `vehicle_master_reg_no_key`: CREATE UNIQUE INDEX vehicle_master_reg_no_key ON public.vehicle_master USING btree (reg_no)
- `id_no`: CREATE INDEX id_no ON public.vehicle_master USING btree (id_no)
- `index_1`: CREATE INDEX index_1 ON public.vehicle_master USING btree (bus_id)
- `index_2`: CREATE INDEX index_2 ON public.vehicle_master USING btree (reg_no)
## 🗂️ Table: `vehicle_sharing`

**📊 Rows:** 410

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| id_depo | integer | YES |
| reg_no | character varying | YES |
| from_dt | date | YES |
| from_tm | time without time zone | YES |
| to_dt | date | YES |
| to_tm | time without time zone | YES |
| bdown_reason | text | YES |
| bdown_hrs | bigint | YES |
| bdown_option | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vehicle_sharing_pkey`: CREATE UNIQUE INDEX vehicle_sharing_pkey ON public.vehicle_sharing USING btree (id_no)
## 🗂️ Table: `vehicle_status`

**📊 Rows:** 6

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| veh_status | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vehicle_status_pkey`: CREATE UNIQUE INDEX vehicle_status_pkey ON public.vehicle_status USING btree (id_no)
## 🗂️ Table: `vehicle_status_type_new`

**📊 Rows:** 3

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id | integer | NO |
| type_code | text | YES |
| type_name | text | YES |

### 🔐 Primary Keys
- id

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vehicle_status_type_new_pkey`: CREATE UNIQUE INDEX vehicle_status_type_new_pkey ON public.vehicle_status_type_new USING btree (id)
## 🗂️ Table: `vendor_additional_setting`

**📊 Rows:** 305

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| vendor_id | integer | YES |
| region_id | integer | YES |
| erp_code | integer | YES |
| tax_details | text | YES |
| time_stamp | timestamp without time zone | YES |
| var_tax_details | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vendor_additional_setting_pkey`: CREATE UNIQUE INDEX vendor_additional_setting_pkey ON public.vendor_additional_setting USING btree (id_no)
- `vendor_additional_setting_region_id_erp_code_key`: CREATE UNIQUE INDEX vendor_additional_setting_region_id_erp_code_key ON public.vendor_additional_setting USING btree (region_id, erp_code)
## 🗂️ Table: `vendor_email`

**📊 Rows:** 54327

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_plant | integer | NO |
| date_entry | date | NO |
| email_type | character | NO |
| timestamp_entry | timestamp without time zone | YES |

### 🔐 Primary Keys
- id_plant, date_entry, email_type

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vendor_email_pkey`: CREATE UNIQUE INDEX vendor_email_pkey ON public.vendor_email USING btree (id_plant, date_entry, email_type)
## 🗂️ Table: `vendor_invoice_response`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| supplier_no | character varying | YES |
| invoice_no | character varying | YES |
| response | text | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `vendor_iocl_master`

**📊 Rows:** 133

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| vendor_id | integer | YES |
| iocl_card | bigint | NO |
| time_stamp | timestamp without time zone | YES |
| plant_code | character varying | YES |
| region_id | integer | YES |
| vendid | integer | YES |

### 🔐 Primary Keys
- iocl_card

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vendor_iocl_master_pkey`: CREATE UNIQUE INDEX vendor_iocl_master_pkey ON public.vendor_iocl_master USING btree (iocl_card)
## 🗂️ Table: `vendor_master`

**📊 Rows:** 469

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| vendor_name | character varying | YES |
| contact_no | numeric | YES |
| id_plant | integer | YES |
| vendor_code | character varying | YES |
| emailid | text | YES |
| sec_emailid | text | YES |
| iocl_card | character varying | YES |
| erp_code | character varying | YES |
| plant_code | character | YES |
| tax_detail | character varying | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vendor_master_pkey`: CREATE UNIQUE INDEX vendor_master_pkey ON public.vendor_master USING btree (id_no)
- `ven1`: CREATE INDEX ven1 ON public.vendor_master USING btree (id_no)
- `ven2`: CREATE INDEX ven2 ON public.vendor_master USING btree (id_plant)
## 🗂️ Table: `vendor_master1`

**📊 Rows:** 253

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| vendor_name | character varying | YES |
| vendor_code | character varying | YES |
| contact_no | bigint | YES |
| emailid | text | YES |
| sec_emailid | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vendor_master1_pkey`: CREATE UNIQUE INDEX vendor_master1_pkey ON public.vendor_master1 USING btree (id_no)
- `vendor_master1_vendor_name_key`: CREATE UNIQUE INDEX vendor_master1_vendor_name_key ON public.vendor_master1 USING btree (vendor_name)
## 🗂️ Table: `vendor_penalty`

**📊 Rows:** 9

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | YES |
| reason_type | character varying | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `vendor_penalty_detail`

**📊 Rows:** 3326

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| from_plt | integer | NO |
| reg_no | character varying | NO |
| dt_entry | date | YES |
| reason_typ | integer | YES |
| amount_dec | double precision | YES |
| created_by | character varying | YES |
| time_stamp | timestamp without time zone | NO |
| remarks | text | YES |
| vendor_id | integer | YES |
| idno | integer | NO |

### 🔐 Primary Keys
- from_plt, reg_no, time_stamp

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `vendor_penalty_detail_idno_key`: CREATE UNIQUE INDEX vendor_penalty_detail_idno_key ON public.vendor_penalty_detail USING btree (idno)
- `vendor_penalty_detail_pkey`: CREATE UNIQUE INDEX vendor_penalty_detail_pkey ON public.vendor_penalty_detail USING btree (reg_no, from_plt, time_stamp)
## 🗂️ Table: `vendor_tax_master`

**📊 Rows:** 6

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| tax_type | character varying | YES |
| tax_value | double precision | YES |
| description | character varying | YES |
| time_update | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `verify_erp_bill`

**📊 Rows:** 22

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| plantid | integer | YES |
| vendorid | integer | YES |
| fdate | date | YES |
| edate | date | YES |
| fixed_amt | double precision | YES |
| var_amt | double precision | YES |
| grdtot | double precision | YES |
| created_at | timestamp without time zone | NO |
| fixed_bill_no | character varying | YES |
| var_bill_no | character varying | YES |
| fixed_url | character varying | YES |
| var_url | character varying | YES |
| fixed_agree | integer | YES |
| var_agree | integer | YES |
| iocl_amt | double precision | YES |
| status | character varying | YES |
| iocl_status | integer | YES |
| fxd_invoice | date | YES |
| var_invoice | date | YES |
| fxd_status | character | YES |
| var_status | character | YES |
| ho_verify_status | character | YES |
| acct_verify_status | character | YES |
| verify_ho_user | character | YES |
| verify_acct_user | character | YES |
| ho_create_at | timestamp with time zone | YES |
| acct_create_at | timestamp with time zone | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `verify_erp_bill_pkey`: CREATE UNIQUE INDEX verify_erp_bill_pkey ON public.verify_erp_bill USING btree (id_no)
## 🗂️ Table: `violate_report`

**📊 Rows:** 1400608

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| reg_no | character varying | NO |
| start_time | timestamp without time zone | NO |
| end_time | timestamp without time zone | YES |
| duration | time without time zone | YES |
| max_speed | integer | YES |
| driver_id | integer | YES |
| lat | character varying | YES |
| lng | character varying | YES |

### 🔐 Primary Keys
- reg_no, start_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `violate_report_pkey`: CREATE UNIQUE INDEX violate_report_pkey ON public.violate_report USING btree (reg_no, start_time)
- `violate1`: CREATE INDEX violate1 ON public.violate_report USING btree (start_time)
- `violate2`: CREATE INDEX violate2 ON public.violate_report USING btree (reg_no)
## 🗂️ Table: `violate_report_50`

**📊 Rows:** 889577

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| reg_no | character varying | NO |
| start_time | timestamp without time zone | NO |
| end_time | timestamp without time zone | YES |
| duration | time without time zone | YES |
| max_speed | integer | YES |
| driver_id | integer | YES |

### 🔐 Primary Keys
- reg_no, start_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `violate_report_50_pkey`: CREATE UNIQUE INDEX violate_report_50_pkey ON public.violate_report_50 USING btree (reg_no, start_time)
- `viol_50_1`: CREATE INDEX viol_50_1 ON public.violate_report_50 USING btree (start_time)
- `viol_50_2`: CREATE INDEX viol_50_2 ON public.violate_report_50 USING btree (reg_no)
## 🗂️ Table: `violate_report_55`

**📊 Rows:** 327683

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| reg_no | character varying | NO |
| start_time | timestamp without time zone | NO |
| end_time | timestamp without time zone | YES |
| duration | time without time zone | YES |
| max_speed | integer | YES |
| driver_id | integer | YES |

### 🔐 Primary Keys
- reg_no, start_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `violate_report_55_pkey`: CREATE UNIQUE INDEX violate_report_55_pkey ON public.violate_report_55 USING btree (reg_no, start_time)
- `viol_55_1`: CREATE INDEX viol_55_1 ON public.violate_report_55 USING btree (start_time)
- `viol_55_2`: CREATE INDEX viol_55_2 ON public.violate_report_55 USING btree (reg_no)
## 🗂️ Table: `violate_report_60`

**📊 Rows:** 76813

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| reg_no | character varying | NO |
| start_time | timestamp without time zone | NO |
| end_time | timestamp without time zone | YES |
| duration | time without time zone | YES |
| max_speed | integer | YES |
| driver_id | integer | YES |

### 🔐 Primary Keys
- reg_no, start_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `violate_report_60_pkey`: CREATE UNIQUE INDEX violate_report_60_pkey ON public.violate_report_60 USING btree (reg_no, start_time)
- `viol_60_1`: CREATE INDEX viol_60_1 ON public.violate_report_60 USING btree (start_time)
- `viol_60_2`: CREATE INDEX viol_60_2 ON public.violate_report_60 USING btree (reg_no)
## 🗂️ Table: `violate_report_65`

**📊 Rows:** 13427

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| bus_id | integer | YES |
| reg_no | character varying | NO |
| start_time | timestamp without time zone | NO |
| end_time | timestamp without time zone | YES |
| duration | time without time zone | YES |
| max_speed | integer | YES |
| driver_id | integer | YES |

### 🔐 Primary Keys
- reg_no, start_time

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `violate_report_65_pkey`: CREATE UNIQUE INDEX violate_report_65_pkey ON public.violate_report_65 USING btree (reg_no, start_time)
- `viol_65_1`: CREATE INDEX viol_65_1 ON public.violate_report_65 USING btree (start_time)
- `viol_65_2`: CREATE INDEX viol_65_2 ON public.violate_report_65 USING btree (reg_no)
## 🗂️ Table: `weighbridge_master`

**📊 Rows:** 718212

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| tm_no | character varying | YES |
| location_code | character varying | YES |
| date_time | timestamp without time zone | YES |
| tare_weight | double precision | YES |
| time_stamp | timestamp without time zone | YES |
| tm_load | character | YES |
| id_no | integer | NO |
| gross_weight | double precision | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `whole_corrupt_packet`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| ip_address | character varying | YES |
| raw_string | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `whole_data_packet`

**📊 Rows:** 2555

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| raw_string | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `RAW1`: CREATE INDEX "RAW1" ON public.whole_data_packet USING btree (raw_string)
- `raw2`: CREATE INDEX raw2 ON public.whole_data_packet USING btree (time_stamp)
## 🗂️ Table: `whole_id_packet`

**📊 Rows:** 9865

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| raw_string | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `whole_repo_packet`

**📝 Comment:** Stores the trip start and trip end report packet string 

**📊 Rows:** 1586

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| raw_string | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `whole_stop_data_packet`

**📝 Comment:** store regular data packet of display

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| box_no | integer | YES |
| data_packet | text | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `whole_stop_id_packet`

**📊 Rows:** 0

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| raw_string | character varying | YES |
| time_stamp | timestamp without time zone | YES |

### 🔐 Primary Keys
- None

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- None
## 🗂️ Table: `working_status`

**📊 Rows:** 197048

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| sr_no | integer | NO |
| depo_id | integer | YES |
| inst_total | integer | YES |
| work_total | integer | YES |
| remark | text | YES |
| date_entry | date | YES |
| uncondition | integer | YES |
| tot_rdc | integer | YES |
| tm_type | integer | YES |
| oth_type | integer | YES |
| tm_detail | text | YES |
| tm1_detail | text | YES |
| tm2_detail | text | YES |
| cnt1 | integer | YES |
| cnt2 | integer | YES |
| cnt3 | integer | YES |

### 🔐 Primary Keys
- sr_no

### 🔗 Foreign Keys
- None

### 🧭 Indexes
- `working_status_date_entry_key`: CREATE UNIQUE INDEX working_status_date_entry_key ON public.working_status USING btree (date_entry, depo_id)
- `working_status_pkey`: CREATE UNIQUE INDEX working_status_pkey ON public.working_status USING btree (sr_no)
- `work1`: CREATE INDEX work1 ON public.working_status USING btree (date_entry, depo_id)
## 🗂️ Table: `zone_master`

**📊 Rows:** 1

**🌍 Business Context:** Zone master table - highest level in the organizational hierarchy. Defines geographical zones for business operations. Each zone contains multiple districts/regions.

### Columns
| Column Name | Data Type | Is Nullable |
|-------------|-----------|-------------|
| id_no | integer | NO |
| zone_name | character varying | YES |
| cont_no | character varying | YES |
| email_id | character varying | YES |
| remarks | text | YES |

### 🔐 Primary Keys
- id_no

### 🔗 Foreign Keys
- None (Top level in hierarchy)

### 🔗 Referenced By (Hierarchical Children)
- district_master.id_zone → zone_master.id_no (Districts/Regions under this zone)

### 🧭 Indexes
- None

import psycopg2
import os
from dotenv import load_dotenv
import datetime
import streamlit as st

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("hostname", "localhost"),
        dbname=os.getenv("dbname", "rdc_dump"),
        user=os.getenv("user_name", "postgres"),
        password=os.getenv("password", "Akshit@123"),
        port=5432
    )

# Add persistent debug log to Streamlit sidebar
if 'debug_log' not in st.session_state:
    st.session_state['debug_log'] = []

def run_query(query):
    try:
        debug_msg = f"[DEBUG] SQL Query: {query}"
        print(f"\n{debug_msg}\n", flush=True)
        st.session_state['debug_log'].append(debug_msg)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        debug_msg2 = f"[DEBUG] Rows returned: {len(rows)}"
        print(f"{debug_msg2}\n", flush=True)
        st.session_state['debug_log'].append(debug_msg2)
        cur.close()
        conn.close()
        return columns, rows
    except Exception as e:
        err_msg = f"❌ SQL Execution Error: {e}"
        print(err_msg, flush=True)
        st.session_state['debug_log'].append(err_msg)
        raise

def get_text_columns(schema=None, table=None):
    """Return all text/varchar columns in the database or filtered by schema/table."""
    query = """
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE data_type IN ('text', 'character varying', 'character')
        AND table_schema NOT IN ('information_schema', 'pg_catalog')
    """
    if schema:
        query += f" AND table_schema = '{schema}'"
    if table:
        query += f" AND table_name = '{table}'"

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ Failed to fetch text columns:", e)
        return []

def get_primary_key_column(schema, table):
    """Returns the primary key column of a table if available, otherwise None."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = """
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY'
              AND tc.table_schema = %s
              AND tc.table_name = %s;
        """
        cur.execute(query, (schema, table))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"❌ Failed to get primary key for {schema}.{table}:", e)
        return None

def fix_encoding_for_column(schema, table, column, id_column="id", corruption_regex=None):
    """
    Fix encoding issues in a single column.
    If corruption_regex is provided, it will filter values using it.
    """
    fixed_count = 0
    try:
        conn = get_connection()
        cur = conn.cursor()

        full_table = f'"{schema}"."{table}"'
        corruption_clause = f"WHERE {column} ~ '{corruption_regex}'" if corruption_regex else ""

        query = f"""
            SELECT {id_column}, {column}
            FROM {full_table}
            {corruption_clause};
        """

        cur.execute(query)
        rows = cur.fetchall()

        for row_id, bad_value in rows:
            if not isinstance(bad_value, str):
                continue
            try:
                fixed_value = bad_value.encode('latin1').decode('utf-8')
                if fixed_value != bad_value:
                    cur.execute(
                        f"UPDATE {full_table} SET {column} = %s WHERE {id_column} = %s",
                        (fixed_value, row_id)
                    )
                    fixed_count += 1
            except UnicodeDecodeError:
                continue 

        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Fixed {fixed_count} entries in {schema}.{table}.{column}")
    except Exception as e:
        print(f"❌ Error processing {schema}.{table}.{column}:", e)

def fix_all_encoding_issues(corruption_regex="Ã|â€™|â€“|â€œ|â€|Ãƒ"):
    """
    Run fix_encoding_for_column on all text/varchar/char columns in all tables.
    `corruption_regex` can be changed or set to None for full scan.
    """
    columns_info = get_text_columns()
    for schema, table, column in columns_info:
        id_column = get_primary_key_column(schema, table)
        if id_column:
            fix_encoding_for_column(schema, table, column, id_column, corruption_regex)
        else:
            print(f"Skipping {schema}.{table} - no suitable primary key found.")

def get_full_schema():
    """
    Returns a dictionary of all tables and their columns for all user schemas.
    Example: { 'public': { 'film': ['film_id', 'title', ...], ... }, ... }
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT table_schema, table_name, column_name
            FROM information_schema.columns
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name, ordinal_position
        """)
        schema = {}
        for table_schema, table_name, column_name in cur.fetchall():
            if table_schema not in schema:
                schema[table_schema] = {}
            if table_name not in schema[table_schema]:
                schema[table_schema][table_name] = []
            schema[table_schema][table_name].append(column_name)
        cur.close()
        conn.close()
        return schema
    except Exception as e:
        print("❌ Failed to fetch schema:", e)
        return {}

def print_schema(schema):
    for schema_name, tables in schema.items():
        print(f"Schema: {schema_name}")
        for table, columns in tables.items():
            print(f"  Table: {table} (" + ", ".join(columns) + ")")

def get_column_types(schema=None, table=None):
    """
    Returns column data types for validation.
    Returns dict: {schema.table.column: data_type}
    """
    query = """
        SELECT table_schema, table_name, column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
    """
    
    if schema:
        query += f" AND table_schema = '{schema}'"
    if table:
        query += f" AND table_name = '{table}'"
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        # Return dictionary with full column path and data type
        return {f"{row[0]}.{row[1]}.{row[2]}": row[3] for row in rows}
    except Exception as e:
        print("❌ Failed to fetch column types:", e)
        return {}

def get_numeric_columns(schema=None, table=None):
    """Return all numeric columns in the database."""
    query = """
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE data_type IN ('integer', 'bigint', 'smallint', 'decimal', 'numeric', 'real', 'double precision', 'money')
        AND table_schema NOT IN ('information_schema', 'pg_catalog')
    """
    
    if schema:
        query += f" AND table_schema = '{schema}'"
    if table:
        query += f" AND table_name = '{table}'"

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("❌ Failed to fetch numeric columns:", e)
        return []

if __name__ == "__main__":
    schema = get_full_schema()
    print_schema(schema)

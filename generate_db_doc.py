import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("hostname", "localhost"),
        dbname=os.getenv("dbname", "pagila"),
        user=os.getenv("user_name", "support"),
        password=os.getenv("password", "Akshit@123"),
        port=5432
    )

def generate_markdown():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()

    markdown = "# 📘 PostgreSQL Database Documentation (With Full Data)\n\n"

    for table in tables:
        table_name = table[0]
        markdown += f"## 🗂️ Table: `{table_name}`\n\n"

        # Table comment
        cursor.execute("SELECT obj_description(%s::regclass, 'pg_class');", (table_name,))
        comment = cursor.fetchone()[0]
        if comment:
            markdown += f"**📝 Comment:** {comment}\n\n"

        # Row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        row_count = cursor.fetchone()[0]
        markdown += f"**📊 Rows:** {row_count}\n\n"

        # Column definitions
        markdown += "### Columns\n"
        markdown += "| Column Name | Data Type | Is Nullable |\n"
        markdown += "|-------------|-----------|-------------|\n"
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s;
        """, (table_name,))
        columns = cursor.fetchall()
        for col in columns:
            markdown += f"| {col[0]} | {col[1]} | {col[2]} |\n"

        # Primary keys
        markdown += "\n### 🔐 Primary Keys\n"
        cursor.execute("""
            SELECT a.attname
            FROM pg_index i
            JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = %s::regclass AND i.indisprimary;
        """, (table_name,))
        pks = cursor.fetchall()
        markdown += "- " + ", ".join(pk[0] for pk in pks) if pks else "- None"
        markdown += "\n"

        # Foreign keys
        markdown += "\n### 🔗 Foreign Keys\n"
        cursor.execute("""
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table,
                ccu.column_name AS foreign_column
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s;
        """, (table_name,))
        fks = cursor.fetchall()
        if fks:
            for fk in fks:
                markdown += f"- `{fk[0]}` → `{fk[1]}.{fk[2]}`\n"
        else:
            markdown += "- None\n"

        # Indexes
        markdown += "\n### 🧭 Indexes\n"
        cursor.execute("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = %s;
        """, (table_name,))
        indexes = cursor.fetchall()
        if indexes:
            for index in indexes:
                markdown += f"- `{index[0]}`: {index[1]}\n"
        else:
            markdown += "- None\n"

        # Full data
        markdown += "\n### 📄 Full Table Data\n"
        try:
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

            if rows:
                markdown += "| " + " | ".join(col_names) + " |\n"
                markdown += "| " + " | ".join("---" for _ in col_names) + " |\n"
                for row in rows:
                    row_str = [str(item) if item is not None else "NULL" for item in row]
                    markdown += "| " + " | ".join(row_str) + " |\n"
            else:
                markdown += "_No data available._\n"

        except Exception as e:
            markdown += f"_Error fetching data: {e}_\n"

        markdown += "\n---\n\n"

    cursor.close()
    conn.close()

    with open("database_reference.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    print("✅ Markdown file 'database_reference.md' generated successfully!")

if __name__ == "__main__":
    generate_markdown()

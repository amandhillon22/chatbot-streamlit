import requests
import csv
import re

API_URL = "http://localhost:8501/chat"  # Adjust if needed

def load_reference_tables(md_path):
    tables = {}
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()
    current_table = None
    headers = []
    for line in lines:
        if line.startswith("## "):
            current_table = line.strip("# \n")
            tables[current_table] = []
            headers = []
        elif line.startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            if not headers:
                headers = cells
            else:
                tables[current_table].append(dict(zip(headers, cells)))
    return tables

def find_expected_answer(question, tables):
    q = question.lower()
    for table, rows in tables.items():
        for row in rows:
            for value in row.values():
                if value and value.lower() in q:
                    return value
    return None

def run_tests():
    tables = load_reference_tables("database_reference.md")
    with open("test_questions.csv", newline='', encoding='utf-8') as f, \
         open("test_report.csv", "w", newline='', encoding='utf-8') as out:
        reader = csv.reader(f)
        writer = csv.writer(out)
        writer.writerow(["question", "gemini_answer", "expected", "result"])
        for row in reader:
            question = row[0].strip('"')
            resp = requests.post(API_URL, json={"user_input": question})
            answer = resp.json().get("response", "")
            expected = find_expected_answer(question, tables)
            if expected and expected.lower() in answer.lower():
                result = "PASS"
            else:
                result = "FAIL"
            writer.writerow([question, answer, expected or "N/A", result])
            print(f"Q: {question}\nA: {answer}\nExpected: {expected}\nResult: {result}\n{'-'*60}")

if __name__ == "__main__":
    run_tests()

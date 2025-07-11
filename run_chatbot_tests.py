import requests
import csv
import re

API_URL = "http://localhost:8501/chat"  # Adjust if needed

def run_tests():
    with open("test_questions.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        results = []
        for i, row in enumerate(reader, 1):
            question = row["question"]
            expected_pattern = row.get("expected_pattern", "")
            resp = requests.post(API_URL, json={"user_input": question})
            answer = resp.json().get("response", "")
            match = bool(re.search(expected_pattern, answer, re.IGNORECASE)) if expected_pattern else "N/A"
            results.append({
                "question": question,
                "answer": answer,
                "expected_pattern": expected_pattern,
                "match": match
            })
            print(f"Test {i}: {'PASS' if match or match=='N/A' else 'FAIL'}")
            print(f"Q: {question}\nA: {answer}\nExpected: {expected_pattern}\n{'-'*60}")

    # Optionally, write results to a markdown report
    with open("test_report.md", "w", encoding="utf-8") as report:
        report.write("# Chatbot Test Report\n\n")
        for r in results:
            report.write(f"## Q: {r['question']}\n")
            report.write(f"**Expected Pattern:** `{r['expected_pattern']}`\n\n")
            report.write(f"**Answer:**\n```")
            report.write(f"{r['answer']}\n")
            report.write("```\n")
            report.write(f"**Match:** {'PASS' if r['match'] or r['match']=='N/A' else 'FAIL'}\n\n---\n")

if __name__ == "__main__":
    run_tests()

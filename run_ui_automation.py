import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Updated selectors and URL for your custom frontend
CHAT_URL = "http://localhost:8501/frontend_new/index.html"
INPUT_SELECTOR = "#inputField"
SEND_BUTTON_SELECTOR = "#sendBtn"
RESPONSE_CONTAINER_SELECTOR = ".chat-messages"  # Update if needed


def run_ui_automation():
    driver = webdriver.Chrome()  # or webdriver.Firefox()
    driver.get(CHAT_URL)
    time.sleep(3)  # Wait for page to load

    results = []
    with open("test_questions.csv", newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            question = row[0].strip('"')
            # Find the input box and type the question
            input_box = driver.find_element(By.CSS_SELECTOR, INPUT_SELECTOR)
            input_box.clear()
            input_box.send_keys(question)
            time.sleep(0.5)
            # Click the send button
            send_btn = driver.find_element(By.CSS_SELECTOR, SEND_BUTTON_SELECTOR)
            send_btn.click()
            # Wait for response to appear (adjust as needed)
            time.sleep(5)
            # Get the last bot response
            try:
                chat_messages = driver.find_element(By.CSS_SELECTOR, ".chat-messages")
                bot_responses = chat_messages.find_elements(By.CSS_SELECTOR, ".bot-message")
                if bot_responses:
                    response = bot_responses[-1].text.strip()
                else:
                    response = "(No response found)"
            except Exception:
                response = "(Error reading response)"
            print(f"Q: {question}\nA: {response}\n{'-'*40}")
            results.append((question, response))

    driver.quit()

    # Save results to a markdown file
    with open("ui_test_report.md", "w", encoding="utf-8") as out:
        out.write("# Chatbot UI Automation Test Report\n\n")
        for q, a in results:
            out.write(f"## Q: {q}\n")
            out.write(f"**A:**\n```\n{a}\n```\n\n---\n")

if __name__ == "__main__":
    run_ui_automation()

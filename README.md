# 🤖 AI Agent for Automated Website Testing (Enterprise Edition)

This is an **Advanced AI-Powered Web Automation Agent** designed to execute end-to-end testing using Natural Language Instructions. Unlike traditional testing frameworks that require writing code, this agents listens to simple text commands, executes them on a real browser, and generates professional PDF/JSON reports.

It features **Self-Healing Capabilities**, **Visual Reporting**, and a **Persistent History Database**, making it a robust tool for QA Automation.

---

## 🚀 Key Features

### 1. 🧠 Smart Automation Engine
*   **Natural Language Processing**: Parses human-readable commands like `CLICK "Login"` or `TYPE "user" INTO "Username"`.
*   **Playwright Integration**: Uses Microsoft Playwright for high-speed, reliable browser automation.

### 2. 🏥 Self-Healing AI
*   **Fuzzy Matching**: If a button text changes slightly (e.g., "Sign In" -> "Log In") or has a dynamic ID, the agent uses `difflib` similarity matching to find the closest element instead of failing.
*   **Smart Visibility**: Automatically filters out hidden elements to interact only with what the user sees (fixes issues with mobile menus on desktop sites).

### 3. 📊 Comprehensive Reporting
*   **Screenshot-on-Every-Step**: Captures screenshots for every passed or failed action.
*   **PDF Test Reports**: Generates a professional PDF containing execution logs and embedded screenshots.
*   **Frontend Gallery**: View screenshots directly in the Streamlit UI.

### 4. 🗄️ Database & History
*   **SQLite Integration**: Automatically saves every test run into `test_history.db`.
*   **Analytics Dashboard**: The "History" tab shows detailed metrics:
    *   Pass/Fail Status
    *   Execution Time
    *   Pass Percentage (📈)
    *   Total Steps

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | **Streamlit** | Interactive UI for running tests and viewing history. |
| **Backend** | **Flask** | REST API handling requests, database logic, and file serving. |
| **Core Engine** | **Playwright (Python)** | Headless browser automation. |
| **Database** | **SQLite** | Lightweight, file-based database for persistence. |
| **Report Engine** | **ReportLab** | PDF generation library. |
| **Self-Healing** | **Difflib** | Python standard library for fuzzy string matching. |

---

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <repo-url>
    cd ai-agent-testing
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r backend/requirements.txt
    pip install streamlit
    ```

3.  **Initialize Playwright Browsers**
    ```bash
    playwright install
    ```

4.  **Run the Application**
    *   **Step 1: Start Backend** (Terminal 1)
        ```bash
        python backend/app.py
        ```
    *   **Step 2: Start Frontend** (Terminal 2)
        ```bash
        streamlit run frontend/app.py
        ```

5.  **Access the UI**
    *   Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📖 How to Use (Supported Commands)

The agent uses a **Strict Keyword Parser** for reliability. Use the following syntax in the text area:

| Command | Usage | Example |
| :--- | :--- | :--- |
| **GOTO** | Opens a website | `GOTO "https://www.google.com"` |
| **CLICK** | Clicks a button/link | `CLICK "Login"` |
| **TYPE** | Types text into a specific input | `TYPE "admin" INTO "Username"` |
| **SEARCH** | Finds the generic search bar & searches | `SEARCH "Laptop"` |
| **VERIFY** | Checks if text exists on the page | `VERIFY "Welcome User"` |

---

## 🧪 Test Case Examples

### ✅ 1. Passing Scenario (Login Flow)
*Use this to test the `TYPE` command and Form Filling.*
```text
1. GOTO "https://www.saucedemo.com"
2. TYPE "standard_user" INTO "Username"
3. TYPE "secret_sauce" INTO "Password"
4. CLICK "Login"
5. VERIFY "Products"
```

### ❌ 2. Failing Scenario (Verification Error)
*Use this to test Screenshot capturing on Failure.*
```text
1. GOTO "https://www.saucedemo.com"
2. TYPE "locked_out_user" INTO "Username"
3. TYPE "secret_sauce" INTO "Password"
4. CLICK "Login"
5. VERIFY "Welcome"
```
*(This fails because the user is locked out, and "Welcome" is not shown.)*

### 🏥 3. Self-Healing Scenario (Fuzzy Match)
*Use this to test the AI's ability to find buttons even if the text isn't exact.*
```text
1. GOTO "https://www.saucedemo.com/inventory.html"
2. CLICK "Add to cart"  
```
*(If the button says "ADD TO CART" (uppercase), the fuzzy matcher will still find it.)*

---

## 📂 Project Structure

```
/backend
    /agent
        executor.py     # Core Playwright Logic (Run Tests)
        parser.py       # Parses Text -> JSON Instructions
        generator.py    # Maps JSON -> Playwright Actions
        reporter.py     # Generates PDF/JSON Reports
    /utils
        dom_mapper.py   # Smart Element Selector (Finds visible inputs)
        healing.py      # AI Self-Healing Logic
    app.py              # Flask API Entry Point
    database.py         # SQLite Database Handler
    requirements.txt    # Python Dependencies

/frontend
    app.py              # Streamlit UI (History, Runner, Visuals)

/docs
    api.md              # API Documentation
```

---

## 🔮 Future Scope
1.  **Visual Regression**: Compare screenshots against a "Golden Baseline" to detect UI bugs.
2.  **LLM Integration**: Re-integrate GPT-4 for "Generic Intent" parsing (e.g., "Buy me a milk") instead of strict commands.
3.  **Cloud Execution**: Run tests in Docker containers or AWS Lambda.

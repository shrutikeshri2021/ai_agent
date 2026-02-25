# 📘 Comprehensive Project Guide: AI Agent for Automated Website Testing

## 1. Project Overview
The **AI Agent for Automated Website Testing** is a next-generation Quality Assurance (QA) tool. It replaces brittle, code-heavy automation scripts (like Selenium/Cypress) with an **Intelligent Agent** that understands plain English. 

Instead of writing `driver.findElement(By.id("btn-login")).click()`, a user simply types:
> *"Go to the login page, enter my credentials, and verify the dashboard loads."*

The system is designed to be **Self-Healing**, meaning it automatically adapts to changes in the website's structure (DOM), drastically reducing ongoing maintenance costs.

---

## 2. Core Problem & Solution

### The Problem: Brittleness in Test Automation
Traditional automation relies on "Selectors" (CSS IDs, Class Names, XPaths). 
*   **Scenario**: A developer changes a button from `<button id="submit">` to `<div class="btn-primary">`.
*   **Result**: The automated test fails immediately. The QA engineer must spend hours debugging and updating scripts.

### The Solution: AI + Semantic Search
Our agent doesn't just look for "IDs". It mimics human behavior:
1.  **Intent Understanding**: Uses an LLM (Llama 3 via Groq) to understand *what* the user wants to do, not just *how* to do it.
2.  **Visual Healing**: If the exact element isn't found, the `healing.py` module scans the page for the *closest matching element* using fuzzy string matching and attribute analysis. It "heals" the broken test on the fly.

---

## 3. Architecture Deep Dive

The project follows a decoupled **Client-Server Architecture**.

### 🎨 Frontend (The Face)
*   **Tech**: Streamlit (Python)
*   **Role**: Provides the User Interface.
*   **Key Components**:
    *   **Input Area**: Accepts natural language test scripts.
    *   **Live Runner**: Shows real-time status of each step (Pass/Fail).
    *   **Protocol Gallery**: Displays screenshots of every action taken.
    *   **Sidebar**: Manages API Keys and History.

### 🧠 Backend (The Brain)
*   **Tech**: Flask (Python)
*   **Role**: Orchestrates the entire testing lifecycle.
*   **Workflow**:
    1.  Receives text command from Frontend.
    2.  Passes text to the **Agent Graph**.

### 🔗 The Agent (The Logic)
The agent is built on **LangGraph** (a stateful graph library built on top of LangChain).
1.  **Parser Node**: 
    *   Primary: **LLM Parser** (`llm_agent.py`) -> Uses Groq/Llama-3 to convert text into JSON (e.g., `{"action": "click", "value": "Login"}`).
    *   Fallback: **Regex Parser** (`parser.py`) -> If the LLM causes an error or no key is provided, a strict keyword parser takes over.
2.  **Executor Node** (`executor.py`):
    *   Iterates through the JSON steps.
    *   Uses **Playwright** to drive the browser.
    *   Handling:
        *   `open`: Navigates to a URL.
        *   `click`: Attempts to find an element. If failed -> **Triggers Healing**.
        *   `type`: Enters text into inputs.
    *   **Evidence Collection**: Takes a screenshot after *every* step.

### 🏥 The Healer (The Safety Net)
Located in `backend/utils/healing.py`.
*   **Trigger**: When Playwright throws a `TimeoutError` or `ElementNotFound` exception.
*   **Process**:
    1.  Scrapes *all* interactive elements currently visible on the page.
    2.  Extracts their text, `aria-label`, `placeholder`, and `title`.
    3.  Uses `difflib.get_close_matches` to find the element most similar to the user's intent.
    4.  Returns the new locator to the Executor to retry the action.

### 📄 The Reporter (The Evidence)
Located in `backend/agent/reporter.py`.
*   **Output**: A PDF (`test_report.pdf`) and JSON file.
*   **Content**: A step-by-step log including:
    *   Action Name
    *   Target Element
    *   Status (PASS/FAIL)
    *   Embedded Screenshot of the result.

---

## 4. End-to-End Data Flow

Let's trace a request: **"Search for 'Laptops' on Amazon."**

1.  **User** types the instruction in Streamlit.
2.  **Streamlit** sends a POST request to `http://127.0.0.1:5000/run`.
3.  **Flask** calls `run_agent()`.
4.  **LLM Agent** (Groq) interprets the text:
    ```json
    [
      {"action": "open", "value": "https://www.amazon.com"},
      {"action": "type", "value": "Laptops", "target": "Search"},
      {"action": "click", "value": "Go"}
    ]
    ```
5.  **Executor** starts a Playwright browser instance.
    *   **Step 1**: Opens Amazon. *Success*. Screenshot taken.
    *   **Step 2**: Looks for an input named "Search". *Found*. Types "Laptops". Screenshot taken.
    *   **Step 3**: Looks for a button named "Go". *Not Found*.
        *   **Healing Triggered**: Scans page. Finds `<input type="submit" value="Go">`. Match found!
        *   **Action Retried**: Clicks the healed element. *Success*.
6.  **Reporter** compiles the 3 screenshots into a PDF.
7.  **Flask** returns the JSON report to Streamlit.
8.  **Streamlit** renders the success message and offers the PDF download.

---

## 5. Detailed Feature List

| Feature | Description | File Reference |
| :--- | :--- | :--- |
| **Natural Language Parsing** | Compiles free-text into machine instructions. Supports "Click", "Type", "Scroll", "Wait", "Verify". | `backend/agent/llm_agent.py` |
| **Self-Healing Selectors** | Automatically recovers from UI changes using fuzzy logic. | `backend/utils/healing.py` |
| **Visual Evidence** | Captures screenshots for 100% of steps (Pass & Fail) for audit trails. | `backend/agent/executor.py` |
| **PDF Reporting** | Generates business-ready PDF reports with embedded images. | `backend/agent/reporter.py` |
| **History Database** | SQLite database tracks pass rates and historic run data. | `backend/database.py` |
| **Hybrid Parsing** | Switches between LLM (AI) and Regex (Rule-based) parsing for reliability. | `backend/agent/graph.py` |

---

## 6. Supported Actions (Cheatsheet)

The agent supports the following atomic actions, which can be combined infinitely:

1.  **Open / Goto**: `GOTO "url"` - Launch the browser.
2.  **Click**: `CLICK "text"` - Click buttons, links, or images.
3.  **Type**: `TYPE "text" INTO "field"` - Fill forms.
4.  **Search**: `SEARCH "query"` - Special helper for search bars.
5.  **Hover**: `HOVER "element"` - Triggers dropdowns or tooltips.
6.  **Scroll**: `SCROLL "up/down"` - Moves the viewport.
7.  **Wait**: `WAIT 5` - Hard pause (useful for animations).
8.  **Verify**: `VERIFY "text"` - Asserts that specific text is visible on the page.
9.  **Play**: `PLAY "video"` - Clicks play buttons on media players.

---

## 7. Technical Requirements

*   **Python**: 3.10 or higher.
*   **RAM**: 4GB+ (Browser automation is memory intensive).
*   **Operating System**: Windows, MacOS, or Linux.
*   **Network**: Active internet connection (for Groq API & fetching websites).
*   **API Key**: A valid Groq API key is required for the LLM features (Free tier available).

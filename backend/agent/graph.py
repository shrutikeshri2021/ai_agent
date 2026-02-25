from agent.parser import parse_instruction
from agent.generator import generate_playwright_steps
from agent.executor import run_test
from agent.reporter import generate_pdf_report, generate_report

import os

# Updated to use environment variable for security
DEFAULT_API_KEY = os.environ.get("GROQ_API_KEY")

def run_agent(user_input, api_key=None):
    parsed = []
    
    # Use hardcoded key if user didn't provide one
    if not api_key:
        api_key = DEFAULT_API_KEY
    
    llm_error = None
    # 1. Try LLM Parsing if Key is provided
    # Updated: Allow both 'sk-' (OpenAI) and 'gsk_' (Groq) or just check if key exists
    if api_key and len(api_key) > 10:
        try:
            from agent.llm_agent import parse_with_llm
            print("🧠 using LLM Parser (Groq/OpenAI)...")
            parsed = parse_with_llm(user_input, api_key)
            if not parsed:
                print("⚠️ LLM returned empty steps. Parsing manually.")
        except Exception as e:
            llm_error = str(e)
            print(f"⚠️ LLM Crashed: {e}")
            parsed = [] # Reset to trigger fallback
    else:
        print("ℹ️ No API Key provided. Using Regex Parser.")

    # 2. Handle Critical LLM Errors (Quota/Auth) - Do NOT fallback to Regex
    # Updated to include Groq specific error messages if possible, though '429' is standard
    if llm_error and ("insufficient_quota" in llm_error or "invalid_api_key" in llm_error or "429" in llm_error or "401" in llm_error):
         print("❌ Aborting due to Critical LLM Error")
         return {
             "summary": {"total_steps": 0, "passed": 0, "failed": 1, "pass_percentage": 0},
             "steps": [{
                 "step_no": 1, 
                 "action": "LLM_ERROR", 
                 "target": "LLM Provider API",
                 "status": "FAIL", 
                 "error": f"LLM Account Error (Quota/Auth): {llm_error}. Please check your API key and billing.",
                 "screenshot": None
             }],
             "logs": [f"Critical LLM Failure: {llm_error}"]
         }

    # 3. Fallback to Regex if LLM failed (non-critical) or yielded no steps
    if not parsed:
        print("⚠️ Falling back to Rule-Based (Regex) logic...")
        parsed = parse_instruction(user_input)
        print(f"📋 Regex Parsed Steps: {len(parsed)}")
        
    steps = generate_playwright_steps(parsed)
    results, logs = run_test(steps)
    report = generate_report(results, logs)
    generate_pdf_report(report)

    return report

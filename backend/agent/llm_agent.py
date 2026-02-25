import json
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def parse_with_llm(instruction, api_key):
    """
    Uses Groq (free + fast) to convert natural language instructions into
    structured JSON steps for the automation agent.
    """
    if not api_key:
        raise ValueError("API Key is required for LLM features.")

    # Initialize LLM with Groq
    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0,
        api_key=api_key
    )

    # Define the schema we want
    format_instructions = """
    You are an automation parsing engine. Convert the user's natural language text into a JSON array of execution steps.
    
    Valid Actions:
    1. "open"   -> {"action": "open", "value": "Full URL (must match https://...)"}
    2. "click"  -> {"action": "click", "value": "Button/Link Text"}
    3. "type"   -> {"action": "type", "value": "Text to type", "target": "Input Field Name/Label"}
    4. "search" -> {"action": "search", "value": "Query"} (Use this if user just says 'Search for X' without specifying a field)
    5. "verify" -> {"action": "verify", "value": "Text to expect"}
    6. "wait"   -> {"action": "wait", "value": int_seconds}
    7. "scroll" -> {"action": "scroll", "value": "up/down"}
    8. "hover"  -> {"action": "hover", "value": "Element Text"}
    9. "select" -> {"action": "select", "value": "Option", "target": "Dropdown Label"}
    10. "play"  -> {"action": "play", "value": "Video Title or 'first video'"} (Use this when user says 'Play video', 'Watch it', or 'Play it')

    RULES:
    - Return ONLY the JSON list.
    - Do NOT skip any steps.
    - **URL RULES**: If the user says "Go to [Site]", you MUST convert it to a full valid URL (e.g. "youtube" -> "https://www.youtube.com", "google" -> "https://www.google.com").
    - If the user says "Type X into Y", you MUST use the "type" action with "value": "X" and "target": "Y".
    - If the user says "Search for X", use "search" action or "type" if a field is implied.
    
    Example Input: "Navigate to youtube, search for 'Groq', and play the first video."
    Example Output:
    [
        {"action": "open", "value": "https://www.youtube.com"},
        {"action": "search", "value": "Groq"},
        {"action": "play", "value": "first video"}
    ]
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert QA Automation Engineer. Your goal is to convert user intent into specific execution steps for a Playwright-based agent. \n\n{format_instructions}"),
        ("user", "{instruction}")
    ])

    chain = prompt | llm | JsonOutputParser()

    # Let exceptions propagate to graph.py so triggers fallback
    result = chain.invoke({
        "instruction": instruction,
        "format_instructions": format_instructions
    })
    return result

if __name__ == "__main__":
    # Test execution
    pass

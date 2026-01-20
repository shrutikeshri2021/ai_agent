import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def parse_with_llm(instruction, api_key):
    """
    Uses OpenAI GPT-4o/3.5 to convert natural language instructions into
    structured JSON steps for the automation agent.
    """
    if not api_key:
        raise ValueError("API Key is required for LLM features.")

    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=api_key,
        max_tokens=1000
    )

    # Define the schema we want
    format_instructions = """
    Return a JSON array of objects. Each object must have an "action" and "value".
    Some actions require "target".
    
    Valid Actions:
    1. "open" -> value: URL
    2. "click" -> value: text or description of element
    3. "type" -> value: text to type, target: placeholder, label, or element description
    4. "search" -> value: search term
    5. "verify" -> value: text to expect on page
    
    Example Input: "Go to amazon, search for laptop, and click the first result."
    Example Output:
    [
        {"action": "open", "value": "https://www.amazon.com"},
        {"action": "type", "value": "laptop", "target": "Search bar"}, 
        {"action": "click", "value": "Search icon"}
    ]
    (Note: The LLM should infer the logic like 'type' into search bar usually works better than 'search' command for complex sites)
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert QA Automation Engineer. Your goal is to convert user intent into specific execution steps for a Playwright-based agent. \n\n{format_instructions}"),
        ("user", "{instruction}")
    ])

    chain = prompt | llm | JsonOutputParser()

    try:
        result = chain.invoke({
            "instruction": instruction,
            "format_instructions": format_instructions
        })
        return result
    except Exception as e:
        print(f"LLM Parsing Error: {e}")
        # Fallback to empty list or raise
        return []

if __name__ == "__main__":
    # Test execution
    pass

def generate_playwright_steps(parsed_steps):
    code_steps = []

    for step in parsed_steps:
        if step["action"] == "open":
            val = step["value"]
            # Smart URL handling
            if not val.startswith("http"):
                val = f"https://{val}"
            if "." not in val:
                val = f"{val}.com"
                
            code_steps.append({"type": "goto", "value": val})
            
        elif step["action"] == "search":
            code_steps.append({"type": "search", "value": step["value"]})
            
        elif step["action"] == "click":
            code_steps.append({"type": "click", "value": step["value"]})
            
        elif step["action"] == "type":
            code_steps.append({"type": "type", "value": step["value"], "target": step["target"]})
            
        elif step["action"] == "verify":
            code_steps.append({"type": "verify", "value": step["value"]})

    return code_steps

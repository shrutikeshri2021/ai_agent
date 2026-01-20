import re

def parse_instruction(text):
    steps = []
    lines = text.split("\n")  # Keep original case for values

    for line in lines:
        line_clean = line.strip()
        if not line_clean: continue
        
        # Remove leading numbers (e.g. "1. Open..." -> "Open...")
        line_clean = re.sub(r'^\d+\.?\s*', '', line_clean)
        
        lower_line = line_clean.lower()
        
        if lower_line.startswith(("open", "goto", "navigate to")):
            # Extract URL/Site
            value = re.sub(r'^(open|goto|navigate to)\s+', '', line_clean, flags=re.IGNORECASE).strip()
            # Remove quotes if user added them
            value = value.strip('"').strip("'")
            steps.append({"action": "open", "value": value})
            
        elif lower_line.startswith("search"):
            # Extract search term
            value = re.sub(r'^search\s+(for\s+)?', '', line_clean, flags=re.IGNORECASE).strip()
            value = value.strip('"').strip("'")
            steps.append({"action": "search", "value": value})

        elif lower_line.startswith("click"):
            # Extract target to click
            value = re.sub(r'^click\s+(on\s+)?', '', line_clean, flags=re.IGNORECASE).strip()
            value = value.strip('"').strip("'")
            steps.append({"action": "click", "value": value})
            
        elif lower_line.startswith("type"):
            # Extract value and target: Type "value" into "Target"
            match = re.search(r'type\s+["\'](.+?)["\']\s+into\s+["\'](.+?)["\']', line_clean, re.IGNORECASE)
            if match:
                value, target = match.groups()
                steps.append({"action": "type", "value": value, "target": target})
            
        elif any(x in lower_line for x in ["verify", "check", "analyze", "validate"]):
             # Remove the command word
             value = re.sub(r'^(verify|check|analyze|validate)\s+', '', line_clean, flags=re.IGNORECASE).strip()
             value = value.strip('"').strip("'")
             steps.append({"action": "verify", "value": value})
            
    return steps

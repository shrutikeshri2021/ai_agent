import re

COMMANDS = ["open", "go", "goto", "navigate", "search", "click", "type", "hover", "select", "wait", "scroll", "verify", "check", "analyze", "validate", "play"]

def preprocess_text(text):
    """
    intelligent splitter handling newlines, periods, commas, and 'and'.
    Attempts to break text into distinct command steps.
    """
    # 1. Normalize separators: Replace commas and 'and' with newlines 
    # (unless inside quotes - simplistic approach)
    text = re.sub(r'[,|&]', '\n', text)
    text = re.sub(r'\s+and\s+', '\n', text, flags=re.IGNORECASE)
    
    raw_lines = text.split("\n")
    final_lines = []
    
    for rline in raw_lines:
        rline = rline.strip()
        if not rline: continue
        
        # Split by period-space to separate sentences
        parts = rline.split(". ")
        buffer = ""
        
        for part in parts:
            part = part.strip()
            if not part: continue
            
            # Simple check: If part matches a command start, it's a new line
            # Clean leading numbers if any (e.g. "2. Click") for the check
            clean_part = re.sub(r'^\d+\.?\s*', '', part).lower()
            is_command = any(clean_part.startswith(cmd) for cmd in COMMANDS)
            
            if is_command or not buffer:
                if buffer: final_lines.append(buffer)
                buffer = part
            else:
                 # Likely a continuation
                 buffer += ". " + part
        
        if buffer:
            final_lines.append(buffer)
            
    return final_lines

def parse_instruction(text):
    steps = []
    lines = preprocess_text(text)

    for line in lines:
        line_clean = line.strip()
        if not line_clean: continue
        
        # Remove leading numbers (e.g. "1. Open..." -> "Open...")
        line_clean = re.sub(r'^\d+\.?\s*', '', line_clean)
        # Remove trailing period
        if line_clean.endswith("."):
            line_clean = line_clean[:-1]
        
        lower_line = line_clean.lower()
        
        if lower_line.startswith(("open", "goto", "navigate to", "go to", "go")):
            # Extract URL/Site. Handle "go to" vs "go"
            value = re.sub(r'^(open|goto|navigate to|go to|go)\s+', '', line_clean, flags=re.IGNORECASE).strip()
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

        elif lower_line.startswith("hover"):
            # Extract target to hover
            value = re.sub(r'^hover\s+(over\s+)?', '', line_clean, flags=re.IGNORECASE).strip()
            value = value.strip('"').strip("'")
            steps.append({"action": "hover", "value": value})

        elif lower_line.startswith("select"):
            # Extract option and target: Select "Option" from "Dropdown"
            match = re.search(r'select\s+["\'](.+?)["\']\s+from\s+["\'](.+?)["\']', line_clean, re.IGNORECASE)
            if match:
                value, target = match.groups()
                steps.append({"action": "select", "value": value, "target": target})
        
        elif lower_line.startswith("play"):
             # "Play it" or "Play video"
             value = re.sub(r'^play\s+', '', line_clean, flags=re.IGNORECASE).strip()
             if value.lower() in ["it", "video", "first video"]:
                 value = "first video" # Generic marker
             steps.append({"action": "play", "value": value})

        elif lower_line.startswith("wait"):
            # Extract seconds: Wait 5 seconds
            match = re.search(r'wait\s+(\d+)', line_clean, re.IGNORECASE)
            if match:
                steps.append({"action": "wait", "value": int(match.group(1))})
        
        elif lower_line.startswith("scroll"):
            # Scroll Down / Up
            direction = "down"
            if "up" in lower_line: direction = "up"
            steps.append({"action": "scroll", "value": direction})
            
        elif any(x in lower_line for x in ["verify", "check", "analyze", "validate"]):
             # Remove the command word
             value = re.sub(r'^(verify|check|analyze|validate)\s+', '', line_clean, flags=re.IGNORECASE).strip()
             value = value.strip('"').strip("'")
             steps.append({"action": "verify", "value": value})
            
    return steps

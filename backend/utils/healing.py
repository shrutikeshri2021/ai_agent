from playwright.sync_api import Page
import difflib

def heal_element(page: Page, target_text: str):
    """
    Scans the DOM for interactive elements and uses fuzzy matching
    to find the closest match to 'target_text'.
    """
    print(f"🏥 Healing initiated for: '{target_text}'")
    
    # 1. Get handles to all potential interactive elements
    # We look for buttons, links, and inputs
    elements = page.locator("button, a, input[type='submit'], input[type='button'], [role='button']").all()
    
    candidates = []
    element_map = {}

    for el in elements:
        try:
            if not el.is_visible():
                continue
                
            # Extract text attributes
            text = (el.text_content() or "").strip()
            label = (el.get_attribute("aria-label") or "").strip()
            placeholder = (el.get_attribute("placeholder") or "").strip()
            value = (el.get_attribute("value") or "").strip()
            title = (el.get_attribute("title") or "").strip()
            
            # Combine all text signals
            signature = f"{text} {label} {placeholder} {value} {title}".strip().lower()
            
            if signature:
                # Store for matching
                candidates.append(signature)
                # Map signature back to element (using index if duplicates exist, but simple map here)
                element_map[signature] = el
        except:
            continue

    # 2. Find closest match using difflib
    # cutoff=0.4 means we accept 40% similarity (quite loose, good for finding renamed things)
    # We use a lower cutoff (0.3) to catch substrings like "Feeling Lucky" in "I'm Feeling Lucky"
    matches = difflib.get_close_matches(target_text.lower(), candidates, n=1, cutoff=0.3)
    
    if matches:
        best_match_key = matches[0]
        print(f"✅ Healed! Found replacement: '{best_match_key}' (Match for '{target_text}')")
        return element_map[best_match_key]
    
    # Fallback: check for substring manually if difflib fails
    for candidate in candidates:
         if target_text.lower() in candidate:
             print(f"✅ Healed (Substring Match)! Found replacement: '{candidate}'")
             return element_map[candidate]

    print("❌ Healing failed. No similar elements found.")
    return None

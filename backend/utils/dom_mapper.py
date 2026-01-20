from playwright.sync_api import Page, Locator

def find_element(page: Page, selector: str, timeout: int = 5000) -> Locator:
    """
    Tries to find an element using multiple strategies to handle dynamic IDs or changes.
    """
    # Prioritize original casing, then Title, then lower
    variations = [selector]
    if selector.title() != selector: variations.append(selector.title())
    if selector.lower() != selector: variations.append(selector.lower())
    
    strategies = []
    for s in variations:
        strategies.extend([
            f"[placeholder='{s}']",                 # Placeholder (High priority for inputs)
            f"[aria-label='{s}']",                  # Aria Label
            f"input[name='{s}']",                   # Input Name
            f"input[id='{s}']",                     # Input ID
            f"button:has-text('{s}')",              # Button text
            f"a:has-text('{s}')",                   # Link text
            f"input[value='{s}']",                  # Input Value
            f"[title='{s}']",                       # Title attribute
            f"[data-testid='{s}']",                 # Test ID
            f"text={s}",                            # Text content (Low priority)
             # Basic IDs if valid CSS 
            f"#{s}" if " " not in s else None, 
        ])
    
    # Filter out None and duplicate strategies while preserving order
    seen = set()
    cleaned_strategies = []
    for s in strategies:
        if s and s not in seen:
            cleaned_strategies.append(s)
            seen.add(s)
    
    # Add generic fallbacks at the end
    cleaned_strategies.append(selector)

    best_candidate = None

    for strategy in cleaned_strategies:
        try:
            # Get all matches for this strategy
            locs = page.locator(strategy).all()
            
            for loc in locs:
                if loc.is_visible():
                    return loc # Found a visible match! Best case.
                
                # Keep the first finding as a fallback
                if best_candidate is None:
                    best_candidate = loc
        except Exception:
            continue
            
    # Fallback: If no visible element found, return the first invisible one we found
    return best_candidate

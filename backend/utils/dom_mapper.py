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
    
    # 1. STRICT EXACT MATCHES (Highest Priority)
    # This prevents partial matches (e.g., 'Electronics' matching 'Consumer Electronics Policy')
    for s in variations:
        strategies.extend([
            f"text='{s}'",                          # Exact text match (Case-sensitive-ish)
            f"a:text-is('{s}')",                    # Exact link text
            f"button:text-is('{s}')",               # Exact button text
            f"[aria-label='{s}']",                  # Exact Aria
            f"[placeholder='{s}']",                 # Exact Placeholder
            f"input[value='{s}']",                  # Exact Input Value
        ])
        
    # 2. LOOSE/SUBSTRING MATCHES (Fallback)
    for s in variations:
        strategies.extend([
            f"button:has-text('{s}')",              # Button containing text
            f"a:has-text('{s}')",                   # Link containing text
            f"input[name*='{s}']",                  # Input Name partial
            f"text={s}",                            # Generic text content (Low priority)
            f"[data-testid='{s}']",                 # Test ID
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

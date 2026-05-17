import re

# 1. ВБУДОВАНІ СЛОВНИКИ
COLORS_DICT = {
    "red": "red", "blue": "blue", "green": "green", "yellow": "yellow",
    "black": "black", "white": "white", "gray": "gray", "grey": "gray",
    "brown": "brown", "pink": "pink", "purple": "purple", "orange": "orange",
    "navy": "blue", "blonde": "yellow", "dark": "black"
}

LOCATIONS_DICT = {
    "street": "street", "road": "street", "sidewalk": "street", "highway": "street",
    "beach": "beach", "sand": "beach", "ocean": "water_area", "river": "water_area",
    "sea": "water_area", "pool": "water_area", "lake": "water_area",
    "park": "park", "forest": "forest", "woods": "forest", "grass": "field",
    "field": "field", "room": "indoor", "building": "building", "kitchen": "indoor",
    "restaurant": "indoor", "store": "indoor", "market": "market"
}

TEXT_NUMBERS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", 
    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
    "group": "many", "bunch": "many", "crowd": "many", "several": "many"
}

# 2. ФУНКЦІЇ ЕКСТРАКЦІЇ

def extract_quantity(text: str) -> list:
    results = []
    words = '|'.join(TEXT_NUMBERS.keys())
    pattern = rf'(?i)(?<![-#])(?<!number\s)\b(\d+|{words})\b(?![-%])'
    
    for match in re.finditer(pattern, text):
        val = match.group(1).lower()
        norm_val = TEXT_NUMBERS.get(val, val)
        
        results.append({
            "field_type": "QUANTITY",
            "value": norm_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "regex_qty_strict"
        })
    return results

def extract_colors(text: str) -> list:
    results = []
    words = '|'.join(COLORS_DICT.keys())
    pattern = rf'(?i)(?<!out of the\s)\b({words})\b(?!(?:\s+eye|\s+collar|\s+slip|\s+card|\s+Cross))'

    for match in re.finditer(pattern, text):
        raw_val = match.group(1)
        if raw_val.istitle() and match.start() > 0:
            continue
            
        norm_val = COLORS_DICT[raw_val.lower()]
        results.append({
            "field_type": "COLOR",
            "value": norm_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "dict_colors_strict"
        })
    return results

def extract_locations(text: str) -> list:
    results = []
    words = '|'.join(LOCATIONS_DICT.keys())
    pattern = rf'(?i)\b({words})\b(?!(?:\s+vendor|\s+polo|\s+block))'
    
    for match in re.finditer(pattern, text):
        raw_val = match.group(1)
        if raw_val.istitle() and match.start() > 0:
            continue
            
        norm_val = LOCATIONS_DICT[raw_val.lower()]
        results.append({
            "field_type": "LOCATION",
            "value": norm_val,
            "start_char": match.start(),
            "end_char": match.end(),
            "method": "dict_locations_strict"
        })
    return results

def extract_all(text: str) -> dict:
    if not isinstance(text, str):
        return {"QUANTITY": [], "COLOR": [], "LOCATION": []}
        
    return {
        "QUANTITY": extract_quantity(text),
        "COLOR": extract_colors(text),
        "LOCATION": extract_locations(text)
    }
def extract_visual_attributes(input_data: dict) -> dict:
    """
    Витягує кольори та елементи одягу з тексту.
    Очікуваний input: {"text": "A man in a red shirt"}
    """
    try:
        text = input_data.get("text", "").lower()
        if not text:
            raise ValueError("Field 'text' is missing or empty.")
            
        colors = ["red", "blue", "green", "black", "white", "yellow", "brown", "pink", "grey", "orange"]
        clothing = ["shirt", "hat", "pants", "dress", "jacket", "shoes", "jeans", "coat", "suit"]

        found_colors = [c for c in colors if c in text]
        found_clothing = [c for c in clothing if c in text]

        return {
            "colors_found": found_colors,
            "clothing_found": found_clothing,
            "is_visually_detailed": len(found_colors) > 0 or len(found_clothing) > 0
        }
    except Exception as e:
        raise ValueError(f"Extraction failed: {str(e)}")


def validate_caption_length(input_data: dict) -> dict:
    """
    Перевіряє, чи опис відповідає мінімальним вимогам щодо довжини (мінімум 5 слів).
    Очікуваний input: {"text": "A man running"}
    """
    try:
        text = input_data.get("text", "")
        if not text:
            raise ValueError("Field 'text' is missing or empty.")
            
        words = text.split()
        word_count = len(words)
        is_valid = word_count >= 5
        
        return {
            "word_count": word_count,
            "is_valid": is_valid,
            "message": "Valid length" if is_valid else "Caption is too short."
        }
    except Exception as e:
        raise ValueError(f"Validation failed: {str(e)}")


def check_animal_presence(input_data: dict) -> dict:
    """
    Перевіряє, чи є в описі тварини (собаки, коти тощо).
    Очікуваний input: {"text": "A dog playing"}
    """
    try:
        text = input_data.get("text", "").lower()
        animals = ["dog", "cat", "horse", "bird", "elephant", "bear", "cow", "sheep", "puppy"]
        
        found_animals = [a for a in animals if a in text]
        
        return {
            "animals_found": found_animals,
            "contains_animals": len(found_animals) > 0
        }
    except Exception as e:
        raise ValueError(f"Animal check failed: {str(e)}")

# Реєстр доступних інструментів
AVAILABLE_TOOLS = {
    "extract_visual_attributes": extract_visual_attributes,
    "validate_caption_length": validate_caption_length,
    "check_animal_presence": check_animal_presence
}
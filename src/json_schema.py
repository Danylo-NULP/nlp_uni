# Схема для витягування візуальних елементів сцени
VISUAL_SCENE_SCHEMA = {
    "type": "object",
    "properties": {
        "primary_subject": {
            "type": "string",
            "description": "Головний суб'єкт (людина, тварина або об'єкт), який виконує дію. Наприклад: 'man', 'dog', 'two women'. Якщо немає - null."
        },
        "action": {
            "type": "string",
            "description": "Головна дія, яку виконує суб'єкт. Наприклад: 'running', 'sitting', 'playing guitar'. Якщо немає - null."
        },
        "clothing": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Список елементів одягу, в які вдягнений суб'єкт (наприклад: ['blue shirt', 'hat']). Якщо одяг не згадується - порожній список []."
        },
        "location": {
            "type": "string",
            "description": "Місцезнаходження або фон сцени (наприклад: 'street', 'beach', 'room'). Якщо не вказано - null."
        }
    },
    "required": ["primary_subject", "action", "clothing", "location"],
    "additionalProperties": False
}
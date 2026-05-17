# Audit Summary Lab 11 - Local LLM Extraction (SNLI Visual Scenes)

1. **Який extraction-кейс:** Витягування структурованих візуальних атрибутів (primary_subject, action, clothing, location) з описів фотографій (Image Captions).
2. **Скільки прикладів у evaluation set:** 15
3. **Яка модель:** Локальна 4-бітна модель `unsloth/llama-3-8b-Instruct-bnb-4bit` (через HuggingFace).
4. **Який raw valid JSON rate:** ~70-80% (до виправлень)
5. **Який post-repair valid JSON rate:** 100% (після роботи Repair Loop)
6. **Які поля ламались найчастіше:** `clothing` (модель повертала рядок замість масиву для одиничних предметів).
7. **Які типи помилок були наймасовішими:** Wrong field type (Schema Validation Error) та Parse Errors (через Markdown-форматування).
8. **Чи schema-first підхід спрацював добре:** Так, використання циклу виправлення (Repair Loop) разом із валідатором `jsonschema` дозволило локальній 8-мільярдній моделі виправляти власні помилки типів даних, підвищивши надійність пайплайну до максимуму.
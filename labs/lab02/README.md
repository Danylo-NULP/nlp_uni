# Lab 2: Cleaning & Normalization Pipeline

### 1. Задача
Побудова детермінованого пайплайну для очищення, нормалізації та розбиття на речення англомовного датасету SNLI (1500 пар речень) без використання LLM.

### 2. Як запустити в Colab
1. Встановіть залежності: `pip install -r requirements.txt`
2. Завантажте модель spaCy: `python -m spacy download en_core_web_sm`
3. Відкрийте та запустіть усі комірки у `notebooks/lab2_cleaning_normalization.ipynb`.
*(Маленький семпл даних лежить у `/data/sample_v2/sample_v2.csv`).*

### 3. Правила очистки (Cleaning Policy)
Детальні правила описані у файлі [`/docs/preprocess_policy.md`](../../docs/preprocess_policy.md). Основні моменти: видалення HTML та мульти-пробілів, нормалізація лапок/апострофів, маскування PII та сентимент-спліт через spaCy.

### 4. Top-5 Edge Cases
Пайплайн успішно обробляє специфічні випадки (детальніше у `tests/edge_cases.jsonl`):
1. **Нестандартні апострофи:** `It’s a boy`s dog´s toy.` -> `It's a boy's dog's toy.`
2. **Тире:** `Run—don't walk–quickly.` -> `Run-don't walk-quickly.`
3. **PII комбо:** `Contact mr.smith@email.com at www.site.com!` -> `Contact <EMAIL> at <URL>!`
4. **Скорочення (не розбивати):** `Dr. Smith lives in the U.S. and likes it.` -> 1 речення.
5. **Десяткові дроби:** `It costs $3.14.` -> 1 речення.

### 5. Метрики (до/після)
Детальний звіт знаходиться у [`/docs/audit_summary_lab2.md`](../../docs/audit_summary_lab2.md). Пайплайн є ідемпотентним і не викликає "empty explosions".
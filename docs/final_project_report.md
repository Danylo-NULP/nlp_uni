# EN NLI (SNLI Subset) Logical Verification Pipeline

## Release Info

| Parameter | Value |
|---|---|
| **Тег версії** | `final-project` |
| **Поточний статус** | `Completed` |
| **Основний use case** | Retrieval / Evidence Checking (Логічна верифікація гіпотез) |

---

# Опис проєкту (Project Overview)

Цей проєкт присвячений побудові автоматизованої системи класифікації та аудиту логічних зв'язків між твердженнями на основі підмножини англомовного датасету **SNLI (Stanford Natural Language Inference)**.

Система приймає на вхід два речення:

- **Premise** — вихідне твердження або доказ
- **Hypothesis** — припущення або запит

та класифікує їхній взаємозв'язок за трьома категоріями:

| Клас | Опис |
|---|---|
| **Entailment** | Гіпотеза логічно випливає з передумови |
| **Contradiction** | Гіпотеза прямо суперечить передумові |
| **Neutral** | Недостатньо інформації для підтвердження або спростування |

---

Проєкт демонструє еволюційний перехід від базових лінійних ML-моделей до стійких та керованих архітектур із багаторівневим контролем якості даних.

---

# Архітектура конвеєра (Pipeline Architecture)

Система побудована у вигляді модульного конвеєра обробки даних.

---

## Ingestion & Profiling

- Імпорт пар тверджень із датасету SNLI
- Аналіз балансу класів
- Виявлення структурних аномалій
- Попередня фільтрація шуму

---

## Text Cleaning

Очищення текстів від:

- HTML-тегів
- технічного шуму
- службових символів

та приведення рядків до:

- нижнього регістру
- стандартизованого формату

---

## Feature Engineering

### Основні підходи:

- Об'єднання речень через спеціальний токен:

```text
[SEP]
```

- Витягування додаткових ознак:
  - `no`
  - `not`
  - `never`
  - інші маркери заперечення

---

## Classification Layer

### Використані методи:

- TF-IDF Word n-grams
- TF-IDF Character n-grams
- Logistic Regression
- Class Weight Balancing

### Мета:
Компенсація дисбалансу класів та підвищення стабільності моделі.

---

## Quality Assurance (Multi-agent Preview)

Симуляція роботи окремого Reviewer-модуля:

- аудит JSON-структур,
- перевірка консистентності,
- валідація reasoning-блоків,
- контроль відповідності фінального класу.

---

# Структура репозиторію

```text
data/raw/
│
├── вихідні сирі підмножини датасету SNLI

data/processed_v2/
│
├── очищені текстові пари
├── витягнуті ознаки
└── службові розділювачі

notebooks/en_snli_demo.ipynb
│
└── фінальний End-to-End демо-ноутбук

docs/crew_logs_lab13.jsonl
│
└── логи оркестрації та валідації

docs/audit_summary_lab13.md
│
└── аналіз помилок та аудит стійкості системи

requirements.txt
│
└── список залежностей

README.md
│
└── технічна документація
```

---

# Інструкція із запуску (Quick Start)

## Клонування репозиторію

```bash
git clone https://github.com/Danylo-NULP/nlp_uni.git
cd nlp_uni
git checkout lab-13
```

---

## Створення віртуального середовища

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## Встановлення залежностей

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

---

## Запуск аналітики

Відкрийте файл:

```text
notebooks/en_snli_demo.ipynb
```

у:
- Jupyter Notebook
- Google Colab

для перегляду:
- звітів моделі,
- метрик,
- confusion matrix,
- прикладів класифікації.

---

# Аналіз помилок та висновки (Error Analysis Summary)

Під час аналізу пограничних кейсів було виявлено:

## Сильні сторони моделі

Модель на базі класичного TF-IDF добре працює для:

- явних суперечностей,
- лексичних заперечень,
- простих entailment-конструкцій.

Особливо ефективно модель обробляє клас:

```text
Contradiction
```

за наявності маркерів:
- `not`
- `never`
- `no`

---

## Обмеження системи

Складнощі виникають при:

- метафоричних конструкціях,
- складних синонімах,
- прихованих логічних залежностях,
- розмежуванні класів:
  - `Neutral`
  - `Entailment`

---

## Напрямки подальшого розвитку

Для покращення якості моделі рекомендується:

- FastText embeddings
- Transformer embeddings
- Sentence Transformers
- BERT-based architectures

---

## Multi-agent Validation Layer

Побудований каскадний інтерфейс валідації:

- блокує структурні збої,
- контролює формат JSON,
- забезпечує стабільність пайплайну,
- гарантує передбачуваний формат вихідних даних.

---

# Статус проєкту

- Completed
- Stable Pipeline
- End-to-End NLP Workflow
- Ready for Demonstration
- ML + QA Validation Architecture
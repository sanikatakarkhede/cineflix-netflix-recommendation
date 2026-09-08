# CineFlix AI 🎬
### Intelligent Netflix Movie Recommendation Engine & Conversational CineBot

CineFlix AI is an advanced movie recommendation system that analyzes viewing history, star ratings, and conversational natural language inputs to curate personalized films and TV series on Netflix.

---

## 🌟 Key Features

1. **Hybrid NLP & Preference Vector Recommender**:
   - **TF-IDF & Metadata Soup Vectorization**: Analyzes plot synopses, weighted genres, directors, cast, mood tags, and keywords.
   - **Dynamic User Profiling**: Dynamically weights watch history, 1-5 star ratings, and negative feedback into a multi-dimensional taste vector.
   - **Explainable AI (XAI)**: Generates human-readable match explanations (e.g., *"98% Match: Recommended because you loved the psychological tension and mind-bending narrative of Inception"*).

2. **Conversational CineBot AI Curator**:
   - Understands mood (*"I'm stressed, give me something light and funny"*), actor/director preferences (*"Christopher Nolan mind games"*), era filters (*"90s classic thrillers"*), and title comparisons (*"Something like Dark and Stranger Things"*).
   - Multi-turn conversation memory with refinement support and embedded interactive movie cards.

3. **Cinematic Netflix Dark UI**:
   - Obsidian dark theme (`#141414`) with Netflix Crimson highlights (`#E50914`), glassmorphic panels, and neon glow accents.
   - Hero spotlight billboard with dynamic background lighting.
   - Netflix-style horizontal carousels with smooth scrolling.
   - Instant Persona Switcher (*Alex: Sci-Fi Geek*, *Sarah: True Crime Buff*, *Jordan: Feel-Good Fan*, *Marcus: Action Adrenaline*, *Clean Slate*).
   - Interactive Taste Profile & Sliders Dashboard with live genre analytics and watch history manager.

---

## 🚀 Quick Start

### 1. Requirements
Ensure Python 3.9+ is installed with the required libraries:
```bash
pip install flask flask-cors scikit-learn pandas numpy nltk
```

### 2. Launch the Application
Run the server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Run Automated Tests
```bash
python -m unittest discover tests
```

---

## 📁 Architecture Overview

```
NLP 2/
├── app.py                      # Flask REST API & Web Server
├── dataset_builder.py          # Netflix catalog builder
├── data/
│   └── netflix_catalog.json    # Curated Netflix movies & TV shows dataset
├── engine/
│   ├── recommender.py          # TF-IDF, Cosine Similarity, Taste Profiler & Personas
│   └── nlp_chat.py             # Conversational CineBot Dialogue & Entity Extractor
├── static/
│   ├── css/
│   │   └── style.css           # Cinematic Netflix-themed stylesheet
│   └── js/
│       └── app.js              # Reactive frontend application logic
├── templates/
│   └── index.html              # Single-page cinematic web interface
└── tests/
    └── test_engine.py          # Automated unit and integration test suite
```

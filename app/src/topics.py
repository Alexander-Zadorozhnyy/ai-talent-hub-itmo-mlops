# Все возможные темы из модели с эмодзи и цветами
TOPICS_MAP = {
    "U.S. NEWS": {"emoji": "🇺🇸", "color": "#2E86C1"},
    "GOOD NEWS": {"emoji": "😊", "color": "#27AE60"},
    "DIVORCE": {"emoji": "💔", "color": "#E74C3C"},
    "WELLNESS": {"emoji": "🧘", "color": "#1ABC9C"},
    "WEIRD NEWS": {"emoji": "🤪", "color": "#F39C12"},
    "MONEY": {"emoji": "💰", "color": "#2ECC71"},
    "FOOD & DRINK": {"emoji": "🍽️", "color": "#E67E22"},
    "WORLDPOST": {"emoji": "🌍", "color": "#3498DB"},
    "COMEDY": {"emoji": "😂", "color": "#F1C40F"},
    "WEDDINGS": {"emoji": "💍", "color": "#E91E63"},
    "THE WORLDPOST": {"emoji": "🌏", "color": "#2980B9"},
    "BLACK VOICES": {"emoji": "✊", "color": "#17202A"},
    "RELIGION": {"emoji": "⛪", "color": "#8E44AD"},
    "PARENTING": {"emoji": "👶", "color": "#F4A460"},
    "HOME & LIVING": {"emoji": "🏠", "color": "#D4A574"},
    "TRAVEL": {"emoji": "✈️", "color": "#5DADE2"},
    "FIFTY": {"emoji": "🎂", "color": "#E67E22"},
    "HEALTHY LIVING": {"emoji": "💪", "color": "#2ECC71"},
    "WOMEN": {"emoji": "👩", "color": "#EC407A"},
    "POLITICS": {"emoji": "🏛️", "color": "#E74C3C"},
    "TASTE": {"emoji": "👅", "color": "#F39C12"},
    "SCIENCE": {"emoji": "🔬", "color": "#1A237E"},
    "STYLE": {"emoji": "👗", "color": "#9B59B6"},
    "QUEER VOICES": {"emoji": "🏳️‍🌈", "color": "#FF6B6B"},
    "TECH": {"emoji": "💻", "color": "#2C3E50"},
    "GREEN": {"emoji": "🌿", "color": "#27AE60"},
    "ENVIRONMENT": {"emoji": "🌍", "color": "#1ABC9C"},
    "EDUCATION": {"emoji": "📚", "color": "#F39C12"},
    "SPORTS": {"emoji": "⚽", "color": "#3498DB"},
    "CULTURE & ARTS": {"emoji": "🎨", "color": "#8E44AD"},
    "MEDIA": {"emoji": "📺", "color": "#607D8B"},
    "COLLEGE": {"emoji": "🎓", "color": "#9C27B0"},
    "WORLD NEWS": {"emoji": "🌐", "color": "#1565C0"},
    "CRIME": {"emoji": "🚔", "color": "#424242"},
    "STYLE & BEAUTY": {"emoji": "💄", "color": "#E91E63"},
    "ENTERTAINMENT": {"emoji": "🎬", "color": "#FF6F00"},
    "LATINO VOICES": {"emoji": "🌎", "color": "#D84315"},
    "IMPACT": {"emoji": "🌟", "color": "#F57C00"},
    "ARTS & CULTURE": {"emoji": "🎭", "color": "#6A1B9A"},
    "BUSINESS": {"emoji": "💼", "color": "#2E7D32"},
    "ARTS": {"emoji": "🖼️", "color": "#AD1457"},
    "PARENTS": {"emoji": "👨‍👩‍👧", "color": "#4CAF50"},
}

DEFAULT_TOPIC = {"emoji": "📰", "color": "#95A5A6"}


def get_topic_info(label):
    if label in TOPICS_MAP:
        return TOPICS_MAP[label]
    else:
        return {**DEFAULT_TOPIC, "color": "#95A5A6"}

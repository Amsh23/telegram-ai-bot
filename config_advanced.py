# -*- coding: utf-8 -*-
"""
🚀 Advanced AI Telegram Bot Configuration v3.0
⚡ Optimized for Persian/English with Machine Learning
"""

import os

# ========================================
# 🔧 CORE SYSTEM SETTINGS
# ========================================

# Tesseract OCR Configuration
TESSERACT_PATH = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
OCR_LANGUAGES = 'fas+eng'
OCR_CONFIG = '--psm 6 -c tessedit_char_whitelist=آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئيةك٠١٢٣٤٥٦٧٨٩0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|;:,.<>?/~`"'

# Coordinate Settings (Updated from GUI)
CHAT_REGION = {
    'x': 2652,
    'y': 135,
    'width': 494,
    'height': 1256
}

INPUT_CLICK_POSITION = {
    'x': 2732,
    'y': 1368
}

SEND_BUTTON_POSITION = {
    'x': 2866,
    'y': 1372
}

# ========================================
# ⏱️ TIMING & PERFORMANCE
# ========================================

CHECK_INTERVAL = 8  # Reduced for faster response
RESPONSE_DELAY = 1.5  # Faster response
PYAUTOGUI_PAUSE = 0.3  # Optimized pause

# Advanced Timing
OCR_TIMEOUT = 10
AI_ANALYSIS_TIMEOUT = 5
RESPONSE_GENERATION_TIMEOUT = 3

# ========================================
# 🧠 AI & MACHINE LEARNING SETTINGS
# ========================================

# TensorFlow Settings
TF_ENABLE_GPU = False  # Use CPU for stability
TF_MEMORY_LIMIT = 2048  # MB

# OCR Confidence Thresholds
MIN_OCR_CONFIDENCE = 25
PREFERRED_OCR_CONFIDENCE = 70
EXCELLENT_OCR_CONFIDENCE = 90

# AI Analysis Thresholds
MIN_REAL_MESSAGE_CONFIDENCE = 0.4
HIGH_CONFIDENCE_THRESHOLD = 0.8
INTENT_CONFIDENCE_THRESHOLD = 0.3

# ========================================
# 🌍 LANGUAGE & TEXT PROCESSING
# ========================================

# Persian Language Patterns (Enhanced)
PERSIAN_PATTERNS = [
    r'[آ-ی]{2,}',  # Persian characters
    r'(چطور|چی|کجا|کی|چرا|چه|کدوم)',  # Question words
    r'(سلام|درود|احوال|هلو|هللو)',  # Greetings
    r'(ممنون|مرسی|تشکر|دستت|قربونت)',  # Thanks
    r'(باشه|اوکی|حله|چشم|اره|نه)',  # Agreement/Disagreement
    r'(میخوام|میگم|میدونم|میتونم|نمیتونم)',  # Verbs
    r'(کمک|مشکل|سوال|جواب|راهنمایی)',  # Help/Problem words
    r'(چرا|چون|برای|اینکه|ولی|اما)',  # Connectors
    r'(خوب|بد|عالی|افتضاح|خفن|کول)',  # Adjectives
    r'[؟!.]{1,3}',  # Persian punctuation
]

# Real Message Indicators (Comprehensive)
REAL_MESSAGE_INDICATORS = [
    r'[آ-ی]{3,}',  # Persian text
    r'(سلام|هلو|hi|hello|hey)',  # Greetings
    r'(چطور|چی|چرا|کجا|what|how|why|where)',  # Questions
    r'(ممنون|مرسی|thank|thanks)',  # Thanks
    r'(باشه|اوکی|ok|okay|اره|yeah)',  # Confirmations
    r'(کمک|help|راهنمایی|guide)',  # Help requests
    r'(مشکل|problem|خرابی|issue)',  # Problems
    r'(میخوام|want|need|لازم)',  # Wants/Needs
    r'[؟!.]{1,3}',  # Punctuation
    r'\?+',  # Question marks
    r'[a-zA-Z]{4,}',  # English words
]

# ========================================
# 🚫 INTERFACE FILTERING (Enhanced)
# ========================================

# Interface Filters (More Comprehensive)
INTERFACE_FILTERS = [
    'KAMHEREI314', 'Click here', 'view updates', 'You joined', 'channel',
    'Emoji', 'Stickers', 'GIFs', 'Search', 'incognito', 'Incognito',
    'Sign in', 'SafeSearch', 'Allockmaks', 'Turkce', 'typing',
    'Online', 'Last seen', 'Active', 'Forwarded', 'Reply', 'Edit',
    'Delete', 'Pin', 'Unpin', 'Mute', 'Unmute', 'Block', 'Unblock',
    'Add contact', 'Voice message', 'Video message', 'Document',
    'Photo', 'Video', 'Audio', 'Location', 'Contact', 'Poll',
    'This message', 'was deleted', 'You deleted', 'Message was',
    'Today', 'Yesterday', 'AM', 'PM', 'Jan', 'Feb', 'Mar', 'Apr',
    'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]

# Interface Patterns (More Specific)
INTERFACE_PATTERNS = [
    r'^\s*\*\s*[A-Z]\s*\|',  # Navigation elements
    r'^[<>-]+\s*[ox]\s*[x&®@]+.*incognito',  # Browser UI
    r'KAMHEREI314.*Sign\s+in',  # Specific UI text
    r'SafeSearch.*Mode',  # Search UI
    r'^[\s\-]+[ox]\s*[x&®@:]+.*',  # Generic UI patterns
    r'\d{1,2}:\d{2}\s*(AM|PM)',  # Timestamps
    r'^(Today|Yesterday)\s+\d{1,2}:\d{2}',  # Date stamps
    r'(Forwarded\s+from|Reply\s+to)',  # Message metadata
    r'^(Online|Last\s+seen|Active)',  # Status indicators
    r'(Voice\s+message|Video\s+message)',  # Media types
    r'^[\d\s\-\:\.\,]+$',  # Pure numbers/punctuation
    r'^[^\w\u0600-\u06FF]+$',  # Pure symbols (excluding Persian)
]

# ========================================
# 🎭 RESPONSE GENERATION
# ========================================

# Response Rules (Enhanced with AI-friendly structure)
RESPONSE_RULES = {
    'greetings': {
        'keywords': ['سلام', 'hello', 'hi', 'hey', 'درود', 'هلو', 'هللو'],
        'responses': [
            'سلام عزیزم! چطوری؟ چه خبرا؟ 😊',
            'هللو! حالت چطوره داداش؟ 👋',
            'سلام و احترام! چطور می‌تونم کمکت کنم؟ 🙏',
            'های! چه خبر از زندگی؟ 😄',
            'سلاااام! خوش اومدی! 🤗'
        ],
        'context': 'greeting',
        'emotion': 'positive'
    },
    
    'time_request': {
        'keywords': ['ساعت', 'time', 'زمان', 'وقت', 'چندیه', 'چنده'],
        'response': 'current_time',
        'context': 'information',
        'emotion': 'neutral'
    },
    
    'goodbyes': {
        'keywords': ['خداحافظ', 'bye', 'goodbye', 'فعلا', 'برم', 'رفتم'],
        'responses': [
            'فعلاً عزیز! مواظب خودت باش! 👋💕',
            'خداحافظ! موفق باشی! 🌟',
            'بای بای! منتظر برگشتتم! 😊',
            'برو به سلامت! خوش بگذره! 🎉'
        ],
        'context': 'goodbye',
        'emotion': 'positive'
    },
    
    'how_are_you': {
        'keywords': ['چطوری', 'حالت', 'how are you', 'احوالت', 'خوبی'],
        'responses': [
            'ممنون خوبم! تو چطوری عزیزم؟ 😊',
            'عالی! تو چطوری؟ چه خبرا؟ 😄',
            'خوبم والا! تو خوبی؟ حالت چطوره؟ 🤗',
            'فوق‌العادم! تو چی؟ همه چی اوکیه؟ 😍'
        ],
        'context': 'personal_inquiry',
        'emotion': 'positive'
    },
    
    'thanks': {
        'keywords': ['ممنون', 'مرسی', 'thank', 'متشکرم', 'دستت', 'قربونت'],
        'responses': [
            'خواهش می‌کنم عزیزم! قابلی نداشت! 😊💕',
            'نوکرتم! همیشه! 🤗',
            'دمت گرم! خیلی لطف داری! 😄',
            'عشقی! هرموقع کمک خواستی بگو! 💪'
        ],
        'context': 'gratitude',
        'emotion': 'positive'
    },
    
    'questions': {
        'keywords': ['چی', 'چرا', 'چطور', 'کی', 'کجا', 'what', 'why', 'how', 'when', 'where'],
        'responses': [
            'خوب سوال پرسیدی! بذار ببینم... 🤔',
            'جالب! این رو چک می‌کنم برات 🔍',
            'سوال جالبیه! کمی صبر کن 📝',
            'بذار فکر کنم... یکم توضیح بیشتر بده 🧐'
        ],
        'context': 'question',
        'emotion': 'thoughtful'
    },
    
    'help_request': {
        'keywords': ['کمک', 'help', 'راهنمایی', 'میتونی', 'can you', 'لطفا', 'please'],
        'responses': [
            'البته! چه کمکی از دستم بر میاد؟ 💪',
            'حتماً! بگو چیکار کنم؟ 🤝',
            'در خدمتم! چه مشکلی داری؟ 🛠️',
            'آماده‌ام! چطور کمکت کنم؟ 🚀'
        ],
        'context': 'help_request',
        'emotion': 'helpful'
    },
    
    'compliments': {
        'keywords': ['عالی', 'خفن', 'حرف', 'کول', 'great', 'awesome', 'perfect', 'excellent'],
        'responses': [
            'وای ممنون! خوشحالم که راضی هستی! 😍',
            'اییی چقدر مهربونی! ممنونم! 🥰',
            'دمت گرم! خیلی لطف داری! 😊💕',
            'عشقی! این حرفا رو نزن! 😄❤️'
        ],
        'context': 'compliment',
        'emotion': 'happy'
    },
    
    'problems': {
        'keywords': ['مشکل', 'خرابی', 'problem', 'issue', 'نمیتونم', 'can\'t', 'error'],
        'responses': [
            'چه مشکلی پیش اومده؟ بگو ببینم چیکار کنیم 🔧',
            'اوه نه! چی شده؟ بگو ببینم 😟',
            'مشکل؟ نگران نباش حلش می‌کنیم! 💪',
            'بگو چی شده تا کمکت کنم 🛠️'
        ],
        'context': 'problem',
        'emotion': 'concerned'
    }
}

# Default Responses (More Varied & Personality-Rich)
DEFAULT_RESPONSES = [
    "یکم گیج شدم! می‌تونی ساده‌تر بگی؟ 🤔",
    "نفهمیدم چی گفتی بابا! دوباره بگو؟ 😅",
    "اوووپس! نگرفتم! یکم بیشتر توضیح بده 🙃",
    "ببخشید عزیزم کاملاً متوجه نشدم! 😊",
    "وای! گیج شدم! یکم واضح‌تر لطفاً 🤯",
    "اممم... نگرفتم! دوباره میگی؟ 🧐",
    "چی؟ یکم بلندتر! شوخی 😄 دوباره بگو",
    "هاااا؟ متوجه نشدم عزیزم! 🤨"
]

# ========================================
# 🛡️ SECURITY & SAFETY
# ========================================

# Message Validation
MAX_MESSAGE_LENGTH = 800  # Increased for longer messages
MIN_MESSAGE_LENGTH = 2
MIN_MEANINGFUL_WORDS = 1

# Anti-Spam & Duplicate Detection
NEW_MESSAGE_THRESHOLD = 45  # Reduced for faster response
SIMILARITY_THRESHOLD = 0.65  # More lenient
CACHE_SIZE = 100  # Number of messages to keep in cache

# Safety Features
FAILSAFE_ENABLED = True
EMERGENCY_STOP_CORNER_SIZE = 10  # Pixels from corner
MAX_CONSECUTIVE_ERRORS = 5

# Toxicity & Content Filtering
MAX_TOXICITY_SCORE = 0.6
BLOCKED_PATTERNS = [
    r'(spam|advertisement|promotion)',
    r'(virus|malware|hack)',
    r'(buy.*now|click.*here|visit.*site)',
]

# ========================================
# 📊 LOGGING & MONITORING
# ========================================

# Logging Configuration
LOG_FILENAME = 'telegram_ai_bot.log'
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Debug & Development
DEBUG_MODE = True
SAVE_DEBUG_SCREENSHOTS = True
SAVE_DEBUG_OCR_RESULTS = True
PERFORMANCE_MONITORING = True

# Statistics Collection
COLLECT_STATS = True
STATS_REPORT_INTERVAL = 50  # Every N messages
DETAILED_ANALYSIS_LOG = True

# ========================================
# 🎨 UI & EXPERIENCE
# ========================================

# Visual Feedback
SHOW_PROGRESS_INDICATORS = True
COLORED_CONSOLE_OUTPUT = True
EMOJI_IN_LOGS = True

# Response Personalization
USE_EMOJI = True
PERSONALITY_STYLE = 'friendly'  # formal, casual, friendly, professional
RESPONSE_VARIETY = True  # Use different responses for same intent

# ========================================
# 🚀 ADVANCED FEATURES
# ========================================

# AI Enhancement Features
ENABLE_SENTIMENT_ANALYSIS = True
ENABLE_INTENT_DETECTION = True
ENABLE_CONTEXT_AWARENESS = True
ENABLE_LEARNING_MODE = False  # Future feature

# Multi-Engine OCR
ENABLE_MULTI_OCR = True
OCR_ENGINE_PREFERENCE = 'best'  # 'tesseract', 'easyocr', 'best'
OCR_FALLBACK_ENABLED = True

# Performance Optimization
ENABLE_CACHING = True
PRELOAD_AI_MODELS = True
OPTIMIZE_FOR_SPEED = True

# Experimental Features (Use with caution)
EXPERIMENTAL_FEATURES = False
AUTO_LEARNING = False
DYNAMIC_RESPONSE_ADJUSTMENT = False

# ========================================
# 📱 PLATFORM SPECIFIC
# ========================================

# Telegram Specific
TELEGRAM_DESKTOP_MODE = True
HANDLE_MEDIA_MESSAGES = False  # Future feature
RESPOND_TO_FORWARDS = False
RESPOND_TO_REPLIES = True

# System Requirements
REQUIRED_PYTHON_VERSION = '3.8'
REQUIRED_MEMORY_MB = 1024
RECOMMENDED_MEMORY_MB = 2048

print("🚀 Advanced AI Configuration Loaded Successfully!")
print(f"🎯 Mode: {'DEBUG' if DEBUG_MODE else 'PRODUCTION'}")
print(f"🧠 AI Features: {'ENABLED' if ENABLE_SENTIMENT_ANALYSIS else 'BASIC'}")
print(f"📊 Monitoring: {'ON' if PERFORMANCE_MONITORING else 'OFF'}")
print("="*50)

# -*- coding: utf-8 -*-
"""
فایل تنظیمات ربات تلگرام - تولید شده توسط رابط گرافیکی
"""

# تنظیمات Tesseract OCR
TESSERACT_PATH = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
OCR_LANGUAGES = 'fas+eng'
OCR_CONFIG = '--psm 6'

# تنظیمات مختصات
CHAT_REGION = {
    'x': 2920,
    'y': 134,
    'width': 514,
    'height': 1252
}

INPUT_CLICK_POSITION = {
    'x': 3024,
    'y': 1368
}

SEND_BUTTON_POSITION = {
    'x': 2866,
    'y': 1372
}

# تنظیمات زمان‌بندی
CHECK_INTERVAL = 10
RESPONSE_DELAY = 2
PYAUTOGUI_PAUSE = 0.5

# قوانین پاسخ‌دهی
RESPONSE_RULES = {
    'greetings': {
        'keywords': ['سلام', 'hello', 'hi', 'hey', 'درود'],
        'response': 'سلام! چطور کمکتون کنم؟'
    },
    'time_request': {
        'keywords': ['ساعت', 'time', 'زمان', 'وقت'],
        'response': 'current_time'
    },
    'goodbyes': {
        'keywords': ['خداحافظ', 'bye', 'goodbye', 'فعلا'],
        'response': 'فعلاً! موفق باشید! 👋'
    },
    'how_are_you': {
        'keywords': ['چطوری', 'حالت', 'how are you', 'احوالت'],
        'response': 'ممنون، خوبم! شما چطورید؟ 😊'
    },
    'thanks': {
        'keywords': ['ممنون', 'مرسی', 'thank', 'متشکرم'],
        'response': 'خواهش می‌کنم! 😊'
    }
}

DEFAULT_RESPONSE = "متوجه نشدم، لطفاً واضح‌تر بگو. 🤔"

# پاسخ‌های پیش‌فرض متنوع
DEFAULT_RESPONSES = [
    "نفهمیدم چی گفتی بابا! یه بار دیگه بگو؟ 🤔",
    "اوم... نگرفتم! می‌تونی واضح‌تر بگی؟",
    "ببخشید عزیزم نفهمیدم! دوباره بگو ببینم",
    "وای نگرفتم چی گفتی! یکم بیشتر توضیح بده!"
]

# تنظیمات امنیتی
FAILSAFE_ENABLED = True
MAX_MESSAGE_LENGTH = 500
MIN_MESSAGE_LENGTH = 2

# تنظیمات تشخیص پیام
DEBUG_MODE = True
NEW_MESSAGE_THRESHOLD = 60
SIMILARITY_THRESHOLD = 0.7

# فیلترهای رابط کاربری
INTERFACE_FILTERS = [
    'KAMHEREI314', 'Click here', 'view updates', 'You joined', 'channel',
    'Emoji', 'Stickers', 'GIFs', 'Search', 'incognito', 'Incognito',
    'Sign in', 'SafeSearch', 'Allockmaks', 'Turkce', 'typing'
]

# الگوهای رابط کاربری
INTERFACE_PATTERNS = [
    r'^\s*\*\s*[A-Z]\s*\|',
    r'^[<>-]+\s*[ox]\s*[x&®@]+.*incognito',
    r'KAMHEREI314.*Sign\s+in',
    r'SafeSearch.*Mode',
    r'^[\s\-]+[ox]\s*[x&®@:]+.*',
]

# حداقل کلمات معنادار
MIN_MEANINGFUL_WORDS = 1

# الگوهای پیام واقعی
REAL_MESSAGE_INDICATORS = [
    r'[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]{2,}',
    r'[ؤئيةك]+',
    r'چطور', r'چی', r'کجا', r'کی', r'چرا', r'چه',
    r'سلام', r'مرسی', r'ممنون', r'باشه', r'اوکی',
    r'می\u200cخوام', r'می\u200cگم', r'نمی\u200cدونم',
    r'hello', r'thanks', r'please', r'can', r'what',
    r'[؟!.]',
    r'\?',
    r'[a-zA-Z]{3,}',
]

# تنظیمات لاگ‌گیری
LOG_FILENAME = 'telegram_bot.log'
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

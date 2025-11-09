# 🚀 Advanced Telegram Auto Responder v4.0

## About This Project This project was created as part of my personal AI experiments. It combines my own ideas with code and content generated using tools like ChatGPT. The main purpose is to explore and test how AI can assist in development and creativity. *Note: This is an AI-assisted project made for learning and experimentation.*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-4.0-red.svg)
![Persian](https://img.shields.io/badge/Language-Persian/English-orange.svg)

**🎯 Ultimate AI-Powered Telegram Auto Responder with Advanced Learning**

*The most comprehensive Telegram automation system with intelligent conversation capabilities*

*Persian/English Dual Language Support • TensorFlow Integration • Learning System*

</div>

---

## 🌟 Overview

An advanced, AI-powered auto-reply bot for Telegram Desktop that uses TensorFlow, computer vision, and machine learning to intelligently respond to messages. The bot learns from conversations and gradually adapts to your communication style.

### ✨ Key Features

- 🧠 **AI-Powered Analysis**: Advanced message analysis using TensorFlow and Transformers
- 🎓 **Learning System**: Learns from conversations and improves responses over time
- 🌍 **Dual Language Support**: Full Persian and English language processing
- 🔍 **Multi-Engine OCR**: Tesseract + EasyOCR for superior text recognition
- 🎯 **Intent Detection**: Smart intent classification (greetings, questions, thanks, etc.)
- 😊 **Sentiment Analysis**: Emotional context understanding
- 📊 **Performance Monitoring**: Real-time analytics and reporting
- ⚡ **Smart Response Generation**: Context-aware, personality-driven responses

---

## 🚀 Quick Start

### Method 1: One-Click Launch (Recommended)

```bash
# Navigate to project directory
cd /path/to/telegram-ai-bot

# Run the smart launcher
C:/Users/Arian/OneDrive/Desktop/telagent/.venv/Scripts/python.exe start_ai_bot.py
```

### Method 2: Direct Bot Launch

```bash
# Run the AI bot directly
C:/Users/Arian/OneDrive/Desktop/telagent/.venv/Scripts/python.exe telegram_ai_bot.py
```

---

## 📋 System Requirements

### Hardware
- **OS**: Windows 10/11
- **RAM**: Minimum 4GB (8GB recommended)
- **CPU**: Multi-core processor (16 cores optimal)
- **Storage**: 2GB free space

### Software
- **Python**: 3.8+ (3.13+ recommended)
- **Telegram Desktop**: Latest version
- **Tesseract OCR**: Optional (EasyOCR works standalone)

---

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/YourUsername/telegram-ai-bot.git
cd telegram-ai-bot
```

### 2. Automatic Setup
```bash
# Run the installation script
python install_ai_bot.py
```

### 3. Manual Setup (Alternative)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Bot
```bash
# Run coordinate setup
python start_ai_bot.py
# Select option 5: Setup Coordinates
```

---

## 🎯 Quick Setup Guide

### Step 1: Open Telegram Desktop
- Launch Telegram Desktop
- Navigate to your desired chat

### Step 2: Configure Coordinates
```bash
python start_ai_bot.py
```
Select option `5` and follow the interactive setup:
1. Move mouse to top-left of chat area
2. Move mouse to bottom-right of chat area  
3. Move mouse to text input box

### Step 3: Start Bot
Select option `1` to start the AI bot with full learning capabilities.

---

## 🧠 Learning System

### How It Works
The bot uses a sophisticated learning system that:

1. **📚 Saves Conversations**: Every interaction is stored and analyzed
2. **🎯 Pattern Recognition**: Identifies response patterns based on:
   - Message intent (greeting, question, thanks, etc.)
   - Sentiment (positive, negative, neutral)
   - Language (Persian/English)
   - User communication style

3. **🤖 Response Generation**: Creates responses using:
   - Learned conversation patterns
   - Similarity matching with previous interactions
   - Style-aware generation that matches your tone

### Learning Features
- **Automatic Learning**: No manual training required
- **Style Adaptation**: Gradually learns your communication style
- **Context Awareness**: Understands conversation context
- **Pattern Evolution**: Response patterns improve over time

### View Learning Progress
```bash
# View learning statistics and data
python learning_viewer.py
```

---

## 📊 Performance Stats

Based on latest test results (`ai_test_results_20250804_193355.json`):

| Metric | Score |
|--------|-------|
| **Message Detection Accuracy** | 90% |
| **Response Generation Rate** | 90% |
| **Average Analysis Time** | 0.17ms |
| **Overall Performance Score** | 94% |

### Language Support
- **Persian Messages**: 4 samples, 100% accuracy
- **English Messages**: 6 samples, 83% accuracy
- **Mixed Content**: Advanced filtering for UI elements

---

## 🎮 Usage

### Smart Launcher Menu
```
🎯 LAUNCHER MENU
==================================================
1. 🚀 Start Advanced AI Bot
2. 🧪 Run AI Test Suite  
3. 🔧 System Diagnostics
4. 📊 Performance Benchmark
5. ⚙️ Setup Coordinates
6. 📖 Help & Documentation
7. ❌ Exit
```

### Bot Interface
Once running, the bot displays:
```
🤖 Advanced AI Bot Running
============================================================
📊 Region: (x, y, width, height)
⏱️ Interval: 8s
🔍 Debug: ON/OFF
🧠 AI Analysis: ACTIVE
⚡ Multi-Engine OCR: ACTIVE
� Learning System: ACTIVE
============================================================
```

---

## 🔧 Configuration

### Main Config (`config.py`)
```python
# Chat region coordinates
CHAT_REGION = {
    'x': 2652, 'y': 185,
    'width': 495, 'height': 1212
}

# Response settings
CHECK_INTERVAL = 8  # seconds
RESPONSE_DELAY = 2  # seconds
```

### Advanced Config (`config_advanced.py`)
- AI model settings
- Performance optimizations
- Debug configurations
- Learning system parameters

---

## 🧪 Testing

### Run Test Suite
```bash
python start_ai_bot.py
# Select option 2: Run AI Test Suite
```

### Test Coverage
- **Message Detection**: Real vs interface text
- **Language Recognition**: Persian/English classification
- **Intent Analysis**: Greeting, question, thanks, etc.
- **Response Generation**: Context-appropriate replies
- **Learning System**: Pattern recognition and adaptation

---

## 📈 Monitoring & Analytics

### Real-time Monitoring
- Live message detection logging
- Response generation tracking
- Performance metrics
- Learning progress statistics

### Performance Reports
The bot generates detailed reports including:
- Total runtime and messages processed
- Response success rate
- AI analysis performance
- Learning system statistics
- OCR engine performance comparison

### Learning Analytics
```bash
# View learning data
python learning_viewer.py

# Export learning data
# Select option 5 in learning viewer
```

---

## 🛠️ Advanced Features

### Multi-Engine OCR
- **Primary**: EasyOCR (CPU optimized)
- **Secondary**: Tesseract (optional)
- **Auto-Selection**: Best result based on confidence

### AI Components
- **TensorFlow**: Deep learning analysis
- **Transformers**: Advanced NLP processing
- **scikit-learn**: Text similarity and classification
- **HAZM**: Persian language processing

### Learning System
- **Conversation Storage**: JSON-based data persistence
- **Pattern Recognition**: TF-IDF vectorization
- **Style Analysis**: User communication profiling
- **Response Evolution**: Continuous improvement

---

## 🔍 Troubleshooting

### Common Issues

**1. Bot Not Responding**
```bash
# Check coordinates
python start_ai_bot.py
# Select option 5: Setup Coordinates
```

**2. Low Detection Accuracy**
- Ensure Telegram is in foreground
- Check chat region coordinates
- Verify text size and clarity

**3. Learning System Issues**
```bash
# Check learning data
python learning_viewer.py
# Select option 4: Show Learning Progress
```

### Debug Mode
Enable debug mode in `config.py`:
```python
DEBUG_MODE = True
```

### Log Files
- `telegram_ai_bot.log`: Main bot activity
- `conversation_data/`: Learning system data
- `ai_test_results_*.json`: Test results

---

## 📁 Project Structure

```
telegram-ai-bot/
├── 🤖 Core Bot Files
│   ├── telegram_ai_bot.py          # Main AI bot (94% accuracy)
│   ├── telegram_enhanced_bot.py    # Lightweight version
│   └── telegram_auto_reply.py      # Basic version
│
├── 🧠 Learning System
│   ├── learning_system.py          # ML learning engine
│   └── learning_viewer.py          # Data management tool
│
├── � Launchers & Tools
│   ├── start_ai_bot.py            # Smart launcher
│   ├── start_bot.bat              # Windows batch file
│   └── install_ai_bot.py          # Installation script
│
├── ⚙️ Configuration
│   ├── config.py                  # Basic settings
│   ├── config_advanced.py         # Advanced AI settings
│   └── requirements.txt           # Dependencies
│
├── 🧪 Testing & Analysis
│   ├── test_ai_suite.py           # Comprehensive testing
│   ├── performance_analyzer.py    # Performance monitoring
│   └── ai_test_results_*.json     # Test results
│
├── 🔧 Utilities
│   ├── gui_configurator.py        # GUI setup tool
│   ├── project_summary.py         # Project documentation
│   └── final_test.py             # Final validation
│
└── 📊 Data & Logs
    ├── conversation_data/          # Learning system data
    ├── *.log                      # Activity logs
    └── *.png                      # Debug screenshots
```

---

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/YourUsername/telegram-ai-bot.git

# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_ai_suite.py
```

### Code Style
- Follow PEP 8 guidelines
- Add type hints for new functions
- Document new features thoroughly
- Test on Windows 10/11

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **TensorFlow Team**: Advanced AI capabilities
- **Transformers Library**: State-of-the-art NLP
- **EasyOCR**: Excellent OCR performance
- **HAZM**: Persian language processing
- **PyAutoGUI**: GUI automation

---

## 📞 Support

### Getting Help
1. Check the troubleshooting section
2. Review log files for errors
3. Use the diagnostic tools:
   ```bash
   python start_ai_bot.py
   # Select option 3: System Diagnostics
   ```

### Performance Optimization
- **RAM Usage**: Monitor with built-in tools
- **Response Time**: Adjust `CHECK_INTERVAL` in config
- **Learning Speed**: Review learning statistics regularly

---

## � Future Roadmap

- [ ] **GPU Acceleration**: CUDA support for faster processing
- [ ] **Voice Recognition**: Audio message support
- [ ] **Multi-Language**: Arabic, Spanish, French support
- [ ] **Cloud Sync**: Conversation backup and sync
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Plugin System**: Extensible architecture

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

**💡 Have questions? Open an issue!**

**🚀 Ready to get started? Run the installation!**

---

**Developed with ❤️ by Arian**  
*Last Updated: August 2025 • Version: 3.0*

</div>

## پیش‌نیازها 📋

### سیستم
- ویندوز 10/11
- Python 3.8 یا بالاتر
- حداقل 4 گیگابایت رم
- تلگرام دسکتاپ

### نرم‌افزارها
- [Python 3.11+](https://www.python.org/downloads/)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (شامل زبان فارسی)

## نصب و راه‌اندازی 🚀

### گام 1: کلون کردن پروژه
```bash
git clone https://github.com/your-repo/telegram-auto-reply.git
cd telegram-auto-reply
```

### گام 2: اجرای اسکریپت راه‌اندازی
```bash
python setup.py
```

این اسکریپت:
- بررسی می‌کند که تمام پیش‌نیازها نصب شده باشند
- پکیج‌های مورد نیاز را نصب می‌کند  
- راهنمای نصب Tesseract را نمایش می‌دهد
- میانبر روی دسکتاپ ایجاد می‌کند

### گام 3: نصب Tesseract OCR

1. از [این لینک](https://github.com/UB-Mannheim/tesseract/wiki) فایل نصب را دانلود کنید
2. حین نصب، مطمئن شوید که زبان **Persian** انتخاب شده باشد
3. مسیر نصب پیشنهادی: `D:\Program Files\Tesseract-OCR\`

## استفاده 🖱️

### راه‌اندازی اولیه

1. **تلگرام دسکتاپ را باز کنید** و به چت مورد نظر بروید
2. **اسکریپت را اجرا کنید**:
   ```bash
   python telegram_auto_reply.py
   ```
3. **گزینه "تنظیم تعاملی مختصات"** را انتخاب کنید
4. **دستورالعمل‌های روی صفحه** را دنبال کنید:
   - ماوس را روی گوشه بالا-چپ ناحیه چت ببرید
   - ماوس را روی گوشه پایین-راست ناحیه چت ببرید  
   - ماوس را روی جعبه ورودی متن ببرید

### اجرای عادی
پس از تنظیم اولیه، فقط کافی است اسکریپت را اجرا کنید و ربات شروع به کار خواهد کرد.

## منطق پاسخ‌دهی 🧠

ربات بر اساس کلمات کلیدی پاسخ می‌دهد:

| ورودی | پاسخ |
|-------|------|
| سلام، hello، hi | "سلام! چطور کمکتون کنم؟" |
| ساعت، time، زمان | نمایش ساعت و تاریخ فعلی |
| خداحافظ، bye | "فعلاً! موفق باشید! 👋" |
| چطوری، حالت | "ممنون، خوبم! شما چطورید؟ 😊" |
| ممنون، مرسی، thank | "خواهش می‌کنم! همیشه در خدمتم! 😊" |
| سایر موارد | "متوجه نشدم، لطفاً واضح‌تر بگو. 🤔" |

## تنظیمات ⚙️

### فایل `config.py`
تمام تنظیمات در فایل `config.py` قابل تغییر است:

```python
# تنظیم منطقه چت
CHAT_REGION = {
    'x': 100,       # موقعیت افقی
    'y': 200,       # موقعیت عمودی  
    'width': 800,   # عرض
    'height': 400   # ارتفاع
}

# فاصله زمانی بررسی (ثانیه)
CHECK_INTERVAL = 10

# قوانین پاسخ‌دهی
RESPONSE_RULES = {
    'greetings': {
        'keywords': ['سلام', 'hello'],
        'response': 'سلام! چطور کمکتون کنم؟'
    }
}
```

### افزودن پاسخ‌های جدید
برای افزودن قوانین پاسخ‌دهی جدید، فایل `config.py` را ویرایش کنید:

```python
'custom_rule': {
    'keywords': ['کلمه1', 'کلمه2'],
    'response': 'پاسخ دلخواه شما'
}
```

## ساختار پروژه 📁

```
telegram-auto-reply/
├── telegram_auto_reply.py    # اسکریپت اصلی ربات
├── config.py                 # فایل تنظیمات
├── setup.py                  # اسکریپت راه‌اندازی
├── README.md                 # راهنمای استفاده
└── requirements.txt          # پکیج‌های مورد نیاز
```

## عیب‌یابی 🔧

### مشکلات رایج

**1. Tesseract یافت نمی‌شود**
```
❌ Tesseract OCR در مسیر ... یافت نشد!
```
**راه‌حل**: مسیر Tesseract را در `config.py` تصحیح کنید:
```python
TESSERACT_PATH = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
```

**2. متن تشخیص داده نمی‌شود**
- کیفیت تصویر چت را بررسی کنید
- منطقه چت را دوباره تنظیم کنید
- اندازه فونت تلگرام را بزرگ‌تر کنید

**3. ربات پاسخ نمی‌دهد**
- مختصات جعبه ورودی را بررسی کنید
- تلگرام در پیش‌زمینه باشد
- فایل لاگ (`telegram_bot.log`) را بررسی کنید

### فایل‌های لاگ
تمام فعالیت‌های ربات در فایل `telegram_bot.log` ثبت می‌شود.

## محدودیت‌ها ⚠️

- فقط با تلگرام دسکتاپ کار می‌کند
- نیاز به تنظیم دستی مختصات برای هر دستگاه
- تشخیص متن بستگی به کیفیت تصویر دارد
- فقط از آخرین پیام دریافتی پاسخ می‌دهد

## مشارکت 🤝

برای مشارکت در بهبود این پروژه:

1. پروژه را Fork کنید
2. شاخه جدید ایجاد کنید (`git checkout -b feature/amazing-feature`)
3. تغییرات را Commit کنید (`git commit -m 'Add amazing feature'`)
4. به شاخه Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request ایجاد کنید

## مجوز 📄

این پروژه تحت مجوز MIT منتشر شده است - فایل [LICENSE](LICENSE) را برای جزئیات بیشتر مطالعه کنید.

## تشکر 🙏

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) برای موتور تشخیص متن
- [PyAutoGUI](https://github.com/asweigart/pyautogui) برای اتوماسیون رابط کاربری
- [pytesseract](https://github.com/madmaze/pytesseract) برای پل ارتباطی پایتون-Tesseract

## پشتیبانی 💬

اگر مشکلی داشتید:
1. ابتدا بخش عیب‌یابی را مطالعه کنید
2. فایل لاگ را بررسی کنید  
3. در صورت ادامه مشکل، Issue جدید ایجاد کنید

---

**توسعه‌دهنده**: Arian  
**آخرین بروزرسانی**: آگوست 2025  
**نسخه**: 1.0.0

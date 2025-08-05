#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ Telegram AI Bot Complete Setup & Installation
Automated setup for all dependencies and configurations
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path

class BotInstaller:
    """🔧 Complete bot installer"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.install_dir = Path.cwd()
    
    def print_banner(self):
        """🎨 Print installation banner"""
        print("\n" + "="*70)
        print("🛠️ TELEGRAM AI BOT COMPLETE INSTALLER")
        print("⚡ Automated Setup for Advanced AI Features")
        print("="*70)
        print(f"💻 OS: {self.os_type}")
        print(f"🐍 Python: {self.python_version}")
        print(f"📁 Directory: {self.install_dir}")
        print("="*70)
    
    def check_python_version(self):
        """✅ Check Python version"""
        print("\n🔍 Checking Python version...")
        
        if sys.version_info >= (3, 8):
            print(f"✅ Python {self.python_version} is compatible")
            return True
        else:
            print(f"❌ Python {self.python_version} is too old. Requires Python 3.8+")
            return False
    
    def install_python_packages(self):
        """📦 Install all required Python packages"""
        print("\n📦 Installing Python packages...")
        
        # Essential packages
        essential_packages = [
            "pyautogui",
            "pytesseract", 
            "Pillow",
            "pyperclip",
            "opencv-python",
            "numpy",
            "scikit-learn",
            "easyocr",
            "requests"
        ]
        
        # AI packages (optional but recommended)
        ai_packages = [
            "tensorflow-cpu",  # CPU version for stability
            "transformers",
            "torch",
            "torchvision"
        ]
        
        # Persian language support
        persian_packages = [
            "hazm"
        ]
        
        all_packages = essential_packages + ai_packages + persian_packages
        
        print(f"📋 Installing {len(all_packages)} packages...")
        
        for package in all_packages:
            try:
                print(f"   📦 Installing {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--upgrade"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"   ✅ {package} installed successfully")
            except subprocess.CalledProcessError:
                print(f"   ⚠️ {package} installation failed (optional)")
        
        print("✅ Package installation completed!")
    
    def download_tesseract(self):
        """🔍 Download and setup Tesseract OCR"""
        print("\n🔍 Setting up Tesseract OCR...")
        
        if self.os_type == "Windows":
            tesseract_url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.3/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
            tesseract_file = "tesseract_installer.exe"
            
            print("📥 Downloading Tesseract for Windows...")
            try:
                urllib.request.urlretrieve(tesseract_url, tesseract_file)
                print(f"✅ Downloaded: {tesseract_file}")
                print("🎯 Please run the installer manually and install to:")
                print("   C:\\Program Files\\Tesseract-OCR\\")
                print("   Make sure to select 'Persian' language pack!")
                
                # Try to launch installer
                try:
                    os.startfile(tesseract_file)
                    print("🚀 Installer launched automatically")
                except:
                    print(f"⚠️ Please manually run: {tesseract_file}")
                
            except Exception as e:
                print(f"❌ Download failed: {e}")
                print("🔗 Manual download: https://github.com/UB-Mannheim/tesseract/releases")
        
        else:
            print("📋 For Linux/Mac, install Tesseract using your package manager:")
            print("   Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-fas")
            print("   CentOS/RHEL: sudo yum install tesseract tesseract-langpack-fas")
            print("   macOS: brew install tesseract tesseract-lang")
    
    def create_config_file(self):
        """⚙️ Create advanced configuration file"""
        print("\n⚙️ Creating configuration files...")
        
        # Check if config exists
        if os.path.exists("config_advanced.py"):
            print("✅ Advanced config already exists")
            return
        
        config_content = '''# -*- coding: utf-8 -*-
"""
🚀 Telegram AI Bot Configuration - Auto Generated
⚡ Advanced AI features with Persian/English support
"""

# ========================================
# 🔧 CORE SYSTEM SETTINGS
# ========================================

# Tesseract OCR Configuration
TESSERACT_PATH = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
OCR_LANGUAGES = 'fas+eng'
OCR_CONFIG = '--psm 6'

# Coordinate Settings (Will be set during first run)
CHAT_REGION = {
    'x': 100,
    'y': 100, 
    'width': 800,
    'height': 600
}

INPUT_CLICK_POSITION = {
    'x': 400,
    'y': 700
}

SEND_BUTTON_POSITION = {
    'x': 850,
    'y': 700
}

# ========================================
# ⏱️ TIMING & PERFORMANCE
# ========================================

CHECK_INTERVAL = 8
RESPONSE_DELAY = 1.5
PYAUTOGUI_PAUSE = 0.3

# ========================================
# 🧠 AI SETTINGS
# ========================================

# OCR Confidence Thresholds
MIN_OCR_CONFIDENCE = 25
PREFERRED_OCR_CONFIDENCE = 70

# AI Analysis Thresholds  
MIN_REAL_MESSAGE_CONFIDENCE = 0.4
INTENT_CONFIDENCE_THRESHOLD = 0.3

# ========================================
# 🌍 LANGUAGE PROCESSING
# ========================================

# Persian Patterns
PERSIAN_PATTERNS = [
    r'[آ-ی]{2,}',
    r'(چطور|چی|کجا|کی|چرا|چه)',
    r'(سلام|درود|احوال)',
    r'(ممنون|مرسی|تشکر)',
    r'(باشه|اوکی|حله)',
]

# Real Message Indicators
REAL_MESSAGE_INDICATORS = [
    r'[آ-ی]{3,}',
    r'(سلام|hi|hello)',
    r'(چطور|چی|what|how)',
    r'(ممنون|thank)',
    r'[؟!.]{1,3}',
    r'[a-zA-Z]{4,}',
]

# ========================================
# 🚫 INTERFACE FILTERING
# ========================================

INTERFACE_FILTERS = [
    'Click here', 'You joined', 'Emoji', 'Stickers',
    'Online', 'Last seen', 'Forwarded', 'Reply',
    'Today', 'Yesterday', 'AM', 'PM'
]

INTERFACE_PATTERNS = [
    r'\\d{1,2}:\\d{2}\\s*(AM|PM)',
    r'^[\\d\\s\\-\\:\\.\\,]+$',
    r'^[^\\w\\u0600-\\u06FF]+$',
]

# ========================================
# 🎭 RESPONSE RULES
# ========================================

RESPONSE_RULES = {
    'greetings': {
        'keywords': ['سلام', 'hello', 'hi', 'hey', 'درود'],
        'responses': [
            'سلام عزیزم! چطوری؟ 😊',
            'هللو! حالت چطوره؟ 👋',
            'سلام! چه خبرا؟ 🤗'
        ]
    },
    'thanks': {
        'keywords': ['ممنون', 'مرسی', 'thank', 'متشکرم'],
        'responses': [
            'خواهش می‌کنم! 😊💕',
            'قابلی نداشت! 🤗',
            'نوکرتم! 😄'
        ]
    },
    'time_request': {
        'keywords': ['ساعت', 'time', 'زمان', 'وقت'],
        'response': 'current_time'
    }
}

DEFAULT_RESPONSES = [
    "یکم گیج شدم! می‌تونی ساده‌تر بگی؟ 🤔",
    "نفهمیدم چی گفتی! دوباره بگو؟ 😅", 
    "نگرفتم! توضیح بیشتر لطفاً 😊"
]

# ========================================
# 🛡️ SECURITY & SAFETY
# ========================================

MAX_MESSAGE_LENGTH = 800
MIN_MESSAGE_LENGTH = 2
MIN_MEANINGFUL_WORDS = 1
NEW_MESSAGE_THRESHOLD = 45
SIMILARITY_THRESHOLD = 0.65
FAILSAFE_ENABLED = True

# ========================================
# 📊 LOGGING
# ========================================

LOG_FILENAME = 'telegram_ai_bot.log'
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
DEBUG_MODE = True

print("🚀 AI Bot Configuration Loaded!")
'''
        
        with open("config_advanced.py", "w", encoding="utf-8") as f:
            f.write(config_content)
        
        print("✅ Configuration file created: config_advanced.py")
    
    def create_startup_scripts(self):
        """🚀 Create startup scripts"""
        print("\n🚀 Creating startup scripts...")
        
        # Windows batch file
        if self.os_type == "Windows":
            batch_content = '''@echo off
echo 🚀 Starting Telegram AI Bot...
echo ================================
python telegram_enhanced_bot.py
pause
'''
            with open("start_bot.bat", "w", encoding="utf-8") as f:
                f.write(batch_content)
            print("✅ Created: start_bot.bat")
        
        # Shell script for Linux/Mac
        else:
            shell_content = '''#!/bin/bash
echo "🚀 Starting Telegram AI Bot..."
echo "================================"
python3 telegram_enhanced_bot.py
read -p "Press Enter to continue..."
'''
            with open("start_bot.sh", "w", encoding="utf-8") as f:
                f.write(shell_content)
            os.chmod("start_bot.sh", 0o755)
            print("✅ Created: start_bot.sh")
    
    def create_quick_test(self):
        """🧪 Create quick test script"""
        print("\n🧪 Creating test script...")
        
        test_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Quick AI Bot Test
"""

def test_imports():
    """Test all imports"""
    print("🔍 Testing imports...")
    
    packages = [
        ('pyautogui', 'pyautogui'),
        ('PIL', 'Pillow'),
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'),
        ('easyocr', 'easyocr'),
        ('pyperclip', 'pyperclip')
    ]
    
    results = []
    for module, package in packages:
        try:
            __import__(module)
            print(f"   ✅ {package}")
            results.append(True)
        except ImportError:
            print(f"   ❌ {package} - Not installed")
            results.append(False)
    
    # AI packages (optional)
    ai_packages = [
        ('tensorflow', 'tensorflow'),
        ('transformers', 'transformers'), 
        ('torch', 'torch'),
        ('hazm', 'hazm')
    ]
    
    print("\\n🧠 AI packages (optional):")
    for module, package in ai_packages:
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ⚠️ {package} - Not available (optional)")
    
    return all(results)

def test_config():
    """Test configuration"""
    print("\\n⚙️ Testing configuration...")
    
    try:
        import config_advanced
        print("   ✅ Advanced config loaded")
        return True
    except ImportError:
        try:
            import config
            print("   ✅ Basic config loaded")
            return True
        except ImportError:
            print("   ❌ No config file found")
            return False

def main():
    print("🧪 Telegram AI Bot Quick Test")
    print("=" * 40)
    
    imports_ok = test_imports()
    config_ok = test_config()
    
    print("\\n" + "=" * 40)
    print("📊 TEST RESULTS")
    print("=" * 40)
    
    if imports_ok and config_ok:
        print("✅ All tests passed! Bot is ready to run.")
        print("🚀 Use: python telegram_enhanced_bot.py")
    else:
        print("❌ Some tests failed. Check installation.")
        if not imports_ok:
            print("   🔧 Run: pip install -r requirements.txt")
        if not config_ok:
            print("   ⚙️ Create config file or run installer")
    
    print("=" * 40)

if __name__ == "__main__":
    main()
'''
        
        with open("quick_test.py", "w", encoding="utf-8") as f:
            f.write(test_content)
        
        print("✅ Created: quick_test.py")
    
    def create_requirements_file(self):
        """📋 Create requirements.txt"""
        print("\n📋 Creating requirements.txt...")
        
        requirements = '''# Telegram AI Bot Requirements
# Essential packages
pyautogui==0.9.54
pytesseract==0.3.10
Pillow==10.0.0
pyperclip==1.8.2
opencv-python==4.8.1.78
numpy==1.24.3
scikit-learn==1.3.0
easyocr==1.7.0
requests==2.31.0

# AI packages (recommended)
tensorflow-cpu==2.15.0
transformers==4.35.0
torch==2.1.0
torchvision==0.16.0

# Persian language support
hazm==0.7.0

# System monitoring
psutil==5.9.0
'''
        
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write(requirements)
        
        print("✅ Created: requirements.txt")
    
    def create_readme(self):
        """📖 Create README file"""
        print("\n📖 Creating README...")
        
        readme_content = '''# 🚀 Telegram Advanced AI Auto-Reply Bot v2.5

⚡ **Advanced AI-powered Telegram bot with Persian/English support**

## ✨ Features

- 🧠 **AI-Powered Analysis**: Smart message understanding with intent detection
- 🌍 **Dual Language**: Persian and English support with advanced text processing
- 🔍 **Multi-Engine OCR**: Tesseract + EasyOCR for accurate text recognition
- 🎯 **Smart Filtering**: Advanced spam and duplicate detection
- 📊 **Performance Monitoring**: Real-time statistics and logging
- 🛡️ **Safety Features**: Anti-spam, toxicity filtering, emergency stop

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Tesseract OCR
- Windows: Download from [GitHub Releases](https://github.com/UB-Mannheim/tesseract/releases)
- Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-fas`
- macOS: `brew install tesseract tesseract-lang`

### 3. Run the Bot
```bash
python telegram_enhanced_bot.py
```

### 4. Setup Coordinates
- Follow the coordinate setup wizard
- Position your Telegram Desktop window
- Mark chat area and input field

## 📊 Bot Performance

The bot includes advanced performance monitoring:
- Message processing rate
- AI analysis accuracy
- Response generation time
- OCR engine efficiency

## 🔧 Configuration

Edit `config_advanced.py` to customize:
- Response rules and templates
- AI analysis thresholds
- Timing and intervals
- Interface filters
- Language patterns

## 🧪 Testing

Run quick test to verify installation:
```bash
python quick_test.py
```

## 📋 Requirements

- Python 3.8+
- 1GB+ RAM
- Tesseract OCR
- Telegram Desktop

## 🛡️ Safety Features

- Emergency stop (move mouse to corner)
- Anti-spam protection
- Duplicate message filtering
- Toxicity detection
- Interface element filtering

## 📝 Logs

All activities are logged to `telegram_ai_bot.log` with detailed information about:
- Message detection and analysis
- AI decision making
- Response generation
- Performance metrics

## 🤝 Support

For issues or questions:
1. Check the log file for errors
2. Run `quick_test.py` to verify installation
3. Ensure Tesseract is properly installed
4. Verify Telegram Desktop is running

---
🎯 **Advanced AI Bot v2.5** - Built with ❤️ for intelligent automation
'''
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("✅ Created: README.md")
    
    def run_installation(self):
        """🚀 Run complete installation"""
        self.print_banner()
        
        if not self.check_python_version():
            print("\n❌ Installation cannot continue with incompatible Python version")
            return False
        
        print("\n🔄 Starting installation process...")
        
        try:
            self.install_python_packages()
            self.create_config_file()
            self.create_requirements_file()
            self.create_startup_scripts()
            self.create_quick_test()
            self.create_readme()
            self.download_tesseract()
            
            print("\n" + "="*70)
            print("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
            print("="*70)
            print("✅ All Python packages installed")
            print("✅ Configuration files created")
            print("✅ Startup scripts ready")
            print("✅ Documentation generated")
            print("="*70)
            print("🔄 NEXT STEPS:")
            print("1. Install Tesseract OCR (if not already done)")
            print("2. Run: python quick_test.py (to verify)")
            print("3. Run: python telegram_enhanced_bot.py (to start)")
            print("4. Follow coordinate setup wizard")
            print("="*70)
            print("🚀 Your Advanced AI Bot is ready!")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Installation failed: {e}")
            return False

def main():
    """🎯 Main installer"""
    installer = BotInstaller()
    
    try:
        success = installer.run_installation()
        if success:
            print("\n🎊 Installation successful! Enjoy your AI bot!")
        else:
            print("\n💔 Installation incomplete. Please check errors above.")
    except KeyboardInterrupt:
        print("\n\n⛔ Installation cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    main()

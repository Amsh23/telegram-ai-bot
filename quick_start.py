#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Quick Start - Telegram Auto Responder
راه‌اندازی سریع سیستم پاسخ‌دهی خودکار تلگرام
"""

import os
import sys
import json
import time

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║              🤖 Telegram Auto Responder                     ║
║                  راه‌اندازی سریع                           ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_requirements():
    """✅ Check if all files are present"""
    required_files = [
        'advanced_telegram_responder.py',
        'simple_learning.py', 
        'smart_ocr.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("✅ All required files present")
    return True

def create_default_config():
    """📁 Create default configuration"""
    config = {
        "telegram_executable": "C:\\TelegramDesktop\\Telegram.exe",
        "monitoring_interval": 5,
        "response_delay": 3,
        "auto_response_enabled": True,
        "max_responses_per_chat": 3,
        "working_hours": {
            "enabled": False,
            "start": "09:00", 
            "end": "18:00"
        },
        "response_triggers": [
            "سلام", "hello", "hi", "hey",
            "؟", "?", "چطوری", "how are you",
            "کجایی", "where are you", "چه خبر"
        ],
        "excluded_chats": [
            "Saved Messages", 
            "پیام‌های ذخیره شده",
            "Telegram"
        ],
        "screen_regions": {
            "chat_list": {"x": 0, "y": 100, "width": 300, "height": 600},
            "chat_area": {"x": 300, "y": 100, "width": 700, "height": 600}, 
            "input_area": {"x": 300, "y": 650, "width": 600, "height": 50}
        }
    }
    
    with open('telegram_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✅ Default configuration created")

def setup_directories():
    """📂 Create necessary directories"""
    directories = ['conversation_data', 'logs', 'temp_images']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Directories created")

def quick_setup():
    """⚡ Quick setup process"""
    print("⚡ Starting Quick Setup...")
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Create directories
    setup_directories()
    
    # Create config if not exists
    if not os.path.exists('telegram_config.json'):
        create_default_config()
    else:
        print("ℹ️ Configuration file already exists")
    
    print("\n✅ Quick setup completed!")
    return True

def show_menu():
    """📋 Show main menu"""
    print("\n🎯 Quick Start Options:")
    print("1. ⚡ Quick Setup (First time)")
    print("2. 🚀 Start Auto Responder")
    print("3. 🎯 Setup Screen Coordinates")
    print("4. 🧪 Test System")
    print("5. ⚙️ Advanced Options")
    print("6. 📚 View Guide")
    print("7. 🚪 Exit")
    
def run_auto_responder():
    """🚀 Run the auto responder"""
    print("\n🚀 Starting Telegram Auto Responder...")
    
    if not os.path.exists('telegram_config.json'):
        print("❌ Configuration not found. Running quick setup first...")
        if quick_setup():
            time.sleep(2)
        else:
            return
    
    try:
        os.system('python advanced_telegram_responder.py')
    except KeyboardInterrupt:
        print("\n🛑 Auto responder stopped")

def setup_coordinates():
    """🎯 Setup screen coordinates"""
    print("\n🎯 Setting up screen coordinates...")
    print("This will help the system find Telegram windows")
    
    try:
        import subprocess
        subprocess.run([sys.executable, 'advanced_telegram_responder.py'], 
                      input='2\n', text=True, timeout=60)
    except:
        print("❌ Failed to run coordinate setup")

def test_system():
    """🧪 Test system components"""
    print("\n🧪 Testing System Components...")
    
    print("\n1. Testing Simple Learning System:")
    try:
        os.system('python simple_learning.py')
        print("✅ Learning system OK")
    except:
        print("❌ Learning system failed")
    
    print("\n2. Testing Smart OCR:")
    try:
        os.system('python smart_ocr.py')
        print("✅ OCR system OK")  
    except:
        print("❌ OCR system failed")

def advanced_options():
    """⚙️ Advanced options menu"""
    print("\n⚙️ Advanced Options:")
    print("1. 📊 View Current Configuration")
    print("2. 🔧 Edit Configuration")
    print("3. 📈 View Learning Statistics") 
    print("4. 🧹 Clean Temporary Files")
    print("5. 🔄 Reload Training Data")
    print("6. ⬅️ Back to Main Menu")
    
    choice = input("\nSelect option (1-6): ").strip()
    
    if choice == "1":
        # View config
        try:
            with open('telegram_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("\n📊 Current Configuration:")
            for key, value in config.items():
                print(f"  {key}: {value}")
        except:
            print("❌ Configuration file not found")
            
    elif choice == "2":
        print("\n🔧 To edit configuration:")
        print("1. Open 'telegram_config.json' in text editor")
        print("2. Modify settings as needed")
        print("3. Save and restart the system")
        
    elif choice == "3":
        try:
            os.system('python -c "from simple_learning import SimpleLearningSystem; s=SimpleLearningSystem(); print(s.get_stats())"')
        except:
            print("❌ Failed to get statistics")
            
    elif choice == "4":
        # Clean temp files
        import glob
        files_to_clean = glob.glob('temp_image_*.png') + glob.glob('telegram_capture_*.png')
        for file in files_to_clean:
            try:
                os.remove(file)
            except:
                pass
        print(f"🧹 Cleaned {len(files_to_clean)} temporary files")
        
    elif choice == "5":
        print("\n🔄 Reloading training data...")
        try:
            os.system('python load_dataset.py')
        except:
            print("❌ Failed to reload data")

def show_guide():
    """📚 Show quick guide"""
    guide = """
📚 Quick Start Guide:

🎯 First Time Setup:
1. Run option 1: "⚡ Quick Setup"
2. Run option 3: "🎯 Setup Screen Coordinates"
3. Open Telegram Desktop
4. Run option 2: "🚀 Start Auto Responder"

⌨️ Control Keys (while running):
- Press 'q' to quit
- Press 'p' to pause/resume
- Press 's' to show statistics

⚙️ Important Settings:
- monitoring_interval: How often to check (seconds)
- response_delay: Delay before responding (seconds)
- auto_response_enabled: Enable/disable auto responses

🛡️ Safety Tips:
- Test on personal chats first
- Monitor the system activity
- Use excluded_chats for important groups
- Set working_hours if needed

📱 Screen Setup:
- chat_list: Left side chat list area
- chat_area: Main conversation area
- input_area: Message input field

🔧 Troubleshooting:
- Check telegram_config.json for correct paths
- Ensure Telegram Desktop is running
- Verify screen coordinates are correct
- Check logs for error messages
    """
    print(guide)

def main():
    """🎯 Main function"""
    print_banner()
    
    while True:
        try:
            show_menu()
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                quick_setup()
                
            elif choice == "2":
                run_auto_responder()
                
            elif choice == "3":
                setup_coordinates()
                
            elif choice == "4":
                test_system()
                
            elif choice == "5":
                advanced_options()
                
            elif choice == "6":
                show_guide()
                
            elif choice == "7":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-7.")
                
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

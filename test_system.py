# -*- coding: utf-8 -*-
"""
اسکریپت تست سیستم ربات تلگرام
این اسکریپت تمام اجزای سیستم را تست می‌کند
"""

import sys
import os
from pathlib import Path

def test_imports():
    """تست import کردن پکیج‌ها"""
    print("🔍 تست import پکیج‌ها...")
    
    try:
        import pyautogui
        print("✅ pyautogui")
    except ImportError:
        print("❌ pyautogui - لطفاً نصب کنید: pip install pyautogui")
        return False
    
    try:
        import pytesseract
        print("✅ pytesseract")
    except ImportError:
        print("❌ pytesseract - لطفاً نصب کنید: pip install pytesseract")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow")
    except ImportError:
        print("❌ Pillow - لطفاً نصب کنید: pip install Pillow")
        return False
    
    try:
        import schedule
        print("✅ schedule")
    except ImportError:
        print("❌ schedule - لطفاً نصب کنید: pip install schedule")
        return False
    
    return True

def test_config():
    """تست فایل تنظیمات"""
    print("\n🔍 تست فایل تنظیمات...")
    
    try:
        import config
        print("✅ فایل config.py بارگذاری شد")
        
        # بررسی متغیرهای مهم
        required_vars = [
            'TESSERACT_PATH', 'CHAT_REGION', 'INPUT_CLICK_POSITION',
            'CHECK_INTERVAL', 'RESPONSE_RULES'
        ]
        
        for var in required_vars:
            if hasattr(config, var):
                print(f"✅ {var}")
            else:
                print(f"❌ {var} - متغیر در config.py یافت نشد")
                return False
        
        return True
        
    except ImportError:
        print("❌ فایل config.py یافت نشد!")
        return False

def test_tesseract():
    """تست Tesseract OCR"""
    print("\n🔍 تست Tesseract OCR...")
    
    try:
        import config
        
        if not os.path.exists(config.TESSERACT_PATH):
            print(f"❌ Tesseract در مسیر {config.TESSERACT_PATH} یافت نشد!")
            return False
        
        print(f"✅ فایل Tesseract یافت شد: {config.TESSERACT_PATH}")
        
        # تست عملکرد Tesseract
        import pytesseract
        from PIL import Image
        
        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH
        
        # ایجاد تصویر تست
        test_image = Image.new('RGB', (200, 50), color='white')
        
        # تست با متن انگلیسی
        result = pytesseract.image_to_string(test_image, lang='eng')
        print("✅ تست انگلیسی Tesseract موفق")
        
        # تست با متن فارسی (اگر نصب باشد)
        try:
            result = pytesseract.image_to_string(test_image, lang='fas')
            print("✅ تست فارسی Tesseract موفق")
        except:
            print("⚠️ زبان فارسی در Tesseract نصب نشده - اختیاری")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست Tesseract: {e}")
        return False

def test_main_script():
    """تست اسکریپت اصلی"""
    print("\n🔍 تست اسکریپت اصلی...")
    
    if not os.path.exists('telegram_auto_reply.py'):
        print("❌ فایل telegram_auto_reply.py یافت نشد!")
        return False
    
    try:
        # تست import کلاس اصلی
        sys.path.insert(0, os.getcwd())
        from telegram_auto_reply import TelegramAutoReply
        
        print("✅ کلاس TelegramAutoReply بارگذاری شد")
        
        # ایجاد نمونه تست
        bot = TelegramAutoReply()
        print("✅ نمونه ربات ایجاد شد")
        
        # تست تابع تحلیل پیام
        test_messages = [
            "سلام",
            "ساعت چنده؟",
            "خداحافظ",
            "متن تصادفی"
        ]
        
        for msg in test_messages:
            response = bot.analyze_message(msg)
            if response:
                print(f"✅ پیام: '{msg}' -> پاسخ: '{response[:30]}...'")
            else:
                print(f"⚠️ پیام: '{msg}' -> بدون پاسخ")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست اسکریپت اصلی: {e}")
        return False

def generate_report():
    """تولید گزارش نهایی"""
    print("\n" + "="*60)
    print("📊 گزارش تست سیستم")
    print("="*60)
    
    tests = [
        ("تست پکیج‌ها", test_imports),
        ("تست تنظیمات", test_config),
        ("تست Tesseract", test_tesseract),
        ("تست اسکریپت اصلی", test_main_script)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "="*60)
    print("📈 خلاصه نتایج")
    print("="*60)
    
    all_passed = True
    for test_name, success in results:
        status = "✅ موفق" if success else "❌ ناموفق"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 تمام تست‌ها موفق! سیستم آماده اجرا است.")
        print("\nبرای اجرای ربات:")
        print("python telegram_auto_reply.py")
    else:
        print("❌ برخی تست‌ها ناموفق! لطفاً مشکلات را برطرف کنید.")
        print("\nبرای نصب پکیج‌ها:")
        print("pip install -r requirements.txt")
    print("="*60)

def main():
    """تابع اصلی"""
    print("🧪 تست سیستم ربات پاسخ‌دهی تلگرام")
    print("=" * 60)
    
    generate_report()

if __name__ == "__main__":
    main()

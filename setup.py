# -*- coding: utf-8 -*-
"""
اسکریپت راه‌اندازی ربات تلگرام
این اسکریپت کمک می‌کند تا سیستم را برای اجرای ربات آماده کنید
"""

import os
import sys
import urllib.request
import zipfile
import subprocess
from pathlib import Path

def print_header():
    """چاپ هدر برنامه"""
    print("=" * 60)
    print("🚀 راه‌اندازی ربات پاسخ‌دهی خودکار تلگرام")
    print("=" * 60)
    print()

def check_python_version():
    """بررسی نسخه پایتون"""
    print("🔍 بررسی نسخه پایتون...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ نسخه پایتون: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ نسخه پایتون باید 3.8 یا بالاتر باشد. نسخه فعلی: {version.major}.{version.minor}")
        return False

def check_tesseract():
    """بررسی نصب Tesseract OCR"""
    print("\n🔍 بررسی Tesseract OCR...")
    
    # مسیرهای معمول نصب Tesseract در ویندوز
    possible_paths = [
        r'D:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Tesseract یافت شد در: {path}")
            return path
    
    print("❌ Tesseract OCR یافت نشد!")
    return None

def download_tesseract_installer():
    """راهنمای دانلود و نصب Tesseract"""
    print("\n📥 راهنمای نصب Tesseract OCR:")
    print("-" * 40)
    print("1. به لینک زیر بروید:")
    print("   https://github.com/UB-Mannheim/tesseract/wiki")
    print()
    print("2. فایل نصب ویندوز را دانلود کنید:")
    print("   tesseract-ocr-w64-setup-v5.x.x.exe")
    print()
    print("3. نصب کنید و مطمئن شوید زبان فارسی (Persian) انتخاب شده")
    print()
    print("4. مسیر نصب پیشنهادی: D:\\Program Files\\Tesseract-OCR\\")
    print()
    
    choice = input("آیا می‌خواهید صفحه دانلود باز شود؟ (y/n): ").lower()
    if choice == 'y':
        try:
            os.system('start https://github.com/UB-Mannheim/tesseract/wiki')
        except:
            print("لطفاً لینک را به صورت دستی باز کنید")

def install_python_packages():
    """نصب پکیج‌های مورد نیاز پایتون"""
    print("\n📦 نصب پکیج‌های پایتون...")
    
    packages = [
        'pyautogui',
        'pytesseract', 
        'Pillow',
        'schedule'
    ]
    
    for package in packages:
        print(f"نصب {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} نصب شد")
        except subprocess.CalledProcessError:
            print(f"❌ خطا در نصب {package}")
            return False
    
    return True

def create_desktop_shortcut():
    """ایجاد میانبر روی دسکتاپ"""
    print("\n🔗 ایجاد میانبر...")
    
    try:
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        script_path = os.path.abspath('telegram_auto_reply.py')
        python_path = sys.executable
        
        # ایجاد فایل bat برای اجرای آسان
        bat_content = f'''@echo off
cd /d "{os.path.dirname(script_path)}"
"{python_path}" "{script_path}"
pause
'''
        
        bat_file = os.path.join(desktop, 'ربات_تلگرام.bat')
        
        with open(bat_file, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        print(f"✅ میانبر ایجاد شد: {bat_file}")
        return True
        
    except Exception as e:
        print(f"❌ خطا در ایجاد میانبر: {e}")
        return False

def test_setup():
    """تست تنظیمات"""
    print("\n🧪 تست تنظیمات...")
    
    try:
        # تست import کردن پکیج‌ها
        import pyautogui
        import pytesseract
        from PIL import Image
        import schedule
        
        print("✅ تمام پکیج‌ها با موفقیت import شدند")
        
        # تست Tesseract
        tesseract_path = check_tesseract()
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            
            # تست ساده OCR
            test_image = Image.new('RGB', (100, 30), color='white')
            pytesseract.image_to_string(test_image, lang='eng')
            
            print("✅ Tesseract OCR به درستی کار می‌کند")
            return True
        else:
            print("❌ Tesseract نصب نشده")
            return False
            
    except Exception as e:
        print(f"❌ خطا در تست: {e}")
        return False

def show_usage_guide():
    """راهنمای استفاده"""
    print("\n" + "=" * 60)
    print("📖 راهنمای استفاده")
    print("=" * 60)
    print()
    print("1. تلگرام دسکتاپ را باز کنید")
    print("2. به چت مورد نظر بروید")
    print("3. اسکریپت telegram_auto_reply.py را اجرا کنید")
    print("4. گزینه تنظیم تعاملی مختصات را انتخاب کنید")
    print("5. دستورالعمل‌های روی صفحه را دنبال کنید")
    print()
    print("⚠️ نکات مهم:")
    print("- تلگرام دسکتاپ باید در پیش‌زمینه باشد")
    print("- ربات فقط از آخرین پیام دریافتی پاسخ می‌دهد")
    print("- برای توقف: Ctrl+C")
    print("- برای توقف اضطراری: ماوس را به گوشه صفحه ببرید")
    print()

def main():
    """تابع اصلی راه‌اندازی"""
    print_header()
    
    # بررسی نسخه پایتون
    if not check_python_version():
        print("\n❌ لطفاً نسخه جدیدتر پایتون نصب کنید")
        return
    
    # بررسی Tesseract
    tesseract_path = check_tesseract()
    if not tesseract_path:
        download_tesseract_installer()
        print("\n⏸️ لطفاً ابتدا Tesseract را نصب کنید، سپس این اسکریپت را دوباره اجرا کنید")
        return
    
    # نصب پکیج‌های پایتون
    if not install_python_packages():
        print("\n❌ خطا در نصب پکیج‌ها")
        return
    
    # تست تنظیمات
    if not test_setup():
        print("\n❌ خطا در تست تنظیمات")
        return
    
    # ایجاد میانبر
    create_desktop_shortcut()
    
    # نمایش راهنما
    show_usage_guide()
    
    print("🎉 راه‌اندازی با موفقیت تکمیل شد!")
    print("\nاکنون می‌توانید ربات را اجرا کنید:")
    print("python telegram_auto_reply.py")

if __name__ == "__main__":
    main()

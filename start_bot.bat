@echo off
chcp 65001 >nul
title ربات پاسخ‌دهی خودکار تلگرام

echo ================================================================
echo               ربات پاسخ‌دهی خودکار تلگرام
echo ================================================================
echo.

echo 🔍 بررسی محیط Python...
C:\Users\Arian\OneDrive\Desktop\telagent\.venv\Scripts\python.exe --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Python یافت نشد! لطفاً مسیر Python را بررسی کنید.
    pause
    exit /b 1
)

echo.
echo 🚀 اجرای ربات...
echo ⚠️ برای توقف: Ctrl+C یا بستن پنجره
echo ⚠️ برای توقف اضطراری: ماوس را به گوشه صفحه ببرید
echo.

C:\Users\Arian\OneDrive\Desktop\telagent\.venv\Scripts\python.exe telegram_auto_reply.py

echo.
echo ================================================================
echo                        برنامه پایان یافت
echo ================================================================
pause

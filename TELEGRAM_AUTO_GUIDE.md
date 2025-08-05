# 🤖 راهنمای استفاده از سیستم پاسخ‌دهی خودکار تلگرام

## 🎯 مراحل راه‌اندازی

### مرحله 1: آماده‌سازی اولیه
1. **نصب تلگرام دسکتاپ**: از سایت رسمی تلگرام دانلود کنید
2. **تنظیم مسیر تلگرام**: فایل `telegram_config.json` را باز کنید و مسیر درست تلگرام را وارد کنید

### مرحله 2: تنظیم مختصات صفحه
```bash
python advanced_telegram_responder.py
# گزینه 2 را انتخاب کنید: "🎯 Setup Screen Coordinates"
```

#### راهنمای تنظیم مختصات:
1. **chat_list**: ناحیه لیست چت‌ها (سمت چپ)
2. **chat_area**: ناحیه اصلی گفتگو (وسط)
3. **input_area**: ناحیه تایپ پیام (پایین)

### مرحله 3: تنظیمات پیشرفته
فایل `telegram_config.json` را ویرایش کنید:

```json
{
  "telegram_executable": "C:\\TelegramDesktop\\Telegram.exe",
  "monitoring_interval": 3,
  "response_delay": 2,
  "auto_response_enabled": true,
  "response_triggers": [
    "سلام", "hello", "hi", "؟", "?", 
    "چطوری", "how are you", "کجایی"
  ],
  "excluded_chats": ["Saved Messages", "پیام‌های ذخیره شده"]
}
```

## 🚀 راه‌اندازی سیستم

### روش 1: استفاده از منوی اصلی
```bash
python advanced_telegram_responder.py
# گزینه 1: "🚀 Start Auto Responder"
```

### روش 2: اجرای مستقیم
```bash
python advanced_telegram_responder.py --start
```

## ⌨️ کلیدهای کنترل حین اجرا

- **`q`**: خروج از برنامه
- **`p`**: توقف/ادامه پاسخ‌دهی خودکار
- **`s`**: نمایش آمار جلسه

## 🎛️ تنظیمات کلیدی

### تنظیمات زمانی
- `monitoring_interval`: فاصله زمانی بین هر بررسی (ثانیه)
- `response_delay`: تأخیر قبل از ارسال پاسخ (ثانیه)

### تنظیمات پاسخ‌دهی
- `auto_response_enabled`: فعال/غیرفعال کردن پاسخ خودکار
- `max_responses_per_chat`: حداکثر پاسخ در هر چت
- `response_triggers`: کلمات محرک برای پاسخ‌دهی

### تنظیمات ساعات کاری
```json
"working_hours": {
  "enabled": true,
  "start": "09:00",
  "end": "18:00"
}
```

## 🧪 تست سیستم

### تست OCR
```bash
python advanced_telegram_responder.py
# گزینه 4: "🧪 Test OCR"
```

### تست پاسخ‌دهی
```bash
python simple_learning.py
```

## 📊 نظارت و آمار

### مشاهده آمار لحظه‌ای
- حین اجرا کلید `s` را فشار دهید

### فایل‌های لاگ
- `telegram_auto_reply.log`: لاگ کامل عملیات
- `session_stats.json`: آمار جلسه
- `simple_learning.json`: داده‌های یادگیری

## ⚠️ نکات مهم ایمنی

### 1. تنظیم failsafe
```python
pyautogui.FAILSAFE = True  # ماوس را به گوشه صفحه ببرید تا متوقف شود
```

### 2. تست در محیط امن
- ابتدا روی چت‌های شخصی تست کنید
- از گروه‌های مهم خودداری کنید

### 3. نظارت مستمر
- همیشه سیستم را تحت نظر داشته باشید
- آمار عملکرد را بررسی کنید

## 🔧 عیب‌یابی

### مشکلات متداول

#### 1. تلگرام پیدا نمی‌شود
```bash
# بررسی مسیر تلگرام
ls "C:\TelegramDesktop\Telegram.exe"
```

#### 2. OCR کار نمی‌کند
```bash
# تست OCR
python smart_ocr.py
```

#### 3. پاسخ‌ها ارسال نمی‌شوند
- مختصات input_area را دوباره تنظیم کنید
- تأخیر response_delay را افزایش دهید

### فایل‌های مورد نیاز
```
📁 Project Directory/
├── 🤖 advanced_telegram_responder.py
├── 🧠 simple_learning.py
├── 👁️ smart_ocr.py
├── ⚙️ telegram_config.json
├── 📊 conversation_data/
│   ├── collected_chats.json
│   ├── simple_learning.json
│   └── session_stats.json
└── 📝 logs/
    └── telegram_auto_reply.log
```

## 🎯 نکات بهینه‌سازی

### 1. تنظیم OCR
- رزولوشن صفحه را افزایش دهید
- از تم روشن تلگرام استفاده کنید
- فونت سایز را بزرگ کنید

### 2. بهبود یادگیری
```bash
# افزودن داده‌های بیشتر
python load_dataset.py
```

### 3. تنظیم عملکرد
- `monitoring_interval` را کاهش دهید برای پاسخ سریع‌تر
- `response_delay` را افزایش دهید برای طبیعی‌تر بودن

## 📱 مثال کاربرد

```python
# شروع سیستم
responder = AdvancedTelegramResponder()

# تنظیم مختصات (یک بار)
responder.setup_screen_coordinates()

# شروع نظارت
responder.start_monitoring()
```

## 🛡️ توصیه‌های امنیتی

1. **هرگز رمز عبور را در پاسخ‌ها قرار ندهید**
2. **چت‌های حساس را در excluded_chats اضافه کنید**
3. **از ساعات کاری استفاده کنید**
4. **به طور مرتب لاگ‌ها را بررسی کنید**

## 🔄 به‌روزرسانی سیستم

```bash
# به‌روزرسانی داده‌های یادگیری
python expand_dataset.py

# آموزش مجدد سیستم
python load_dataset.py
```

---

## 🆘 پشتیبانی

برای مشکلات فنی:
1. فایل `telegram_auto_reply.log` را بررسی کنید
2. تنظیمات `telegram_config.json` را کنترل کنید
3. سیستم را در حالت تست اجرا کنید

**موفق باشید! 🚀**

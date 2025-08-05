# -*- coding: utf-8 -*-
"""
رابط گرافیکی برای تنظیم ربات تلگرام
این اسکریپت یک رابط ساده برای تنظیم مختصات و پیکربندی ربات فراهم می‌کند
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyautogui
import json
import os

class BotConfigurator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("تنظیمات ربات تلگرام")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # متغیرهای ذخیره موقعیت
        self.chat_coords = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
        self.input_coords = {"x": 0, "y": 0}
        
        self.setup_ui()
        
    def setup_ui(self):
        """ایجاد رابط کاربری"""
        
        # عنوان
        title_label = tk.Label(
            self.root, 
            text="🤖 تنظیمات ربات پاسخ‌دهی تلگرام",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # تبها
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # تب تنظیم مختصات
        coords_frame = ttk.Frame(notebook)
        notebook.add(coords_frame, text="تنظیم مختصات")
        self.setup_coordinates_tab(coords_frame)
        
        # تب تنظیمات عمومی
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="تنظیمات عمومی")
        self.setup_settings_tab(settings_frame)
        
        # تب پاسخ‌ها
        responses_frame = ttk.Frame(notebook)
        notebook.add(responses_frame, text="مدیریت پاسخ‌ها")
        self.setup_responses_tab(responses_frame)
        
        # دکمه‌های پایین
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            button_frame,
            text="💾 ذخیره تنظیمات",
            command=self.save_config,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white"
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="📂 بارگذاری تنظیمات",
            command=self.load_config,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white"
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="🚀 اجرای ربات",
            command=self.run_bot,
            font=("Arial", 10),
            bg="#FF9800",
            fg="white"
        ).pack(side="right", padx=5)

    def setup_coordinates_tab(self, parent):
        """تب تنظیم مختصات"""
        
        # راهنما
        guide_text = """
📍 راهنمای تنظیم مختصات:

1. ابتدا تلگرام دسکتاپ را باز کنید
2. به چت مورد نظر بروید
3. روی دکمه‌های زیر کلیک کنید و ماوس را به موقعیت مناسب ببرید
4. پس از هر کلیک، موقعیت ماوس ثبت می‌شود
        """
        
        tk.Label(parent, text=guide_text, justify="left", font=("Arial", 9)).pack(
            anchor="w", padx=10, pady=5
        )
        
        # منطقه چت
        chat_frame = tk.LabelFrame(parent, text="منطقه چت", font=("Arial", 10, "bold"))
        chat_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            chat_frame,
            text="📍 تعیین گوشه بالا-چپ چت",
            command=lambda: self.get_coordinate("chat_top_left"),
            width=30
        ).pack(pady=5)
        
        tk.Button(
            chat_frame,
            text="📍 تعیین گوشه پایین-راست چت",
            command=lambda: self.get_coordinate("chat_bottom_right"),
            width=30
        ).pack(pady=5)
        
        self.chat_info_label = tk.Label(chat_frame, text="منطقه چت تنظیم نشده", fg="red")
        self.chat_info_label.pack(pady=5)
        
        # محل ورودی
        input_frame = tk.LabelFrame(parent, text="محل ورودی متن", font=("Arial", 10, "bold"))
        input_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(
            input_frame,
            text="📍 تعیین موقعیت جعبه ورودی",
            command=lambda: self.get_coordinate("input_box"),
            width=30
        ).pack(pady=5)
        
        self.input_info_label = tk.Label(input_frame, text="موقعیت ورودی تنظیم نشده", fg="red")
        self.input_info_label.pack(pady=5)

    def setup_settings_tab(self, parent):
        """تب تنظیمات عمومی"""
        
        # فاصله زمانی بررسی
        interval_frame = tk.LabelFrame(parent, text="زمان‌بندی", font=("Arial", 10, "bold"))
        interval_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(interval_frame, text="فاصله بررسی پیام‌ها (ثانیه):").pack(anchor="w", padx=5)
        self.interval_var = tk.StringVar(value="10")
        tk.Entry(interval_frame, textvariable=self.interval_var, width=10).pack(anchor="w", padx=5, pady=2)
        
        tk.Label(interval_frame, text="تاخیر قبل از پاسخ (ثانیه):").pack(anchor="w", padx=5)
        self.delay_var = tk.StringVar(value="2")
        tk.Entry(interval_frame, textvariable=self.delay_var, width=10).pack(anchor="w", padx=5, pady=2)
        
        # مسیر Tesseract
        tesseract_frame = tk.LabelFrame(parent, text="تنظیمات Tesseract", font=("Arial", 10, "bold"))
        tesseract_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(tesseract_frame, text="مسیر Tesseract:").pack(anchor="w", padx=5)
        self.tesseract_var = tk.StringVar(value=r"D:\Program Files\Tesseract-OCR\tesseract.exe")
        
        path_frame = tk.Frame(tesseract_frame)
        path_frame.pack(fill="x", padx=5, pady=2)
        
        tk.Entry(path_frame, textvariable=self.tesseract_var, width=40).pack(side="left")
        tk.Button(path_frame, text="انتخاب", command=self.browse_tesseract).pack(side="left", padx=5)

    def setup_responses_tab(self, parent):
        """تب مدیریت پاسخ‌ها"""
        
        tk.Label(parent, text="📝 مدیریت پاسخ‌های خودکار", font=("Arial", 12, "bold")).pack(pady=5)
        
        # لیست پاسخ‌ها
        list_frame = tk.Frame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # اسکرول بار
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.responses_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=8)
        self.responses_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.responses_listbox.yview)
        
        # پاسخ‌های پیش‌فرض
        default_responses = [
            "سلام -> سلام! چطور کمکتون کنم؟",
            "ساعت -> نمایش ساعت فعلی",
            "خداحافظ -> فعلاً! موفق باشید!",
            "چطوری -> ممنون، خوبم! شما چطورید؟"
        ]
        
        for response in default_responses:
            self.responses_listbox.insert(tk.END, response)
        
        # دکمه‌های مدیریت
        button_frame = tk.Frame(parent)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(button_frame, text="➕ افزودن", command=self.add_response).pack(side="left", padx=2)
        tk.Button(button_frame, text="✏️ ویرایش", command=self.edit_response).pack(side="left", padx=2)
        tk.Button(button_frame, text="🗑️ حذف", command=self.delete_response).pack(side="left", padx=2)

    def get_coordinate(self, coord_type):
        """دریافت مختصات از کاربر"""
        
        def capture_mouse():
            self.root.withdraw()  # پنهان کردن پنجره
            
            # تاخیر برای آماده شدن کاربر
            self.root.after(3000, lambda: self._capture_position(coord_type))
        
        messagebox.showinfo(
            "آماده‌سازی",
            f"پس از بستن این پیام، 3 ثانیه فرصت دارید.\nماوس را به موقعیت مناسب ببرید."
        )
        
        capture_mouse()

    def _capture_position(self, coord_type):
        """گرفتن موقعیت ماوس"""
        x, y = pyautogui.position()
        
        if coord_type == "chat_top_left":
            self.chat_coords["x1"] = x
            self.chat_coords["y1"] = y
            self.update_chat_info()
            
        elif coord_type == "chat_bottom_right":
            self.chat_coords["x2"] = x
            self.chat_coords["y2"] = y
            self.update_chat_info()
            
        elif coord_type == "input_box":
            self.input_coords["x"] = x
            self.input_coords["y"] = y
            self.input_info_label.config(
                text=f"موقعیت ورودی: ({x}, {y})",
                fg="green"
            )
        
        self.root.deiconify()  # نمایش مجدد پنجره

    def update_chat_info(self):
        """بروزرسانی اطلاعات منطقه چت"""
        x1, y1 = self.chat_coords["x1"], self.chat_coords["y1"]
        x2, y2 = self.chat_coords["x2"], self.chat_coords["y2"]
        
        if x1 and y1 and x2 and y2:
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            self.chat_info_label.config(
                text=f"منطقه چت: ({x1}, {y1}) تا ({x2}, {y2}) - اندازه: {width}x{height}",
                fg="green"
            )
        else:
            self.chat_info_label.config(
                text="منطقه چت تنظیم نشده",
                fg="red"
            )

    def browse_tesseract(self):
        """انتخاب فایل Tesseract"""
        filename = filedialog.askopenfilename(
            title="انتخاب فایل tesseract.exe",
            filetypes=[("Executable files", "*.exe")]
        )
        if filename:
            self.tesseract_var.set(filename)

    def add_response(self):
        """افزودن پاسخ جدید"""
        # پنجره ساده برای ورود
        dialog = tk.Toplevel(self.root)
        dialog.title("افزودن پاسخ")
        dialog.geometry("400x150")
        
        tk.Label(dialog, text="کلمات کلیدی (با کاما جدا کنید):").pack(pady=5)
        keywords_entry = tk.Entry(dialog, width=50)
        keywords_entry.pack(pady=5)
        
        tk.Label(dialog, text="متن پاسخ:").pack(pady=5)
        response_entry = tk.Entry(dialog, width=50)
        response_entry.pack(pady=5)
        
        def save_response():
            keywords = keywords_entry.get().strip()
            response = response_entry.get().strip()
            if keywords and response:
                self.responses_listbox.insert(tk.END, f"{keywords} -> {response}")
                dialog.destroy()
        
        tk.Button(dialog, text="ذخیره", command=save_response).pack(pady=10)

    def edit_response(self):
        """ویرایش پاسخ انتخاب شده"""
        selection = self.responses_listbox.curselection()
        if selection:
            messagebox.showinfo("ویرایش", "قابلیت ویرایش در نسخه آینده اضافه خواهد شد")

    def delete_response(self):
        """حذف پاسخ انتخاب شده"""
        selection = self.responses_listbox.curselection()
        if selection:
            self.responses_listbox.delete(selection[0])

    def save_config(self):
        """ذخیره تنظیمات در فایل"""
        config = {
            "chat_region": {
                "x": self.chat_coords["x1"],
                "y": self.chat_coords["y1"],
                "width": abs(self.chat_coords["x2"] - self.chat_coords["x1"]),
                "height": abs(self.chat_coords["y2"] - self.chat_coords["y1"])
            },
            "input_position": self.input_coords,
            "tesseract_path": self.tesseract_var.get(),
            "check_interval": int(self.interval_var.get()),
            "response_delay": int(self.delay_var.get())
        }
        
        # نوشتن در فایل config.py
        self.write_config_file(config)
        messagebox.showinfo("موفقیت", "تنظیمات با موفقیت ذخیره شد!")

    def write_config_file(self, config):
        """نوشتن فایل config.py"""
        config_content = f'''# -*- coding: utf-8 -*-
"""
فایل تنظیمات ربات تلگرام - تولید شده توسط رابط گرافیکی
"""

# تنظیمات Tesseract OCR
TESSERACT_PATH = r'{config["tesseract_path"]}'
OCR_LANGUAGES = 'fas+eng'
OCR_CONFIG = '--psm 6'

# تنظیمات مختصات
CHAT_REGION = {{
    'x': {config["chat_region"]["x"]},
    'y': {config["chat_region"]["y"]},
    'width': {config["chat_region"]["width"]},
    'height': {config["chat_region"]["height"]}
}}

INPUT_CLICK_POSITION = {{
    'x': {config["input_position"]["x"]},
    'y': {config["input_position"]["y"]}
}}

SEND_BUTTON_POSITION = {{
    'x': {config["input_position"]["x"] + 100},
    'y': {config["input_position"]["y"]}
}}

# تنظیمات زمان‌بندی
CHECK_INTERVAL = {config["check_interval"]}
RESPONSE_DELAY = {config["response_delay"]}
PYAUTOGUI_PAUSE = 0.5

# قوانین پاسخ‌دهی
RESPONSE_RULES = {{
    'greetings': {{
        'keywords': ['سلام', 'hello', 'hi', 'hey', 'درود'],
        'response': 'سلام! چطور کمکتون کنم؟'
    }},
    'time_request': {{
        'keywords': ['ساعت', 'time', 'زمان', 'وقت'],
        'response': 'current_time'
    }},
    'goodbyes': {{
        'keywords': ['خداحافظ', 'bye', 'goodbye', 'فعلا'],
        'response': 'فعلاً! موفق باشید! 👋'
    }},
    'how_are_you': {{
        'keywords': ['چطوری', 'حالت', 'how are you', 'احوالت'],
        'response': 'ممنون، خوبم! شما چطورید؟ 😊'
    }},
    'thanks': {{
        'keywords': ['ممنون', 'مرسی', 'thank', 'متشکرم'],
        'response': 'خواهش می‌کنم! 😊'
    }}
}}

DEFAULT_RESPONSE = "متوجه نشدم، لطفاً واضح‌تر بگو. 🤔"

# تنظیمات امنیتی
FAILSAFE_ENABLED = True
MAX_MESSAGE_LENGTH = 500
MIN_MESSAGE_LENGTH = 2

# تنظیمات لاگ‌گیری
LOG_FILENAME = 'telegram_bot.log'
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
'''
        
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(config_content)

    def load_config(self):
        """بارگذاری تنظیمات از فایل"""
        messagebox.showinfo("بارگذاری", "قابلیت بارگذاری در نسخه آینده اضافه خواهد شد")

    def run_bot(self):
        """اجرای ربات"""
        if os.path.exists("telegram_auto_reply.py"):
            os.system("start cmd /c python telegram_auto_reply.py")
            messagebox.showinfo("اجرا", "ربات در پنجره جدید اجرا شد")
        else:
            messagebox.showerror("خطا", "فایل telegram_auto_reply.py یافت نشد!")

    def run(self):
        """اجرای رابط گرافیکی"""
        self.root.mainloop()

def main():
    """تابع اصلی"""
    app = BotConfigurator()
    app.run()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Telegram AI Bot Performance Report Generator
تحلیل کامل عملکرد و آمار ربات هوش مصنوعی
"""

import json
import time
import os
from datetime import datetime, timedelta
import re

class PerformanceAnalyzer:
    """📈 تحلیلگر عملکرد پیشرفته"""
    
    def __init__(self):
        self.log_file = "telegram_ai_bot.log"
        self.stats = {
            'total_messages': 0,
            'total_responses': 0,
            'ai_analysis_count': 0,
            'success_rate': 0,
            'average_response_time': 0,
            'language_distribution': {},
            'intent_distribution': {},
            'ocr_engine_performance': {},
            'error_count': 0,
            'session_duration': 0
        }
    
    def analyze_logs(self):
        """📊 تحلیل فایل لاگ"""
        if not os.path.exists(self.log_file):
            print(f"❌ فایل لاگ یافت نشد: {self.log_file}")
            return
        
        print("🔍 در حال تحلیل لاگ‌ها...")
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        sessions = []
        current_session = None
        
        for line in lines:
            # شناسایی شروع جلسه جدید
            if "Enhanced AI monitoring started" in line or "Advanced AI monitoring started" in line:
                if current_session:
                    sessions.append(current_session)
                current_session = {
                    'start_time': self.extract_timestamp(line),
                    'messages': [],
                    'responses': [],
                    'errors': [],
                    'intents': [],
                    'languages': [],
                    'ocr_engines': []
                }
            
            if current_session:
                # پیام‌های تشخیص داده شده
                if "📨 Detected:" in line or "📨 New message detected:" in line:
                    self.stats['total_messages'] += 1
                    current_session['messages'].append(line)
                    
                    # استخراج intent
                    intent_match = re.search(r'Intent: (\w+)', line)
                    if intent_match:
                        intent = intent_match.group(1)
                        current_session['intents'].append(intent)
                        self.stats['intent_distribution'][intent] = self.stats['intent_distribution'].get(intent, 0) + 1
                
                # پاسخ‌های ارسال شده
                if "📤 Sent:" in line or "Response sent:" in line:
                    self.stats['total_responses'] += 1
                    current_session['responses'].append(line)
                
                # موتور OCR
                if "[tesseract]" in line or "[easyocr]" in line:
                    engine_match = re.search(r'\[(\w+)\]', line)
                    if engine_match:
                        engine = engine_match.group(1)
                        current_session['ocr_engines'].append(engine)
                        self.stats['ocr_engine_performance'][engine] = self.stats['ocr_engine_performance'].get(engine, 0) + 1
                
                # خطاها
                if "ERROR" in line or "❌" in line:
                    self.stats['error_count'] += 1
                    current_session['errors'].append(line)
        
        # اضافه کردن آخرین جلسه
        if current_session:
            sessions.append(current_session)
        
        # محاسبه آمار کلی
        if self.stats['total_messages'] > 0:
            self.stats['success_rate'] = (self.stats['total_responses'] / self.stats['total_messages']) * 100
        
        return sessions
    
    def extract_timestamp(self, line):
        """⏰ استخراج timestamp از خط لاگ"""
        timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
        if timestamp_match:
            return datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')
        return None
    
    def generate_report(self):
        """📋 تولید گزارش کامل"""
        sessions = self.analyze_logs()
        
        print("\n" + "="*70)
        print("📊 گزارش عملکرد ربات هوش مصنوعی تلگرام")
        print("="*70)
        print(f"📅 تاریخ تولید گزارش: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 فایل لاگ: {self.log_file}")
        print(f"🔄 تعداد جلسات: {len(sessions)}")
        print("="*70)
        
        # آمار کلی
        print("\n📈 آمار کلی:")
        print(f"   📨 کل پیام‌های پردازش شده: {self.stats['total_messages']}")
        print(f"   📤 کل پاسخ‌های ارسال شده: {self.stats['total_responses']}")
        print(f"   📊 نرخ موفقیت: {self.stats['success_rate']:.1f}%")
        print(f"   ❌ تعداد خطاها: {self.stats['error_count']}")
        
        # توزیع intent
        if self.stats['intent_distribution']:
            print("\n🎯 توزیع Intent پیام‌ها:")
            sorted_intents = sorted(self.stats['intent_distribution'].items(), key=lambda x: x[1], reverse=True)
            for intent, count in sorted_intents:
                percentage = (count / self.stats['total_messages']) * 100
                print(f"   {intent}: {count} ({percentage:.1f}%)")
        
        # عملکرد موتورهای OCR
        if self.stats['ocr_engine_performance']:
            print("\n🔍 عملکرد موتورهای OCR:")
            total_ocr = sum(self.stats['ocr_engine_performance'].values())
            for engine, count in self.stats['ocr_engine_performance'].items():
                percentage = (count / total_ocr) * 100
                print(f"   {engine}: {count} استفاده ({percentage:.1f}%)")
        
        # آمار جلسات
        if sessions:
            print("\n📊 آمار جلسات:")
            total_duration = 0
            
            for i, session in enumerate(sessions, 1):
                if session['start_time']:
                    # محاسبه مدت زمان جلسه (تخمینی)
                    session_duration = len(session['messages']) * 10  # تخمین 10 ثانیه بین پیام‌ها
                    total_duration += session_duration
                    
                    print(f"   📋 جلسه {i}:")
                    print(f"      ⏰ شروع: {session['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"      📨 پیام‌ها: {len(session['messages'])}")
                    print(f"      📤 پاسخ‌ها: {len(session['responses'])}")
                    print(f"      ❌ خطاها: {len(session['errors'])}")
                    print(f"      ⏱️ مدت تخمینی: {session_duration//60} دقیقه")
            
            print(f"\n⏱️ کل مدت زمان فعالیت: {total_duration//3600} ساعت و {(total_duration%3600)//60} دقیقه")
        
        # توصیه‌های بهبود
        self.generate_recommendations()
        
        # ذخیره گزارش
        self.save_report_json()
        
        print("\n" + "="*70)
        print("✅ گزارش تولید شد!")
        print("💾 گزارش JSON: performance_report.json")
        print("="*70)
    
    def generate_recommendations(self):
        """💡 تولید توصیه‌های بهبود"""
        print("\n💡 توصیه‌های بهبود عملکرد:")
        
        # توصیه براساس نرخ موفقیت
        if self.stats['success_rate'] < 50:
            print("   🔧 نرخ پاسخ پایین است. بررسی کنید:")
            print("      • تنظیمات فیلتر interface")
            print("      • آستانه confidence برای OCR")
            print("      • قوانین تشخیص پیام واقعی")
        
        elif self.stats['success_rate'] > 80:
            print("   🎉 نرخ پاسخ عالی است!")
            print("   ⚡ برای بهبود بیشتر:")
            print("      • اضافه کردن قوانین پاسخ جدید")
            print("      • بهینه‌سازی زمان پاسخ")
        
        # توصیه براساس خطاها
        if self.stats['error_count'] > self.stats['total_messages'] * 0.1:
            print("   ⚠️ تعداد خطاها زیاد است:")
            print("      • بررسی نصب Tesseract")
            print("      • بررسی تنظیمات مختصات")
            print("      • بررسی حافظه سیستم")
        
        # توصیه براساس intent
        unknown_intent_ratio = self.stats['intent_distribution'].get('unknown', 0) / max(self.stats['total_messages'], 1)
        if unknown_intent_ratio > 0.6:
            print("   🎯 تعداد intent های ناشناخته زیاد است:")
            print("      • اضافه کردن الگوهای جدید")
            print("      • بهبود تشخیص زبان")
            print("      • افزایش قوانین intent")
    
    def save_report_json(self):
        """💾 ذخیره گزارش در فرمت JSON"""
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'statistics': self.stats,
            'system_info': {
                'python_version': f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
                'platform': __import__('platform').system()
            }
        }
        
        with open('performance_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

def main():
    """🚀 تابع اصلی"""
    print("📊 تحلیلگر عملکرد ربات هوش مصنوعی تلگرام")
    print("="*50)
    
    analyzer = PerformanceAnalyzer()
    analyzer.generate_report()

if __name__ == "__main__":
    main()

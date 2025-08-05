#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Ultimate Telegram Auto Responder v4.0
All advanced features combined in one system
"""

import os
import json
import time
import random
import hashlib
import logging
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path
import re

# Import existing proven systems
from smart_ocr import SmartOCR
from simple_learning import SimpleLearningSystem

# Optional heavy dependencies with fallbacks
try:
    import pyautogui
    import keyboard
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False
    print("⚠️ Automation libraries not available - install with: pip install pyautogui keyboard")

try:
    import win32gui
    import win32con
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("⚠️ Win32 libraries not available - install with: pip install pywin32")
# -*- coding: utf-8 -*-
"""
🚀 Ultimate Telegram AI Auto Responder v4.0
🤖 Advanced automation with intelligent learning, OCR, and desktop automation
🌍 Persian/English dual language support
"""

import pyautogui
import time
import os
import subprocess
import json
import cv2
import numpy as np
from datetime import datetime
import logging
import keyboard
# Remove duplicate imports that are in try block above
import sqlite3
import re
import random
from collections import defaultdict, Counter
from typing import Optional, List, Dict, Tuple, Any
import hashlib
from pathlib import Path

# Import existing systems
from smart_ocr import SmartOCR
from simple_learning import SimpleLearningSystem

# Configure pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

class UltimateTelegramResponder:
    """ Ultimate Telegram Auto Responder with all advanced features"""
    
    def __init__(self):
        self.setup_logging()
        self.init_ai_systems()
        self.load_configuration()
        self.init_stats()
        self.running = False
        self.telegram_hwnd = None
        
    def setup_logging(self):
        """📝 Setup comprehensive logging"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        os.makedirs('conversation_data', exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('conversation_data/ultimate_responder.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def init_ai_systems(self):
        """🧠 Initialize all AI systems"""
        self.logger.info("🚀 Initializing Ultimate AI Systems...")
        
        try:
            # Initialize OCR system
            self.ocr = SmartOCR()
            self.logger.info("✅ Smart OCR System ready")
            
            # Initialize learning system
            self.learning = SimpleLearningSystem()
            self.logger.info("✅ Simple Learning System ready")
            
        except Exception as e:
            self.logger.error(f"❌ AI Systems initialization failed: {e}")
            
    def load_configuration(self):
        """⚙️ Load system configuration"""
        self.config = {
            'check_interval': 2.0,
            'response_delay': (1.5, 3.0),
            'screenshot_delay': 0.5,
            'max_response_length': 200,
            'auto_response_enabled': True,
            'language_detection': True,
            'learning_enabled': True,
            'ocr_confidence_threshold': 0.7
        }
        
        # Load config from file if exists
        try:
            if os.path.exists('ultimate_config.json'):
                with open('ultimate_config.json', 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
                    self.logger.info("📋 Configuration loaded from file")
        except Exception as e:
            self.logger.warning(f"⚠️ Config load warning: {e}")
    
    def init_stats(self):
        """📊 Initialize comprehensive statistics"""
        self.stats = {
            'total_screenshots': 0,
            'successful_ocr': 0,
            'failed_ocr': 0,
            'messages_detected': 0,
            'responses_sent': 0,
            'learning_interactions': 0,
            'session_start': datetime.now().isoformat(),
            'languages_detected': defaultdict(int),
            'response_categories': defaultdict(int),
            'performance_metrics': {
                'avg_ocr_time': 0.0,
                'avg_response_time': 0.0,
                'success_rate': 0.0
            }
        }
        
    def find_telegram_window(self):
        """🔍 Find Telegram Desktop window"""
        try:
            if not WIN32_AVAILABLE:
                self.logger.warning("⚠️ Win32 not available - using fallback window detection")
                return True  # Assume window is available
                
            import win32gui
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if 'telegram' in window_title.lower():
                        windows.append((hwnd, window_title))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                # Select best match
                for hwnd, title in windows:
                    if 'telegram desktop' in title.lower() or title.lower() == 'telegram':
                        self.telegram_hwnd = hwnd
                        self.logger.info(f"📱 Found Telegram: {title}")
                        return True
                        
                # Fallback to first Telegram window
                self.telegram_hwnd = windows[0][0]
                self.logger.info(f"📱 Using Telegram window: {windows[0][1]}")
                return True
            else:
                self.logger.error("❌ No Telegram window found!")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Window search failed: {e}")
            return False
    
    def capture_screen(self):
        """📸 Capture screen with enhanced detection"""
        try:
            if not AUTOMATION_AVAILABLE:
                self.logger.error("❌ Automation libraries not available")
                return None
                
            import pyautogui
            import time
            
            if self.telegram_hwnd and WIN32_AVAILABLE:
                # Focus Telegram window
                import win32gui
                win32gui.SetForegroundWindow(self.telegram_hwnd)
                time.sleep(self.config['screenshot_delay'])
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"conversation_data/screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            self.stats['total_screenshots'] += 1
            return screenshot_path
            
        except Exception as e:
            self.logger.error(f"❌ Screenshot failed: {e}")
            return None
    
    def process_screenshot(self, screenshot_path):
        """🔍 Process screenshot with advanced OCR"""
        start_time = time.time()
        
        try:
            # Extract text using OCR
            ocr_result = self.ocr.extract_text(screenshot_path)
            
            if not ocr_result:
                self.stats['failed_ocr'] += 1
                return None
            
            self.stats['successful_ocr'] += 1
            
            # Process OCR result
            extracted_text = ocr_result.get('text', '')
            language = ocr_result.get('language', 'unknown')
            confidence = ocr_result.get('confidence', 0.0)
            
            if confidence < self.config['ocr_confidence_threshold']:
                self.logger.warning(f"⚠️ Low OCR confidence: {confidence:.2f}")
                return None
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats['performance_metrics']['avg_ocr_time'] = (
                (self.stats['performance_metrics']['avg_ocr_time'] + processing_time) / 2
            )
            
            self.stats['languages_detected'][language] += 1
            self.stats['messages_detected'] += 1
            
            self.logger.info(f"📖 Detected text ({language}): {extracted_text[:50]}...")
            
            return {
                'text': extracted_text,
                'language': language,
                'confidence': confidence,
                'processing_time': processing_time
            }
            
        except Exception as e:
            self.logger.error(f"❌ OCR processing failed: {e}")
            self.stats['failed_ocr'] += 1
            return None
    
    def generate_response(self, message_data):
        """🤖 Generate intelligent response"""
        start_time = time.time()
        
        try:
            if not self.config['auto_response_enabled']:
                return None
                
            message_text = message_data['text']
            language = message_data['language']
            
            # Generate response using learning system
            response = self.learning.generate_response(message_text)
            
            if not response:
                # Fallback response
                fallback_responses = {
                    'persian': ['سلام! 😊', 'چطوری؟', 'ممنون از پیامت'],
                    'english': ['Hello! 😊', 'How are you?', 'Thanks for your message'],
                    'unknown': ['Hello! 😊', 'سلام! 😊']
                }
                response = random.choice(fallback_responses.get(language, fallback_responses['unknown']))
            
            # Limit response length
            if len(response) > self.config['max_response_length']:
                response = response[:self.config['max_response_length']] + '...'
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats['performance_metrics']['avg_response_time'] = (
                (self.stats['performance_metrics']['avg_response_time'] + processing_time) / 2
            )
            
            # Categorize response
            category = self.categorize_response(response)
            self.stats['response_categories'][category] += 1
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Response generation failed: {e}")
            return None
    
    def categorize_response(self, response):
        """📂 Categorize response type"""
        response_lower = response.lower()
        
        if any(word in response_lower for word in ['سلام', 'درود', 'hello', 'hi']):
            return 'greeting'
        elif any(word in response_lower for word in ['ممنون', 'مرسی', 'thanks', 'thank']):
            return 'thanks'
        elif any(word in response_lower for word in ['عالی', 'خوب', 'great', 'good']):
            return 'positive'
        elif '؟' in response or '?' in response:
            return 'question'
        else:
            return 'general'
    
    def send_response(self, response_text):
        """💬 Send response to Telegram"""
        try:
            if not AUTOMATION_AVAILABLE:
                self.logger.error("❌ Automation libraries not available")
                return False
                
            if not response_text:
                return False
            
            import pyautogui
            import time
            
            # Add random delay
            delay = random.uniform(*self.config['response_delay'])
            time.sleep(delay)
            
            # Type response
            pyautogui.typewrite(response_text)
            time.sleep(0.5)
            
            # Send message (Enter)
            pyautogui.press('enter')
            
            self.stats['responses_sent'] += 1
            self.logger.info(f"💬 Response sent: {response_text[:30]}...")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send response: {e}")
            return False
    
    def learn_from_interaction(self, message_data, response_text):
        """🎓 Learn from interactions"""
        try:
            if not self.config['learning_enabled']:
                return
                
            message_text = message_data['text']
            language = message_data['language']
            
            # Add to learning system
            self.learning.add_conversation(message_text, response_text, language)
            
            self.stats['learning_interactions'] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Learning failed: {e}")
    
    def calculate_success_rate(self):
        """📈 Calculate success rate"""
        total_attempts = self.stats['successful_ocr'] + self.stats['failed_ocr']
        if total_attempts > 0:
            return self.stats['successful_ocr'] / total_attempts
        return 0.0
    
    def print_status(self):
        """📊 Print comprehensive status"""
        success_rate = self.calculate_success_rate()
        self.stats['performance_metrics']['success_rate'] = success_rate
        
        print("\n" + "="*60)
        print("🚀 ULTIMATE TELEGRAM RESPONDER STATUS")
        print("="*60)
        print(f"📸 Screenshots: {self.stats['total_screenshots']}")
        print(f"✅ Successful OCR: {self.stats['successful_ocr']}")
        print(f"❌ Failed OCR: {self.stats['failed_ocr']}")
        print(f"📨 Messages detected: {self.stats['messages_detected']}")
        print(f"💬 Responses sent: {self.stats['responses_sent']}")
        print(f"🎓 Learning interactions: {self.stats['learning_interactions']}")
        print(f"📈 Success rate: {success_rate:.1%}")
        
        print(f"\n🌍 Languages detected:")
        for lang, count in self.stats['languages_detected'].items():
            print(f"   {lang}: {count}")
            
        print(f"\n📂 Response categories:")
        for category, count in self.stats['response_categories'].items():
            print(f"   {category}: {count}")
            
        print(f"\n⚡ Performance:")
        metrics = self.stats['performance_metrics']
        print(f"   Avg OCR time: {metrics['avg_ocr_time']:.2f}s")
        print(f"   Avg response time: {metrics['avg_response_time']:.2f}s")
        
        # Learning system stats
        if hasattr(self.learning, 'get_stats'):
            learning_stats = self.learning.get_stats()
            print(f"\n🧠 Learning system:")
            print(f"   Total conversations: {learning_stats.get('total_conversations', 0)}")
            print(f"   Patterns learned: {learning_stats.get('patterns_learned', 0)}")
            
        print("="*60)
    
    def save_session_data(self):
        """💾 Save session data"""
        try:
            session_data = {
                'stats': self.stats,
                'config': self.config,
                'session_end': datetime.now().isoformat()
            }
            
            filename = f"conversation_data/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"💾 Session data saved: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save session data: {e}")
    
    def run_monitoring_loop(self):
        """🔄 Main monitoring loop"""
        import time
        
        self.logger.info("🚀 Starting Ultimate Telegram Responder...")
        
        if not self.find_telegram_window():
            print("❌ Please open Telegram Desktop first!")
            return
        
        self.running = True
        last_screenshot = None
        
        try:
            while self.running:
                try:
                    # Capture screenshot
                    screenshot_path = self.capture_screen()
                    if not screenshot_path:
                        time.sleep(self.config['check_interval'])
                        continue
                    
                    # Process screenshot
                    message_data = self.process_screenshot(screenshot_path)
                    if not message_data:
                        time.sleep(self.config['check_interval'])
                        continue
                    
                    # Check if this is a new message
                    current_text = message_data['text']
                    if current_text == last_screenshot:
                        time.sleep(self.config['check_interval'])
                        continue
                    
                    last_screenshot = current_text
                    
                    # Generate and send response
                    response = self.generate_response(message_data)
                    if response:
                        if self.send_response(response):
                            # Learn from interaction
                            self.learn_from_interaction(message_data, response)
                    
                    # Print status every 10 successful operations
                    if self.stats['messages_detected'] % 10 == 0:
                        self.print_status()
                    
                    time.sleep(self.config['check_interval'])
                    
                except KeyboardInterrupt:
                    self.logger.info("⏹️ Stopping by user request...")
                    break
                except Exception as e:
                    self.logger.error(f"❌ Loop error: {e}")
                    time.sleep(5)  # Wait longer on errors
                    
        except Exception as e:
            self.logger.error(f"❌ Critical error: {e}")
        finally:
            self.running = False
            self.save_session_data()
            self.print_status()
            self.logger.info("🏁 Ultimate Telegram Responder stopped")

    def run_interactive_mode(self):
        """🖥️ Interactive control mode"""
        print("\n🚀 ULTIMATE TELEGRAM RESPONDER v4.0")
        print("=====================================")
        print("Commands:")
        print("1. start - Start monitoring")
        print("2. stop - Stop monitoring")
        print("3. status - Show current status")
        print("4. config - Show configuration")
        print("5. stats - Show detailed statistics")
        print("6. test - Test OCR on current screen")
        print("7. exit - Exit program")
        print("=====================================\n")
        
        while True:
            try:
                command = input("Enter command: ").strip().lower()
                
                if command == 'start':
                    if not self.running:
                        self.run_monitoring_loop()
                    else:
                        print("✅ Already running!")
                        
                elif command == 'stop':
                    if self.running:
                        self.running = False
                        print("⏹️ Stopping...")
                    else:
                        print("⚠️ Not running!")
                        
                elif command == 'status':
                    self.print_status()
                    
                elif command == 'config':
                    print("\n⚙️ Current Configuration:")
                    for key, value in self.config.items():
                        print(f"   {key}: {value}")
                    print()
                    
                elif command == 'stats':
                    self.print_status()
                    if hasattr(self.learning, 'get_stats'):
                        stats = self.learning.get_stats()
                        print(f"\n🧠 Detailed Learning Stats:")
                        for key, value in stats.items():
                            print(f"   {key}: {value}")
                    print()
                    
                elif command == 'test':
                    print("📸 Taking test screenshot...")
                    screenshot_path = self.capture_screen()
                    if screenshot_path:
                        result = self.process_screenshot(screenshot_path)
                        if result:
                            print(f"✅ Detected text: {result['text']}")
                            print(f"🌍 Language: {result['language']}")
                            print(f"📊 Confidence: {result['confidence']:.2f}")
                        else:
                            print("❌ No text detected")
                    else:
                        print("❌ Screenshot failed")
                        
                elif command == 'exit':
                    if self.running:
                        self.running = False
                    print("👋 Goodbye!")
                    break
                    
                else:
                    print("❌ Unknown command. Type 'exit' to quit.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """🚀 Main function"""
    try:
        responder = UltimateTelegramResponder()
        responder.run_interactive_mode()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
            
    def load_configuration(self):
        """⚙️ Load advanced configuration"""
        default_config = {
            "telegram_executable": "C:\\TelegramDesktop\\Telegram.exe",
            "monitoring_interval": 2,
            "response_delay": 1.5,
            "auto_response_enabled": True,
            "max_responses_per_chat": 3,
            "ai_confidence_threshold": 0.6,
            "learning_enabled": True,
            "ocr_preprocessing": True,
            "response_caching": True,
            "working_hours": {
                "enabled": False,
                "start": "09:00",
                "end": "18:00"
            },
            "response_triggers": [
                "سلام", "hello", "hi", "سلام", "؟", "?", 
                "چطوری", "how are you", "کجایی", "where are you",
                "ممنون", "thanks", "کمک", "help"
            ],
            "excluded_chats": ["Saved Messages", "پیام‌های ذخیره شده"],
            "screen_regions": {
                "chat_list": {"x": 0, "y": 100, "width": 300, "height": 600},
                "chat_area": {"x": 300, "y": 100, "width": 700, "height": 600},
                "input_area": {"x": 300, "y": 650, "width": 600, "height": 50}
            },
            "ai_settings": {
                "response_creativity": 0.8,
                "learning_rate": 0.1,
                "pattern_matching_threshold": 0.6,
                "sentiment_analysis": True
            }
        }
        
        try:
            with open('conversation_data/ultimate_config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = default_config
            self.save_configuration()
            
    def save_configuration(self):
        """💾 Save configuration"""
        try:
            with open('conversation_data/ultimate_config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            
    def init_stats(self):
        """📊 Initialize comprehensive statistics"""
        self.stats = {
            "session_start": datetime.now().isoformat(),
            "messages_read": 0,
            "responses_sent": 0,
            "chats_processed": 0,
            "ocr_success": 0,
            "ocr_failed": 0,
            "ai_responses": 0,
            "template_responses": 0,
            "learning_interactions": 0,
            "errors": 0,
            "average_response_time": 0,
            "languages_detected": {"persian": 0, "english": 0},
            "response_categories": defaultdict(int)
        }
        
    def find_telegram_window(self):
        """🔍 Find Telegram window with enhanced detection"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if any(keyword in window_title.lower() for keyword in ['telegram', 'تلگرام']):
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append({
                        'hwnd': hwnd,
                        'title': window_title,
                        'rect': rect
                    })
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows[0] if windows else None
        
    def launch_telegram(self):
        """🚀 Launch Telegram with better detection"""
        self.logger.info("🚀 Launching Telegram...")
        
        # Check if already running
        telegram_window = self.find_telegram_window()
        if telegram_window:
            self.telegram_hwnd = telegram_window['hwnd']
            self.focus_telegram()
            self.logger.info("✅ Telegram already running")
            return True
            
        # Launch Telegram
        if os.path.exists(self.config['telegram_executable']):
            try:
                subprocess.Popen(self.config['telegram_executable'])
                time.sleep(5)  # Wait for startup
                
                # Find window after launch
                telegram_window = self.find_telegram_window()
                if telegram_window:
                    self.telegram_hwnd = telegram_window['hwnd']
                    self.focus_telegram()
                    self.logger.info("✅ Telegram launched successfully")
                    return True
                else:
                    self.logger.error("❌ Telegram window not found after launch")
                    return False
                    
            except Exception as e:
                self.logger.error(f"❌ Failed to launch Telegram: {e}")
                return False
        else:
            self.logger.error(f"❌ Telegram not found at: {self.config['telegram_executable']}")
            return False
            
    def focus_telegram(self):
        """🎯 Focus Telegram window"""
        try:
            if self.telegram_hwnd:
                win32gui.SetForegroundWindow(self.telegram_hwnd)
                win32gui.ShowWindow(self.telegram_hwnd, win32con.SW_RESTORE)
                time.sleep(0.3)
        except Exception as e:
            self.logger.error(f"Failed to focus Telegram: {e}")
            
    def capture_screen_region(self, region):
        """📸 Capture screen region with enhanced quality"""
        try:
            x, y, width, height = region['x'], region['y'], region['width'], region['height']
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Save with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            filename = f"conversation_data/capture_{timestamp}.png"
            screenshot.save(filename)
            
            return filename
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return None
            
    def read_chat_messages(self, image_path):
        """📖 Read messages with AI enhancement"""
        try:
            start_time = time.time()
            result = self.ocr.extract_text(image_path)
            
            if result and result['text']:
                self.stats['ocr_success'] += 1
                self.stats['languages_detected'][result['language']] += 1
                
                # Split into individual messages
                lines = result['text'].split('\n')
                messages = []
                
                for line in lines:
                    line = line.strip()
                    if len(line) > 3 and not line.isdigit():
                        # Filter out timestamps and system messages
                        if not any(word in line.lower() for word in ['online', 'آنلاین', 'typing', 'در حال تایپ']):
                            messages.append({
                                'text': line,
                                'language': result['language'],
                                'confidence': result['confidence'],
                                'quality': result['quality'],
                                'timestamp': datetime.now().isoformat(),
                                'processing_time': time.time() - start_time
                            })
                
                self.stats['messages_read'] += len(messages)
                return messages
            else:
                self.stats['ocr_failed'] += 1
                return []
                
        except Exception as e:
            self.logger.error(f"Failed to read messages: {e}")
            self.stats['ocr_failed'] += 1
            return []
            
    def should_respond(self, message):
        """🤔 Advanced decision making for responses"""
        text = message['text'].lower()
        
        # Check confidence threshold
        if message['confidence'] < self.config['ai_confidence_threshold']:
            return False
        
        # Check for trigger words
        for trigger in self.config['response_triggers']:
            if trigger.lower() in text:
                return True
                
        # Check for questions
        if '?' in text or '؟' in text:
            return True
            
        # Check message length (avoid very short messages)
        if len(message['text']) < 5:
            return False
        
        # AI-based decision (sentiment analysis)
        if self.config['ai_settings']['sentiment_analysis']:
            category = self.learning.categorize_message(message['text'])
            if category in ['question', 'greeting', 'thanks']:
                return True
            
        return True
        
    def generate_response(self, message):
        """🤖 Generate intelligent AI response"""
        try:
            start_time = time.time()
            
            # Use AI learning system
            response = self.learning.generate_intelligent_response(message['text'])
            
            if response:
                self.stats['ai_responses'] += 1
                response_category = self.learning.categorize_message(message['text'])
                self.stats['response_categories'][response_category] += 1
            else:
                # Fallback to templates
                self.stats['template_responses'] += 1
                if message['language'] == 'persian':
                    response = random.choice(['سلام! چطوری؟ 😊', 'ممنون از پیامت! 🙏', 'جالب بود! بیشتر بگو 🤔'])
                else:
                    response = random.choice(['Hello! How are you? 😊', 'Thanks for your message! 🙏', 'Interesting! Tell me more 🤔'])
            
            # Update response time stats
            response_time = time.time() - start_time
            if self.stats['average_response_time'] == 0:
                self.stats['average_response_time'] = response_time
            else:
                self.stats['average_response_time'] = (self.stats['average_response_time'] + response_time) / 2
                
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to generate response: {e}")
            return "متوجه نشدم / I don't understand"
            
    def send_response(self, response):
        """⌨️ Send response with enhanced reliability"""
        try:
            # Focus Telegram first
            self.focus_telegram()
            time.sleep(0.3)
            
            # Click on input area
            input_region = self.config['screen_regions']['input_area']
            input_x = input_region['x'] + input_region['width'] // 2
            input_y = input_region['y'] + input_region['height'] // 2
            
            pyautogui.click(input_x, input_y)
            time.sleep(0.3)
            
            # Clear any existing text
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            # Type the response with variable speed
            pyautogui.typewrite(response, interval=0.02)
            time.sleep(0.3)
            
            # Send message
            pyautogui.press('enter')
            
            self.stats['responses_sent'] += 1
            self.logger.info(f"✅ Sent: {response[:50]}...")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send response: {e}")
            self.stats['errors'] += 1
            return False
            
    def process_chat_cycle(self):
        """🔄 Enhanced chat processing cycle"""
        try:
            # Focus Telegram
            self.focus_telegram()
            
            # Capture chat area
            chat_region = self.config['screen_regions']['chat_area']
            screenshot_path = self.capture_screen_region(chat_region)
            
            if not screenshot_path:
                return
                
            # Read messages with AI
            messages = self.read_chat_messages(screenshot_path)
            
            if messages:
                self.logger.info(f"📖 Found {len(messages)} messages")
                
                # Process latest messages
                for message in messages[-2:]:  # Process last 2 messages
                    if self.should_respond(message):
                        self.logger.info(f"💬 Processing: {message['text'][:50]}...")
                        
                        # Generate AI response
                        response = self.generate_response(message)
                        
                        # Send response if enabled
                        if self.config['auto_response_enabled']:
                            time.sleep(self.config['response_delay'])
                            if self.send_response(response):
                                # Learn from this interaction
                                if self.config['learning_enabled']:
                                    self.learning.learn_from_interaction(message['text'], response)
                                    self.stats['learning_interactions'] += 1
                                time.sleep(1)  # Wait between messages
                        else:
                            self.logger.info(f"🤖 Would respond: {response}")
                            
                self.stats['chats_processed'] += 1
                            
            # Cleanup
            try:
                os.remove(screenshot_path)
            except:
                pass
                
        except Exception as e:
            self.logger.error(f"Error in chat cycle: {e}")
            self.stats['errors'] += 1
            
    def start_monitoring(self):
        """🚀 Start the ultimate monitoring system"""
        self.logger.info("🚀 Starting Ultimate Telegram Auto Responder...")
        
        # Launch Telegram
        if not self.launch_telegram():
            self.logger.error("❌ Cannot start - Telegram unavailable")
            return False
            
        self.running = True
        cycle_count = 0
        
        print("\n🤖 Ultimate Telegram AI Auto Responder v4.0 Active!")
        print("🧠 AI Learning System: ENABLED")
        print("🔍 Advanced OCR: ENABLED")
        print("📊 Data Collection: ENABLED")
        print("🌍 Languages: Persian + English")
        print("⌨️ Press 'q' to quit safely")
        print("⏸️ Press 'p' to pause/resume")
        print("📊 Press 's' to show stats")
        print("🧠 Press 'l' to show learning stats")
        print("-" * 70)
        
        try:
            while self.running:
                cycle_count += 1
                
                if cycle_count % 20 == 0:
                    self.logger.info(f"🔄 Monitoring cycle #{cycle_count}")
                    
                # Process current chat view
                self.process_chat_cycle()
                
                # Check for control keys
                if keyboard.is_pressed('q'):
                    self.logger.info("🛑 Quit requested")
                    break
                elif keyboard.is_pressed('p'):
                    self.toggle_pause()
                elif keyboard.is_pressed('s'):
                    self.show_stats()
                elif keyboard.is_pressed('l'):
                    self.show_learning_stats()
                    
                # Auto-save stats every 50 cycles
                if cycle_count % 50 == 0:
                    self.save_session_data()
                    
                # Wait for next cycle
                time.sleep(self.config['monitoring_interval'])
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Interrupted by user")
        finally:
            self.stop_monitoring()
            
        return True
        
    def toggle_pause(self):
        """⏸️ Toggle pause state"""
        self.config['auto_response_enabled'] = not self.config['auto_response_enabled']
        status = "ACTIVE" if self.config['auto_response_enabled'] else "PAUSED"
        self.logger.info(f"⏸️ Auto response: {status}")
        time.sleep(1)  # Prevent key repeat
        
    def show_stats(self):
        """📊 Show comprehensive statistics"""
        print("\n📊 Ultimate Responder Statistics:")
        print(f"  ⏰ Session time: {datetime.now() - datetime.fromisoformat(self.stats['session_start'])}")
        print(f"  📖 Messages read: {self.stats['messages_read']}")
        print(f"  💬 Responses sent: {self.stats['responses_sent']}")
        print(f"  💰 Chats processed: {self.stats['chats_processed']}")
        print(f"  ✅ OCR success: {self.stats['ocr_success']}")
        print(f"  ❌ OCR failed: {self.stats['ocr_failed']}")
        print(f"  🤖 AI responses: {self.stats['ai_responses']}")
        print(f"  📝 Template responses: {self.stats['template_responses']}")
        print(f"  🎓 Learning interactions: {self.stats['learning_interactions']}")
        print(f"  ⚡ Avg response time: {self.stats['average_response_time']:.3f}s")
        print(f"  🇮🇷 Persian: {self.stats['languages_detected']['persian']}")
        print(f"  🇺🇸 English: {self.stats['languages_detected']['english']}")
        print(f"  🚨 Errors: {self.stats['errors']}")
        print("-" * 50)
        time.sleep(3)  # Prevent key repeat
        
    def show_learning_stats(self):
        """🧠 Show learning system statistics"""
        learning_stats = self.learning.get_stats()
        print("\n🧠 AI Learning System Statistics:")
        print(f"  📚 Total conversations: {learning_stats['total_conversations']}")
        print(f"  🇮🇷 Persian conversations: {learning_stats['persian_conversations']}")
        print(f"  🇺🇸 English conversations: {learning_stats['english_conversations']}")
        print(f"  🎯 Patterns learned: {learning_stats['patterns_learned']}")
        print(f"  🔗 Word associations: {learning_stats['word_associations']}")
        print(f"  💾 Cache size: {learning_stats['cache_size']}")
        
        # Top response categories
        print("\n📊 Top Response Categories:")
        for category, count in sorted(self.stats['response_categories'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"    {category}: {count}")
        print("-" * 50)
        time.sleep(3)  # Prevent key repeat
        
    def save_session_data(self):
        """💾 Save session data"""
        try:
            # Save statistics
            with open('conversation_data/session_stats.json', 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
                
            # Save learning data
            self.learning.save_learning_data()
            
            self.logger.info("💾 Session data saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save session data: {e}")
        
    def stop_monitoring(self):
        """🛑 Stop monitoring and cleanup"""
        self.running = False
        self.save_session_data()
        
        self.logger.info("💾 All data saved")
        self.logger.info("👋 Ultimate Responder stopped")
        
    def setup_screen_coordinates(self):
        """🎯 Interactive setup for screen coordinates"""
        print("🎯 Ultimate Screen Coordinate Setup")
        print("Follow the instructions to set up screen regions for optimal AI performance")
        print("-" * 70)
        
        regions = ['chat_list', 'chat_area', 'input_area']
        
        for region in regions:
            input(f"\n📍 Position your mouse over the {region} and press Enter...")
            x, y = pyautogui.position()
            
            # Get region size with intelligent defaults
            if region == 'chat_list':
                width = int(input(f"Enter width for {region} (default 300): ") or "300")
                height = int(input(f"Enter height for {region} (default 600): ") or "600")
            elif region == 'chat_area':
                width = int(input(f"Enter width for {region} (default 700): ") or "700")
                height = int(input(f"Enter height for {region} (default 600): ") or "600")
            else:  # input_area
                width = int(input(f"Enter width for {region} (default 600): ") or "600")
                height = int(input(f"Enter height for {region} (default 50): ") or "50")
            
            self.config['screen_regions'][region] = {
                'x': x, 'y': y, 'width': width, 'height': height
            }
            
            print(f"✅ {region}: x={x}, y={y}, w={width}, h={height}")
            
        self.save_configuration()
        print("💾 Screen coordinates saved with AI optimization!")

def main():
    """🎯 Main application entry point"""
    responder = UltimateTelegramResponder()
    
    print("🚀 Ultimate Telegram AI Auto Responder v4.0")
    print("🤖 Advanced OCR + Intelligent Learning + Desktop Automation")
    print("=" * 70)
    print("1. 🚀 Start Ultimate Auto Responder")
    print("2. 🎯 Setup Screen Coordinates")
    print("3. ⚙️ View Configuration")
    print("4. 🧪 Test AI Systems")
    print("5. 📊 View Statistics")
    print("6. 🧠 Learning System Info")
    print("7. 🚪 Exit")
    
    try:
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == "1":
            responder.start_monitoring()
            
        elif choice == "2":
            responder.setup_screen_coordinates()
            
        elif choice == "3":
            print("\n⚙️ Ultimate Configuration:")
            for key, value in responder.config.items():
                if isinstance(value, dict):
                    print(f"  {key}:")
                    for subkey, subvalue in value.items():
                        print(f"    {subkey}: {subvalue}")
                else:
                    print(f"  {key}: {value}")
                
        elif choice == "4":
            # Test all AI systems
            print("\n🧪 Testing AI Systems...")
            
            # Test OCR
            screenshot = responder.capture_screen_region(responder.config['screen_regions']['chat_area'])
            if screenshot:
                messages = responder.read_chat_messages(screenshot)
                print(f"\n🔍 OCR Test Results ({len(messages)} messages):")
                for i, msg in enumerate(messages, 1):
                    print(f"  {i}. {msg['text']} (Lang: {msg['language']}, Conf: {msg['confidence']:.2f})")
            
            # Test learning system
            test_messages = ["سلام، حالت چطوره؟", "Hello, how are you?", "ممنون از کمکت", "Thank you for your help"]
            print(f"\n🧠 AI Learning Test:")
            for msg in test_messages:
                response = responder.learning.generate_intelligent_response(msg)
                print(f"  Q: {msg}")
                print(f"  A: {response}")
                print()
                
        elif choice == "5":
            responder.show_stats()
            
        elif choice == "6":
            responder.show_learning_stats()
            
        elif choice == "7":
            print("👋 Goodbye!")
            
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check dependencies
    missing_packages = []
    
    required_packages = {
        'pyautogui': 'pyautogui',
        'keyboard': 'keyboard', 
        'win32gui': 'pywin32',
        'cv2': 'opencv-python',
        'easyocr': 'easyocr'
    }
    
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"  pip install {package}")
        print("\nInstall missing packages and try again.")
    else:
        main()

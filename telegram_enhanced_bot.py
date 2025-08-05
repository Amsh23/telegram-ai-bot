#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Telegram Enhanced AI Auto-Reply Bot v2.5
⚡ Lightweight version with smart AI features
🧠 Advanced Persian/English Message Analysis
"""

import os
import time
import re
import random
import logging
import json
import numpy as np
import cv2
import pyautogui
import pyperclip
import pytesseract
from PIL import Image, ImageEnhance
from datetime import datetime
from typing import Optional, List, Dict, Tuple, Any
import hashlib
from collections import deque

# Optional AI imports (graceful fallback)
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("⚠️ EasyOCR not available, using Tesseract only")

try:
    from hazm import Normalizer
    HAZM_AVAILABLE = True
except ImportError:
    HAZM_AVAILABLE = False
    print("⚠️ Hazm not available, using basic text processing")

# Import configurations
try:
    from config_advanced import *
    print("✅ Advanced configuration loaded")
except ImportError:
    try:
        from config import *
        print("✅ Basic configuration loaded")
    except ImportError:
        print("❌ No configuration file found!")
        exit(1)

class EnhancedLogger:
    """📊 Enhanced logging with performance tracking"""
    
    def __init__(self):
        self.setup_logging()
        self.stats = {
            'messages_processed': 0,
            'responses_sent': 0,
            'ai_analysis_count': 0,
            'start_time': time.time()
        }
    
    def setup_logging(self):
        """Setup enhanced logging"""
        self.logger = logging.getLogger('TelegramEnhancedBot')
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # File handler
        handler = logging.FileHandler(LOG_FILENAME, encoding='utf-8')
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)
    
    def log_performance(self):
        """Log performance statistics"""
        uptime = time.time() - self.stats['start_time']
        if self.stats['messages_processed'] > 0:
            response_rate = (self.stats['responses_sent'] / self.stats['messages_processed']) * 100
            self.logger.info(f"📊 STATS: {self.stats['messages_processed']} msgs, {self.stats['responses_sent']} responses ({response_rate:.1f}%), {uptime/60:.1f}m uptime")

class SmartOCR:
    """🔍 Enhanced OCR with multiple engines"""
    
    def __init__(self):
        self.tesseract_config = OCR_CONFIG
        self.languages = OCR_LANGUAGES
        self.easyocr_reader = None
        self.ocr_cache = {}
        
        if EASYOCR_AVAILABLE:
            try:
                self.easyocr_reader = easyocr.Reader(['fa', 'en'], gpu=False)
                print("✅ EasyOCR initialized")
            except Exception as e:
                print(f"⚠️ EasyOCR init failed: {e}")
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """🎨 Smart image preprocessing"""
        # Convert to OpenCV
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Noise reduction
        cv_image = cv2.bilateralFilter(cv_image, 9, 75, 75)
        
        # Adaptive threshold
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        return Image.fromarray(thresh)
    
    def extract_text_smart(self, image: Image.Image) -> Dict[str, Any]:
        """🧠 Smart multi-engine text extraction"""
        # Create cache key
        img_hash = hashlib.md5(image.tobytes()).hexdigest()
        if img_hash in self.ocr_cache:
            return self.ocr_cache[img_hash]
        
        result = {'text': '', 'confidence': 0, 'engine': 'none'}
        
        # Preprocess image
        processed = self.preprocess_image(image)
        
        # Try Tesseract
        try:
            tesseract_data = pytesseract.image_to_data(
                processed, lang=self.languages, config=self.tesseract_config, 
                output_type=pytesseract.Output.DICT
            )
            
            words = []
            confidences = []
            for i, conf in enumerate(tesseract_data['conf']):
                if int(conf) > 30:
                    text = tesseract_data['text'][i].strip()
                    if text:
                        words.append(text)
                        confidences.append(int(conf))
            
            if words:
                result = {
                    'text': ' '.join(words),
                    'confidence': np.mean(confidences),
                    'engine': 'tesseract'
                }
        except Exception as e:
            print(f"Tesseract error: {e}")
        
        # Try EasyOCR if available and Tesseract confidence is low
        if self.easyocr_reader and (result['confidence'] < 60 or not result['text']):
            try:
                easyocr_results = self.easyocr_reader.readtext(np.array(processed))
                
                texts = []
                confidences = []
                for (bbox, text, conf) in easyocr_results:
                    if conf > 0.3:
                        texts.append(text)
                        confidences.append(conf * 100)
                
                if texts and (not result['text'] or np.mean(confidences) > result['confidence']):
                    result = {
                        'text': ' '.join(texts),
                        'confidence': np.mean(confidences),
                        'engine': 'easyocr'
                    }
            except Exception as e:
                print(f"EasyOCR error: {e}")
        
        # Cache result
        self.ocr_cache[img_hash] = result
        return result

class SmartAnalyzer:
    """🧠 Enhanced message analysis with AI features"""
    
    def __init__(self):
        self.normalizer = Normalizer() if HAZM_AVAILABLE else None
        self.conversation_history = deque(maxlen=20)
        self.persian_patterns = self.load_patterns()
    
    def load_patterns(self) -> List[str]:
        """Load Persian patterns"""
        return [
            r'[آ-ی]{2,}',
            r'(چطور|چی|کجا|کی|چرا|چه)',
            r'(سلام|درود|احوال)',
            r'(ممنون|مرسی|تشکر)',
            r'(باشه|اوکی|حله)',
            r'(میخوام|میگم|میدونم)',
        ]
    
    def detect_language(self, text: str) -> Dict[str, float]:
        """🌍 Smart language detection"""
        if not text:
            return {'persian': 0, 'english': 0, 'mixed': 0}
        
        persian_chars = len(re.findall(r'[آ-ی]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = persian_chars + english_chars
        
        if total_chars == 0:
            return {'persian': 0, 'english': 0, 'mixed': 0}
        
        persian_ratio = persian_chars / total_chars
        english_ratio = english_chars / total_chars
        
        if persian_ratio > 0.7:
            return {'persian': persian_ratio, 'english': english_ratio, 'mixed': 0}
        elif english_ratio > 0.7:
            return {'persian': persian_ratio, 'english': english_ratio, 'mixed': 0}
        else:
            return {'persian': persian_ratio, 'english': english_ratio, 'mixed': 1.0}
    
    def extract_intent(self, text: str) -> Dict[str, Any]:
        """🎯 Enhanced intent detection"""
        intent_patterns = {
            'greeting': [r'(سلام|hi|hello|hey|درود)', r'(احوال|چطور|how.*are)'],
            'question': [r'(چی|what|چطور|how|کجا|where|چرا|why)', r'[؟?]'],
            'thanks': [r'(ممنون|مرسی|thank|تشکر)', r'(خواهش|welcome)'],
            'goodbye': [r'(خداحافظ|bye|goodbye|فعلا)', r'(برم|رفتم|leaving)'],
            'request': [r'(میخوام|want|need|لطفا|please)', r'(کمک|help)'],
            'complaint': [r'(مشکل|problem|خراب|broken)', r'(نمیتونم|can.*not)'],
            'compliment': [r'(عالی|great|خوب|good|perfect)', r'(دوست.*دارم|love)'],
        }
        
        text_lower = text.lower()
        detected_intents = {}
        
        for intent, patterns in intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches * 0.4
            
            if score > 0:
                detected_intents[intent] = min(score, 1.0)
        
        if detected_intents:
            best_intent = max(detected_intents.items(), key=lambda x: x[1])
            return {'intent': best_intent[0], 'confidence': best_intent[1]}
        
        return {'intent': 'unknown', 'confidence': 0}
    
    def analyze_comprehensive(self, text: str) -> Dict[str, Any]:
        """📊 Comprehensive analysis"""
        if not text:
            return {}
        
        # Normalize text
        normalized = self.normalizer.normalize(text) if self.normalizer else text
        
        analysis = {
            'original_text': text,
            'normalized_text': normalized,
            'timestamp': time.time(),
            'length': len(text),
            'word_count': len(normalized.split()),
            'language': self.detect_language(normalized),
            'intent': self.extract_intent(normalized),
            'is_real_message': self.is_real_user_message(normalized),
            'complexity_score': self.calculate_complexity(normalized)
        }
        
        self.conversation_history.append(analysis)
        return analysis
    
    def is_real_user_message(self, text: str) -> Dict[str, Any]:
        """🔍 Enhanced real message detection"""
        if not text or len(text.strip()) < 2:
            return {'is_real': False, 'confidence': 0, 'reasons': ['too_short']}
        
        reasons = []
        score = 0
        
        # Check for real message indicators
        for pattern in REAL_MESSAGE_INDICATORS:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.25
                reasons.append(f'real_pattern')
        
        # Language check
        lang_info = self.detect_language(text)
        if lang_info['persian'] > 0.3 or lang_info['english'] > 0.3:
            score += 0.3
            reasons.append('language_detected')
        
        # Interface patterns (negative score)
        interface_count = 0
        for pattern in INTERFACE_PATTERNS:
            if re.search(pattern, text):
                interface_count += 1
                score -= 0.2
        
        if interface_count > 0:
            reasons.append(f'interface_patterns: {interface_count}')
        
        # Meaningful words
        words = text.split()
        meaningful_words = sum(1 for word in words 
                             if len(word) > 1 and not word.isdigit() and 
                             re.search(r'[a-zA-Zآ-ی]', word))
        
        if meaningful_words >= MIN_MEANINGFUL_WORDS:
            score += 0.3
            reasons.append(f'meaningful_words: {meaningful_words}')
        
        # Intent confidence boost
        intent_info = self.extract_intent(text)
        if intent_info['confidence'] > 0.4:
            score += 0.2
            reasons.append(f'intent: {intent_info["intent"]}')
        
        is_real = score > 0.5
        return {
            'is_real': is_real,
            'confidence': min(max(score, 0), 1),
            'reasons': reasons
        }
    
    def calculate_complexity(self, text: str) -> float:
        """🧮 Calculate text complexity"""
        if not text:
            return 0
        
        words = text.split()
        if not words:
            return 0
        
        avg_word_length = np.mean([len(word) for word in words])
        sentences = len(re.split(r'[.!?؟]', text))
        
        complexity = (avg_word_length / 8) + (len(words) / 15) + (sentences / 3)
        return min(complexity, 1.0)

class EnhancedResponseGenerator:
    """🎨 Smart response generation"""
    
    def __init__(self):
        self.load_templates()
    
    def load_templates(self):
        """Load response templates"""
        self.templates = {
            'greeting': {
                'casual': [
                    "سلاام! چطوری؟ چه خبرا؟ 😊",
                    "هللو! حالت چطوره؟ 👋",
                    "سلام عزیزم! خوش اومدی! 🤗"
                ],
                'formal': [
                    "سلام و احترام! چطور می‌تونم کمکتون کنم؟ 🙏",
                    "درود بر شما! در خدمتم 😊"
                ]
            },
            'question': [
                "خوب سوال پرسیدی! بذار ببینم... 🤔",
                "جالب! این رو چک می‌کنم 🔍",
                "میشه یکم بیشتر توضیح بدی؟ 🤗"
            ],
            'thanks': [
                "خواهش می‌کنم عزیزم! 😊💕",
                "قابلی نداشت! 🤗",
                "نوکرتم! همیشه! 😄"
            ],
            'goodbye': [
                "فعلاً! مواظب خودت باش! 👋😊",
                "خداحافظ عزیز! موفق باشی! 🌟",
                "بای بای! منتظرتم! 💕"
            ],
            'compliment': [
                "وای ممنون! خوشحالم! 😍",
                "چقدر مهربونی! ممنونم! 🥰",
                "دمت گرم! خیلی لطف داری! 😊"
            ],
            'confusion': [
                "ببخشید نفهمیدم چی گفتی! 😅",
                "یکم گیج شدم... دوباره بگو؟ 🤔",
                "نگرفتم! توضیح بیشتر لطفاً 😊"
            ]
        }
    
    def generate_smart_response(self, analysis: Dict[str, Any]) -> str:
        """🎯 Generate smart contextual response"""
        if not analysis.get('is_real_message', {}).get('is_real', False):
            return ""
        
        intent = analysis.get('intent', {}).get('intent', 'unknown')
        confidence = analysis.get('intent', {}).get('confidence', 0)
        language = analysis.get('language', {})
        
        # Choose response based on intent
        if intent == 'greeting' and confidence > 0.3:
            style = 'casual' if language.get('persian', 0) > 0.5 else 'formal'
            responses = self.templates['greeting'].get(style, self.templates['greeting']['casual'])
            return random.choice(responses)
        
        elif intent == 'question' and confidence > 0.3:
            return random.choice(self.templates['question'])
        
        elif intent == 'thanks' and confidence > 0.3:
            return random.choice(self.templates['thanks'])
        
        elif intent == 'goodbye' and confidence > 0.3:
            return random.choice(self.templates['goodbye'])
        
        elif intent == 'compliment' and confidence > 0.3:
            return random.choice(self.templates['compliment'])
        
        else:
            # Check traditional rules
            traditional = self.check_traditional_rules(analysis['normalized_text'])
            if traditional:
                return traditional
            
            # Default confusion response
            return random.choice(self.templates['confusion'])
    
    def check_traditional_rules(self, text: str) -> str:
        """Check traditional response rules"""
        text_lower = text.lower()
        
        for rule_name, rule_data in RESPONSE_RULES.items():
            keywords = rule_data['keywords']
            
            matched = [kw for kw in keywords if kw.lower() in text_lower]
            
            if matched:
                if 'responses' in rule_data:
                    return random.choice(rule_data['responses'])
                elif 'response' in rule_data:
                    response = rule_data['response']
                    if response == 'current_time':
                        return f"الان ساعت {datetime.now().strftime('%H:%M')} هست! ⏰"
                    return response
        
        return ""

class TelegramEnhancedBot:
    """🚀 Enhanced Telegram AI Bot"""
    
    def __init__(self):
        print("\n" + "="*60)
        print("🚀 Telegram Enhanced AI Bot v2.5 Starting...")
        print("="*60)
        
        # Initialize components
        self.logger = EnhancedLogger()
        self.ocr = SmartOCR()
        self.analyzer = SmartAnalyzer()
        self.response_generator = EnhancedResponseGenerator()
        
        # Settings
        self.chat_region = (CHAT_REGION['x'], CHAT_REGION['y'], CHAT_REGION['width'], CHAT_REGION['height'])
        self.input_position = (INPUT_CLICK_POSITION['x'], INPUT_CLICK_POSITION['y'])
        self.check_interval = CHECK_INTERVAL
        self.debug_mode = DEBUG_MODE
        
        # State
        self.is_running = False
        self.message_cache = {}
        
        self.logger.logger.info("🚀 Enhanced AI Bot initialized")
        print("✅ Bot ready!")
    
    def capture_and_analyze(self) -> Optional[Dict[str, Any]]:
        """📸 Capture and analyze screenshot"""
        try:
            # Capture
            screenshot = pyautogui.screenshot(region=self.chat_region)
            
            if self.debug_mode:
                screenshot.save('debug_screenshot.png')
            
            # OCR
            ocr_result = self.ocr.extract_text_smart(screenshot)
            text = ocr_result['text']
            
            if not text or len(text.strip()) < 2:
                return None
            
            # AI Analysis
            analysis = self.analyzer.analyze_comprehensive(text)
            analysis['ocr_info'] = ocr_result
            
            self.logger.stats['ai_analysis_count'] += 1
            
            if self.debug_mode:
                engine = ocr_result['engine']
                confidence = ocr_result['confidence']
                intent = analysis['intent']['intent']
                self.logger.logger.debug(f"📝 [{engine}] '{text[:40]}...' | Intent: {intent} | Conf: {confidence:.1f}")
            
            return analysis
            
        except Exception as e:
            self.logger.logger.error(f"❌ Analysis error: {e}")
            return None
    
    def should_respond(self, analysis: Dict[str, Any]) -> bool:
        """🤔 Smart response decision"""
        if not analysis:
            return False
        
        # Real message check
        real_info = analysis.get('is_real_message', {})
        if not real_info.get('is_real', False):
            if self.debug_mode:
                self.logger.logger.debug(f"❌ Not real: {real_info.get('reasons', [])}")
            return False
        
        # OCR confidence check
        ocr_confidence = analysis.get('ocr_info', {}).get('confidence', 0)
        if ocr_confidence < 25:
            if self.debug_mode:
                self.logger.logger.debug(f"❌ Low OCR confidence: {ocr_confidence}")
            return False
        
        # Duplicate check
        text_hash = hashlib.md5(analysis['normalized_text'].encode()).hexdigest()
        current_time = time.time()
        
        if text_hash in self.message_cache:
            last_time = self.message_cache[text_hash]
            if current_time - last_time < NEW_MESSAGE_THRESHOLD:
                if self.debug_mode:
                    self.logger.logger.debug("❌ Duplicate detected")
                return False
        
        self.message_cache[text_hash] = current_time
        
        # Clean old cache
        old_keys = [k for k, v in self.message_cache.items() if current_time - v > NEW_MESSAGE_THRESHOLD * 2]
        for k in old_keys:
            del self.message_cache[k]
        
        return True
    
    def send_response(self, response: str) -> bool:
        """📤 Send response with error handling"""
        if not response:
            return False
        
        try:
            # Click input
            pyautogui.click(self.input_position[0], self.input_position[1])
            time.sleep(0.3)
            
            # Clear and send
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            pyperclip.copy(response)
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            
            pyautogui.press('enter')
            
            self.logger.stats['responses_sent'] += 1
            self.logger.logger.info(f"📤 Sent: '{response[:30]}...'")
            
            return True
            
        except Exception as e:
            self.logger.logger.error(f"❌ Send error: {e}")
            return False
    
    def run(self):
        """🔄 Main bot loop"""
        self.is_running = True
        self.logger.logger.info("🚀 Enhanced AI monitoring started")
        
        print("\n" + "="*60)
        print("🤖 Enhanced AI Bot Running")
        print("="*60)
        print(f"📊 Region: {self.chat_region}")
        print(f"⏱️ Interval: {self.check_interval}s")
        print(f"🔍 Debug: {'ON' if self.debug_mode else 'OFF'}")
        print(f"🧠 AI Analysis: ACTIVE")
        print("="*60)
        print("⚠️ Press Ctrl+C to stop")
        print("🚨 Emergency: Move mouse to corner")
        print("="*60)
        
        try:
            while self.is_running:
                # Emergency stop check
                mouse_x, mouse_y = pyautogui.position()
                screen_width, screen_height = pyautogui.size()
                if (mouse_x < 5 or mouse_y < 5 or 
                    mouse_x > screen_width - 5 or mouse_y > screen_height - 5):
                    print("\n🚨 Emergency stop!")
                    break
                
                # Main processing
                analysis = self.capture_and_analyze()
                
                if analysis:
                    self.logger.stats['messages_processed'] += 1
                    
                    intent = analysis.get('intent', {}).get('intent', 'unknown')
                    confidence = analysis.get('is_real_message', {}).get('confidence', 0)
                    
                    self.logger.logger.info(f"📨 Detected: '{analysis['original_text'][:50]}...' | Intent: {intent} | Conf: {confidence:.2f}")
                    
                    if self.should_respond(analysis):
                        response = self.response_generator.generate_smart_response(analysis)
                        
                        if response:
                            self.logger.logger.info(f"🧠 Response: '{response[:40]}...'")
                            
                            if self.send_response(response):
                                self.logger.logger.info("✅ Response sent successfully")
                            else:
                                self.logger.logger.warning("⚠️ Failed to send")
                        else:
                            if self.debug_mode:
                                self.logger.logger.debug("🤐 No response generated")
                    else:
                        if self.debug_mode:
                            self.logger.logger.debug("🚫 Response not triggered")
                
                # Performance logging
                if self.logger.stats['messages_processed'] % 10 == 0 and self.logger.stats['messages_processed'] > 0:
                    self.logger.log_performance()
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n⛔ Bot stopped by user (Ctrl+C)")
        except Exception as e:
            self.logger.logger.error(f"❌ Critical error: {e}")
        finally:
            self.is_running = False
            self.logger.logger.info("🛑 Bot stopped")
            self.log_final_stats()
    
    def log_final_stats(self):
        """📈 Log final statistics"""
        uptime = time.time() - self.logger.stats['start_time']
        
        print("\n" + "="*50)
        print("📊 FINAL PERFORMANCE REPORT")
        print("="*50)
        print(f"⏱️ Runtime: {uptime/60:.1f} minutes")
        print(f"📨 Messages: {self.logger.stats['messages_processed']}")
        print(f"📤 Responses: {self.logger.stats['responses_sent']}")
        print(f"🧠 AI Analysis: {self.logger.stats['ai_analysis_count']}")
        
        if self.logger.stats['messages_processed'] > 0:
            response_rate = (self.logger.stats['responses_sent'] / self.logger.stats['messages_processed']) * 100
            print(f"📈 Response Rate: {response_rate:.1f}%")
        
        print("="*50)

def main():
    """🚀 Main entry point"""
    print("🤖 Starting Enhanced Telegram AI Bot...")
    
    try:
        bot = TelegramEnhancedBot()
        bot.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        print("\n👋 Bot shutdown complete!")

if __name__ == "__main__":
    main()

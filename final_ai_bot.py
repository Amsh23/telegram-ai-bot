#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Final AI Bot System
Complete solution with advanced OCR, learning, and Telegram integration
"""

import logging
import os
import json
import asyncio
import re
from datetime import datetime
from simple_learning import SimpleLearningSystem
from smart_ocr import SmartOCR

# Bot configuration
BOT_TOKEN = "7891967985:AAEDJMvNAT_SoWm6qoUGQLJTw7WaDvtd5qY"

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

class FinalAIBot:
    """🤖 Final AI Bot with Complete Functionality"""
    
    def __init__(self):
        self.setup_logging()
        self.init_systems()
        self.load_stats()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('final_ai_bot.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def init_systems(self):
        """🔧 Initialize all AI systems"""
        self.logger.info("🚀 Initializing Final AI Bot Systems...")
        
        # Initialize Simple Learning System
        self.learning = SimpleLearningSystem()
        self.logger.info(f"✅ Learning System: {self.learning.get_stats()['total_conversations']} conversations")
        
        # Initialize Smart OCR
        self.ocr = SmartOCR()
        self.logger.info("✅ Smart OCR initialized")
        
        # Initialize response enhancer
        self.init_response_enhancer()
        
    def init_response_enhancer(self):
        """🎯 Initialize response enhancement patterns"""
        self.response_enhancer = {
            'persian': {
                'polite_endings': ['😊', '🙂', '❤️', '🌹'],
                'question_starters': ['راستی', 'ببین', 'بگو ببینم', 'نظرت چیه'],
                'positive_reactions': ['واقعاً؟', 'جالبه!', 'عالیه!', 'چه خوب!'],
                'empathy': ['متوجهم', 'درکت می‌کنم', 'حق با توئه', 'کاملاً درسته']
            },
            'english': {
                'polite_endings': ['😊', '🙂', '👍', '✨'],
                'question_starters': ['By the way', 'Tell me', 'What do you think', 'How about'],
                'positive_reactions': ['Really?', 'Interesting!', 'That\'s great!', 'Awesome!'],
                'empathy': ['I understand', 'I see your point', 'That makes sense', 'You\'re right']
            }
        }
        
    def load_stats(self):
        """📊 Load comprehensive statistics"""
        try:
            with open('conversation_data/final_bot_stats.json', 'r', encoding='utf-8') as f:
                self.stats = json.load(f)
        except:
            self.stats = {
                'total_interactions': 0,
                'text_messages': 0,
                'image_messages': 0,
                'successful_ocr': 0,
                'failed_ocr': 0,
                'learned_responses': 0,
                'enhanced_responses': 0,
                'user_satisfaction': [],
                'session_start': datetime.now().isoformat(),
                'languages_detected': {'persian': 0, 'english': 0},
                'response_types': {
                    'learned': 0,
                    'pattern': 0,
                    'template': 0,
                    'enhanced': 0
                }
            }
    
    def save_stats(self):
        """💾 Save detailed statistics"""
        try:
            os.makedirs('conversation_data', exist_ok=True)
            self.stats['last_updated'] = datetime.now().isoformat()
            
            # Calculate additional metrics
            total_ocr = self.stats['successful_ocr'] + self.stats['failed_ocr']
            if total_ocr > 0:
                self.stats['ocr_success_rate'] = self.stats['successful_ocr'] / total_ocr
            
            if self.stats['user_satisfaction']:
                self.stats['avg_satisfaction'] = sum(self.stats['user_satisfaction']) / len(self.stats['user_satisfaction'])
            
            with open('conversation_data/final_bot_stats.json', 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save stats: {e}")
    
    def detect_language(self, text):
        """🌍 Enhanced language detection"""
        persian_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if persian_chars > english_chars:
            return 'persian'
        elif english_chars > 0:
            return 'english'
        else:
            return 'unknown'
    
    def enhance_response(self, response, language, intent):
        """✨ Enhance responses with personality and context"""
        if not response or language not in self.response_enhancer:
            return response
        
        enhancer = self.response_enhancer[language]
        enhanced = response
        
        # Add appropriate reactions based on intent
        if intent == 'positive':
            if language == 'persian' and not any(emoji in enhanced for emoji in enhancer['polite_endings']):
                enhanced += ' ' + enhancer['positive_reactions'][0] + ' ' + enhancer['polite_endings'][0]
            elif language == 'english':
                enhanced += ' ' + enhancer['positive_reactions'][0] + ' ' + enhancer['polite_endings'][0]
        
        # Add empathy for negative sentiments
        elif intent == 'negative':
            if language == 'persian':
                enhanced = enhancer['empathy'][0] + '، ' + enhanced
            else:
                enhanced = enhancer['empathy'][0] + '. ' + enhanced
        
        # Enhance questions with engagement
        elif intent == 'question':
            if '?' in enhanced or '؟' in enhanced:
                if language == 'persian':
                    enhanced += ' ' + enhancer['question_starters'][0] + ' نظرت چیه؟'
                else:
                    enhanced += ' ' + enhancer['question_starters'][0] + '?'
        
        self.stats['enhanced_responses'] += 1
        return enhanced
    
    def generate_smart_response(self, user_message):
        """🧠 Generate intelligent response with enhancements"""
        # Get basic response from learning system
        basic_response = self.learning.generate_response(user_message)
        
        if not basic_response:
            return None
        
        # Detect language and intent
        language = self.detect_language(user_message)
        intent = self.learning.detect_intent(user_message)
        
        # Enhance the response
        enhanced_response = self.enhance_response(basic_response, language, intent)
        
        # Update statistics
        self.stats['languages_detected'][language] = self.stats['languages_detected'].get(language, 0) + 1
        self.stats['response_types']['enhanced'] += 1
        
        return enhanced_response
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🎯 Enhanced start command"""
        learning_stats = self.learning.get_stats()
        
        welcome_msg = f"""
🤖 سلام! من بات هوشمند پیشرفته هستم

📊 آمار فعلی من:
🧠 {learning_stats['total_conversations']} مکالمه یاد گرفته‌ام
🇮🇷 {learning_stats['persian_conversations']} مکالمه فارسی
🇺🇸 {learning_stats['english_conversations']} مکالمه انگلیسی
🎯 {learning_stats['patterns_learned']} الگو شناخته‌ام

قابلیت‌هایم:
📱 تشخیص دقیق متن از تصاویر
🧠 یادگیری هوشمند از مکالمات
💬 پاسخ‌دهی با شخصیت
📊 تحلیل احساسات و قصد
✨ بهبود خودکار پاسخ‌ها

Hello! I'm an Advanced AI Bot

📊 My current stats:
🧠 Learned {learning_stats['total_conversations']} conversations
🇮🇷 {learning_stats['persian_conversations']} Persian conversations  
🇺🇸 {learning_stats['english_conversations']} English conversations
🎯 {learning_stats['patterns_learned']} patterns recognized

عکس بفرست یا باهام حرف بزن! / Send image or chat with me!
        """
        
        await update.message.reply_text(welcome_msg)
        self.stats['total_interactions'] += 1
        
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """💬 Enhanced text message handling"""
        try:
            user_message = update.message.text
            user_id = update.effective_user.id
            
            self.logger.info(f"📨 Message from {user_id}: {user_message[:50]}...")
            
            # Generate smart response
            response = self.generate_smart_response(user_message)
            
            if response:
                await update.message.reply_text(response)
                
                # Learn from this interaction
                self.learning.learn_from_conversation(user_message, response)
                self.learning.save_data()
                
                self.stats['learned_responses'] += 1
                self.logger.info(f"🤖 Enhanced response: {response[:50]}...")
            else:
                # Fallback with personality
                language = self.detect_language(user_message)
                fallback_responses = {
                    'persian': [
                        "جالب بود! بیشتر بگو 🤔",
                        "متوجه شدم، ادامه بده 😊", 
                        "خوب، چه خبر دیگه؟ 🌟",
                        "فهمیدم، نظرت چیه؟ 💭"
                    ],
                    'english': [
                        "Interesting! Tell me more 🤔",
                        "I see, please continue 😊",
                        "Got it, what else? 🌟", 
                        "Understood, what do you think? 💭"
                    ]
                }
                
                import random
                fallback = random.choice(fallback_responses.get(language, fallback_responses['english']))
                await update.message.reply_text(fallback)
                
                self.stats['response_types']['template'] += 1
            
            self.stats['text_messages'] += 1
            self.stats['total_interactions'] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Error handling text: {e}")
            await update.message.reply_text("❌ خطا در پردازش پیام / Processing error")
    
    async def handle_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🖼️ Enhanced image handling with smart OCR"""
        try:
            user_id = update.effective_user.id
            self.logger.info(f"🖼️ Image from {user_id}")
            
            # Download image
            photo = update.message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            
            # Save with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            image_path = f"temp_image_{user_id}_{timestamp}.jpg"
            await file.download_to_drive(image_path)
            
            self.stats['image_messages'] += 1
            
            # Process with Smart OCR
            await update.message.reply_text("🔍 تشخیص هوشمند متن... / Smart text recognition...")
            
            result = self.ocr.get_best_chat_text(image_path)
            
            if result:
                self.stats['successful_ocr'] += 1
                
                # Enhanced OCR response
                confidence_emoji = "🎯" if result['quality'] > 0.8 else "📊" if result['quality'] > 0.6 else "⚡"
                language_flag = "🇮🇷" if result['language'] == 'persian' else "🇺🇸"
                
                response_msg = f"""
✅ متن با دقت بالا شناسایی شد / High-accuracy text recognition:

📱 "{result['text']}"

{confidence_emoji} کیفیت: {result['quality']:.0%} / Quality: {result['quality']:.0%}
{language_flag} زبان: {result['language']} / Language: {result['language']}
🔧 روش: {result['method']} / Method: {result['method']}
                """
                
                if result.get('alternatives'):
                    response_msg += f"\n💡 گزینه‌های دیگر / Other options:\n"
                    for i, alt in enumerate(result['alternatives'][:2], 1):
                        response_msg += f"  {i}. {alt}\n"
                
                await update.message.reply_text(response_msg)
                
                # Generate intelligent response to the recognized text
                if len(result['text']) > 10 and result['quality'] > 0.6:
                    smart_response = self.generate_smart_response(result['text'])
                    if smart_response:
                        await update.message.reply_text(
                            f"🤖 پاسخ هوشمند / Smart response:\n\n{smart_response}"
                        )
                        
                        # Learn from OCR conversation
                        self.learning.learn_from_conversation(result['text'], smart_response)
                        self.learning.save_data()
                        self.stats['learned_responses'] += 1
                
            else:
                self.stats['failed_ocr'] += 1
                await update.message.reply_text(
                    "❌ متن واضحی تشخیص داده نشد / No clear text recognized\n" +
                    "💡 نکته: عکس واضح‌تری بفرستید / Tip: Send a clearer image"
                )
            
            # Clean up
            if os.path.exists(image_path):
                os.remove(image_path)
            
            self.stats['total_interactions'] += 1
                
        except Exception as e:
            self.logger.error(f"❌ Error handling image: {e}")
            await update.message.reply_text("❌ خطا در پردازش تصویر / Image processing error")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📊 Comprehensive statistics"""
        learning_stats = self.learning.get_stats()
        
        # Calculate OCR success rate
        total_ocr = self.stats['successful_ocr'] + self.stats['failed_ocr']
        ocr_rate = (self.stats['successful_ocr'] / total_ocr * 100) if total_ocr > 0 else 0
        
        stats_msg = f"""
📊 آمار کامل سیستم / Complete System Statistics

🤖 عملکرد بات / Bot Performance:
💬 کل تعاملات: {self.stats['total_interactions']}
📝 پیام‌های متنی: {self.stats['text_messages']}
🖼️ پیام‌های تصویری: {self.stats['image_messages']}
✅ OCR موفق: {self.stats['successful_ocr']} ({ocr_rate:.1f}%)
❌ OCR ناموفق: {self.stats['failed_ocr']}

🧠 یادگیری / Learning:
📚 کل مکالمات: {learning_stats['total_conversations']}
🇮🇷 فارسی: {learning_stats['persian_conversations']}
🇺🇸 انگلیسی: {learning_stats['english_conversations']}
🎯 الگوهای شناخته شده: {learning_stats['patterns_learned']}
🔗 ارتباطات کلمات: {learning_stats['word_associations']}

✨ پاسخ‌ها / Responses:
🎓 پاسخ‌های یادگرفته: {self.stats['learned_responses']}
🌟 پاسخ‌های بهبود یافته: {self.stats['enhanced_responses']}

⏰ شروع جلسه: {self.stats['session_start'][:19]}
        """
        
        await update.message.reply_text(stats_msg)
        self.stats['total_interactions'] += 1
    
    def run(self):
        """🚀 Run the complete AI bot system"""
        if not TELEGRAM_AVAILABLE:
            print("❌ Telegram library not available. Running console mode...")
            self.console_mode()
            return
            
        self.logger.info("🚀 Starting Final AI Bot System...")
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add all handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        application.add_handler(MessageHandler(filters.PHOTO, self.handle_image))
        
        self.logger.info("✅ Final AI Bot System ready!")
        
        # Auto-save stats
        async def auto_save():
            while True:
                await asyncio.sleep(300)
                self.save_stats()
        
        asyncio.create_task(auto_save())
        
        # Run the bot
        application.run_polling(drop_pending_updates=True)
    
    def console_mode(self):
        """💻 Enhanced console mode"""
        print("🤖 Final AI Bot - Enhanced Console Mode")
        print("Commands: /stats, /test, /ocr [image_path], /quit")
        print("Or chat normally!")
        print("=" * 60)
        
        learning_stats = self.learning.get_stats()
        print(f"🧠 Loaded with {learning_stats['total_conversations']} conversations")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['/quit', 'quit', 'exit']:
                    print("👋 نمی‌بینمت! / See you later!")
                    break
                    
                elif user_input == '/stats':
                    stats = self.learning.get_stats()
                    print("\n📊 Learning Statistics:")
                    for key, value in stats.items():
                        print(f"  📌 {key}: {value}")
                    print(f"\n🤖 Bot interactions: {self.stats['total_interactions']}")
                    
                elif user_input == '/test':
                    test_cases = [
                        "سلام چطوری؟", "Hello how are you?", 
                        "خسته‌ام", "I'm tired",
                        "چه کار می‌کنی؟", "What are you doing?"
                    ]
                    print("\n🧪 Enhanced Test Results:")
                    for test in test_cases:
                        response = self.generate_smart_response(test)
                        print(f"  👤 {test}")
                        print(f"  🤖 {response}")
                        print()
                        
                elif user_input.startswith('/ocr '):
                    image_path = user_input[5:].strip()
                    if os.path.exists(image_path):
                        print(f"🔍 Processing image: {image_path}")
                        result = self.ocr.get_best_chat_text(image_path)
                        if result:
                            print(f"✅ Recognized: {result['text']}")
                            print(f"🎯 Quality: {result['quality']:.0%}")
                            print(f"🌍 Language: {result['language']}")
                        else:
                            print("❌ No text recognized")
                    else:
                        print(f"❌ Image not found: {image_path}")
                        
                elif user_input:
                    response = self.generate_smart_response(user_input)
                    print(f"🤖 Bot: {response}")
                    
                    # Learn and update stats
                    self.learning.learn_from_conversation(user_input, response)
                    self.stats['total_interactions'] += 1
                    self.stats['text_messages'] += 1
                    
            except KeyboardInterrupt:
                print("\n👋 نمی‌بینمت! / Goodbye!")
                break
            except Exception as e:
                print(f"❌ خطا / Error: {e}")
        
        # Save final data
        self.learning.save_data()
        self.save_stats()
        print("💾 تمام اطلاعات ذخیره شد / All data saved!")

if __name__ == "__main__":
    import sys
    
    bot = FinalAIBot()
    
    if '--console' in sys.argv:
        bot.console_mode()
    else:
        bot.run()

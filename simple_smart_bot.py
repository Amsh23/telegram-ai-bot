#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Simple Smart Bot
Telegram bot using simple learning system and smart OCR
"""

import logging
import os
import json
import asyncio
from datetime import datetime
from simple_learning import SimpleLearningSystem
from smart_ocr import SmartOCR

# Configuration
BOT_TOKEN = "7891967985:AAEDJMvNAT_SoWm6qoUGQLJTw7WaDvtd5qY"  # Your bot token

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ Telegram library not available. Install with: pip install python-telegram-bot")

class SimpleSmartBot:
    """🤖 Simple Smart Bot with Learning and OCR"""
    
    def __init__(self):
        self.setup_logging()
        self.init_systems()
        self.load_stats()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('simple_bot.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def init_systems(self):
        """🔧 Initialize AI systems"""
        self.logger.info("🚀 Initializing Simple Smart Bot...")
        
        # Initialize Simple Learning System
        self.learning = SimpleLearningSystem()
        self.logger.info("✅ Simple Learning System loaded")
        
        # Initialize Smart OCR
        self.ocr = SmartOCR()
        self.logger.info("✅ Smart OCR initialized")
        
    def load_stats(self):
        """📊 Load bot statistics"""
        try:
            with open('conversation_data/simple_bot_stats.json', 'r', encoding='utf-8') as f:
                self.stats = json.load(f)
        except:
            self.stats = {
                'messages_processed': 0,
                'images_processed': 0,
                'successful_ocr': 0,
                'responses_generated': 0,
                'start_time': datetime.now().isoformat()
            }
    
    def save_stats(self):
        """💾 Save bot statistics"""
        try:
            os.makedirs('conversation_data', exist_ok=True)
            with open('conversation_data/simple_bot_stats.json', 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save stats: {e}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🎯 Start command"""
        welcome_msg = """
🤖 سلام! من بات هوشمند ساده هستم

قابلیت‌هایم:
📱 تشخیص متن از عکس (فارسی و انگلیسی)
🧠 یادگیری از مکالمات (۲۹۵ مکالمه آموخته‌ام!)
💬 پاسخ‌دهی هوشمند
📊 آمار عملکرد

Hello! I'm a Simple Smart Bot

My capabilities:
📱 Text recognition from images (Persian & English)  
🧠 Learning from conversations (trained on 295 conversations!)
💬 Smart responses
📊 Performance statistics

عکس بفرست یا باهام حرف بزن! / Send image or chat with me!
        """
        
        await update.message.reply_text(welcome_msg)
        self.stats['messages_processed'] += 1
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """❓ Help command"""
        help_msg = """
🆘 راهنما / Help

دستورات / Commands:
/start - شروع / Start
/help - راهنما / Help  
/stats - آمار / Statistics
/test - تست سیستم / Test System

استفاده / Usage:
📸 عکس چت = تشخیص متن / Send chat image = Text recognition
💬 پیام = یادگیری و پاسخ / Send message = Learning & response

نمونه‌ها / Examples:
👤 سلام چطوری؟
👤 Hello how are you?
👤 چه کار می‌کنی؟
👤 What's up?
        """
        
        await update.message.reply_text(help_msg)
        self.stats['messages_processed'] += 1
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📊 Statistics command"""
        learning_stats = self.learning.get_stats()
        
        stats_msg = f"""
📊 آمار سیستم / System Statistics

🤖 آمار بات / Bot Stats:
📈 پیام‌ها: {self.stats['messages_processed']}
🖼️ تصاویر: {self.stats['images_processed']}  
✅ OCR موفق: {self.stats['successful_ocr']}
💬 پاسخ‌ها: {self.stats['responses_generated']}

🧠 آمار یادگیری / Learning Stats:
📚 کل مکالمات: {learning_stats['total_conversations']}
🇮🇷 فارسی: {learning_stats['persian_conversations']}
🇺🇸 انگلیسی: {learning_stats['english_conversations']}
🎯 الگوها: {learning_stats['patterns_learned']}
🔗 ارتباطات: {learning_stats['word_associations']}

⏰ شروع: {self.stats['start_time'][:19]}
        """
        
        await update.message.reply_text(stats_msg)
        self.stats['messages_processed'] += 1
    
    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🧪 Test command"""
        test_cases = [
            "سلام چطوری؟",
            "Hello how are you?",
            "چه کار می‌کنی؟", 
            "What's up?"
        ]
        
        test_msg = "🧪 تست سیستم / System Test:\n\n"
        
        for test_input in test_cases:
            response = self.learning.generate_response(test_input)
            test_msg += f"👤 {test_input}\n🤖 {response}\n\n"
        
        await update.message.reply_text(test_msg)
        self.stats['messages_processed'] += 1
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """💬 Handle text messages"""
        try:
            user_message = update.message.text
            user_id = update.effective_user.id
            
            self.logger.info(f"📨 Text from {user_id}: {user_message[:50]}...")
            
            # Generate response using learning system
            response = self.learning.generate_response(user_message)
            
            if response:
                await update.message.reply_text(response)
                
                # Learn from this interaction
                self.learning.learn_from_conversation(user_message, response)
                self.learning.save_data()  # Save after each interaction
                
                self.stats['responses_generated'] += 1
                self.logger.info(f"🤖 Response: {response[:50]}...")
            else:
                await update.message.reply_text("متوجه نشدم / I don't understand")
            
            self.stats['messages_processed'] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Error handling text: {e}")
            await update.message.reply_text("❌ خطا در پردازش / Processing error")
    
    async def handle_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🖼️ Handle image messages"""
        try:
            user_id = update.effective_user.id
            self.logger.info(f"🖼️ Image from {user_id}")
            
            # Download image
            photo = update.message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            
            # Save image temporarily
            image_path = f"temp_image_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            await file.download_to_drive(image_path)
            
            self.stats['images_processed'] += 1
            
            # Process with Smart OCR
            await update.message.reply_text("🔍 تشخیص متن... / Recognizing text...")
            
            result = self.ocr.get_best_chat_text(image_path)
            
            if result:
                self.stats['successful_ocr'] += 1
                
                # Format response
                response_msg = f"""
✅ متن شناسایی شد / Text Recognized:

📱 {result['text']}

🎯 کیفیت: {result['quality']:.0%}
🌍 زبان: {result['language']}
                """
                
                await update.message.reply_text(response_msg)
                
                # Try to generate a response to the recognized text
                if len(result['text']) > 5 and result['quality'] > 0.5:
                    chat_response = self.learning.generate_response(result['text'])
                    if chat_response:
                        await update.message.reply_text(f"🤖 پاسخ پیشنهادی:\n{chat_response}")
                        self.stats['responses_generated'] += 1
                        
                        # Learn from the recognized conversation
                        self.learning.learn_from_conversation(result['text'], chat_response)
                        self.learning.save_data()
                
            else:
                await update.message.reply_text("❌ متن تشخیص داده نشد / No text recognized")
            
            # Clean up
            if os.path.exists(image_path):
                os.remove(image_path)
                
        except Exception as e:
            self.logger.error(f"❌ Error handling image: {e}")
            await update.message.reply_text("❌ خطا در پردازش تصویر / Image processing error")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🚨 Handle errors"""
        self.logger.error(f"❌ Update {update} caused error {context.error}")
    
    def run(self):
        """🚀 Run the bot"""
        if not TELEGRAM_AVAILABLE:
            print("❌ Cannot run bot - Telegram library not available")
            return
            
        self.logger.info("🚀 Starting Simple Smart Bot...")
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("test", self.test_command))
        
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        application.add_handler(MessageHandler(filters.PHOTO, self.handle_image))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        self.logger.info("✅ Simple Smart Bot is ready!")
        
        # Save stats periodically
        async def save_stats_periodically():
            while True:
                await asyncio.sleep(300)  # Every 5 minutes
                self.save_stats()
        
        # Start periodic stats saving
        asyncio.create_task(save_stats_periodically())
        
        # Run bot
        application.run_polling(drop_pending_updates=True)

# Console interface for testing without Telegram
def console_test():
    """💻 Console interface for testing"""
    print("🤖 Simple Smart Bot - Console Test Mode")
    print("Commands: /stats, /test, /quit")
    print("Or just chat normally!")
    print("-" * 50)
    
    bot = SimpleSmartBot()
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['/quit', 'quit', 'exit']:
                print("👋 Goodbye!")
                break
                
            elif user_input == '/stats':
                stats = bot.learning.get_stats()
                print("📊 Learning Statistics:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                    
            elif user_input == '/test':
                test_cases = ["سلام", "Hello", "چطوری؟", "How are you?"]
                print("🧪 Test Results:")
                for test in test_cases:
                    response = bot.learning.generate_response(test)
                    print(f"  👤 {test}")
                    print(f"  🤖 {response}")
                    
            elif user_input:
                response = bot.learning.generate_response(user_input)
                print(f"🤖 Bot: {response}")
                
                # Learn from interaction
                bot.learning.learn_from_conversation(user_input, response)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Save final data
    bot.learning.save_data()
    bot.save_stats()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--console':
        console_test()
    elif TELEGRAM_AVAILABLE:
        bot = SimpleSmartBot()
        bot.run()
    else:
        print("🤖 Simple Smart Bot")
        print("Options:")
        print("  python simple_smart_bot.py --console    # Console test mode")
        print("  python simple_smart_bot.py              # Telegram bot mode")
        print()
        print("⚠️ For Telegram mode, install: pip install python-telegram-bot")
        console_test()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Enhanced Telegram AI Bot
Advanced bot with smart OCR, expanded learning, and high accuracy
"""

import logging
import os
import json
import asyncio
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import cv2
import numpy as np
from smart_ocr import SmartOCR
from learning_system import LearningSystem

# Load configuration
from config_advanced import *

class EnhancedTelegramBot:
    """🤖 Enhanced Telegram Bot with Smart Learning"""
    
    def __init__(self):
        self.setup_logging()
        self.init_systems()
        self.load_stats()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_bot.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def init_systems(self):
        """🔧 Initialize AI systems"""
        self.logger.info("🚀 Initializing Enhanced Bot Systems...")
        
        # Initialize Smart OCR
        self.ocr = SmartOCR()
        self.logger.info("✅ Smart OCR initialized")
        
        # Initialize Learning System
        self.learning = LearningSystem()
        self.logger.info("✅ Learning System initialized")
        
        # Load conversation data
        self.load_conversation_data()
        
    def load_conversation_data(self):
        """📚 Load conversation data for learning"""
        try:
            with open('conversation_data/collected_chats.json', 'r', encoding='utf-8') as f:
                conversations = json.load(f)
            
            # Feed high-quality conversations to learning system
            added_count = 0
            for conv in conversations:
                if conv.get('quality', 0) > 0.8:  # Only high quality
                    self.learning.learn_from_conversation(
                        conv['input'], 
                        conv['response']
                    )
                    added_count += 1
            
            self.logger.info(f"📚 Loaded {added_count} quality conversations for learning")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load conversation data: {e}")
    
    def load_stats(self):
        """📊 Load bot statistics"""
        try:
            with open('conversation_data/bot_stats.json', 'r', encoding='utf-8') as f:
                self.stats = json.load(f)
        except:
            self.stats = {
                'messages_processed': 0,
                'images_processed': 0,
                'successful_ocr': 0,
                'learned_conversations': 0,
                'start_time': datetime.now().isoformat()
            }
    
    def save_stats(self):
        """💾 Save bot statistics"""
        try:
            with open('conversation_data/bot_stats.json', 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save stats: {e}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🎯 Start command handler"""
        welcome_msg = """
🤖 سلام! من بات هوشمند تلگرام هستم

قابلیت‌های من:
📱 تشخیص متن فارسی و انگلیسی از تصاویر
🧠 یادگیری از مکالمات شما
💬 پاسخ‌دهی هوشمند
📊 تحلیل احساسات

کافیه عکس چت بفرستی یا با من صحبت کنی!

Hello! I'm an intelligent Telegram bot

My capabilities:
📱 Persian & English text recognition from images  
🧠 Learning from your conversations
💬 Smart responses
📊 Sentiment analysis

Just send me a chat screenshot or talk to me!
        """
        
        await update.message.reply_text(welcome_msg)
        self.stats['messages_processed'] += 1
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """❓ Help command handler"""
        help_msg = """
🆘 راهنما / Help

دستورات / Commands:
/start - شروع / Start
/help - راهنما / Help  
/stats - آمار / Statistics
/quality - کیفیت یادگیری / Learning Quality

استفاده / Usage:
📸 عکس چت بفرست = متن رو تشخیص می‌دم
💬 پیام بفرست = یاد می‌گیرم و جواب می‌دم

📸 Send chat image = I'll recognize text
💬 Send message = I'll learn and respond
        """
        
        await update.message.reply_text(help_msg)
        self.stats['messages_processed'] += 1
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """📊 Statistics command handler"""
        stats_msg = f"""
📊 آمار بات / Bot Statistics

📈 پیام‌های پردازش شده: {self.stats['messages_processed']}
🖼️ تصاویر پردازش شده: {self.stats['images_processed']}
✅ OCR موفق: {self.stats['successful_ocr']}
🧠 مکالمات یادگرفته: {self.stats['learned_conversations']}

📈 Messages processed: {self.stats['messages_processed']}
🖼️ Images processed: {self.stats['images_processed']}
✅ Successful OCR: {self.stats['successful_ocr']}
🧠 Learned conversations: {self.stats['learned_conversations']}

⏰ شروع کار: {self.stats['start_time'][:19]}
        """
        
        await update.message.reply_text(stats_msg)
        self.stats['messages_processed'] += 1
    
    async def quality_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🎯 Quality command handler"""
        try:
            # Load conversation stats
            with open('conversation_data/expansion_stats.json', 'r', encoding='utf-8') as f:
                conv_stats = json.load(f)
            
            quality_msg = f"""
🎯 کیفیت یادگیری / Learning Quality

📚 کل مکالمات: {conv_stats['total_conversations']}
🇮🇷 فارسی: {conv_stats['persian_conversations']}
🇺🇸 انگلیسی: {conv_stats['english_conversations']}
⭐ میانگین کیفیت: {conv_stats['average_quality']:.2f}

📁 منابع: {', '.join(conv_stats['sources'][:5])}...

📚 Total conversations: {conv_stats['total_conversations']}
🇮🇷 Persian: {conv_stats['persian_conversations']}
🇺🇸 English: {conv_stats['english_conversations']}
⭐ Average quality: {conv_stats['average_quality']:.2f}
            """
            
        except:
            quality_msg = "❌ خطا در بارگیری آمار کیفیت / Error loading quality stats"
        
        await update.message.reply_text(quality_msg)
        self.stats['messages_processed'] += 1
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """💬 Handle text messages"""
        try:
            user_message = update.message.text
            user_id = update.effective_user.id
            
            self.logger.info(f"📨 Text from {user_id}: {user_message[:50]}...")
            
            # Generate learned response
            response = self.learning.generate_learned_response(user_message)
            
            if response:
                await update.message.reply_text(response)
                
                # Learn from this interaction
                self.learning.learn_from_conversation(user_message, response)
                self.stats['learned_conversations'] += 1
                
                self.logger.info(f"🤖 Response: {response[:50]}...")
            else:
                # Fallback responses
                fallback_responses = {
                    'persian': [
                        "جالب بود! بیشتر بگو",
                        "متوجه شدم، ادامه بده",
                        "خوب، چه خبر دیگه؟",
                        "فهمیدم، نظرت چیه؟"
                    ],
                    'english': [
                        "Interesting! Tell me more",
                        "I see, please continue",
                        "Understood, what else?",
                        "Got it, what do you think?"
                    ]
                }
                
                # Detect language
                import re
                is_persian = bool(re.search(r'[\u0600-\u06FF]', user_message))
                lang = 'persian' if is_persian else 'english'
                
                import random
                fallback = random.choice(fallback_responses[lang])
                await update.message.reply_text(fallback)
                
                # Still learn from interaction
                self.learning.learn_from_conversation(user_message, fallback)
                self.stats['learned_conversations'] += 1
            
            self.stats['messages_processed'] += 1
            
        except Exception as e:
            self.logger.error(f"❌ Error handling text: {e}")
            await update.message.reply_text("❌ خطا در پردازش پیام / Error processing message")
    
    async def handle_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🖼️ Handle image messages"""
        try:
            user_id = update.effective_user.id
            self.logger.info(f"🖼️ Image from {user_id}")
            
            # Download image
            photo = update.message.photo[-1]  # Get highest resolution
            file = await context.bot.get_file(photo.file_id)
            
            # Save image temporarily
            image_path = f"temp_image_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            await file.download_to_drive(image_path)
            
            self.stats['images_processed'] += 1
            
            # Process with Smart OCR
            await update.message.reply_text("🔍 در حال تشخیص متن... / Recognizing text...")
            
            result = self.ocr.get_best_chat_text(image_path)
            
            if result:
                self.stats['successful_ocr'] += 1
                
                # Format response
                response_msg = f"""
✅ متن شناسایی شد / Text Recognized:

📱 {result['text']}

🎯 کیفیت: {result['quality']:.0%} / Quality: {result['quality']:.0%}
🌍 زبان: {result['language']} / Language: {result['language']}
🔧 روش: {result['method']} / Method: {result['method']}
                """
                
                if result['alternatives']:
                    response_msg += f"\n💡 گزینه‌های دیگر / Alternatives:\n"
                    for i, alt in enumerate(result['alternatives'][:3], 1):
                        response_msg += f"{i}. {alt}\n"
                
                await update.message.reply_text(response_msg)
                
                # Learn from recognized text if it looks like a conversation
                if len(result['text']) > 10 and result['quality'] > 0.7:
                    # Try to generate a response to the recognized text
                    learned_response = self.learning.generate_learned_response(result['text'])
                    if learned_response:
                        await update.message.reply_text(f"🤖 پاسخ پیشنهادی / Suggested response:\n{learned_response}")
                
            else:
                await update.message.reply_text("❌ متن قابل تشخیص پیدا نشد / No recognizable text found")
            
            # Clean up
            if os.path.exists(image_path):
                os.remove(image_path)
                
        except Exception as e:
            self.logger.error(f"❌ Error handling image: {e}")
            await update.message.reply_text("❌ خطا در پردازش تصویر / Error processing image")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """🚨 Handle errors"""
        self.logger.error(f"❌ Update {update} caused error {context.error}")
    
    def run(self):
        """🚀 Run the bot"""
        self.logger.info("🚀 Starting Enhanced Telegram Bot...")
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("quality", self.quality_command))
        
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
        application.add_handler(MessageHandler(filters.PHOTO, self.handle_image))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        self.logger.info("✅ Enhanced Bot is ready!")
        
        # Save stats periodically
        async def save_stats_periodically():
            while True:
                await asyncio.sleep(300)  # Every 5 minutes
                self.save_stats()
        
        # Start periodic stats saving
        asyncio.create_task(save_stats_periodically())
        
        # Run bot
        application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    bot = EnhancedTelegramBot()
    bot.run()

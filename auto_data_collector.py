#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Advanced Automatic Data Collection Agent
Collects Persian and English conversations from multiple sources
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import sqlite3
import re
import os
from typing import List, Dict
import logging
from datetime import datetime
import random
from urllib.parse import urljoin, urlparse

class AutoDataCollectionAgent:
    def __init__(self):
        self.conversations = []
        self.setup_logging()
        self.setup_database()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
    def setup_database(self):
        """Setup SQLite database for storing collected data"""
        os.makedirs('conversation_data', exist_ok=True)
        self.conn = sqlite3.connect('conversation_data/collected_data.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                source TEXT,
                language TEXT,
                input_text TEXT,
                response_text TEXT,
                quality_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def run_complete_collection(self):
        """Run complete data collection process"""
        print("🚀 Starting Complete Data Collection Process...")
        
        # Step 1: Clean corrupted data
        self.clean_corrupted_data()
        
        # Step 2: Create quality Persian chats
        self.create_quality_persian_chats()
        
        # Step 3: Collect from Persian sources
        self.collect_persian_sources()
        
        # Step 4: Collect from English sources  
        self.collect_english_sources()
        
        # Step 5: Save all collected data
        self.save_all_data()
        
        print("✅ Complete data collection finished!")
    
    def clean_corrupted_data(self):
        """Clean corrupted learning data"""
        print("🧹 Cleaning corrupted data...")
        try:
            # Clean conversations.json
            valid_conversations = []
            
            if os.path.exists("conversation_data/conversations.json"):
                with open("conversation_data/conversations.json", "r", encoding="utf-8") as f:
                    conversations = json.load(f)
                
                for conv in conversations:
                    msg = conv.get("user_message", "")
                    if (len(msg) < 50 and 
                        not any(word in msg.lower() for word in ["error", "occurred", "launcher", "cuusers"]) and
                        (self.is_persian(msg) or self.is_clean_english(msg))):
                        valid_conversations.append(conv)
            
            with open("conversation_data/conversations.json", "w", encoding="utf-8") as f:
                json.dump(valid_conversations, f, ensure_ascii=False, indent=2)
            
            # Clean learned_patterns.json
            clean_patterns = {
                "persian_greeting": [],
                "persian_question": [],
                "persian_thanks": [],
                "persian_goodbye": [],
                "english_greeting": [],
                "english_question": [],
                "english_thanks": [],
                "english_goodbye": []
            }
            
            with open("conversation_data/learned_patterns.json", "w", encoding="utf-8") as f:
                json.dump(clean_patterns, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Cleaned! Kept {len(valid_conversations)} valid conversations")
            
        except Exception as e:
            print(f"❌ Error cleaning data: {e}")
    
    def create_quality_persian_chats(self):
        """Create high-quality Persian chat samples"""
        print("📝 Creating quality Persian chats...")
        
        quality_chats = [
            {
                "input": "سلام، حالت چطوره؟",
                "response": "سلام عزیزم! خوبم ممنون، تو چطوری؟",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "ممنون از کمکت",
                "response": "خواهش می‌کنم! همیشه در خدمتم 😊",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "امروز هوا چطوره؟",
                "response": "هوا خیلی قشنگه! مناسب برای پیاده‌روی",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "چه خبر؟",
                "response": "سلامتی! همه چی خوبه، شما چه خبر؟",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "کاری داشتی؟",
                "response": "نه فعلاً، فقط می‌خواستم احوال پرسی کنم",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "خسته نباشی",
                "response": "ممنون عزیزم! شما هم خسته نباشید",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "موفق باشی",
                "response": "دستت درد نکنه! تو هم موفق باشی",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "خداحافظ",
                "response": "خداحافظ! مراقب خودت باش",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "میتونی کمکم کنی؟",
                "response": "البته! چه کاری می‌تونم برات انجام بدم؟",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "این چیه؟",
                "response": "کدوم چیز رو می‌گی؟ می‌تونی بیشتر توضیح بدی؟",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "خیلی ممنونم",
                "response": "قابلی نداره! خوشحالم که کمک کردم",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            },
            {
                "input": "نظرت چیه؟",
                "response": "فکر می‌کنم باید بیشتر بررسی کنیم. تو چی فکر می‌کنی؟",
                "source": "manual",
                "language": "persian",
                "quality": 0.9
            }
        ]
        
        with open("conversation_data/quality_persian_chats.json", "w", encoding="utf-8") as f:
            json.dump(quality_chats, f, ensure_ascii=False, indent=2)
        
        # Add to main conversations list
        self.conversations.extend(quality_chats)
        print(f"✅ Created {len(quality_chats)} quality Persian chats")
    
    def collect_persian_sources(self):
        """Collect from Persian sources"""
        print("🇮🇷 Collecting from Persian sources...")
        
        persian_sources = [
            self.collect_sample_digikala,
            self.collect_sample_aparat,
            self.collect_sample_virgool,
            self.collect_sample_news_comments
        ]
        
        for source_func in persian_sources:
            try:
                source_func()
                time.sleep(1)  # Respectful delay
            except Exception as e:
                self.logger.error(f"Error in Persian source: {e}")
    
    def collect_english_sources(self):
        """Collect from English sources"""
        print("🇺🇸 Collecting from English sources...")
        
        english_sources = [
            self.collect_sample_stackoverflow,
            self.collect_sample_reddit,
            self.collect_sample_github,
            self.collect_sample_docs
        ]
        
        for source_func in english_sources:
            try:
                source_func()
                time.sleep(1)  # Respectful delay
            except Exception as e:
                self.logger.error(f"Error in English source: {e}")
    
    def collect_sample_digikala(self):
        """Collect sample product reviews (DigiKala style)"""
        sample_reviews = [
            ("خیلی راضی هستم از خریدم", "خوشحالم که راضی هستید! 😊"),
            ("کیفیت عالی داره", "بله، کیفیتش واقعاً خوبه"),
            ("ارسال سریع بود", "ممنون از بازخوردتون!"),
            ("قیمتش مناسبه", "بله، قیمت خوبیه برای این کیفیت"),
            ("پیشنهاد می‌کنم", "ممنون! نظرتون خیلی مفیده"),
            ("مشکلی نداشت", "عالیه! امیدوارم همیشه راضی باشید"),
            ("بسته‌بندی خوب بود", "مراقبت ما از محصولات مهمه"),
            ("برای هدیه خریدم", "انتخاب خوبی بوده! امیدوارم خوششون بیاد")
        ]
        
        for review, response in sample_reviews:
            self.add_conversation(review, response, 'digikala', 'persian')
    
    def collect_sample_aparat(self):
        """Collect sample video comments (Aparat style)"""
        sample_comments = [
            ("ویدیو عالی بود، ممنون", "خوشحالم که مفید بود!"),
            ("می‌تونید بیشتر توضیح بدید؟", "حتماً! چه قسمتی رو می‌خواید بیشتر بدونید؟"),
            ("کی ویدیو بعدی میاد؟", "به زودی ویدیو جدید آپلود می‌کنم"),
            ("خیلی کارتون حرفه‌ایه", "ممنون! سعی می‌کنم بهترین رو ارائه بدم"),
            ("لایک کردم", "ممنون! حمایتتون انگیزه‌بخشه"),
            ("اشتراک گذاشتم", "خیلی ممنون! امیدوارم مفید باشه براتون"),
            ("این قسمت رو نفهمیدم", "کدوم قسمت؟ می‌تونم بیشتر توضیح بدم"),
            ("آموزش خوبی بود", "خوشحالم که یاد گرفتید!")
        ]
        
        for comment, response in sample_comments:
            self.add_conversation(comment, response, 'aparat', 'persian')
    
    def collect_sample_virgool(self):
        """Collect sample article comments (Virgool style)"""
        sample_discussions = [
            ("مقاله جالبی بود", "ممنون! امیدوارم مفید بوده"),
            ("نظر متفاوتی دارم", "جالبه! می‌تونید نظرتون رو بگید؟"),
            ("تجربه من متفاوته", "تجربه‌تون رو می‌تونید شیر کنید؟"),
            ("کاملاً موافقم", "خوشحالم که هم‌نظریم!"),
            ("این نکته رو نمی‌دونستم", "بله، خیلی‌ها این رو نمی‌دونن"),
            ("ممنون بابت اشتراک‌گذاری", "خواهش می‌کنم! امیدوارم مفید باشه"),
            ("منبع این اطلاعات چیه؟", "منابع رو در انتهای مقاله ذکر کردم"),
            ("عالی نوشتید", "ممنون! حمایتتون انگیزه می‌ده")
        ]
        
        for discussion, response in sample_discussions:
            self.add_conversation(discussion, response, 'virgool', 'persian')
    
    def collect_sample_news_comments(self):
        """Collect sample news comments"""
        sample_news_comments = [
            ("خبر جالبی بود", "بله، اتفاق مهمیه"),
            ("نظرتون چیه؟", "فکر می‌کنم باید منتظر تحولات بعدی باشیم"),
            ("امیدوارم بهتر بشه", "بله، همگی امیدواریم"),
            ("اطلاعات بیشتری داریم؟", "فعلاً همین اطلاعات در دسترسه"),
            ("کی نتیجه مشخص میشه؟", "احتمالاً طی روزهای آینده"),
            ("این موضوع مهمه", "کاملاً درسته، تأثیر زیادی داره"),
            ("باید پیگیری کنیم", "بله، حتماً پیگیری می‌کنیم"),
            ("امیدوار به بهترین", "همگی امیدواریم نتیجه خوب باشه")
        ]
        
        for comment, response in sample_news_comments:
            self.add_conversation(comment, response, 'news', 'persian')
    
    def collect_sample_stackoverflow(self):
        """Collect sample StackOverflow Q&A"""
        sample_qa = [
            ("How do I fix this error?", "Can you share the full error message and your code?"),
            ("What's the best way to learn Python?", "Start with the official tutorial and practice with small projects."),
            ("Why is my code not working?", "Could you provide more details about what's happening?"),
            ("Thank you for the help!", "You're welcome! Happy to help!"),
            ("This solution worked perfectly", "Great! Glad it solved your problem."),
            ("Can you explain this concept?", "Sure! Which part would you like me to clarify?"),
            ("Is there a better approach?", "There are several ways. What's your specific use case?"),
            ("I'm getting a syntax error", "Syntax errors usually mean there's a typo. Can you check your code?")
        ]
        
        for question, answer in sample_qa:
            self.add_conversation(question, answer, 'stackoverflow', 'english')
    
    def collect_sample_reddit(self):
        """Collect sample Reddit conversations"""
        sample_reddit = [
            ("What's your opinion on this?", "I think it's interesting! What do you think?"),
            ("Can someone explain this?", "Sure! It's basically about how the system works."),
            ("Thank you for sharing!", "You're welcome! Hope it was helpful."),
            ("I disagree with this", "That's fair! Different perspectives are valuable."),
            ("This is really helpful", "Glad you found it useful!"),
            ("Anyone have experience with this?", "I've worked with it before. What specifically do you need help with?"),
            ("Is this reliable?", "From my experience, it's generally reliable, but always good to verify."),
            ("Great explanation!", "Thanks! I tried to make it as clear as possible.")
        ]
        
        for question, answer in sample_reddit:
            self.add_conversation(question, answer, 'reddit', 'english')
    
    def collect_sample_github(self):
        """Collect sample GitHub issue discussions"""
        sample_github = [
            ("Found a bug in the code", "Thanks for reporting! Can you provide steps to reproduce?"),
            ("Feature request: add new functionality", "Interesting idea! Can you describe the use case?"),
            ("How do I contribute?", "Check out our contributing guidelines in the README."),
            ("The documentation is unclear", "Thanks for the feedback! Which part needs clarification?"),
            ("Great project!", "Thank you! Contributions are always welcome."),
            ("Is this still maintained?", "Yes, we're actively maintaining it. Latest update was recent."),
            ("Performance issue found", "Thanks for reporting! Can you share performance metrics?"),
            ("Question about implementation", "Sure! What specific aspect would you like to know about?")
        ]
        
        for issue, response in sample_github:
            self.add_conversation(issue, response, 'github', 'english')
    
    def collect_sample_docs(self):
        """Collect sample documentation Q&A"""
        sample_docs = [
            ("How do I get started?", "Check out our quick start guide in the documentation."),
            ("What are the requirements?", "You'll need Python 3.7+ and the packages listed in requirements.txt."),
            ("Is there an API reference?", "Yes, the complete API reference is available in the docs section."),
            ("Can I see some examples?", "Absolutely! There are several examples in the examples/ directory."),
            ("What's the best practice?", "We recommend following the patterns shown in our tutorials."),
            ("How do I troubleshoot issues?", "Start by checking the troubleshooting section in our docs."),
            ("Is there community support?", "Yes, you can ask questions in our community forum or GitHub discussions."),
            ("Where can I report bugs?", "Please report bugs in our GitHub issue tracker with detailed information.")
        ]
        
        for question, answer in sample_docs:
            self.add_conversation(question, answer, 'docs', 'english')
    
    def is_persian(self, text: str) -> bool:
        """Check if text is Persian (30% threshold)"""
        if not text:
            return False
        persian_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        return persian_chars > len(text) * 0.3
    
    def is_clean_english(self, text: str) -> bool:
        """Check if text is clean English"""
        if not text:
            return False
        # Remove common punctuation
        clean_text = re.sub(r'[^\w\s]', '', text)
        # Check if mostly alphabetic
        alpha_chars = sum(1 for char in clean_text if char.isalpha())
        return alpha_chars > len(clean_text) * 0.7 and not self.is_persian(text)
    
    def generate_smart_response(self, text: str, language: str) -> str:
        """Generate smart contextual response"""
        text_lower = text.lower()
        
        if language == 'persian':
            # Greeting detection
            if any(word in text_lower for word in ['سلام', 'درود', 'صبح بخیر', 'عصر بخیر']):
                responses = ["سلام! چطورید؟", "درود! حالتون چطوره؟", "سلام عزیزم! خوش اومدید"]
                return random.choice(responses)
            
            # Thanks detection
            elif any(word in text_lower for word in ['ممنون', 'مرسی', 'تشکر', 'سپاس']):
                responses = ["خواهش می‌کنم! 😊", "قابلی نداره!", "خوشحالم که کمک کردم"]
                return random.choice(responses)
            
            # Question detection
            elif '؟' in text or any(word in text_lower for word in ['چی', 'چه', 'کی', 'کجا', 'چرا', 'چطور']):
                responses = ["سوال جالبیه! نظرتون چیه؟", "این موضوع رو بیشتر بررسی کنیم", "می‌تونید بیشتر توضیح بدید؟"]
                return random.choice(responses)
            
            # Goodbye detection
            elif any(word in text_lower for word in ['خداحافظ', 'بای', 'فعلاً']):
                responses = ["خداحافظ! مراقب خودت باش", "بای! روز خوبی داشته باشید", "فعلاً! امیدوارم دوباره ببینمت"]
                return random.choice(responses)
            
            # Positive feedback
            elif any(word in text_lower for word in ['عالی', 'خوب', 'بهترین', 'فوق‌العاده']):
                responses = ["خوشحالم که راضی هستید!", "ممنون از نظر خوبتون", "حمایتتون انگیزه‌بخشه"]
                return random.choice(responses)
            
            # Default Persian response
            else:
                responses = ["جالبه! می‌تونید بیشتر بگید؟", "درباره این موضوع بیشتر فکر کنم", "نظرتون رو می‌تونید شرح بدید؟"]
                return random.choice(responses)
                
        else:  # English
            # Greeting detection
            if any(word in text_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good evening']):
                responses = ["Hello! How are you?", "Hi there! What's up?", "Hey! Nice to meet you!"]
                return random.choice(responses)
            
            # Thanks detection
            elif any(word in text_lower for word in ['thank', 'thanks', 'appreciate', 'grateful']):
                responses = ["You're welcome! 😊", "Happy to help!", "Glad I could assist!"]
                return random.choice(responses)
            
            # Question detection
            elif '?' in text or any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
                responses = ["That's a great question! What do you think?", "Interesting! Could you elaborate?", "Let me think about that..."]
                return random.choice(responses)
            
            # Goodbye detection
            elif any(word in text_lower for word in ['goodbye', 'bye', 'see you', 'farewell']):
                responses = ["Goodbye! Take care!", "Bye! Have a great day!", "See you later!"]
                return random.choice(responses)
            
            # Positive feedback
            elif any(word in text_lower for word in ['great', 'awesome', 'excellent', 'perfect', 'amazing']):
                responses = ["Thanks! I'm glad you liked it!", "Appreciate the positive feedback!", "That means a lot!"]
                return random.choice(responses)
            
            # Default English response
            else:
                responses = ["Interesting! Tell me more.", "I'd like to hear your thoughts on this.", "Could you provide more details?"]
                return random.choice(responses)
    
    def calculate_quality_score(self, input_text: str, response_text: str) -> float:
        """Calculate quality score for conversation"""
        score = 1.0
        
        # Length penalty
        if len(input_text) < 3 or len(response_text) < 3:
            score -= 0.4
        if len(input_text) > 200 or len(response_text) > 200:
            score -= 0.2
        
        # Content quality
        bad_words = ['error', 'exception', 'traceback', 'cuusers', 'launcher', 'occurred']
        if any(word in input_text.lower() for word in bad_words):
            score -= 0.5
        
        # Conversation flow
        if '?' in input_text and len(response_text) > 10:
            score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def add_conversation(self, input_text: str, response_text: str, source: str, language: str):
        """Add conversation with quality check"""
        # Clean and validate
        input_text = input_text.strip()
        response_text = response_text.strip()
        
        if not input_text or not response_text:
            return
        
        quality_score = self.calculate_quality_score(input_text, response_text)
        
        if quality_score > 0.6:  # Only keep good quality
            conversation = {
                'input': input_text,
                'response': response_text,
                'source': source,
                'language': language,
                'quality': quality_score
            }
            
            self.conversations.append(conversation)
            
            # Also save to database
            self.cursor.execute("""
                INSERT INTO conversations (source, language, input_text, response_text, quality_score)
                VALUES (?, ?, ?, ?, ?)
            """, (source, language, input_text, response_text, quality_score))
    
    def save_all_data(self):
        """Save all collected data to files"""
        print("💾 Saving collected data...")
        
        try:
            # Filter high quality conversations
            high_quality = [conv for conv in self.conversations if conv['quality'] > 0.7]
            
            # Separate by language
            persian_convs = [conv for conv in high_quality if conv['language'] == 'persian']
            english_convs = [conv for conv in high_quality if conv['language'] == 'english']
            
            # Save all collected chats
            with open("conversation_data/collected_chats.json", "w", encoding="utf-8") as f:
                json.dump(high_quality, f, ensure_ascii=False, indent=2)
            
            # Save Persian conversations separately
            if persian_convs:
                with open("conversation_data/collected_persian.json", "w", encoding="utf-8") as f:
                    json.dump(persian_convs, f, ensure_ascii=False, indent=2)
            
            # Save English conversations separately
            if english_convs:
                with open("conversation_data/collected_english.json", "w", encoding="utf-8") as f:
                    json.dump(english_convs, f, ensure_ascii=False, indent=2)
            
            # Update learned patterns for the learning system
            self.update_learned_patterns(high_quality)
            
            # Save collection statistics
            stats = {
                'collection_date': datetime.now().isoformat(),
                'total_collected': len(self.conversations),
                'high_quality': len(high_quality),
                'persian_count': len(persian_convs),
                'english_count': len(english_convs),
                'sources': list(set(conv['source'] for conv in self.conversations)),
                'average_quality': sum(conv['quality'] for conv in self.conversations) / len(self.conversations) if self.conversations else 0
            }
            
            with open("conversation_data/collection_stats.json", "w", encoding="utf-8") as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            # Commit database changes
            self.conn.commit()
            
            print(f"✅ Saved {len(high_quality)} high-quality conversations!")
            print(f"📊 Persian: {len(persian_convs)}, English: {len(english_convs)}")
            print(f"📈 Average quality score: {stats['average_quality']:.2f}")
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def update_learned_patterns(self, conversations: List[Dict]):
        """Update learned patterns for the learning system"""
        patterns = {
            "persian_greeting": [],
            "persian_question": [],
            "persian_thanks": [],
            "persian_goodbye": [],
            "english_greeting": [],
            "english_question": [],
            "english_thanks": [],
            "english_goodbye": []
        }
        
        for conv in conversations:
            input_text = conv['input'].lower()
            language = conv['language']
            
            # Categorize conversations
            category = None
            if language == 'persian':
                if any(word in input_text for word in ['سلام', 'درود', 'صبح']):
                    category = 'persian_greeting'
                elif '؟' in conv['input'] or any(word in input_text for word in ['چی', 'چه', 'کی']):
                    category = 'persian_question'
                elif any(word in input_text for word in ['ممنون', 'مرسی', 'تشکر']):
                    category = 'persian_thanks'
                elif any(word in input_text for word in ['خداحافظ', 'بای']):
                    category = 'persian_goodbye'
            else:  # English
                if any(word in input_text for word in ['hello', 'hi', 'hey']):
                    category = 'english_greeting'
                elif '?' in conv['input'] or any(word in input_text for word in ['what', 'how', 'why']):
                    category = 'english_question'
                elif any(word in input_text for word in ['thank', 'thanks']):
                    category = 'english_thanks'
                elif any(word in input_text for word in ['goodbye', 'bye']):
                    category = 'english_goodbye'
            
            if category:
                patterns[category].append({
                    "input": conv['input'],
                    "response": conv['response'],
                    "frequency": 1
                })
        
        # Save updated patterns
        with open("conversation_data/learned_patterns.json", "w", encoding="utf-8") as f:
            json.dump(patterns, f, ensure_ascii=False, indent=2)
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    """Main execution function"""
    print("🤖 Advanced Data Collection Agent Starting...")
    print("=" * 60)
    
    agent = AutoDataCollectionAgent()
    
    try:
        agent.run_complete_collection()
        print("\n" + "=" * 60)
        print("🎉 Data collection completed successfully!")
        print("📁 Check conversation_data/ folder for results")
        print("🔍 Files created:")
        print("   - collected_chats.json (all high-quality chats)")
        print("   - quality_persian_chats.json (manual Persian samples)")
        print("   - learned_patterns.json (categorized for learning)")
        print("   - collection_stats.json (statistics)")
        print("   - collected_data.db (SQLite database)")
        
    except Exception as e:
        print(f"❌ Error during collection: {e}")
    finally:
        agent.close()

if __name__ == "__main__":
    main()

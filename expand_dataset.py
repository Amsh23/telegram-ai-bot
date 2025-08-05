#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Quick Data Expander
Quickly expand the existing conversation dataset with more variety
"""

import json
import random
from datetime import datetime

def expand_conversation_dataset():
    """🎯 Expand existing conversations with more variety and contexts"""
    
    # Load existing conversations
    try:
        with open('conversation_data/collected_chats.json', 'r', encoding='utf-8') as f:
            existing_convs = json.load(f)
    except:
        existing_convs = []
    
    print(f"📊 Current conversations: {len(existing_convs)}")
    
    # Add more Persian conversations
    new_persian_conversations = [
        # بیشتر احوال‌پرسی
        {"input": "حالت خوبه؟", "response": "آره ممنون، تو چطوری؟", "source": "social", "language": "persian", "quality": 0.95},
        {"input": "چه کار می‌کنی؟", "response": "مشغول کارم، تو چه خبر؟", "source": "social", "language": "persian", "quality": 0.95},
        {"input": "کجایی؟", "response": "خونه‌ام، تو کجایی؟", "source": "social", "language": "persian", "quality": 0.95},
        {"input": "چی شده؟", "response": "هیچی خاصی، همه چی عادیه", "source": "social", "language": "persian", "quality": 0.95},
        {"input": "خبری هست؟", "response": "نه خبر خاصی نیست، شما چه خبر؟", "source": "social", "language": "persian", "quality": 0.95},
        
        # مکالمات روزمره
        {"input": "کی بریم بیرون؟", "response": "هر وقت بخوای، کی راحتی؟", "source": "social", "language": "persian", "quality": 0.9},
        {"input": "فیلم جدید دیدی؟", "response": "نه هنوز، کدوم فیلم رو می‌گی؟", "source": "social", "language": "persian", "quality": 0.9},
        {"input": "غذا خوردی؟", "response": "نه هنوز، با هم بریم رستوران؟", "source": "social", "language": "persian", "quality": 0.9},
        {"input": "کارت تموم شد؟", "response": "آره تازه تموم کردم، تو چطور؟", "source": "social", "language": "persian", "quality": 0.9},
        {"input": "خسته شدی؟", "response": "یه کم، ولی حالم خوبه", "source": "social", "language": "persian", "quality": 0.9},
        
        # سوالات کاربردی
        {"input": "این چند قیمته؟", "response": "باید بپرسم ببینم، صبر کن", "source": "shopping", "language": "persian", "quality": 0.9},
        {"input": "تخفیف هست؟", "response": "بله، ۲۰ درصد تخفیف داریم", "source": "shopping", "language": "persian", "quality": 0.9},
        {"input": "کی می‌رسه؟", "response": "احتمالاً فردا می‌رسه", "source": "shopping", "language": "persian", "quality": 0.9},
        {"input": "رنگ دیگه‌ای هست؟", "response": "آره، آبی و سفید هم داریم", "source": "shopping", "language": "persian", "quality": 0.9},
        {"input": "گارانتی داره؟", "response": "بله، ۲ سال گارانتی داره", "source": "shopping", "language": "persian", "quality": 0.9},
        
        # مکالمات کاری
        {"input": "جلسه کی هست؟", "response": "فردا ساعت ۱۰ صبح", "source": "work", "language": "persian", "quality": 0.9},
        {"input": "پروژه چطور پیش میره؟", "response": "خوب پیش میره، تقریباً ۸۰ درصد تموم شده", "source": "work", "language": "persian", "quality": 0.9},
        {"input": "کمک می‌خوای؟", "response": "ممنون، اگه وقت داری خیلی عالی میشه", "source": "work", "language": "persian", "quality": 0.9},
        {"input": "ددلاین کیه؟", "response": "آخر هفته باید تحویل بدیم", "source": "work", "language": "persian", "quality": 0.9},
        {"input": "مشکلی پیش اومده؟", "response": "نه خوشبختانه همه چی روبراهه", "source": "work", "language": "persian", "quality": 0.9},
        
        # مکالمات آموزشی
        {"input": "این چجوری کار می‌کنه؟", "response": "خیلی ساده‌ست، بگو تا توضیح بدم", "source": "education", "language": "persian", "quality": 0.9},
        {"input": "مثال بزن", "response": "مثلاً فرض کن می‌خوای...", "source": "education", "language": "persian", "quality": 0.9},
        {"input": "نفهمیدم", "response": "اشکال نداره، دوباره توضیح می‌دم", "source": "education", "language": "persian", "quality": 0.9},
        {"input": "سخته؟", "response": "اول یه کم سخته، بعد راحت میشه", "source": "education", "language": "persian", "quality": 0.9},
        {"input": "چقدر طول می‌کشه؟", "response": "بستگی داره، ولی حدود یک هفته", "source": "education", "language": "persian", "quality": 0.9},
        
        # مکالمات تکنولوژی
        {"input": "اینترنت قطعه؟", "response": "آره، منم مشکل دارم", "source": "tech", "language": "persian", "quality": 0.9},
        {"input": "آپدیت کردی؟", "response": "نه هنوز، باید آپدیت کنم؟", "source": "tech", "language": "persian", "quality": 0.9},
        {"input": "باگ داره؟", "response": "آره یه باگ کوچیک داره، ولی کار می‌کنه", "source": "tech", "language": "persian", "quality": 0.9},
        {"input": "بک‌آپ گرفتی؟", "response": "نه، حتماً باید بگیرم", "source": "tech", "language": "persian", "quality": 0.9},
        {"input": "پسورد چیه؟", "response": "بهت پیام می‌دم", "source": "tech", "language": "persian", "quality": 0.9},
        
        # احساسات و نظرات
        {"input": "حالم خوش نیست", "response": "چی شده؟ می‌خوای درباره‌ش صحبت کنیم؟", "source": "emotional", "language": "persian", "quality": 0.95},
        {"input": "خیلی خوشحالم", "response": "چه خبر خوبی! بگو ببینم چی شده", "source": "emotional", "language": "persian", "quality": 0.95},
        {"input": "نگرانم", "response": "نگران چی هستی؟ شاید بتونم کمک کنم", "source": "emotional", "language": "persian", "quality": 0.95},
        {"input": "خسته‌ام", "response": "استراحت کن، خودت رو زیاد اذیت نکن", "source": "emotional", "language": "persian", "quality": 0.95},
        {"input": "دلم گرفته", "response": "چرا؟ چی شده که ناراحتی؟", "source": "emotional", "language": "persian", "quality": 0.95},
    ]
    
    # Add more English conversations
    new_english_conversations = [
        # Casual conversations
        {"input": "What's up?", "response": "Not much, just relaxing. How about you?", "source": "casual", "language": "english", "quality": 0.95},
        {"input": "How was your day?", "response": "Pretty good! Had a productive day at work.", "source": "casual", "language": "english", "quality": 0.95},
        {"input": "Any plans for tonight?", "response": "Just staying in and watching a movie. You?", "source": "casual", "language": "english", "quality": 0.95},
        {"input": "Did you see the news?", "response": "Which news are you talking about?", "source": "casual", "language": "english", "quality": 0.95},
        {"input": "How's the weather?", "response": "It's pretty nice today, perfect for a walk.", "source": "casual", "language": "english", "quality": 0.95},
        
        # Work conversations
        {"input": "Meeting's in 10 minutes", "response": "Thanks for the reminder! I'll be right there.", "source": "work", "language": "english", "quality": 0.9},
        {"input": "Can you review this?", "response": "Sure, I'll take a look and get back to you.", "source": "work", "language": "english", "quality": 0.9},
        {"input": "Deadline's tomorrow", "response": "I'm almost done, should be ready by tonight.", "source": "work", "language": "english", "quality": 0.9},
        {"input": "Need any help?", "response": "Actually yes, could you help me with this part?", "source": "work", "language": "english", "quality": 0.9},
        {"input": "Great job on the presentation", "response": "Thank you! I'm glad it went well.", "source": "work", "language": "english", "quality": 0.9},
        
        # Technical conversations
        {"input": "The server is down", "response": "I'll check the logs and restart it.", "source": "tech", "language": "english", "quality": 0.9},
        {"input": "Can you deploy this?", "response": "Sure, I'll deploy it to staging first.", "source": "tech", "language": "english", "quality": 0.9},
        {"input": "Any errors in the logs?", "response": "Let me check... yes, there are a few warnings.", "source": "tech", "language": "english", "quality": 0.9},
        {"input": "Code review needed", "response": "I'll review it this afternoon.", "source": "tech", "language": "english", "quality": 0.9},
        {"input": "Tests are failing", "response": "I'll look into it and fix the issues.", "source": "tech", "language": "english", "quality": 0.9},
        
        # Learning conversations
        {"input": "How does this work?", "response": "Let me explain the basic concept first.", "source": "learning", "language": "english", "quality": 0.9},
        {"input": "Can you give an example?", "response": "Sure! Here's a simple example to illustrate.", "source": "learning", "language": "english", "quality": 0.9},
        {"input": "I don't understand", "response": "No problem, let me try a different approach.", "source": "learning", "language": "english", "quality": 0.9},
        {"input": "Is this correct?", "response": "Yes, that's exactly right! Well done.", "source": "learning", "language": "english", "quality": 0.9},
        {"input": "What's the next step?", "response": "Now that you've got that, let's move on to...", "source": "learning", "language": "english", "quality": 0.9},
        
        # Social conversations
        {"input": "Want to grab lunch?", "response": "Sounds good! Where do you want to go?", "source": "social", "language": "english", "quality": 0.9},
        {"input": "See you tomorrow", "response": "See you! Have a great evening.", "source": "social", "language": "english", "quality": 0.9},
        {"input": "How's your family?", "response": "They're doing well, thanks for asking!", "source": "social", "language": "english", "quality": 0.9},
        {"input": "Nice to meet you", "response": "Nice to meet you too! Welcome to the team.", "source": "social", "language": "english", "quality": 0.9},
        {"input": "Take care", "response": "You too! See you soon.", "source": "social", "language": "english", "quality": 0.9},
    ]
    
    # Combine all new conversations
    all_new_conversations = new_persian_conversations + new_english_conversations
    
    # Add to existing
    all_conversations = existing_convs + all_new_conversations
    
    # Save expanded dataset
    with open('conversation_data/collected_chats.json', 'w', encoding='utf-8') as f:
        json.dump(all_conversations, f, ensure_ascii=False, indent=2)
    
    # Update statistics
    persian_count = len([c for c in all_conversations if c['language'] == 'persian'])
    english_count = len([c for c in all_conversations if c['language'] == 'english'])
    avg_quality = sum(c['quality'] for c in all_conversations) / len(all_conversations)
    
    stats = {
        'expansion_date': datetime.now().isoformat(),
        'total_conversations': len(all_conversations),
        'new_conversations_added': len(all_new_conversations),
        'persian_conversations': persian_count,
        'english_conversations': english_count,
        'average_quality': avg_quality,
        'sources': list(set(c['source'] for c in all_conversations))
    }
    
    with open('conversation_data/expansion_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Dataset Expansion Complete!")
    print(f"📊 Total conversations: {len(all_conversations)}")
    print(f"🆕 New conversations added: {len(all_new_conversations)}")
    print(f"🇮🇷 Persian conversations: {persian_count}")
    print(f"🇺🇸 English conversations: {english_count}")
    print(f"📈 Average quality: {avg_quality:.2f}")
    print(f"📁 Sources: {', '.join(stats['sources'])}")
    
    return len(all_conversations)

if __name__ == "__main__":
    expand_conversation_dataset()

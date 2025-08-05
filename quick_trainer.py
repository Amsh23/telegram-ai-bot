#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Quick Learning Trainer
Fast training with expanded dataset
"""

import json
import numpy as np
from datetime import datetime
from learning_system import LearningSystem

def train_with_expanded_data():
    """🚀 Train learning system with expanded dataset"""
    print("🎓 Starting Quick Learning Training...")
    
    # Initialize learning system
    learning = LearningSystem()
    
    # Load expanded conversations
    try:
        with open('conversation_data/collected_chats.json', 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        print(f"📚 Loaded {len(conversations)} conversations")
    except Exception as e:
        print(f"❌ Error loading conversations: {e}")
        return
    
    # Filter high-quality conversations
    quality_conversations = [c for c in conversations if c.get('quality', 0) >= 0.8]
    print(f"⭐ Found {len(quality_conversations)} high-quality conversations")
    
    # Group by language and source
    persian_convs = [c for c in quality_conversations if c.get('language') == 'persian']
    english_convs = [c for c in quality_conversations if c.get('language') == 'english']
    
    print(f"🇮🇷 Persian: {len(persian_convs)}")
    print(f"🇺🇸 English: {len(english_convs)}")
    
    # Feed conversations to learning system
    learned_count = 0
    
    # Persian conversations
    for conv in persian_convs:
        try:
            learning.learn_from_conversation(
                conv['input'], 
                conv['response'],
                context={'source': conv.get('source', 'unknown')}
            )
            learned_count += 1
            if learned_count % 20 == 0:
                print(f"📖 Processed {learned_count} conversations...")
        except Exception as e:
            print(f"⚠️ Error with conversation: {e}")
    
    # English conversations  
    for conv in english_convs:
        try:
            learning.learn_from_conversation(
                conv['input'], 
                conv['response'],
                context={'source': conv.get('source', 'unknown')}
            )
            learned_count += 1
            if learned_count % 20 == 0:
                print(f"📖 Processed {learned_count} conversations...")
        except Exception as e:
            print(f"⚠️ Error with conversation: {e}")
    
    # Retrain model
    print("🔄 Retraining model...")
    learning.retrain_model()
    
    # Save learning data
    learning.save_data()
    
    # Test some responses
    print("\n🧪 Testing learned responses:")
    
    test_inputs = [
        "سلام چطوری؟",
        "حالت خوبه؟", 
        "چی میخوری؟",
        "Hello how are you?",
        "What's up?",
        "How's it going?"
    ]
    
    for test_input in test_inputs:
        response = learning.generate_learned_response(test_input)
        if response:
            print(f"👤 {test_input}")
            print(f"🤖 {response}")
            print()
    
    # Save training summary
    summary = {
        'training_date': datetime.now().isoformat(),
        'total_conversations_available': len(conversations),
        'quality_conversations_used': len(quality_conversations),
        'conversations_learned': learned_count,
        'persian_conversations': len(persian_convs),
        'english_conversations': len(english_convs),
        'training_completed': True
    }
    
    with open('conversation_data/training_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Training Complete!")
    print(f"📊 Learned from {learned_count} conversations")
    print(f"💾 Model saved and ready to use")
    
    return summary

if __name__ == "__main__":
    train_with_expanded_data()

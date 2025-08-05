#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Dataset Loader for Simple Learning
Load the expanded conversation dataset into simple learning system
"""

import json
from simple_learning import SimpleLearningSystem

def load_dataset_to_simple_learning():
    """📚 Load all conversations into simple learning system"""
    print("🚀 Loading expanded dataset into Simple Learning System...")
    
    # Initialize learning system
    learning = SimpleLearningSystem()
    
    # Load conversations
    try:
        with open('conversation_data/collected_chats.json', 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        print(f"📚 Found {len(conversations)} conversations")
    except Exception as e:
        print(f"❌ Error loading conversations: {e}")
        return
    
    # Filter quality conversations
    quality_conversations = [c for c in conversations if c.get('quality', 0) >= 0.7]
    print(f"⭐ Using {len(quality_conversations)} quality conversations")
    
    # Group by language for balanced learning
    persian_convs = [c for c in quality_conversations if c.get('language') == 'persian']
    english_convs = [c for c in quality_conversations if c.get('language') == 'english']
    
    print(f"🇮🇷 Persian conversations: {len(persian_convs)}")
    print(f"🇺🇸 English conversations: {len(english_convs)}")
    
    # Learn from Persian conversations
    print("🎓 Learning Persian conversations...")
    for i, conv in enumerate(persian_convs):
        try:
            learning.learn_from_conversation(
                conv['input'], 
                conv['response'],
                context={
                    'source': conv.get('source', 'unknown'),
                    'quality': conv.get('quality', 0)
                }
            )
            
            if (i + 1) % 20 == 0:
                print(f"  📖 Processed {i + 1}/{len(persian_convs)} Persian conversations")
                
        except Exception as e:
            print(f"⚠️ Error with Persian conversation {i}: {e}")
    
    # Learn from English conversations
    print("🎓 Learning English conversations...")
    for i, conv in enumerate(english_convs):
        try:
            learning.learn_from_conversation(
                conv['input'], 
                conv['response'],
                context={
                    'source': conv.get('source', 'unknown'),
                    'quality': conv.get('quality', 0)
                }
            )
            
            if (i + 1) % 20 == 0:
                print(f"  📖 Processed {i + 1}/{len(english_convs)} English conversations")
                
        except Exception as e:
            print(f"⚠️ Error with English conversation {i}: {e}")
    
    # Save all learning data
    print("💾 Saving learning data...")
    learning.save_data()
    
    # Get final statistics
    stats = learning.get_stats()
    
    print("\n✅ Dataset Loading Complete!")
    print("📊 Final Statistics:")
    print(f"  📚 Total conversations learned: {stats['total_conversations']}")
    print(f"  🇮🇷 Persian conversations: {stats['persian_conversations']}")
    print(f"  🇺🇸 English conversations: {stats['english_conversations']}")
    print(f"  🎯 Patterns learned: {stats['patterns_learned']}")
    print(f"  🔗 Word associations: {stats['word_associations']}")
    print(f"  🎭 Intent distribution: {stats['intent_distribution']}")
    
    # Test some responses
    print("\n🧪 Testing learned responses:")
    
    test_cases = [
        # Persian tests
        "سلام چطوری؟",
        "حالت خوبه؟",
        "چه کار می‌کنی؟",
        "خسته‌ای؟",
        "کجایی؟",
        "ممنون",
        
        # English tests
        "Hello how are you?",
        "What's up?",
        "How are you doing?",
        "Are you busy?",
        "Where are you?",
        "Thank you"
    ]
    
    for test_input in test_cases:
        response = learning.generate_response(test_input)
        print(f"👤 {test_input}")
        print(f"🤖 {response}")
        print()
    
    # Save test results
    test_results = {
        'test_date': learning.conversations[-1]['timestamp'] if learning.conversations else None,
        'dataset_stats': stats,
        'test_cases': [
            {'input': test_input, 'output': learning.generate_response(test_input)}
            for test_input in test_cases
        ]
    }
    
    with open('conversation_data/simple_learning_test.json', 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print("✅ All done! Simple learning system is trained and ready.")
    return stats

if __name__ == "__main__":
    load_dataset_to_simple_learning()

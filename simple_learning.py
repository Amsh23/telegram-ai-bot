#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Simple Learning System
Fast learning without heavy dependencies
"""

import json
import re
import random
from datetime import datetime
from collections import defaultdict, Counter
import os
import logging

class SimpleLearningSystem:
    """🧠 Simple but effective learning system"""
    
    def __init__(self):
        self.setup_logging()
        self.conversations = []
        self.patterns = defaultdict(list)
        self.word_associations = defaultdict(Counter)
        self.response_templates = {
            'persian': {
                'greeting': ['سلام!', 'درود!', 'چطوری؟', 'سلام عزیز'],
                'question': ['جالبه!', 'خوب پرسیدی', 'بذار فکر کنم', 'سوال جالبیه'],
                'positive': ['عالیه!', 'خوشحالم', 'آفرین', 'چه خوب'],
                'negative': ['متأسفم', 'ناراحت شدم', 'امیدوارم بهتر بشه', 'صبر کن']
            },
            'english': {
                'greeting': ['Hello!', 'Hi there!', 'How are you?', 'Nice to meet you!'],
                'question': ['Interesting!', 'Good question', 'Let me think', 'That\'s interesting'],
                'positive': ['Great!', 'Awesome!', 'That\'s wonderful', 'I\'m happy'],
                'negative': ['Sorry to hear', 'That\'s sad', 'Hope it gets better', 'I understand']
            }
        }
        self.load_data()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def load_data(self):
        """📚 Load existing learning data"""
        try:
            if os.path.exists('conversation_data/simple_learning.json'):
                with open('conversation_data/simple_learning.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversations = data.get('conversations', [])
                    self.patterns = defaultdict(list, data.get('patterns', {}))
                    
                    # Rebuild word associations
                    for conv in self.conversations:
                        self.update_word_associations(conv['input'], conv['response'])
                        
                self.logger.info(f"📚 Loaded {len(self.conversations)} conversations")
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
    
    def save_data(self):
        """💾 Save learning data"""
        try:
            os.makedirs('conversation_data', exist_ok=True)
            data = {
                'conversations': self.conversations,
                'patterns': dict(self.patterns),
                'last_updated': datetime.now().isoformat()
            }
            
            with open('conversation_data/simple_learning.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")
    
    def detect_language(self, text):
        """🌍 Detect if text is Persian or English"""
        persian_chars = len(re.findall(r'[\u0600-\u06FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if persian_chars > english_chars:
            return 'persian'
        else:
            return 'english'
    
    def detect_intent(self, text):
        """🎯 Detect intent of message"""
        text_lower = text.lower()
        
        # Greeting patterns
        greeting_patterns = [
            r'سلام|درود|صبح بخیر|ظهر بخیر|عصر بخیر|شب بخیر',
            r'hello|hi|good morning|good afternoon|good evening|hey'
        ]
        
        # Question patterns
        question_patterns = [
            r'\?|چی|چه|کی|کجا|چرا|چطور|کدام',
            r'what|when|where|why|how|which|who'
        ]
        
        # Check patterns
        for pattern in greeting_patterns:
            if re.search(pattern, text_lower):
                return 'greeting'
        
        for pattern in question_patterns:
            if re.search(pattern, text_lower):
                return 'question'
        
        # Sentiment detection
        positive_words = ['خوب', 'عالی', 'ممنون', 'مرسی', 'خوشحال', 'good', 'great', 'thanks', 'happy', 'nice']
        negative_words = ['بد', 'ناراحت', 'غمگین', 'متأسف', 'bad', 'sad', 'sorry', 'upset', 'angry']
        
        for word in positive_words:
            if word in text_lower:
                return 'positive'
        
        for word in negative_words:
            if word in text_lower:
                return 'negative'
        
        return 'general'
    
    def clean_text(self, text):
        """🧹 Clean and normalize text"""
        # Remove extra spaces
        text = ' '.join(text.split())
        
        # Remove special characters but keep Persian/English/numbers/basic punctuation
        text = re.sub(r'[^\u0600-\u06FFa-zA-Z0-9\s\.\!\?\،\؟]', '', text)
        
        return text.strip()
    
    def update_word_associations(self, input_text, response_text):
        """🔗 Update word associations for better responses"""
        input_words = self.clean_text(input_text).split()
        response_words = self.clean_text(response_text).split()
        
        for input_word in input_words:
            if len(input_word) > 2:  # Only meaningful words
                for response_word in response_words:
                    if len(response_word) > 2:
                        self.word_associations[input_word][response_word] += 1
    
    def learn_from_conversation(self, input_text, response_text, context=None):
        """🎓 Learn from a conversation"""
        try:
            # Clean texts
            clean_input = self.clean_text(input_text)
            clean_response = self.clean_text(response_text)
            
            if not clean_input or not clean_response:
                return
            
            # Detect language and intent
            language = self.detect_language(clean_input)
            intent = self.detect_intent(clean_input)
            
            # Create conversation record
            conversation = {
                'input': clean_input,
                'response': clean_response,
                'language': language,
                'intent': intent,
                'timestamp': datetime.now().isoformat(),
                'context': context or {}
            }
            
            # Add to conversations
            self.conversations.append(conversation)
            
            # Add to patterns
            pattern_key = f"{language}_{intent}"
            self.patterns[pattern_key].append({
                'input': clean_input,
                'response': clean_response
            })
            
            # Limit pattern storage
            if len(self.patterns[pattern_key]) > 50:
                self.patterns[pattern_key] = self.patterns[pattern_key][-50:]
            
            # Update word associations
            self.update_word_associations(clean_input, clean_response)
            
            # Limit total conversations
            if len(self.conversations) > 1000:
                self.conversations = self.conversations[-1000:]
            
        except Exception as e:
            self.logger.error(f"Error learning from conversation: {e}")
    
    def find_similar_input(self, input_text, language):
        """🔍 Find similar inputs for pattern matching"""
        clean_input = self.clean_text(input_text)
        input_words = set(clean_input.lower().split())
        
        best_match = None
        best_score = 0
        
        for conv in self.conversations:
            if conv['language'] == language:
                conv_words = set(conv['input'].lower().split())
                
                # Calculate similarity (Jaccard index)
                intersection = len(input_words & conv_words)
                union = len(input_words | conv_words)
                
                if union > 0:
                    similarity = intersection / union
                    if similarity > best_score and similarity > 0.3:  # Minimum similarity
                        best_score = similarity
                        best_match = conv
        
        return best_match, best_score
    
    def generate_response(self, input_text):
        """🤖 Generate response based on learned patterns"""
        try:
            clean_input = self.clean_text(input_text)
            language = self.detect_language(clean_input)
            intent = self.detect_intent(clean_input)
            
            # Try pattern-based response first
            pattern_key = f"{language}_{intent}"
            if pattern_key in self.patterns and self.patterns[pattern_key]:
                # Find best matching pattern
                similar_conv, score = self.find_similar_input(clean_input, language)
                if similar_conv and score > 0.5:
                    return similar_conv['response']
                
                # Use random pattern response
                pattern_responses = self.patterns[pattern_key]
                return random.choice(pattern_responses)['response']
            
            # Try word association response
            input_words = clean_input.split()
            response_words = []
            
            for word in input_words:
                if word in self.word_associations:
                    # Get most common associated words
                    common_words = self.word_associations[word].most_common(3)
                    if common_words:
                        response_words.extend([w[0] for w in common_words])
            
            if response_words:
                # Create response from associated words
                response = ' '.join(response_words[:5])  # Limit length
                if len(response) > 5:
                    return response
            
            # Fallback to template responses
            if intent in self.response_templates[language]:
                templates = self.response_templates[language][intent]
                return random.choice(templates)
            
            # Final fallback
            default_responses = {
                'persian': ['جالبه!', 'متوجه شدم', 'ادامه بده', 'خوب گفتی'],
                'english': ['Interesting!', 'I see', 'Tell me more', 'That\'s good']
            }
            
            return random.choice(default_responses[language])
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "متوجه نشدم / I don't understand"
    
    def get_stats(self):
        """📊 Get learning statistics"""
        persian_count = len([c for c in self.conversations if c['language'] == 'persian'])
        english_count = len([c for c in self.conversations if c['language'] == 'english'])
        
        intent_counts = Counter(c['intent'] for c in self.conversations)
        
        return {
            'total_conversations': len(self.conversations),
            'persian_conversations': persian_count,
            'english_conversations': english_count,
            'patterns_learned': len(self.patterns),
            'word_associations': len(self.word_associations),
            'intent_distribution': dict(intent_counts)
        }

def test_simple_learning():
    """🧪 Test the simple learning system"""
    learning = SimpleLearningSystem()
    
    # Test with some conversations
    test_data = [
        ("سلام چطوری؟", "سلام! خوبم ممنون، تو چطوری؟"),
        ("خوبم", "خوشحالم که خوبی"),
        ("حالت خوبه؟", "آره ممنون، خودت چطوری؟"),
        ("Hello how are you?", "Hi! I'm doing well, thanks for asking"),
        ("I'm good", "That's great to hear!"),
        ("What's up?", "Not much, just chatting with you")
    ]
    
    # Learn from test data
    print("🎓 Learning from test conversations...")
    for input_text, response in test_data:
        learning.learn_from_conversation(input_text, response)
    
    # Test responses
    print("\n🧪 Testing responses:")
    test_inputs = [
        "سلام",
        "حالت چطوره؟", 
        "خوب هستم",
        "Hi there",
        "How are you doing?",
        "I'm fine"
    ]
    
    for test_input in test_inputs:
        response = learning.generate_response(test_input)
        print(f"👤 {test_input}")
        print(f"🤖 {response}")
        print()
    
    # Show stats
    stats = learning.get_stats()
    print("📊 Learning Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Save data
    learning.save_data()
    print("\n💾 Learning data saved!")

if __name__ == "__main__":
    test_simple_learning()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 AI Bot Test Suite
Test all AI components and performance
"""

import time
import json
from datetime import datetime
from telegram_ai_bot import *

def test_ai_components():
    """Test all AI components"""
    print("\n" + "="*60)
    print("🧪 AI BOT TEST SUITE")
    print("="*60)
    
    # Initialize components
    print("\n🔧 Initializing AI components...")
    
    try:
        ocr = AdvancedOCR()
        analyzer = AIMessageAnalyzer()
        response_generator = SmartResponseGenerator()
        print("✅ All components initialized successfully")
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Test messages
    test_messages = [
        "سلام! چطوری؟ حالت خوبه؟",
        "ممنون از کمکت! خیلی عالی بود",
        "چرا این کار نمیکنه؟ مشکل چیه؟",
        "میخوام کمک بگیرم برای این مساله",
        "Hello! How are you doing today?",
        "Thanks for your help! It was great",
        "What time is it now? I need to know",
        "Goodbye! See you later!",
        "This is just random interface text with timestamps 12:34 PM",
        "* J | 12:52PM a e Video 2S shd be catty gl alas 12",  # Interface noise
    ]
    
    print(f"\n📝 Testing {len(test_messages)} messages...")
    print("-" * 60)
    
    results = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🔍 Test {i}: '{message}'")
        
        # AI Analysis
        start_time = time.time()
        analysis = analyzer.analyze_message_comprehensive(message)
        analysis_time = time.time() - start_time
        
        # Response Generation
        response_start = time.time()
        response = response_generator.generate_contextual_response(analysis)
        response_time = time.time() - response_start
        
        # Results
        is_real = analysis.get('is_real_message', {}).get('is_real', False)
        intent = analysis.get('intent', {}).get('intent', 'unknown')
        confidence = analysis.get('intent', {}).get('confidence', 0)
        language = max(analysis.get('language', {}), key=analysis.get('language', {}).get) if analysis.get('language') else 'unknown'
        sentiment = analysis.get('sentiment', {}).get('label', 'NEUTRAL')
        
        print(f"   🌍 Language: {language}")
        print(f"   🎯 Intent: {intent} (confidence: {confidence:.2f})")
        print(f"   🎭 Sentiment: {sentiment}")
        print(f"   ✅ Real Message: {'Yes' if is_real else 'No'}")
        print(f"   ⏱️ Analysis Time: {analysis_time:.3f}s")
        print(f"   💬 Response: {response if response else 'No response'}")
        print(f"   ⏱️ Response Time: {response_time:.3f}s")
        
        results.append({
            'message': message,
            'is_real': is_real,
            'intent': intent,
            'confidence': confidence,
            'language': language,
            'sentiment': sentiment,
            'response': response,
            'analysis_time': analysis_time,
            'response_time': response_time
        })
    
    # Summary Statistics
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total_messages = len(results)
    real_messages = sum(1 for r in results if r['is_real'])
    responded_messages = sum(1 for r in results if r['response'])
    avg_analysis_time = sum(r['analysis_time'] for r in results) / total_messages
    avg_response_time = sum(r['response_time'] for r in results) / total_messages
    
    print(f"📨 Total Messages: {total_messages}")
    print(f"✅ Real Messages Detected: {real_messages} ({real_messages/total_messages*100:.1f}%)")
    print(f"💬 Responses Generated: {responded_messages} ({responded_messages/total_messages*100:.1f}%)")
    print(f"⏱️ Average Analysis Time: {avg_analysis_time:.3f}s")
    print(f"⏱️ Average Response Time: {avg_response_time:.3f}s")
    
    # Language Analysis
    persian_count = sum(1 for r in results if r['language'] == 'persian')
    english_count = sum(1 for r in results if r['language'] == 'english')
    mixed_count = sum(1 for r in results if r['language'] == 'mixed')
    
    print(f"\n🌍 Language Distribution:")
    print(f"   فارسی: {persian_count}")
    print(f"   English: {english_count}")
    print(f"   Mixed: {mixed_count}")
    
    # Intent Analysis
    intents = {}
    for r in results:
        intent = r['intent']
        if intent in intents:
            intents[intent] += 1
        else:
            intents[intent] = 1
    
    print(f"\n🎯 Intent Distribution:")
    for intent, count in sorted(intents.items(), key=lambda x: x[1], reverse=True):
        print(f"   {intent}: {count}")
    
    # Performance Rating
    print(f"\n🏆 PERFORMANCE RATING")
    print("-" * 30)
    
    # Accuracy Score
    expected_real = [True, True, True, True, True, True, True, True, False, False]
    actual_real = [r['is_real'] for r in results]
    accuracy = sum(1 for e, a in zip(expected_real, actual_real) if e == a) / len(expected_real)
    
    print(f"🎯 Detection Accuracy: {accuracy*100:.1f}%")
    
    # Speed Score
    if avg_analysis_time < 0.1:
        speed_score = "⚡ EXCELLENT"
    elif avg_analysis_time < 0.2:
        speed_score = "🚀 VERY GOOD"
    elif avg_analysis_time < 0.5:
        speed_score = "✅ GOOD"
    else:
        speed_score = "⚠️ NEEDS IMPROVEMENT"
    
    print(f"⚡ Speed Performance: {speed_score}")
    
    # Overall Score
    overall_score = (accuracy * 0.6) + ((1 - min(avg_analysis_time, 1)) * 0.4)
    if overall_score > 0.9:
        overall_rating = "🏆 EXCELLENT"
    elif overall_score > 0.8:
        overall_rating = "🥈 VERY GOOD"
    elif overall_score > 0.7:
        overall_rating = "🥉 GOOD"
    else:
        overall_rating = "⚠️ NEEDS IMPROVEMENT"
    
    print(f"🏆 Overall Rating: {overall_rating} ({overall_score*100:.1f}%)")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ai_test_results_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'summary': {
                'total_messages': total_messages,
                'real_messages': real_messages,
                'responded_messages': responded_messages,
                'accuracy': accuracy,
                'avg_analysis_time': avg_analysis_time,
                'avg_response_time': avg_response_time,
                'overall_score': overall_score
            },
            'results': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Detailed results saved: {filename}")
    print("="*60)

def test_ocr_engines():
    """Test OCR engines performance"""
    print("\n🔍 Testing OCR Engines...")
    
    # This would require actual images to test
    # For now, just verify initialization
    try:
        ocr = AdvancedOCR()
        print("✅ Tesseract OCR: Ready")
        
        if ocr.easyocr_reader:
            print("✅ EasyOCR: Ready")
        else:
            print("⚠️ EasyOCR: Not available")
    except Exception as e:
        print(f"❌ OCR Test Failed: {e}")

def performance_benchmark():
    """Benchmark AI performance"""
    print("\n⚡ Performance Benchmark...")
    
    analyzer = AIMessageAnalyzer()
    
    # Benchmark message analysis
    test_text = "سلام! چطوری؟ میخوام کمک بگیرم در مورد این مساله"
    
    times = []
    for i in range(100):
        start = time.time()
        analyzer.analyze_message_comprehensive(test_text)
        end = time.time()
        times.append(end - start)
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"📊 Analysis Performance (100 runs):")
    print(f"   Average: {avg_time:.4f}s")
    print(f"   Minimum: {min_time:.4f}s")
    print(f"   Maximum: {max_time:.4f}s")
    
    # Performance rating
    if avg_time < 0.05:
        rating = "🚀 BLAZING FAST"
    elif avg_time < 0.1:
        rating = "⚡ VERY FAST"
    elif avg_time < 0.2:
        rating = "✅ FAST"
    elif avg_time < 0.5:
        rating = "👍 ACCEPTABLE"
    else:
        rating = "⚠️ SLOW"
    
    print(f"🏆 Performance Rating: {rating}")

if __name__ == "__main__":
    print("🚀 Starting AI Bot Test Suite...")
    
    try:
        test_ai_components()
        test_ocr_engines()
        performance_benchmark()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n👋 Test suite finished!")

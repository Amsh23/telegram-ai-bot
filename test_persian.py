# -*- coding: utf-8 -*-
"""
Test script for Persian text detection
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_auto_reply import TelegramAutoReply
from config import *

def test_persian_text_detection():
    """Test Persian text detection with sample messages"""
    
    bot = TelegramAutoReply()
    bot.debug_mode = True
    
    # Test messages
    test_messages = [
        "سلام چطوری؟",
        "مرسی داداش",
        "این چیه؟",
        "باشه اوکی",
        "تست فارسی",
        "Hello how are you?",
        "KAMHEREI314 : last seen recently",
        "Video Call Button",
        "1:50 PM",
        "متن فارسی کوتاه",
        "یک پیام ساده",
    ]
    
    print("🧪 Testing Persian Text Detection")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Testing: '{message}'")
        
        # Test if it seems like a user message
        is_user_msg = bot.seems_like_user_message(message)
        print(f"   ✅ Seems like user message: {is_user_msg}")
        
        # Test filtering
        filtered = bot.filter_interface_elements(message)
        print(f"   🔍 After filtering: '{filtered}'")
        
        # Test analysis
        if filtered:
            response = bot.analyze_message(filtered)
            if response:
                print(f"   💬 Would respond: '{response}'")
            else:
                print(f"   🤐 No response generated")
        
        print("-" * 30)

if __name__ == "__main__":
    test_persian_text_detection()

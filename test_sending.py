# -*- coding: utf-8 -*-
"""
Test Persian message sending
"""

import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_auto_reply import TelegramAutoReply
from config import *

def test_persian_sending():
    """Test sending Persian messages"""
    
    bot = TelegramAutoReply()
    
    # Test messages
    test_messages = [
        "سلام! این یک تست است",
        "ممنون از شما",
        "Hello English test",
        "متن فارسی با emoji 😊",
    ]
    
    print("🧪 Testing Persian Message Sending")
    print("=" * 50)
    print("⚠️ Make sure Telegram is open and input field is focused!")
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Testing message: '{message}'")
        
        choice = input("Send this message? (y/n/q): ").lower()
        
        if choice == 'q':
            break
        elif choice == 'y':
            try:
                bot.send_message(message)
                print("✅ Message sent!")
                time.sleep(2)  # Wait between messages
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("⏭️ Skipped")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    test_persian_sending()

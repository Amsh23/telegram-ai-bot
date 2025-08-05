#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 Clean Corrupted Learning Data
"""

import json
import os
from datetime import datetime

def clean_all_corrupted_data():
    """Clean all corrupted learning data"""
    try:
        print("🧹 Cleaning corrupted learning data...")
        
        # Clean conversations.json - keep only valid entries
        valid_conversations = []
        
        if os.path.exists("conversation_data/conversations.json"):
            with open("conversation_data/conversations.json", "r", encoding="utf-8") as f:
                conversations = json.load(f)
            
            for conv in conversations:
                # Keep only clean Persian/English messages
                msg = conv.get("user_message", "")
                if (len(msg) < 50 and  # Short messages
                    not any(word in msg.lower() for word in ["error", "occurred", "launcher", "pm", "cuusers"]) and
                    (any(char in msg for char in "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی") or
                     msg.replace(" ", "").replace("،", "").replace("؟", "").isalpha())):  # Pure alphabetic
                    valid_conversations.append(conv)
        
        # Save clean conversations
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
        
        print(f"✅ Cleaned data! Kept {len(valid_conversations)} valid conversations")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning data: {e}")
        return False

if __name__ == "__main__":
    clean_all_corrupted_data()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 Learning System Manager & Viewer
مدیریت و مشاهده داده‌های یادگیری ربات
"""

import json
import os
from datetime import datetime
from learning_system import ConversationLearner

class LearningViewer:
    """👁️ نمایش و تحلیل داده‌های یادگیری"""
    
    def __init__(self):
        self.learner = ConversationLearner()
        
    def show_conversation_history(self, limit=20):
        """📚 نمایش تاریخچه مکالمات"""
        print("\n" + "="*70)
        print("📚 CONVERSATION HISTORY")
        print("="*70)
        
        conversations = self.learner.conversations[-limit:]
        
        if not conversations:
            print("❌ No conversations found!")
            return
        
        for i, conv in enumerate(conversations, 1):
            timestamp = datetime.fromisoformat(conv['timestamp']).strftime('%Y-%m-%d %H:%M')
            user_msg = conv['user_message'][:50] + "..." if len(conv['user_message']) > 50 else conv['user_message']
            bot_resp = conv['bot_response'][:50] + "..." if len(conv['bot_response']) > 50 else conv['bot_response']
            
            print(f"\n{i}. [{timestamp}]")
            print(f"   👤 User: {user_msg}")
            print(f"   🤖 Bot:  {bot_resp}")
            print(f"   🎯 Intent: {conv['user_features']['sentiment']} | Lang: {conv['user_features']['language']}")
    
    def show_learned_patterns(self):
        """🎯 نمایش الگوهای یادگیری شده"""
        print("\n" + "="*70)
        print("🎯 LEARNED RESPONSE PATTERNS")
        print("="*70)
        
        if not self.learner.response_patterns:
            print("❌ No patterns learned yet!")
            return
        
        for pattern_key, responses in self.learner.response_patterns.items():
            print(f"\n📋 Pattern: {pattern_key}")
            print(f"   📊 Responses: {len(responses)}")
            
            # Show some example responses
            for i, resp in enumerate(responses[:3], 1):
                print(f"   {i}. '{resp['response'][:60]}...'")
            
            if len(responses) > 3:
                print(f"   ... and {len(responses) - 3} more")
    
    def show_user_style_analysis(self):
        """👤 نمایش تحلیل سبک کاربر"""
        print("\n" + "="*70)
        print("👤 USER COMMUNICATION STYLE ANALYSIS")
        print("="*70)
        
        if not self.learner.user_style:
            print("❌ No user style data available!")
            return
        
        for style_key, style_data in self.learner.user_style.items():
            print(f"\n📊 Style: {style_key}")
            print(f"   📏 Average Length: {style_data['avg_length']:.1f} chars")
            print(f"   📝 Message Count: {style_data['count']}")
            
            # Show common words
            common_words = sorted(style_data['common_words'].items(), key=lambda x: x[1], reverse=True)[:10]
            if common_words:
                print(f"   🔤 Common Words:")
                for word, count in common_words:
                    print(f"      • {word}: {count} times")
    
    def show_learning_progress(self):
        """📈 نمایش پیشرفت یادگیری"""
        stats = self.learner.get_learning_stats()
        
        print("\n" + "="*70)
        print("📈 LEARNING PROGRESS REPORT")
        print("="*70)
        print(f"📚 Total Conversations: {stats['total_conversations']}")
        print(f"🎯 Learned Patterns: {stats['learned_patterns']}")
        print(f"👤 User Styles Analyzed: {stats['user_styles']}")
        print(f"📊 Data Quality Score: {stats['data_quality']}%")
        print(f"⏰ Last Update: {stats['last_update']}")
        
        # Learning recommendations
        print(f"\n💡 LEARNING RECOMMENDATIONS:")
        
        if stats['total_conversations'] < 10:
            print("   🎯 Need more conversations to improve learning (min: 10)")
        elif stats['total_conversations'] < 50:
            print("   📈 Good start! More conversations will improve responses")
        else:
            print("   ✅ Excellent conversation data available!")
        
        if stats['data_quality'] < 50:
            print("   ⚠️ Low data quality - encourage longer, clearer messages")
        elif stats['data_quality'] < 80:
            print("   📊 Good data quality - system learning effectively")
        else:
            print("   🌟 Excellent data quality - optimal learning conditions!")
    
    def export_learning_data(self, filename=None):
        """💾 صادر کردن داده‌های یادگیری"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"learning_export_{timestamp}.json"
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'stats': self.learner.get_learning_stats(),
            'conversations': self.learner.conversations,
            'patterns': self.learner.response_patterns,
            'user_style': dict(self.learner.user_style)
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Learning data exported to: {filename}")
            print(f"📊 Exported {len(self.learner.conversations)} conversations")
            print(f"🎯 Exported {len(self.learner.response_patterns)} patterns")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def clear_learning_data(self):
        """🗑️ پاک کردن داده‌های یادگیری"""
        print("\n⚠️ WARNING: This will delete all learning data!")
        confirm = input("Are you sure? Type 'DELETE' to confirm: ")
        
        if confirm == 'DELETE':
            try:
                # Clear data
                self.learner.conversations = []
                self.learner.response_patterns = {}
                self.learner.user_style = {}
                
                # Save empty data
                self.learner.save_data()
                
                print("✅ All learning data cleared successfully!")
                
            except Exception as e:
                print(f"❌ Clear failed: {e}")
        else:
            print("❌ Operation cancelled")
    
    def interactive_menu(self):
        """🎯 منوی تعاملی"""
        while True:
            print("\n" + "="*70)
            print("🧠 LEARNING SYSTEM MANAGER")
            print("="*70)
            print("1. 📚 View Conversation History")
            print("2. 🎯 View Learned Patterns")
            print("3. 👤 View User Style Analysis")
            print("4. 📈 Show Learning Progress")
            print("5. 💾 Export Learning Data")
            print("6. 🗑️ Clear Learning Data")
            print("7. ❌ Exit")
            print("="*70)
            
            try:
                choice = input("👉 Select option (1-7): ").strip()
                
                if choice == '1':
                    limit = input("Enter number of conversations to show (default 20): ").strip()
                    limit = int(limit) if limit.isdigit() else 20
                    self.show_conversation_history(limit)
                
                elif choice == '2':
                    self.show_learned_patterns()
                
                elif choice == '3':
                    self.show_user_style_analysis()
                
                elif choice == '4':
                    self.show_learning_progress()
                
                elif choice == '5':
                    filename = input("Enter filename (press enter for auto): ").strip()
                    self.export_learning_data(filename if filename else None)
                
                elif choice == '6':
                    self.clear_learning_data()
                
                elif choice == '7':
                    print("👋 Goodbye!")
                    break
                
                else:
                    print("❌ Invalid choice! Please select 1-7.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("\nPress Enter to continue...")

def main():
    """🚀 اجرای برنامه اصلی"""
    print("🧠 Learning System Manager v1.0")
    print("مدیریت و مشاهده داده‌های یادگیری ربات تلگرام")
    
    viewer = LearningViewer()
    viewer.interactive_menu()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 Cleanup Script for Advanced Telegram Responder
Removes old/duplicate files and keeps only essential components
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Clean up old files and keep only essential components"""
    
    print("🧹 CLEANING UP PROJECT FILES")
    print("=" * 50)
    
    # Files to keep (essential components)
    keep_files = {
        # Main system
        'advanced_telegram_responder.py',
        'smart_ocr.py', 
        'simple_learning.py',
        
        # Configuration and setup
        'requirements_advanced.txt',
        'advanced_config.json',
        'github_setup.py',
        
        # Documentation
        'README.md',
        'GITHUB_SETUP_GUIDE.md',
        'LICENSE',
        
        # Git files
        '.gitignore',
        
        # Essential data files
        'conversation_data',  # directory
    }
    
    # Files to remove (old/duplicate versions)
    remove_files = [
        'ultimate_telegram_responder.py',
        'ultimate_telegram_responder_simple.py',
        'telegram_ai_bot.py',
        'telegram_auto_reply.py', 
        'telegram_enhanced_bot.py',
        'enhanced_telegram_bot.py',
        'final_ai_bot.py',
        'simple_smart_bot.py',
        'start_ai_bot.py',
        'install_ai_bot.py',
        'advanced_ocr.py',
        'learning_system.py',
        'auto_data_collector.py',
        'real_website_collector.py',
        'expand_dataset.py',
        'load_dataset.py',
        'quick_trainer.py',
        'quick_start.py',
        'performance_analyzer.py',
        'learning_viewer.py',
        'gui_configurator.py',
        'project_summary.py',
        'test_ai_suite.py',
        'test_persian.py',
        'test_sending.py',
        'test_system.py',
        'final_test.py',
        'clean_corrupted_data.py',
        'config_advanced.py',
        'setup.py',
        
        # Old config files
        'config.py',
        'telegram_config.json',
        
        # Old log files
        'final_ai_bot.log',
        'simple_bot.log',
        'telegram_ai_bot.log',
        'telegram_auto_reply.log',
        'telegram_bot.log',
        
        # Old result files
        'ai_test_results_20250804_193355.json',
        'performance_report.json',
        'release_info.json',
        
        # Old batch files
        'start_bot.bat',
        
        # Old installation guides
        'INSTALL_GUIDE.md',
        'TELEGRAM_AUTO_GUIDE.md',
        'PROJECT_SUMMARY.md',
        
        # Old screenshots
        'debug_screenshot.png',
        'debug_screenshot_processed.png',
        'test_screenshot.png',
        'test_screenshot_processed.png',
    ]
    
    removed_count = 0
    
    # Remove old files
    for filename in remove_files:
        file_path = Path(filename)
        if file_path.exists():
            try:
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                print(f"🗑️ Removed: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {filename}: {e}")
    
    # Clean up __pycache__ directories
    pycache_dirs = list(Path('.').rglob('__pycache__'))
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            print(f"🗑️ Removed: {pycache_dir}")
            removed_count += 1
        except Exception as e:
            print(f"❌ Failed to remove {pycache_dir}: {e}")
    
    # Show final status
    print("\n" + "=" * 50)
    print(f"✅ Cleanup completed!")
    print(f"🗑️ Removed {removed_count} old files/directories")
    
    # Show remaining essential files
    print(f"\n📋 Essential files kept:")
    essential_files = []
    for item in Path('.').iterdir():
        if item.name in keep_files or item.name.startswith('.'):
            essential_files.append(item.name)
    
    for file in sorted(essential_files):
        print(f"   ✅ {file}")
    
    print(f"\n🚀 Project is now clean and ready for GitHub!")
    print("=" * 50)

if __name__ == "__main__":
    cleanup_project()

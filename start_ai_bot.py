#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Telegram Advanced AI Bot Launcher v3.0
Smart launcher with system checks and optimization
"""

import os
import sys
import time
import subprocess
import psutil
from datetime import datetime

class SmartLauncher:
    """🎯 Smart launcher with system optimization"""
    
    def __init__(self):
        self.system_info = self.get_system_info()
        self.requirements_met = True
        
    def print_banner(self):
        """🎨 Print startup banner"""
        print("\n" + "="*70)
        print("🚀 TELEGRAM ADVANCED AI BOT v3.0")
        print("⚡ Powered by TensorFlow & Advanced Machine Learning")
        print("🧠 Smart Persian/English Message Analysis")
        print("="*70)
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💻 System: {self.system_info['os']} | Python {self.system_info['python']}")
        print(f"🧮 RAM: {self.system_info['memory_gb']:.1f}GB | CPU: {self.system_info['cpu_count']} cores")
        print("="*70)
    
    def get_system_info(self):
        """📊 Get system information"""
        memory = psutil.virtual_memory()
        return {
            'os': f"{os.name} {sys.platform}",
            'python': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'memory_gb': memory.total / (1024**3),
            'memory_available_gb': memory.available / (1024**3),
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1)
        }
    
    def check_requirements(self):
        """✅ Check system requirements"""
        print("\n🔍 Checking system requirements...")
        
        checks = []
        
        # Python version
        if sys.version_info >= (3, 8):
            checks.append(("✅", "Python version", f"{sys.version_info.major}.{sys.version_info.minor}+"))
        else:
            checks.append(("❌", "Python version", "Requires Python 3.8+"))
            self.requirements_met = False
        
        # Memory check
        if self.system_info['memory_available_gb'] >= 1.0:
            checks.append(("✅", "Available RAM", f"{self.system_info['memory_available_gb']:.1f}GB"))
        else:
            checks.append(("⚠️", "Available RAM", f"{self.system_info['memory_available_gb']:.1f}GB (Low)"))
        
        # Required packages with their import names
        required_packages = [
            ('tensorflow', 'tensorflow'),
            ('transformers', 'transformers'),
            ('torch', 'torch'),
            ('numpy', 'numpy'),
            ('opencv-python', 'cv2'),
            ('easyocr', 'easyocr'),
            ('pyautogui', 'pyautogui'),
            ('pytesseract', 'pytesseract'),
            ('pyperclip', 'pyperclip'),
            ('scikit-learn', 'sklearn')
        ]
        
        for package_name, import_name in required_packages:
            try:
                __import__(import_name)
                checks.append(("✅", f"Package {package_name}", "Installed"))
            except ImportError:
                checks.append(("❌", f"Package {package_name}", "Missing"))
                self.requirements_met = False
        
        # Display results
        for status, item, result in checks:
            print(f"   {status} {item}: {result}")
        
        return self.requirements_met
    
    def check_tesseract(self):
        """🔍 Check Tesseract installation"""
        print("\n🔍 Checking Tesseract OCR...")
        
        try:
            import pytesseract
            
            # Try to get version
            version = pytesseract.get_tesseract_version()
            print(f"   ✅ Tesseract version: {version}")
            
            # Check languages
            try:
                langs = pytesseract.get_languages()
                if 'fas' in langs and 'eng' in langs:
                    print(f"   ✅ Persian & English languages available")
                else:
                    print(f"   ⚠️ Available languages: {', '.join(langs)}")
            except:
                print(f"   ⚠️ Could not check available languages")
                
            return True
            
        except Exception as e:
            print(f"   ❌ Tesseract error: {e}")
            return False
    
    def optimize_system(self):
        """⚡ Apply system optimizations"""
        print("\n⚡ Applying system optimizations...")
        
        # Set environment variables for optimal performance
        optimizations = [
            ("TF_CPP_MIN_LOG_LEVEL", "2", "Reduce TensorFlow logs"),
            ("OMP_NUM_THREADS", str(min(4, psutil.cpu_count())), "Optimize CPU usage"),
            ("TF_ENABLE_ONEDNN_OPTS", "1", "Enable oneDNN optimizations"),
        ]
        
        for var, value, description in optimizations:
            os.environ[var] = value
            print(f"   ✅ {description}: {var}={value}")
        
        # Memory optimization warning
        if self.system_info['memory_available_gb'] < 2.0:
            print(f"   ⚠️ Low memory detected ({self.system_info['memory_available_gb']:.1f}GB)")
            print(f"   💡 Consider closing other applications for better performance")
    
    def show_menu(self):
        """📋 Show launcher menu"""
        print("\n" + "="*50)
        print("🎯 LAUNCHER MENU")
        print("="*50)
        print("1. 🚀 Start Advanced AI Bot")
        print("2. 🧪 Run AI Test Suite")
        print("3. 🔧 System Diagnostics")
        print("4. 📊 Performance Benchmark")
        print("5. ⚙️ Setup Coordinates")
        print("6. 📖 Help & Documentation")
        print("7. ❌ Exit")
        print("="*50)
        
        try:
            choice = input("👉 Select option (1-7): ").strip()
            return choice
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Exiting...")
            return "7"
        except Exception:
            print("\n❌ Input error, please try again.")
            return ""
    
    def run_bot(self):
        """🚀 Launch the main bot"""
        print("\n🚀 Starting Advanced AI Bot...")
        try:
            from telegram_ai_bot import main
            main()
        except Exception as e:
            print(f"❌ Bot startup failed: {e}")
            input("Press Enter to continue...")
    
    def run_tests(self):
        """🧪 Run test suite"""
        print("\n🧪 Running AI Test Suite...")
        try:
            from test_ai_suite import test_ai_components, performance_benchmark
            test_ai_components()
            performance_benchmark()
        except Exception as e:
            print(f"❌ Test suite failed: {e}")
        input("\nPress Enter to continue...")
    
    def run_diagnostics(self):
        """🔧 Run system diagnostics"""
        print("\n🔧 System Diagnostics")
        print("-" * 40)
        
        # Detailed system info
        print(f"🖥️ Operating System: {self.system_info['os']}")
        print(f"🐍 Python Version: {self.system_info['python']}")
        print(f"🧮 Total RAM: {self.system_info['memory_gb']:.2f} GB")
        print(f"💾 Available RAM: {self.system_info['memory_available_gb']:.2f} GB")
        print(f"⚙️ CPU Cores: {self.system_info['cpu_count']}")
        print(f"📊 CPU Usage: {self.system_info['cpu_percent']:.1f}%")
        
        # Check disk space
        disk = psutil.disk_usage('.')
        print(f"💽 Disk Space: {disk.free / (1024**3):.1f}GB free / {disk.total / (1024**3):.1f}GB total")
        
        # GPU check
        try:
            import tensorflow as tf
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                print(f"🎮 GPU: {len(gpus)} device(s) detected")
            else:
                print(f"🎮 GPU: None detected (using CPU)")
        except:
            print(f"🎮 GPU: Could not check")
        
        input("\nPress Enter to continue...")
    
    def run_benchmark(self):
        """📊 Run performance benchmark"""
        print("\n📊 Performance Benchmark")
        print("-" * 40)
        
        # Import timing test
        modules = ['tensorflow', 'transformers', 'torch', 'opencv-python', 'easyocr']
        
        for module in modules:
            try:
                start = time.time()
                __import__(module.replace('-', '_'))
                end = time.time()
                print(f"   📦 {module}: {(end-start)*1000:.1f}ms")
            except ImportError:
                print(f"   ❌ {module}: Not installed")
        
        # Memory usage after imports
        memory = psutil.virtual_memory()
        print(f"\n💾 Memory usage: {(memory.total - memory.available) / (1024**3):.1f}GB")
        
        input("\nPress Enter to continue...")
    
    def setup_coordinates(self):
        """⚙️ Setup coordinates"""
        print("\n⚙️ Coordinate Setup")
        print("-" * 40)
        print("This will start the coordinate setup process...")
        print("Make sure Telegram Desktop is open!")
        
        try:
            # Import and run coordinate setup
            from telegram_auto_reply import TelegramAutoReply
            bot = TelegramAutoReply()
            bot.setup_coordinates_interactive()
        except Exception as e:
            print(f"❌ Setup failed: {e}")
        
        input("\nPress Enter to continue...")
    
    def show_help(self):
        """📖 Show help information"""
        print("\n📖 Help & Documentation")
        print("=" * 50)
        print("🚀 Advanced AI Telegram Bot v3.0")
        print("\nFeatures:")
        print("• 🧠 AI-powered message analysis")
        print("• 🌍 Persian/English dual language support")
        print("• 🔍 Multi-engine OCR (Tesseract + EasyOCR)")
        print("• 🎯 Intent detection & sentiment analysis")
        print("• ⚡ Real-time performance monitoring")
        print("• 🛡️ Advanced spam & duplicate filtering")
        print("• 🎨 Context-aware response generation")
        
        print("\nRequirements:")
        print("• Python 3.8+")
        print("• 1GB+ RAM available")
        print("• Tesseract OCR installed")
        print("• Telegram Desktop")
        
        print("\nUsage:")
        print("1. Start with option 1 (🚀 Start Advanced AI Bot)")
        print("2. Follow coordinate setup if first time")
        print("3. Bot will monitor and respond automatically")
        print("4. Use Ctrl+C or move mouse to corner to stop")
        
        print("\nTroubleshooting:")
        print("• Run option 3 (🔧 System Diagnostics) for issues")
        print("• Check logs in telegram_ai_bot.log")
        print("• Use option 2 (🧪 Run AI Test Suite) to verify")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """🎯 Main launcher loop"""
        self.print_banner()
        
        # Initial checks
        if not self.check_requirements():
            print("\n❌ System requirements not met!")
            print("Please install missing packages and try again.")
            input("Press Enter to exit...")
            return
        
        self.check_tesseract()
        self.optimize_system()
        
        print("\n✅ System ready for AI Bot!")
        
        # Main menu loop
        while True:
            try:
                choice = self.show_menu()
                
                if not choice or choice == "":
                    continue
                    
                if choice == "1":
                    self.run_bot()
                elif choice == "2":
                    self.run_tests()
                elif choice == "3":
                    self.run_diagnostics()
                elif choice == "4":
                    self.run_benchmark()
                elif choice == "5":
                    self.setup_coordinates()
                elif choice == "6":
                    self.show_help()
                elif choice == "7":
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("\n❌ Invalid choice! Please select 1-7.")
                    time.sleep(1)
                    
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Menu error: {e}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        launcher = SmartLauncher()
        launcher.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Launcher error: {e}")
        try:
            input("Press Enter to exit...")
        except (KeyboardInterrupt, EOFError):
            pass

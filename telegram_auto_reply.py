# -*- coding: utf-8 -*-
"""
Telegram Desktop Auto-Reply Automation System
Author: amsh23
Date: August 2025

This script automatically detects incoming messages in Telegram Desktop and responds appropriately.
Note: Telegram Desktop must be open and chat coordinates must be configured before running.
"""

import pyautogui
import pytesseract
from PIL import Image
import time
import datetime
import re
import logging
import sys
import os
import pyperclip
from typing import Tuple, Optional

# Import settings
try:
    from config import *
except ImportError:
    print("❌ config.py file not found! Please place it next to the script.")
    sys.exit(1)

# ==============================================================================
# Initial System Settings
# ==============================================================================

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# pyautogui security settings
pyautogui.FAILSAFE = FAILSAFE_ENABLED  # Move mouse to screen corner to stop
pyautogui.PAUSE = PYAUTOGUI_PAUSE      # Delay between commands

# Logging settings
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILENAME, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==============================================================================
# Main Telegram Bot Class
# ==============================================================================

class TelegramAutoReply:
    def __init__(self):
        """Initialize the bot"""
        
        # Telegram chat region coordinates (from settings file)
        self.chat_region = (
            CHAT_REGION['x'], 
            CHAT_REGION['y'], 
            CHAT_REGION['width'], 
            CHAT_REGION['height']
        )
        
        # Input field click position coordinates (from settings file)
        self.input_click_position = (
            INPUT_CLICK_POSITION['x'], 
            INPUT_CLICK_POSITION['y']
        )
        
        # Send button coordinates (from settings file)
        self.send_button_position = (
            SEND_BUTTON_POSITION['x'], 
            SEND_BUTTON_POSITION['y']
        )
        
        # Last read message (to prevent duplicate responses)
        self.last_message = ""
        self.last_message_time = 0
        
        # Message history for better duplicate detection
        self.message_history = []
        
        # Bot active/inactive status
        self.is_active = True
        
        # Delay between checks (from settings file)
        self.check_interval = CHECK_INTERVAL
        
        # Debug mode (from settings file)
        self.debug_mode = DEBUG_MODE
        
        logger.info("Telegram bot initialized with enhanced detection")
        if self.debug_mode:
            logger.debug("Debug mode enabled")

    def check_tesseract_installation(self) -> bool:
        """Check if Tesseract OCR is properly installed"""
        try:
            # Simple Tesseract test
            test_image = Image.new('RGB', (100, 30), color='white')
            pytesseract.image_to_string(test_image, lang=OCR_LANGUAGES)
            logger.info("Tesseract OCR is properly installed")
            return True
        except Exception as e:
            logger.error(f"Error in Tesseract OCR: {e}")
            return False

    def set_chat_region(self, x: int, y: int, width: int, height: int):
        """Set Telegram chat region"""
        self.chat_region = (x, y, width, height)
        logger.info(f"Chat region set: {self.chat_region}")

    def set_input_position(self, x: int, y: int):
        """Set input field click position"""
        self.input_click_position = (x, y)
        logger.info(f"Input position set: {self.input_click_position}")

    def set_send_button_position(self, x: int, y: int):
        """Set send button position"""
        self.send_button_position = (x, y)
        logger.info(f"Send button position set: {self.send_button_position}")

    def capture_chat_area(self) -> Optional[Image.Image]:
        """Take screenshot of Telegram chat area"""
        try:
            # Validate coordinates
            x, y, width, height = self.chat_region
            
            if width <= 0 or height <= 0:
                logger.error(f"Invalid coordinates: {self.chat_region}")
                return None
            
            # Take screenshot of specified region
            screenshot = pyautogui.screenshot(region=self.chat_region)
            logger.debug(f"Screenshot taken: {width}x{height} from ({x}, {y})")
            return screenshot
            
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            logger.error(f"Current coordinates: {self.chat_region}")
            return None

    def save_coordinates_to_config(self):
        """Save coordinates to config.py file"""
        try:
            # Read current config file
            with open('config.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update chat coordinates
            x, y, width, height = self.chat_region
            new_chat_region = f"""CHAT_REGION = {{
    'x': {x},
    'y': {y},
    'width': {width},
    'height': {height}
}}"""
            
            # Find and replace CHAT_REGION section
            import re
            pattern = r'CHAT_REGION = \{[^}]+\}'
            content = re.sub(pattern, new_chat_region, content, flags=re.DOTALL)
            
            # Update input position
            input_x, input_y = self.input_click_position
            new_input_position = f"""INPUT_CLICK_POSITION = {{
    'x': {input_x},
    'y': {input_y}
}}"""
            
            pattern = r'INPUT_CLICK_POSITION = \{[^}]+\}'
            content = re.sub(pattern, new_input_position, content, flags=re.DOTALL)
            
            # Write new file
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("Coordinates saved to config.py")
            print("💾 Coordinates saved to config.py")
            
        except Exception as e:
            logger.warning(f"Error saving coordinates: {e}")
            print("⚠️ Error saving coordinates to file")

    def test_screenshot_capture(self):
        """Test screenshot capture and show preview"""
        print("\n🧪 Testing screenshot capture...")
        
        try:
            # Take test screenshot
            screenshot = self.capture_chat_area()
            
            if screenshot:
                # Save test screenshot
                test_filename = "test_screenshot.png"
                screenshot.save(test_filename)
                print(f"✅ Test screenshot saved: {test_filename}")
                
                # Test OCR
                text = self.extract_text_from_image(screenshot)
                if text:
                    print(f"✅ Text detected: {text[:100]}...")
                else:
                    print("⚠️ No text detected - region might be empty")
                
                print("💡 Check test_screenshot.png file to verify coordinate accuracy")
                
            else:
                print("❌ Error taking screenshot")
                
        except Exception as e:
            print(f"❌ Test error: {e}")
            logger.error(f"Screenshot test error: {e}")

    def extract_text_from_image(self, image: Image.Image) -> str:
        """Extract text from image using OCR with enhanced filtering"""
        try:
            # Process image to improve OCR quality
            # Convert to grayscale for better recognition
            image = image.convert('L')
            
            # Extract text with Persian and English support
            text = pytesseract.image_to_string(
                image, 
                lang=OCR_LANGUAGES,
                config=OCR_CONFIG
            )
            
            # Clean text
            text = text.strip()
            text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
            
            # Filter out interface elements if debug mode is enabled
            if hasattr(self, 'debug_mode') and self.debug_mode:
                original_text = text
                filtered_text = self.filter_interface_elements(text)
                if original_text != filtered_text:
                    logger.debug(f"Original OCR: {original_text[:100]}...")
                    logger.debug(f"Filtered OCR: {filtered_text[:100]}...")
                text = filtered_text
            
            logger.debug(f"Final extracted text: {text[:50]}...")
            return text
            
        except Exception as e:
            logger.error(f"Text extraction error: {e}")
            return ""

    def filter_interface_elements(self, text: str) -> str:
        """Remove common Telegram interface elements from OCR text with Persian-friendly filtering"""
        if not text:
            return text
        
        original_text = text
        
        # Remove common interface patterns using regex
        import re
        for pattern in INTERFACE_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Remove common interface words/phrases (case-insensitive)
        for filter_pattern in INTERFACE_FILTERS:
            text = re.sub(re.escape(filter_pattern), '', text, flags=re.IGNORECASE)
        
        # Remove timestamp patterns (more specific)
        text = re.sub(r'\b\d{1,2}:\d{2}(:\d{2})?\s*(AM|PM)\b', '', text, flags=re.IGNORECASE)
        
        # Remove standalone numbers and single characters
        words = text.split()
        filtered_words = []
        
        for word in words:
            # Keep words that are:
            # - At least 2 characters long (reduced for Persian)
            # - Not pure numbers or symbols
            # - Have some alphabetic content (Persian or English)
            if (len(word) >= 2 and 
                not word.isdigit() and
                not re.match(r'^[^\w]+$', word) and  # Not pure symbols
                re.search(r'[a-zA-Zآ-ی]', word)):   # Contains Persian or English letters
                filtered_words.append(word)
        
        filtered_text = ' '.join(filtered_words).strip()
        
        # More lenient threshold for Persian text (Persian takes more space)
        if len(filtered_text) < len(original_text) * 0.2:
            if DEBUG_MODE:
                logger.debug(f"Text mostly interface elements, ignoring: '{original_text[:50]}...'")
            return ""
        
        return filtered_text

    def analyze_message(self, text: str) -> str:
        """Analyze message and determine appropriate response with enhanced logic"""
        
        if not text:
            return ""
        
        # Debug logging
        if DEBUG_MODE:
            logger.debug(f"Analyzing message: '{text}'")
            logger.debug(f"Message length: {len(text)} characters")
        
        # Check message length
        if len(text) > MAX_MESSAGE_LENGTH or len(text) < MIN_MESSAGE_LENGTH:
            if DEBUG_MODE:
                logger.debug(f"Message rejected due to length: {len(text)}")
            return ""
        
        # Convert to lowercase for better comparison
        text_lower = text.lower()
        
        # Debug: Show what we're matching against
        if DEBUG_MODE:
            logger.debug(f"Lowercase text for matching: '{text_lower}'")
        
        # Check response rules from settings file
        for rule_name, rule_data in RESPONSE_RULES.items():
            keywords = rule_data['keywords']
            
            # Check if keywords exist in text
            matched_keywords = [keyword for keyword in keywords if keyword.lower() in text_lower]
            
            if matched_keywords:
                if DEBUG_MODE:
                    logger.debug(f"Rule '{rule_name}' matched with keywords: {matched_keywords}")
                
                # Handle multiple responses (your style)
                if 'responses' in rule_data:
                    import random
                    response = random.choice(rule_data['responses'])
                    return response
                elif 'response' in rule_data:
                    # Process special responses
                    response = rule_data['response']
                    if response == 'current_time':
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        current_date = datetime.datetime.now().strftime("%Y/%m/%d")
                        return f"الان ساعت {current_time} هستش!\nتاریخ: {current_date} 📅"
                    else:
                        return response
        
        # If no rules matched, check if it's worth a default response
        # Only respond to messages that seem like actual user input
        if self.seems_like_user_message(text):
            if DEBUG_MODE:
                logger.debug("No rules matched, using random default response")
            import random
            return random.choice(DEFAULT_RESPONSES)
        
        if DEBUG_MODE:
            logger.debug("Message ignored - doesn't seem like user input")
        return ""

    def seems_like_user_message(self, text: str) -> bool:
        """Determine if text seems like an actual user message with Persian-friendly logic"""
        
        if not text or len(text.strip()) < 2:  # More lenient minimum length
            return False
        
        text_lower = text.lower()
        
        # Quick check for obvious real message indicators (Persian-friendly)
        import re
        for pattern in REAL_MESSAGE_INDICATORS:
            if re.search(pattern, text_lower):
                if DEBUG_MODE:
                    logger.debug(f"Real message indicator found: {pattern}")
                return True
        
        # Check for interface indicators (more specific)
        interface_count = 0
        for indicator in INTERFACE_FILTERS:
            if indicator.lower() in text_lower:
                interface_count += 1
        
        # If too many interface indicators, likely not a user message
        if interface_count >= 2:
            return False
        
        # Check interface patterns (more lenient for Persian)
        interface_pattern_matches = 0
        for pattern in INTERFACE_PATTERNS:
            if re.search(pattern, text):
                interface_pattern_matches += 1
        
        if interface_pattern_matches >= 2:
            return False
        
        # Check for excessive timestamps/numbers (interface characteristics)
        time_patterns = len(re.findall(r'\d{1,2}:\d{2}', text))
        if time_patterns > 2:  # More lenient threshold
            return False
        
        # Contains meaningful content (Persian or English)
        words = text.split()
        meaningful_words = 0
        persian_chars = 0
        english_chars = 0
        
        # Count Persian and English characters
        for char in text:
            if re.match(r'[آ-ی]', char):
                persian_chars += 1
            elif re.match(r'[a-zA-Z]', char):
                english_chars += 1
        
        # If significant Persian content, likely a user message
        if persian_chars >= 3:
            if DEBUG_MODE:
                logger.debug(f"Persian characters detected: {persian_chars}")
            return True
        
        # Count meaningful words for English/mixed content
        for word in words:
            if (len(word) > 1 and  # Reduced minimum word length for Persian
                not word.isdigit() and  # Not pure numbers
                not re.match(r'^[^\w]+$', word) and  # Not pure symbols
                (re.search(r'[a-zA-Z]', word) or re.search(r'[آ-ی]', word))):  # Contains letters
                meaningful_words += 1
        
        # Need minimum meaningful words for a user message
        return meaningful_words >= MIN_MEANINGFUL_WORDS

    def send_message(self, message: str):
        """Send message in Telegram with Persian support"""
        try:
            # Click on input field
            pyautogui.click(self.input_click_position[0], self.input_click_position[1])
            time.sleep(0.5)
            
            # Clear previous content (if any)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            
            # For Persian text, use clipboard method
            try:
                # Copy message to clipboard
                pyperclip.copy(message)
                time.sleep(0.1)
                
                # Paste from clipboard
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                
                if DEBUG_MODE:
                    logger.debug(f"Message sent via clipboard: '{message}'")
                
            except Exception as clipboard_error:
                # Fallback to character-by-character typing for English
                logger.warning(f"Clipboard method failed, using fallback: {clipboard_error}")
                
                # Type message character by character with slower interval for Persian
                for char in message:
                    try:
                        pyautogui.write(char)
                        time.sleep(0.1)  # Slower for Persian characters
                    except:
                        # Skip problematic characters
                        continue
                time.sleep(0.5)
            
            # Send message
            pyautogui.press('enter')
            
            logger.info(f"Message sent: {message[:30]}...")
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            # Log the actual message that failed to send
            logger.error(f"Failed message content: '{message}'")


    def is_new_message(self, current_text: str) -> bool:
        """Check if a new message has been received with enhanced anti-spam logic"""
        
        if not current_text:
            return False
        
        current_time = time.time()
        
        # Quick check: if it's exactly the same as last message
        if current_text == self.last_message:
            return False
        
        # Enhanced filtering: check if this looks like interface noise
        if not self.seems_like_user_message(current_text):
            if DEBUG_MODE:
                logger.debug(f"Message rejected - appears to be interface: '{current_text[:50]}...'")
            return False
        
        # Check similarity with recent messages to avoid near-duplicates
        for timestamp, message in self.message_history:
            # Remove old messages (older than threshold)
            if current_time - timestamp > NEW_MESSAGE_THRESHOLD:
                continue
                
            # Calculate similarity (simple approach)
            similarity = self.calculate_similarity(current_text, message)
            if similarity > SIMILARITY_THRESHOLD:
                if DEBUG_MODE:
                    logger.debug(f"Message rejected due to similarity: {similarity:.2f} with previous message")
                return False
        
        # Add to history
        self.message_history.append((current_time, current_text))
        
        # Keep only recent messages in history (memory management)
        self.message_history = [(t, m) for t, m in self.message_history 
                               if current_time - t <= NEW_MESSAGE_THRESHOLD * 2]
        
        # Update last message
        self.last_message = current_text
        self.last_message_time = current_time
        
        if DEBUG_MODE:
            logger.debug(f"✅ VALID USER MESSAGE DETECTED: '{current_text[:50]}...'")
        
        return True

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (0.0 to 1.0)"""
        
        if not text1 or not text2:
            return 0.0
        
        # Simple word-based similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

    def setup_precise_coordinates(self):
        """Precise coordinate setup focusing only on new message area"""
        
        print("\n" + "="*60)
        print("🎯 PRECISE Telegram Bot Coordinate Setup")
        print("="*60)
        
        print("\n📍 CRITICAL: We need to capture ONLY the newest message area.")
        print("This prevents capturing interface elements and old messages.")
        
        print("\n📋 Instructions:")
        print("1. Look at your Telegram chat")
        print("2. Find the LAST message in the chat (yours or someone else's)")
        print("3. We'll capture only that small area")
        
        input("\n➡️ Ready? Press Enter...")
        
        # Get coordinates with focused approach
        print("\n🎯 Step 1: Point to TOP-LEFT of the LAST message")
        print("(Not the entire chat, just the last message bubble)")
        print("⏱️ You have 5 seconds...")
        
        time.sleep(5)
        x1, y1 = pyautogui.position()
        print(f"✅ Top-left of last message: ({x1}, {y1})")
        
        print("\n🎯 Step 2: Point to BOTTOM-RIGHT of the LAST message")
        print("(Include a bit of space for new incoming messages)")
        print("⏱️ You have 5 seconds...")
        
        time.sleep(5)
        x2, y2 = pyautogui.position()
        print(f"✅ Bottom-right recorded: ({x2}, {y2})")
        
        # Calculate focused coordinates
        min_x = min(x1, x2)
        min_y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        # Ensure minimum size but keep it small
        if width < 300:
            width = 300
        if height < 80:
            height = 80
        
        # Ensure maximum size to avoid interface
        if width > 600:
            width = 600
        if height > 150:
            height = 150
        
        self.set_chat_region(min_x, min_y, width, height)
        
        print("\n🎯 Step 3: Point to the message input box")
        print("⏱️ You have 5 seconds...")
        
        time.sleep(5)
        input_x, input_y = pyautogui.position()
        print(f"✅ Input position recorded: ({input_x}, {input_y})")
        
        self.set_input_position(input_x, input_y)
        
        print(f"\n✅ PRECISE setup complete!")
        print(f"📏 Focused chat region: {self.chat_region}")
        print(f"📍 Input position: {self.input_click_position}")
        print(f"🎯 This should capture ONLY new messages, not interface!")
        
        # Save settings
        self.save_coordinates_to_config()
        
        # Test the precise setup
        print("\n🧪 Testing precise coordinates...")
        self.test_screenshot_capture()
        
        print("\n💡 Tips for best results:")
        print("• Region should be small and focused")
        print("• Should NOT include timestamps, usernames, or interface")
        print("• Should capture where NEW messages will appear")
        
        choice = input("\nStart monitoring with these precise coordinates? (y/n): ")
        if choice.lower() == 'y':
            print(f"\n🚀 Starting monitoring with precise coordinates...")
            self.run_monitoring_loop()

    def setup_coordinates_interactive(self):
        """Interactive coordinate setup by user"""
        
        print("\n" + "="*60)
        print("🔧 Telegram Bot Coordinate Setup")
        print("="*60)
        
        print("\n📍 Please open Telegram Desktop and go to the desired chat.")
        print("Then follow these steps:")
        
        input("\n➡️ Ready? Press Enter...")
        
        # Get coordinates with better delay
        print("\n🎯 Step 1: Define chat region")
        print("Move mouse to top-left corner of chat area...")
        print("⏱️ You have 5 seconds...")
        
        time.sleep(5)
        x1, y1 = pyautogui.position()
        print(f"✅ Top-left corner recorded: ({x1}, {y1})")
        
        print("\nNow move mouse to bottom-right corner of chat area...")
        print("⏱️ You have 5 seconds...")
        
        time.sleep(5)
        x2, y2 = pyautogui.position()
        print(f"✅ Bottom-right corner recorded: ({x2}, {y2})")
        
        # Validate coordinates
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        if width < 50 or height < 50:
            print(f"⚠️ Warning: Region too small! ({width}x{height})")
            print("Please set coordinates again.")
            
            retry = input("Do you want to try again? (y/n): ")
            if retry.lower() == 'y':
                return self.setup_coordinates_interactive()
            else:
                print("Using default coordinates.")
                return
        
        # Calculate final coordinates
        min_x = min(x1, x2)
        min_y = min(y1, y2)
        
        self.set_chat_region(min_x, min_y, width, height)
        
        print("\n🎯 Step 2: Define input field position")
        print("Move mouse to the text input box...")
        print("⏱️ You have 5 seconds...")
        
        time.sleep(5)
        input_x, input_y = pyautogui.position()
        print(f"✅ Input position recorded: ({input_x}, {input_y})")
        
        self.set_input_position(input_x, input_y)
        
        print(f"\n✅ Setup complete!")
        print(f"📏 Chat region: {self.chat_region} (Width: {width}, Height: {height})")
        print(f"📍 Input position: {self.input_click_position}")
        
        # Save settings to config file
        self.save_coordinates_to_config()
        
        # Test screenshot capture
        self.test_screenshot_capture()

    def run_monitoring_loop(self):
        """Main message monitoring loop with enhanced detection"""
        
        logger.info("Starting enhanced message monitoring loop")
        logger.info(f"Checking every {self.check_interval} seconds")
        logger.info(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
        logger.info(f"Chat region: {self.chat_region}")
        
        print("\n" + "="*60)
        print("🚀 Enhanced Telegram Bot Started")
        print("="*60)
        print(f"📊 Monitoring region: {self.chat_region}")
        print(f"⏱️ Check interval: {self.check_interval} seconds")
        print(f"🔍 Debug mode: {'ON' if self.debug_mode else 'OFF'}")
        print(f"🎯 Enhanced message detection active")
        print("="*60)
        
        try:
            while self.is_active:
                # Take screenshot of chat area
                chat_image = self.capture_chat_area()
                
                if chat_image:
                    # Extract text from image
                    extracted_text = self.extract_text_from_image(chat_image)
                    
                    if DEBUG_MODE and extracted_text:
                        logger.debug(f"Raw OCR result: '{extracted_text}'")
                    
                    if extracted_text and self.is_new_message(extracted_text):
                        logger.info(f"📨 New message detected: {extracted_text[:50]}...")
                        print(f"\n📨 New message: {extracted_text[:100]}...")
                        
                        # Analyze message and generate response
                        response = self.analyze_message(extracted_text)
                        
                        if response:
                            logger.info(f"💬 Generating response: {response[:50]}...")
                            print(f"💬 Sending response: {response[:50]}...")
                            
                            # Delay before response (more natural)
                            time.sleep(RESPONSE_DELAY)
                            
                            # Send response
                            self.send_message(response)
                            
                            logger.info(f"✅ Response sent successfully")
                            print("✅ Response sent!")
                        else:
                            logger.debug("No response generated for this message")
                            if DEBUG_MODE:
                                print("🔍 No response triggered")
                    elif DEBUG_MODE and extracted_text:
                        logger.debug("Message ignored (duplicate or filtered)")
                
                # Delay until next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user (Ctrl+C)")
            print("\n⛔ Bot stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"\n❌ Error: {e}")
        finally:
            self.stop()

    def stop(self):
        """Stop the bot"""
        self.is_active = False
        logger.info("Bot stopped")

# ==============================================================================
# Helper Functions
# ==============================================================================

def print_coordinate_guide():
    """Display coordinate setup guide"""
    print("\n" + "="*60)
    print("📖 Telegram Coordinate Setup Guide")
    print("="*60)
    
    print("""
🖥️ Preparation:
1. Open Telegram Desktop
2. Go to the desired chat
3. Set window to windowed mode (not fullscreen)
4. Make window medium size

📍 Define Chat Region:
• Top-left corner: on the first chat message
• Bottom-right corner: on the last visible message
• Make sure sidebar and header are not included

⌨️ Define Input Box:
• Click on middle of "Type a message" box
• Usually located at bottom of window

💡 Tips:
• Coordinates are saved to config.py
• You can manually edit them later
• Test screenshot is saved for verification
""")
    
    input("Press Enter to return...")

def check_dependencies():
    """Check if required dependencies exist"""
    
    print("🔍 Checking dependencies...")
    
    # Check Tesseract
    if not os.path.exists(TESSERACT_PATH):
        print(f"❌ Tesseract OCR not found at {TESSERACT_PATH}!")
        print("Please download and install Tesseract from:")
        print("https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    
    print("✅ Tesseract OCR found")
    
    # Check Python packages
    required_packages = ['pyautogui', 'pytesseract', 'PIL', 'schedule']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ Package {package} installed")
        except ImportError:
            print(f"❌ Package {package} not installed!")
            return False
    
    return True

def main():
    """Main program function"""
    
    print("🤖 Enhanced Telegram Auto-Reply Bot v2.0")
    print("="*50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install required dependencies first")
        return
    
    # Create bot instance
    bot = TelegramAutoReply()
    
    # Check Tesseract installation
    if not bot.check_tesseract_installation():
        print("❌ Error in Tesseract OCR. Please check installation path")
        return
    
    print("\n📋 Available options:")
    print("1. Interactive coordinate setup (recommended)")
    print("2. Use current coordinates")
    print("3. Coordinate setup guide")
    print("4. Quick test (take screenshot and analyze)")
    print("5. 🎯 PRECISE COORDINATE SETUP (for new messages only)")
    
    choice = input("\nChoose option (1/2/3/4/5): ").strip()
    
    if choice == '1':
        print("\n📖 Important notes for coordinate setup:")
        print("• Open Telegram Desktop in windowed mode (not fullscreen)")
        print("• Keep Telegram window medium size (not too small or large)")
        print("• Chat area should include ONLY recent messages (not sidebar or header)")
        print("• Input box is usually at the bottom of the window")
        input("\n➡️ Ready? Press Enter...")
        
        bot.setup_coordinates_interactive()
    elif choice == '3':
        print_coordinate_guide()
        return
    elif choice == '4':
        print("\n🧪 Quick Test Mode")
        print("Current chat region:", bot.chat_region)
        bot.test_screenshot_capture()
        
        # Test with current screenshot
        screenshot = bot.capture_chat_area()
        if screenshot:
            text = bot.extract_text_from_image(screenshot)
            print(f"\n📝 Extracted text: '{text}'")
            
            response = bot.analyze_message(text)
            print(f"🤖 Would respond with: '{response}'" if response else "🤖 No response would be generated")
        return
    elif choice == '5':
        print("\n🎯 PRECISE COORDINATE SETUP")
        print("="*50)
        print("This mode helps you set coordinates to capture ONLY the newest message area.")
        print("\n📋 Steps:")
        print("1. Send a test message in Telegram first")
        print("2. We'll capture only the bottom area where YOUR message appears")
        print("3. This avoids capturing interface elements")
        
        input("\n➡️ Send a test message in Telegram, then press Enter...")
        
        bot.setup_precise_coordinates()
        return
    else:
        print("Using current coordinates from config.py")
        print("⚠️ Make sure coordinates are correctly set for your screen")
    
    print(f"\n🚀 Enhanced bot v2.0 starting...")
    print(f"⏱️ Checking every {bot.check_interval} seconds")
    print(f"🔍 Debug mode: {'ON' if bot.debug_mode else 'OFF'}")
    print(f"🎯 Anti-spam protection: ACTIVE")
    print("⚠️ To stop: Ctrl+C")
    print("⚠️ Emergency stop: Move mouse to screen corner")
    
    # Start monitoring loop
    bot.run_monitoring_loop()

# ==============================================================================
# Program Execution
# ==============================================================================

if __name__ == "__main__":
    main()

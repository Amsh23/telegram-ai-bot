#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Smart OCR System
High-accuracy OCR specifically for Persian and English chat messages
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import easyocr
import re
import logging

class SmartOCR:
    """🤖 Smart OCR with Persian/English optimization"""
    
    def __init__(self):
        self.setup_logging()
        self.init_ocr_engines()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def init_ocr_engines(self):
        """Initialize OCR engines"""
        try:
            # EasyOCR for Persian and English
            self.easy_reader = easyocr.Reader(['fa', 'en'], gpu=False)
            self.logger.info("✅ EasyOCR initialized successfully")
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize EasyOCR: {e}")
            self.easy_reader = None
    
    def preprocess_image(self, image_path):
        """🔧 Advanced image preprocessing for better OCR"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return None
                
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Enhance contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(enhanced)
            
            # Threshold
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return thresh
            
        except Exception as e:
            self.logger.error(f"Preprocessing failed: {e}")
            return None
    
    def extract_text_easyocr(self, image_path):
        """Extract text using EasyOCR"""
        if not self.easy_reader:
            return []
            
        try:
            results = self.easy_reader.readtext(image_path)
            extracted_texts = []
            
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # Only high confidence
                    extracted_texts.append({
                        'text': text.strip(),
                        'confidence': confidence,
                        'method': 'easyocr'
                    })
            
            return extracted_texts
            
        except Exception as e:
            self.logger.error(f"EasyOCR extraction failed: {e}")
            return []
    
    def is_valid_chat_text(self, text):
        """🔍 Check if text looks like a chat message"""
        if not text or len(text.strip()) < 2:
            return False
            
        # Remove extra spaces
        text = ' '.join(text.split())
        
        # Persian character check
        persian_chars = re.findall(r'[\u0600-\u06FF]', text)
        english_chars = re.findall(r'[a-zA-Z]', text)
        
        # Must have some meaningful characters
        if len(persian_chars) + len(english_chars) < 3:
            return False
            
        # Check for common UI elements (reject)
        ui_patterns = [
            r'^\d+:\d+$',  # Time only
            r'^[A-Z]{2,}$',  # All caps (buttons)
            r'^\W+$',  # Only symbols
            r'loading|button|click|menu|close|ok|cancel',
            r'آنلاین|آفلاین|ارسال|دانلود|بستن'
        ]
        
        for pattern in ui_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return False
                
        return True
    
    def extract_chat_messages(self, image_path):
        """🎯 Extract and validate chat messages from image"""
        self.logger.info(f"🔍 Analyzing image: {image_path}")
        
        # Get all OCR results
        all_results = []
        
        # Try EasyOCR
        easy_results = self.extract_text_easyocr(image_path)
        all_results.extend(easy_results)
        
        # Try with preprocessed image
        preprocessed_path = image_path.replace('.', '_processed.')
        processed_img = self.preprocess_image(image_path)
        if processed_img is not None:
            cv2.imwrite(preprocessed_path, processed_img)
            easy_processed = self.extract_text_easyocr(preprocessed_path)
            all_results.extend(easy_processed)
        
        # Filter and rank results
        valid_messages = []
        
        for result in all_results:
            text = result['text']
            if self.is_valid_chat_text(text):
                # Calculate quality score
                quality_score = self.calculate_quality_score(text, result['confidence'])
                
                valid_messages.append({
                    'text': text,
                    'confidence': result['confidence'],
                    'quality': quality_score,
                    'method': result['method'],
                    'is_persian': bool(re.search(r'[\u0600-\u06FF]', text)),
                    'is_english': bool(re.search(r'[a-zA-Z]', text))
                })
        
        # Remove duplicates and sort by quality
        unique_messages = self.remove_duplicates(valid_messages)
        unique_messages.sort(key=lambda x: x['quality'], reverse=True)
        
        return unique_messages[:10]  # Top 10 results
    
    def calculate_quality_score(self, text, confidence):
        """📊 Calculate quality score for detected text"""
        score = confidence * 0.6  # Base confidence
        
        # Length bonus
        if 5 <= len(text) <= 100:
            score += 0.2
        elif len(text) > 100:
            score += 0.1
            
        # Language detection bonus
        if re.search(r'[\u0600-\u06FF]', text):  # Persian
            score += 0.1
        if re.search(r'[a-zA-Z]', text):  # English
            score += 0.1
            
        # Sentence structure bonus
        if any(char in text for char in '.!?؟'):
            score += 0.1
            
        return min(score, 1.0)
    
    def remove_duplicates(self, messages):
        """🧹 Remove duplicate messages"""
        seen = set()
        unique = []
        
        for msg in messages:
            # Normalize text for comparison
            normalized = re.sub(r'\s+', ' ', msg['text'].lower().strip())
            if normalized not in seen and len(normalized) > 2:
                seen.add(normalized)
                unique.append(msg)
                
        return unique
    
    def get_best_chat_text(self, image_path):
        """🏆 Get the best chat message from image"""
        messages = self.extract_chat_messages(image_path)
        
        if not messages:
            return None
            
        best_message = messages[0]
        
        result = {
            'text': best_message['text'],
            'confidence': best_message['confidence'],
            'quality': best_message['quality'],
            'language': 'persian' if best_message['is_persian'] else 'english',
            'method': best_message['method'],
            'alternatives': [msg['text'] for msg in messages[1:5]]  # Top 5 alternatives
        }
        
        self.logger.info(f"✅ Best result: '{result['text'][:50]}...' (Quality: {result['quality']:.2f})")
        
        return result

def test_smart_ocr():
    """🧪 Test the Smart OCR system"""
    import os
    
    ocr = SmartOCR()
    
    # Test with available screenshots
    test_images = [
        'test_screenshot.png',
        'debug_screenshot.png'
    ]
    
    for img_path in test_images:
        if os.path.exists(img_path):
            print(f"\n🧪 Testing with {img_path}")
            result = ocr.get_best_chat_text(img_path)
            
            if result:
                print(f"📱 Detected: {result['text']}")
                print(f"🎯 Quality: {result['quality']:.2f}")
                print(f"🌍 Language: {result['language']}")
                print(f"🔧 Method: {result['method']}")
                if result['alternatives']:
                    print(f"💡 Alternatives: {result['alternatives']}")
            else:
                print(f"❌ No valid chat text detected in {img_path}")

if __name__ == "__main__":
    test_smart_ocr()

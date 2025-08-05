#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Advanced OCR System with Better Accuracy
Multi-engine OCR with text cleaning and validation
"""

import cv2
import numpy as np
import easyocr
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
from typing import List, Dict, Tuple
import logging

class AdvancedOCR:
    """🎯 Advanced OCR with multiple engines and text cleaning"""
    
    def __init__(self):
        self.setup_logging()
        self.setup_engines()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def setup_engines(self):
        """Initialize OCR engines"""
        try:
            # EasyOCR with Persian and English
            self.easyocr_reader = easyocr.Reader(['fa', 'en'])
            self.easyocr_available = True
            self.logger.info("✅ EasyOCR initialized")
        except Exception as e:
            self.easyocr_available = False
            self.logger.error(f"❌ EasyOCR failed: {e}")
        
        # Tesseract configuration
        self.tesseract_config = {
            'persian': '--oem 3 --psm 6 -l fas',
            'english': '--oem 3 --psm 6 -l eng',
            'combined': '--oem 3 --psm 6 -l fas+eng'
        }
    
    def preprocess_image(self, image: np.ndarray) -> List[np.ndarray]:
        """🔧 Advanced image preprocessing for better OCR"""
        processed_images = []
        
        # Original image
        processed_images.append(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. High contrast version
        enhanced = cv2.convertScaleAbs(gray, alpha=1.5, beta=30)
        processed_images.append(enhanced)
        
        # 2. Denoised version
        denoised = cv2.fastNlMeansDenoising(gray)
        processed_images.append(denoised)
        
        # 3. Sharpened version
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(gray, -1, kernel)
        processed_images.append(sharpened)
        
        # 4. Adaptive threshold
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        processed_images.append(adaptive)
        
        # 5. OTSU threshold
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed_images.append(otsu)
        
        # 6. Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
        morph = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        processed_images.append(morph)
        
        return processed_images
    
    def extract_text_easyocr(self, image: np.ndarray) -> List[Dict]:
        """📖 Extract text using EasyOCR"""
        results = []
        
        if not self.easyocr_available:
            return results
            
        try:
            # Get all possible text detections
            ocr_results = self.easyocr_reader.readtext(image, detail=1)
            
            for (bbox, text, confidence) in ocr_results:
                if confidence > 0.3:  # Lower threshold for more text
                    results.append({
                        'text': text.strip(),
                        'confidence': confidence,
                        'engine': 'easyocr',
                        'bbox': bbox
                    })
                    
        except Exception as e:
            self.logger.error(f"EasyOCR error: {e}")
            
        return results
    
    def extract_text_tesseract(self, image: np.ndarray, lang: str = 'combined') -> List[Dict]:
        """📖 Extract text using Tesseract"""
        results = []
        
        try:
            config = self.tesseract_config.get(lang, self.tesseract_config['combined'])
            
            # Get text with confidence scores
            data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
            
            current_line = ""
            line_confidence = []
            
            for i in range(len(data['text'])):
                confidence = int(data['conf'][i])
                text = data['text'][i].strip()
                
                if confidence > 30 and text:  # Lower threshold
                    current_line += text + " "
                    line_confidence.append(confidence)
                
                # End of line or block
                if data['block_num'][i] != data['block_num'][i+1] if i+1 < len(data['text']) else True:
                    if current_line.strip():
                        avg_confidence = sum(line_confidence) / len(line_confidence) if line_confidence else 0
                        results.append({
                            'text': current_line.strip(),
                            'confidence': avg_confidence / 100,
                            'engine': f'tesseract_{lang}',
                            'bbox': None
                        })
                    current_line = ""
                    line_confidence = []
                    
        except Exception as e:
            self.logger.error(f"Tesseract error: {e}")
            
        return results
    
    def clean_and_validate_text(self, text: str) -> Tuple[str, float]:
        """🧹 Clean and validate extracted text"""
        if not text:
            return "", 0.0
            
        original_length = len(text)
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # Remove isolated single characters (likely OCR errors)
        words = cleaned.split()
        filtered_words = []
        
        for word in words:
            # Keep word if:
            # - Length > 1
            # - Is a number
            # - Is Persian/English letter
            if (len(word) > 1 or 
                word.isdigit() or 
                any(c.isalpha() for c in word)):
                filtered_words.append(word)
        
        cleaned = ' '.join(filtered_words)
        
        # Calculate quality score
        quality_score = 1.0
        
        # Length penalty
        if len(cleaned) < 5:
            quality_score -= 0.4
        
        # Character quality check
        total_chars = len(cleaned.replace(' ', ''))
        if total_chars > 0:
            # Count valid characters (letters, numbers, common punctuation)
            valid_chars = sum(1 for c in cleaned if (c.isalnum() or 
                                                   c in 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی' or
                                                   c in '.,;:!?()[]{}"\'-'))
            char_quality = valid_chars / total_chars
            quality_score *= char_quality
        
        # Suspicious pattern penalty
        suspicious_patterns = [
            r'[a-zA-Z]{1}\s[a-zA-Z]{1}\s',  # Isolated single letters
            r'\d{1}\s\d{1}\s',              # Isolated single digits
            r'[^\w\s]{3,}',                 # Too many special characters
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, cleaned):
                quality_score -= 0.2
        
        return cleaned, max(0.0, quality_score)
    
    def extract_chat_messages(self, image: np.ndarray) -> List[Dict]:
        """💬 Extract and identify chat messages"""
        all_results = []
        
        # Process image with different preprocessing
        processed_images = self.preprocess_image(image)
        
        for i, proc_img in enumerate(processed_images):
            # Try EasyOCR
            if self.easyocr_available:
                easyocr_results = self.extract_text_easyocr(proc_img)
                for result in easyocr_results:
                    result['preprocessing'] = f'method_{i}'
                    all_results.append(result)
            
            # Try Tesseract with different languages
            for lang in ['combined', 'persian', 'english']:
                tesseract_results = self.extract_text_tesseract(proc_img, lang)
                for result in tesseract_results:
                    result['preprocessing'] = f'method_{i}'
                    all_results.append(result)
        
        # Clean and score all results
        cleaned_results = []
        for result in all_results:
            cleaned_text, quality_score = self.clean_and_validate_text(result['text'])
            
            if quality_score > 0.3 and len(cleaned_text) > 3:
                cleaned_results.append({
                    'text': cleaned_text,
                    'confidence': result['confidence'] * quality_score,
                    'engine': result['engine'],
                    'quality': quality_score,
                    'preprocessing': result['preprocessing']
                })
        
        # Remove duplicates and get best results
        unique_results = self.remove_duplicates(cleaned_results)
        
        # Sort by confidence and quality
        unique_results.sort(key=lambda x: x['confidence'] * x['quality'], reverse=True)
        
        return unique_results[:5]  # Return top 5 results
    
    def remove_duplicates(self, results: List[Dict]) -> List[Dict]:
        """🔄 Remove duplicate texts"""
        seen_texts = set()
        unique_results = []
        
        for result in results:
            text_normalized = re.sub(r'\s+', ' ', result['text'].lower().strip())
            
            # Check for similarity with existing texts
            is_duplicate = False
            for seen_text in seen_texts:
                # Calculate similarity
                similarity = self.calculate_similarity(text_normalized, seen_text)
                if similarity > 0.8:  # 80% similarity threshold
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_texts.add(text_normalized)
                unique_results.append(result)
        
        return unique_results
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """📊 Calculate text similarity"""
        if not text1 or not text2:
            return 0.0
        
        # Simple character-based similarity
        longer = text1 if len(text1) > len(text2) else text2
        shorter = text2 if len(text1) > len(text2) else text1
        
        if len(longer) == 0:
            return 1.0
        
        matches = sum(1 for i, char in enumerate(shorter) if i < len(longer) and char == longer[i])
        return matches / len(longer)
    
    def is_chat_message(self, text: str) -> bool:
        """💬 Determine if text looks like a chat message"""
        if not text or len(text) < 3:
            return False
        
        # Chat message indicators
        chat_indicators = [
            # Persian chat patterns
            r'سلام|درود|چطور|چطوری|حال|احوال',
            r'ممنون|مرسی|تشکر',
            r'خداحافظ|بای|فعلاً',
            r'چی|چه|کی|کجا|چرا|چطور',
            
            # English chat patterns
            r'\bhello\b|\bhi\b|\bhey\b',
            r'\bthanks?\b|\bthank you\b',
            r'\bbye\b|\bgoodbye\b',
            r'\bwhat\b|\bhow\b|\bwhy\b|\bwhen\b|\bwhere\b',
            
            # General chat patterns
            r'[؟?!]',  # Question marks, exclamations
            r'😀|😊|😂|❤️|👍',  # Emojis
        ]
        
        text_lower = text.lower()
        
        # Check for chat indicators
        for pattern in chat_indicators:
            if re.search(pattern, text_lower):
                return True
        
        # Check for conversational length (not too short, not too long)
        word_count = len(text.split())
        if 2 <= word_count <= 20:
            return True
        
        return False
    
    def extract_best_chat_text(self, image: np.ndarray) -> str:
        """🎯 Extract the best chat text from image"""
        results = self.extract_chat_messages(image)
        
        # Filter for chat-like messages
        chat_results = [r for r in results if self.is_chat_message(r['text'])]
        
        if chat_results:
            # Return the best chat message
            best_result = max(chat_results, key=lambda x: x['confidence'] * x['quality'])
            self.logger.info(f"📨 Best chat detected: '{best_result['text']}' "
                           f"(confidence: {best_result['confidence']:.2f}, "
                           f"quality: {best_result['quality']:.2f})")
            return best_result['text']
        
        elif results:
            # Fallback to best general result
            best_result = results[0]
            self.logger.info(f"📝 General text detected: '{best_result['text']}' "
                           f"(confidence: {best_result['confidence']:.2f})")
            return best_result['text']
        
        return ""

# Test function
def test_advanced_ocr():
    """🧪 Test the advanced OCR system"""
    ocr = AdvancedOCR()
    
    # Test with a sample image
    import os
    if os.path.exists("test_screenshot.png"):
        image = cv2.imread("test_screenshot.png")
        results = ocr.extract_chat_messages(image)
        
        print("🔍 OCR Results:")
        for i, result in enumerate(results):
            print(f"{i+1}. Text: '{result['text']}'")
            print(f"   Engine: {result['engine']}")
            print(f"   Confidence: {result['confidence']:.2f}")
            print(f"   Quality: {result['quality']:.2f}")
            print(f"   Is Chat: {ocr.is_chat_message(result['text'])}")
            print()
        
        best_text = ocr.extract_best_chat_text(image)
        print(f"🎯 Best Result: '{best_text}'")

if __name__ == "__main__":
    test_advanced_ocr()

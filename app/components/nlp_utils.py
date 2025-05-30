#!/usr/bin/env python3
"""
NLP Utilities for Novel Companion AI
Contains functions for text processing, sentiment analysis, and named entity recognition.
"""

import re
import string
from typing import Dict, List, Tuple, Optional
from collections import Counter
import pandas as pd

def extract_characters_from_text(text: str) -> List[str]:
    """
    Extract character names from text using simple heuristics.
    In a real implementation, this would use NER models.
    """
    # Simple pattern for capitalized names (placeholder)
    pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
    potential_names = re.findall(pattern, text)
    
    # Filter out common words that aren't names
    common_words = {'The', 'This', 'That', 'When', 'Where', 'What', 'Who', 'How', 'Chapter'}
    characters = [name for name in potential_names if name not in common_words]
    
    # Return most frequent potential character names
    name_counts = Counter(characters)
    return [name for name, count in name_counts.most_common(10) if count > 1]

def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Analyze sentiment of text. 
    In a real implementation, this would use transformer models.
    """
    # Placeholder sentiment analysis
    positive_words = ['love', 'joy', 'happy', 'wonderful', 'excellent', 'beautiful', 'amazing']
    negative_words = ['hate', 'sad', 'terrible', 'awful', 'horrible', 'bad', 'angry']
    
    text_lower = text.lower()
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    total_words = len(text.split())
    
    return {
        'positive': positive_count / max(total_words, 1),
        'negative': negative_count / max(total_words, 1),
        'neutral': 1 - (positive_count + negative_count) / max(total_words, 1)
    }

def extract_themes(text: str) -> List[str]:
    """
    Extract major themes from text.
    In a real implementation, this would use topic modeling.
    """
    # Placeholder theme extraction based on keywords
    theme_keywords = {
        'Love & Romance': ['love', 'romance', 'marriage', 'courtship', 'affection', 'heart'],
        'Social Class': ['class', 'society', 'wealth', 'status', 'gentleman', 'lady'],
        'Pride & Prejudice': ['pride', 'prejudice', 'judgment', 'opinion', 'first impression'],
        'Family': ['family', 'sister', 'brother', 'father', 'mother', 'parent'],
        'Friendship': ['friend', 'friendship', 'companion', 'acquaintance']
    }
    
    text_lower = text.lower()
    detected_themes = []
    
    for theme, keywords in theme_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_themes.append(theme)
    
    return detected_themes

def summarize_chapter(text: str, max_sentences: int = 3) -> str:
    """
    Generate a simple extractive summary of a chapter.
    In a real implementation, this would use transformer-based summarization.
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= max_sentences:
        return ' '.join(sentences)
    
    # Simple scoring based on sentence length and position
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        # Score based on position (beginning and end are important)
        position_score = 1.0 if i < 2 or i >= len(sentences) - 2 else 0.5
        # Score based on length (medium length sentences preferred)
        length_score = 1.0 if 50 <= len(sentence) <= 200 else 0.7
        
        total_score = position_score * length_score
        scored_sentences.append((sentence, total_score))
    
    # Sort by score and take top sentences
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    top_sentences = [s[0] for s in scored_sentences[:max_sentences]]
    
    return ' '.join(top_sentences)

def analyze_character_relationships(text: str, characters: List[str]) -> Dict[str, List[str]]:
    """
    Analyze relationships between characters based on co-occurrence.
    In a real implementation, this would use more sophisticated NLP techniques.
    """
    relationships = {char: [] for char in characters}
    
    # Split text into sentences
    sentences = re.split(r'[.!?]+', text)
    
    for sentence in sentences:
        # Find which characters appear in this sentence
        chars_in_sentence = [char for char in characters if char in sentence]
        
        # Create relationships between characters that appear together
        for i, char1 in enumerate(chars_in_sentence):
            for char2 in chars_in_sentence[i+1:]:
                if char2 not in relationships[char1]:
                    relationships[char1].append(char2)
                if char1 not in relationships[char2]:
                    relationships[char2].append(char1)
    
    return relationships

def generate_reading_insights(text: str) -> Dict[str, any]:
    """
    Generate comprehensive reading insights for the given text.
    """
    characters = extract_characters_from_text(text)
    sentiment = analyze_sentiment(text)
    themes = extract_themes(text)
    summary = summarize_chapter(text)
    relationships = analyze_character_relationships(text, characters)
    
    return {
        'characters': characters,
        'sentiment': sentiment,
        'themes': themes,
        'summary': summary,
        'relationships': relationships,
        'word_count': len(text.split()),
        'reading_time': len(text.split()) / 200  # Assuming 200 WPM reading speed
    }

class NovelAnalyzer:
    """
    A class to handle novel analysis with state management.
    """
    
    def __init__(self):
        self.chapters = {}
        self.characters = set()
        self.global_themes = set()
        
    def add_chapter(self, chapter_id: str, text: str) -> Dict[str, any]:
        """Add a chapter and analyze it."""
        insights = generate_reading_insights(text)
        self.chapters[chapter_id] = insights
        
        # Update global tracking
        self.characters.update(insights['characters'])
        self.global_themes.update(insights['themes'])
        
        return insights
    
    def get_character_development(self, character: str) -> List[Dict[str, any]]:
        """Track character development across chapters."""
        development = []
        
        for chapter_id, chapter_data in self.chapters.items():
            if character in chapter_data['characters']:
                development.append({
                    'chapter': chapter_id,
                    'sentiment': chapter_data['sentiment'],
                    'themes': chapter_data['themes']
                })
        
        return development
    
    def get_global_statistics(self) -> Dict[str, any]:
        """Get statistics across all analyzed chapters."""
        if not self.chapters:
            return {}
        
        total_words = sum(chapter['word_count'] for chapter in self.chapters.values())
        total_reading_time = sum(chapter['reading_time'] for chapter in self.chapters.values())
        
        return {
            'total_chapters': len(self.chapters),
            'total_characters': len(self.characters),
            'total_themes': len(self.global_themes),
            'total_words': total_words,
            'estimated_reading_time': total_reading_time,
            'characters': list(self.characters),
            'themes': list(self.global_themes)
        } 
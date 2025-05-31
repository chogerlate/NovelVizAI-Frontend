import requests
import json
import os
from typing import Dict, List, Optional
from config import API_BASE_URL, API_TIMEOUT

# API Client Class
class NovelCompanionAPIClient:
    """API client for Novel Companion AI backend"""
    
    def __init__(self, base_url: str = API_BASE_URL, timeout: int = API_TIMEOUT):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def get_novels(self, limit: int = 50, skip: int = 0) -> List[Dict]:
        """Get list of novels from API"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/novels/",
                params={"limit": limit, "skip": skip},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # Return mock data when API is unavailable
            return self._get_mock_novels()
    
    def get_novel_by_id(self, novel_id: str) -> Optional[Dict]:
        """Get a specific novel by ID"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/novels/{novel_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # Return mock data when API is unavailable
            return self._get_mock_novel(novel_id)
    
    def get_novel_chapters(self, novel_id: str, limit: int = 100) -> List[Dict]:
        """Get chapters for a novel"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/novels/{novel_id}/chapters",
                params={"limit": limit},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # Return mock data when API is unavailable
            return self._get_mock_chapters(novel_id)
    
    def get_chapter_analysis(self, chapter_id: str) -> Optional[Dict]:
        """Get chapter analysis from API or local files"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/chapters/{chapter_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            chapter_data = response.json()
            
            # Extract analysis data from chapter data if it exists
            if 'analysis_data' in chapter_data:
                return chapter_data['analysis_data']
            else:
                # Return the full chapter data as it may contain analysis fields
                return chapter_data
        except requests.exceptions.RequestException:
            # Fallback to local analysis files
            return self._get_mock_analysis(chapter_id)
    
    def upload_novel_file(self, file_content: bytes, filename: str, **kwargs) -> Optional[Dict]:
        """Upload a novel file"""
        try:
            files = {'file': (filename, file_content, 'text/plain')}
            data = {k: v for k, v in kwargs.items() if v is not None}
            
            response = self.session.post(
                f"{self.base_url}/api/upload",
                files=files,
                data=data,
                timeout=self.timeout * 2
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # Return mock success response
            return {"novel_id": "mock_novel_id", "message": "File uploaded (mock)"}
    
    def summarize_chapter(self, chapter_id: str, length: str = "detailed") -> Optional[Dict]:
        """Get chapter summary from existing chapter data"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/chapters/{chapter_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            chapter_data = response.json()
            
            # Extract summary from chapter data
            if 'summary' in chapter_data:
                return {"summary": chapter_data['summary']}
            elif 'analysis_data' in chapter_data and 'chapter_analysis' in chapter_data['analysis_data']:
                analysis = chapter_data['analysis_data']['chapter_analysis']
                if 'summary' in analysis:
                    return {"summary": analysis['summary']}
            
            return None
        except requests.exceptions.RequestException:
            # Return mock summary response
            return {"summary": "Summary regenerated (mock)", "key_events": []}
    
    def chat_about_novel(self, novel_id: str, message: str) -> Optional[Dict]:
        """Chat about a novel"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/novels/{novel_id}/chat",
                json={"message": message},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # Return mock chat response
            return self._get_mock_chat_response(message)
    
    def _get_mock_novels(self) -> List[Dict]:
        """Return mock novel data"""
        return [
            {
                "id": "683a3adcf4943c13b3ffb951",
                "title": "Omniscient Reader's Viewpoint",
                "author": "Sing Shong",
                "type": "Web Novel",
                "year": 2018,
                "description": "A web novel about a man who becomes trapped in the world of his favorite story.",
                "average_rating": 9.2,
                "vote_count": 15000,
                "status_in_coo": "Completed",
                "genres": ["Fantasy", "Action", "Drama"],
                "tags": ["Apocalypse", "Survival", "Meta-fiction"]
            }
        ]
    
    def _get_mock_novel(self, novel_id: str) -> Dict:
        """Return mock novel data for specific ID"""
        novels = self._get_mock_novels()
        return novels[0] if novels else {}
    
    def _get_mock_chapters(self, novel_id: str) -> List[Dict]:
        """Return mock chapter data"""
        return [
            {
                "id": "ch0",
                "novel_id": novel_id,
                "title": "Prologue",
                "chapter_number": 0,
                "word_count": 785,
                "reading_time_minutes": 4,
                "is_processed": True
            },
            {
                "id": "ch1",
                "novel_id": novel_id,
                "title": "Chapter 1: End",
                "chapter_number": 1,
                "word_count": 1500,
                "reading_time_minutes": 7,
                "is_processed": True
            },
            {
                "id": "ch4",
                "novel_id": novel_id,
                "title": "Chapter 4: Starting the Paid Service, III",
                "chapter_number": 4,
                "word_count": 1727,
                "reading_time_minutes": 8,
                "is_processed": True
            }
        ]
    
    def _get_mock_analysis(self, chapter_id: str) -> Optional[Dict]:
        """Return mock analysis data"""
        # Try to load from local files first
        analysis_files = {
            "ch0": "db/chapter_analysis_collection/ch0_analysis.json",
            "ch1": "db/chapter_analysis_collection/ch1_analysis.json", 
            "ch4": "db/chapter_analysis_collection/ch2_analysis.json"
        }
        
        file_path = analysis_files.get(chapter_id)
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Return basic mock data if file not found
        return {
            "chapter_analysis": {
                "metadata": {
                    "novel_id": "683a3adcf4943c13b3ffb951",
                    "chapter_id": chapter_id,
                    "novel_title": "Omniscient Reader's Viewpoint",
                    "chapter_number": int(chapter_id.replace("ch", "")) if chapter_id.startswith("ch") else 0,
                    "chapter_title": f"Chapter {chapter_id}",
                    "word_count": 1500,
                    "estimated_reading_time": 7
                },
                "summary": {
                    "concise": "A summary of the chapter events.",
                    "detailed": "A more detailed summary of what happens in this chapter.",
                    "key_events": ["Event 1", "Event 2", "Event 3"]
                },
                "sentiment_analysis": {
                    "overall_tone": "Neutral",
                    "emotional_arc": [
                        {"emotion": "Neutral", "intensity": 0.5}
                    ],
                    "character_sentiments": {}
                },
                "themes": [
                    {
                        "theme": "Survival",
                        "relevance": 0.8,
                        "evidence": "Characters face challenges"
                    }
                ],
                "literary_elements": {
                    "narrative_voice": "Third person",
                    "foreshadowing": [
                        {
                            "text": "Sample foreshadowing text",
                            "significance": "Hints at future events"
                        }
                    ],
                    "symbolism": [
                        {
                            "symbol": "Sample symbol",
                            "meaning": "Symbolic meaning"
                        }
                    ]
                }
            },
            "character_mapping": {
                "characters": [
                    {
                        "name": "Sample Character",
                        "role": "Protagonist",
                        "first_appearance": "Chapter 1",
                        "description": "Main character description",
                        "key_traits": ["Trait 1", "Trait 2"],
                        "quotes": ["Sample quote"],
                        "development_status": "Developing"
                    }
                ],
                "relationships": [
                    {
                        "characters": ["Character 1", "Character 2"],
                        "relationship_type": "Friend",
                        "dynamics": "Supportive relationship",
                        "significance": "Important for character development",
                        "interaction_count": 5,
                        "sentiment": "Positive"
                    }
                ],
                "network_data": {
                    "nodes": [
                        {"id": 1, "name": "Character 1", "group": 1, "size": 5},
                        {"id": 2, "name": "Character 2", "group": 1, "size": 3}
                    ],
                    "links": [
                        {"source": 1, "target": 2, "value": 5, "type": "Friend"}
                    ]
                }
            },
            "interactive_companion": {
                "chapter_context": {
                    "setting": "Unknown setting",
                    "timeline_position": "Early in story",
                    "narrative_importance": "Establishes foundation"
                },
                "key_questions": [
                    "What motivates the main character?",
                    "How does this chapter advance the plot?"
                ],
                "suggested_discussion_points": [
                    "Character development themes",
                    "Narrative structure analysis"
                ],
                "vocabulary_notes": [
                    {
                        "term": "Sample term",
                        "definition": "Definition of the term"
                    }
                ],
                "cultural_context": [
                    {
                        "reference": "Cultural reference",
                        "explanation": "Explanation of cultural significance"
                    }
                ]
            },
            "reading_analytics": {
                "complexity_metrics": {
                    "readability_score": 75,
                    "vocabulary_level": "Moderate",
                    "structural_complexity": "Standard narrative structure"
                },
                "pacing_analysis": {
                    "overall_pace": "Moderate pacing throughout",
                    "significant_shifts": [
                        {
                            "position": "Middle",
                            "change": "Pace increases during action sequence"
                        }
                    ]
                },
                "engagement_factors": {
                    "hook": ["Opening scene", "Character introduction"],
                    "engagement_score": 7.5
                }
            }
        }
    
    def _get_mock_chat_response(self, message: str) -> Dict:
        """Return mock chat response"""
        return {
            "response": f"That's an interesting question about '{message}'. Based on the chapter context, I can help you explore this topic further.",
            "references": ["Chapter context", "Character analysis"],
            "suggested_questions": [
                "Can you tell me more about the characters?",
                "What are the main themes?",
                "How does this chapter advance the plot?"
            ]
        }
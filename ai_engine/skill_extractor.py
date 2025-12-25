"""
Skill Extractor - Uses NLP to extract and normalize skills from text
"""

import re
from typing import List, Set, Dict
from config.settings import SKILL_CATEGORIES, SKILL_ALIASES

class SkillExtractor:
    def __init__(self):
        # Build comprehensive skill list from categories
        self.all_skills = []
        for category, skills in SKILL_CATEGORIES.items():
            self.all_skills.extend(skills)
        
        # Add common variations
        self.skill_patterns = self._build_skill_patterns()
    
    def extract_from_text(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills from text and categorize them
        
        Args:
            text: Resume or JD text
            
        Returns:
            Dictionary with categorized skills
        """
        found_skills = set()
        
        # Extract using predefined skill list
        for skill in self.all_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.add(skill)
        
        # Normalize aliases
        normalized_skills = self._normalize_skills(found_skills, text)
        
        # Categorize skills
        categorized = self._categorize_skills(normalized_skills)
        
        return categorized
    
    def _build_skill_patterns(self) -> Dict[str, str]:
        """Build regex patterns for skill matching"""
        patterns = {}
        for skill in self.all_skills:
            # Create pattern that matches the skill with word boundaries
            patterns[skill] = r'\b' + re.escape(skill) + r'\b'
        return patterns
    
    def _normalize_skills(self, skills: Set[str], text: str) -> Set[str]:
        """Normalize skill names using aliases"""
        normalized = set(skills)
        
        # Check for aliases in text
        for alias, canonical in SKILL_ALIASES.items():
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                normalized.add(canonical)
        
        return normalized
    
    def _categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
        """Categorize skills into technical categories"""
        categorized = {
            'programming_languages': [],
            'web_frameworks': [],
            'databases': [],
            'cloud_platforms': [],
            'devops_tools': [],
            'data_science': [],
            'mobile': [],
            'other_technical': []
        }
        
        for skill in skills:
            categorized_flag = False
            for category, skill_list in SKILL_CATEGORIES.items():
                if skill in skill_list:
                    categorized[category].append(skill)
                    categorized_flag = True
                    break
            
            # If not categorized, add to other_technical
            if not categorized_flag:
                categorized['other_technical'].append(skill)
        
        # Sort each category
        for category in categorized:
            categorized[category].sort()
        
        # Add total count
        categorized['all_skills'] = sorted(list(skills))
        
        return categorized
    
    def extract_from_resume(self, resume_data: Dict) -> Dict[str, List[str]]:
        """
        Extract skills from parsed resume data
        
        Args:
            resume_data: Parsed resume dictionary
            
        Returns:
            Categorized skills
        """
        # Prioritize skills section if available
        text = resume_data.get('sections', {}).get('skills', '')
        
        # If no skills section, use full text
        if not text:
            text = resume_data.get('raw_text', '')
        
        return self.extract_from_text(text)
    
    def extract_from_jd(self, jd_data: Dict) -> Dict[str, List[str]]:
        """
        Extract skills from parsed JD data
        
        Args:
            jd_data: Parsed JD dictionary
            
        Returns:
            Categorized skills with required/preferred split
        """
        # Get already extracted skills from JD parser
        required = set(jd_data.get('required_skills', []))
        preferred = set(jd_data.get('preferred_skills', []))
        
        # Also extract from full text to catch any missed skills
        all_extracted = self.extract_from_text(jd_data.get('raw_text', ''))
        all_skills_set = set(all_extracted.get('all_skills', []))
        
        # Combine
        required = required.union(all_skills_set)
        
        return {
            'required_skills': sorted(list(required)),
            'preferred_skills': sorted(list(preferred)),
            'all_skills': sorted(list(required.union(preferred))),
            'categorized': self._categorize_skills(required.union(preferred))
        }
    
    def compare_skills(self, resume_skills: List[str], jd_skills: List[str]) -> Dict:
        """
        Compare resume skills with JD requirements
        
        Args:
            resume_skills: List of skills from resume
            jd_skills: List of required skills from JD
            
        Returns:
            Comparison results
        """
        resume_set = set(skill.lower() for skill in resume_skills)
        jd_set = set(skill.lower() for skill in jd_skills)
        
        matched = resume_set.intersection(jd_set)
        missing = jd_set - resume_set
        extra = resume_set - jd_set
        
        match_percentage = (len(matched) / len(jd_set) * 100) if jd_set else 0
        
        return {
            'matched_skills': sorted(list(matched)),
            'missing_skills': sorted(list(missing)),
            'extra_skills': sorted(list(extra)),
            'match_percentage': round(match_percentage, 2),
            'matched_count': len(matched),
            'total_required': len(jd_set)
        }


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Convenience function to extract skills from text
    
    Args:
        text: Input text
        
    Returns:
        Categorized skills
    """
    extractor = SkillExtractor()
    return extractor.extract_from_text(text)

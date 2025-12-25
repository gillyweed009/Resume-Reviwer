"""
Job Description Parser - Extracts requirements and skills from job descriptions
"""

import re
from typing import Dict, List, Set
from config.settings import SKILL_CATEGORIES

class JDParser:
    def __init__(self):
        self.text = ""
        
    def parse(self, jd_text: str) -> Dict:
        """
        Parse job description and extract structured information
        
        Args:
            jd_text: Job description text
            
        Returns:
            Dictionary containing extracted requirements
        """
        self.text = jd_text
        
        result = {
            'raw_text': jd_text,
            'required_skills': self._extract_required_skills(),
            'preferred_skills': self._extract_preferred_skills(),
            'experience_required': self._extract_experience_requirement(),
            'education_required': self._extract_education_requirement(),
            'job_title': self._extract_job_title(),
            'responsibilities': self._extract_responsibilities()
        }
        
        return result
    
    def _extract_job_title(self) -> str:
        """Extract job title from JD"""
        # Usually in the first few lines
        lines = self.text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            # Job titles are usually short and in the beginning
            if 5 < len(line) < 100 and not line.startswith(('http', 'www')):
                # Common job title patterns
                if any(word in line.lower() for word in ['engineer', 'developer', 'analyst', 'manager', 'designer', 'scientist']):
                    return line
        
        return "Not specified"
    
    def _extract_required_skills(self) -> List[str]:
        """Extract required/must-have skills"""
        skills = set()
        
        # Look for required skills section
        required_section = self._extract_section(r'required|must have|essential|qualifications')
        
        # Extract skills from all known categories
        all_skills = []
        for category, skill_list in SKILL_CATEGORIES.items():
            all_skills.extend(skill_list)
        
        # Search for skills in required section (or full text if no section found)
        search_text = required_section if required_section else self.text
        
        for skill in all_skills:
            # Case-insensitive search with word boundaries
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, search_text, re.IGNORECASE):
                skills.add(skill)
        
        return sorted(list(skills))
    
    def _extract_preferred_skills(self) -> List[str]:
        """Extract preferred/nice-to-have skills"""
        skills = set()
        
        # Look for preferred skills section
        preferred_section = self._extract_section(r'preferred|nice to have|bonus|plus')
        
        if not preferred_section:
            return []
        
        # Extract skills from all known categories
        all_skills = []
        for category, skill_list in SKILL_CATEGORIES.items():
            all_skills.extend(skill_list)
        
        for skill in all_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, preferred_section, re.IGNORECASE):
                skills.add(skill)
        
        return sorted(list(skills))
    
    def _extract_experience_requirement(self) -> str:
        """Extract required years of experience"""
        # Patterns for experience requirements
        patterns = [
            r'(\d+)\+?\s*years?.*?experience',
            r'(\d+)\s*-\s*(\d+)\s*years?',
            r'experience.*?(\d+)\+?\s*years?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            if matches:
                match = matches[0]
                if isinstance(match, tuple):
                    return f"{match[0]}-{match[1]} years" if len(match) > 1 else f"{match[0]}+ years"
                else:
                    return f"{match}+ years"
        
        # Check for fresher/entry-level
        if re.search(r'\b(fresher|entry.level|0.years|fresh graduate)\b', self.text, re.IGNORECASE):
            return "0-1 years (Fresher)"
        
        return "Not specified"
    
    def _extract_education_requirement(self) -> str:
        """Extract education requirements"""
        education_keywords = {
            'B.Tech': r'\b(B\.?Tech|Bachelor.*?Technology)\b',
            'B.E.': r'\b(B\.?E\.?|Bachelor.*?Engineering)\b',
            'M.Tech': r'\b(M\.?Tech|Master.*?Technology)\b',
            'M.E.': r'\b(M\.?E\.?|Master.*?Engineering)\b',
            'Bachelor': r'\bBachelor',
            'Master': r'\bMaster',
            'PhD': r'\b(PhD|Ph\.D\.?|Doctorate)\b',
            'Any Graduate': r'\b(any graduate|graduate|degree)\b'
        }
        
        found_education = []
        for edu, pattern in education_keywords.items():
            if re.search(pattern, self.text, re.IGNORECASE):
                found_education.append(edu)
        
        return ', '.join(found_education) if found_education else "Not specified"
    
    def _extract_responsibilities(self) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []
        
        # Look for responsibilities section
        resp_section = self._extract_section(r'responsibilities|duties|role|what you.*?do')
        
        if resp_section:
            # Split by bullet points or newlines
            lines = resp_section.split('\n')
            for line in lines:
                line = line.strip()
                # Remove bullet point markers
                line = re.sub(r'^[•\-\*\d+\.]\s*', '', line)
                if len(line) > 20 and len(line) < 300:  # Reasonable responsibility length
                    responsibilities.append(line)
        
        return responsibilities[:5]  # Return top 5 responsibilities
    
    def _extract_section(self, section_pattern: str) -> str:
        """Extract a specific section from JD based on header pattern"""
        lines = self.text.split('\n')
        section_content = []
        in_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Check if this is the section we're looking for
            if re.search(section_pattern, line_lower, re.IGNORECASE) and len(line.split()) <= 8:
                in_section = True
                continue
            
            # Check if we've hit another section header (stop collecting)
            if in_section and len(line.split()) <= 8:
                # Common section headers that indicate end of current section
                if re.search(r'^(required|preferred|responsibilities|qualifications|benefits|about|location|salary)', 
                           line_lower):
                    # Only stop if it's not the same section
                    if not re.search(section_pattern, line_lower):
                        break
            
            if in_section:
                section_content.append(line)
        
        return '\n'.join(section_content)


def parse_job_description(jd_text: str) -> Dict:
    """
    Convenience function to parse a job description
    
    Args:
        jd_text: Job description text
        
    Returns:
        Parsed JD data
    """
    parser = JDParser()
    return parser.parse(jd_text)

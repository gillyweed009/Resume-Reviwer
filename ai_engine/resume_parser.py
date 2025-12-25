"""
Resume Parser - Extracts text and structured information from PDF and DOCX files
"""

import re
from typing import Dict, List, Optional
import PyPDF2
import docx

class ResumeParser:
    def __init__(self):
        self.text = ""
        self.sections = {}
        
    def parse_file(self, file_path: str) -> Dict:
        """
        Parse resume file and extract structured information
        
        Args:
            file_path: Path to resume file (PDF or DOCX)
            
        Returns:
            Dictionary containing extracted information
        """
        # Extract text based on file type
        if file_path.endswith('.pdf'):
            self.text = self._extract_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            self.text = self._extract_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF or DOCX.")
        
        # Extract structured information
        result = {
            'raw_text': self.text,
            'email': self._extract_email(),
            'phone': self._extract_phone(),
            'education': self._extract_education(),
            'experience_years': self._estimate_experience(),
            'sections': self._identify_sections()
        }
        
        return result
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        return text
    
    def _extract_email(self) -> Optional[str]:
        """Extract email address from resume text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, self.text)
        return matches[0] if matches else None
    
    def _extract_phone(self) -> Optional[str]:
        """Extract phone number from resume text"""
        # Matches various phone formats
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        matches = re.findall(phone_pattern, self.text)
        return matches[0] if matches else None
    
    def _extract_education(self) -> List[str]:
        """Extract education information"""
        education_keywords = ['B.Tech', 'B.E.', 'M.Tech', 'M.E.', 'Bachelor', 'Master', 
                             'PhD', 'B.S.', 'M.S.', 'MBA', 'BCA', 'MCA']
        
        education = []
        lines = self.text.split('\n')
        
        for line in lines:
            for keyword in education_keywords:
                if keyword.lower() in line.lower():
                    education.append(line.strip())
                    break
        
        return education
    
    def _estimate_experience(self) -> float:
        """Estimate years of experience from resume"""
        # Look for experience section and date patterns
        experience_patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\s*-\s*(\d+)\s*years?'
        ]
        
        years = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        years.append(int(match[0]))
                    else:
                        years.append(int(match))
        
        # Also look for date ranges (e.g., 2020-2023)
        date_pattern = r'(20\d{2})\s*[-–]\s*(20\d{2}|Present|Current)'
        date_matches = re.findall(date_pattern, self.text, re.IGNORECASE)
        
        if date_matches:
            total_exp = 0
            for start, end in date_matches:
                start_year = int(start)
                end_year = 2024 if end.lower() in ['present', 'current'] else int(end)
                total_exp += (end_year - start_year)
            return total_exp
        
        return max(years) if years else 0
    
    def _identify_sections(self) -> Dict[str, str]:
        """Identify and extract major resume sections"""
        sections = {}
        section_headers = {
            'education': r'education|academic|qualification',
            'experience': r'experience|employment|work history',
            'skills': r'skills|technical skills|competencies',
            'projects': r'projects|portfolio',
            'certifications': r'certifications?|licenses?'
        }
        
        lines = self.text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line is a section header
            matched_section = None
            for section_name, pattern in section_headers.items():
                if re.search(pattern, line_lower) and len(line.split()) <= 5:
                    matched_section = section_name
                    break
            
            if matched_section:
                # Save previous section
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)
                
                # Start new section
                current_section = matched_section
                section_content = []
            elif current_section:
                section_content.append(line)
        
        # Save last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        return sections


def parse_resume(file_path: str) -> Dict:
    """
    Convenience function to parse a resume file
    
    Args:
        file_path: Path to resume file
        
    Returns:
        Parsed resume data
    """
    parser = ResumeParser()
    return parser.parse_file(file_path)

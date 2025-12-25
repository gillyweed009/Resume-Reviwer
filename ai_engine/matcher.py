"""
Matcher - Calculates fit score between resume and job description
"""

from typing import Dict
from config.settings import SCORING_WEIGHTS

class Matcher:
    def __init__(self):
        self.weights = SCORING_WEIGHTS
    
    def calculate_match_score(self, resume_data: Dict, jd_data: Dict, 
                             resume_skills: Dict, jd_skills: Dict,
                             skill_comparison: Dict) -> Dict:
        """
        Calculate overall match score between resume and JD
        
        Args:
            resume_data: Parsed resume data
            jd_data: Parsed JD data
            resume_skills: Extracted resume skills
            jd_skills: Extracted JD skills
            skill_comparison: Skill comparison results
            
        Returns:
            Match score and breakdown
        """
        # Component scores
        skills_score = self._calculate_skills_score(skill_comparison)
        experience_score = self._calculate_experience_score(resume_data, jd_data)
        education_score = self._calculate_education_score(resume_data, jd_data)
        semantic_score = self._calculate_semantic_score(resume_data, jd_data)
        
        # Weighted overall score
        overall_score = (
            skills_score * self.weights['skills_match'] +
            experience_score * self.weights['experience_match'] +
            education_score * self.weights['education_match'] +
            semantic_score * self.weights['semantic_similarity']
        )
        
        # Determine fit level
        fit_level = self._determine_fit_level(overall_score)
        
        return {
            'overall_score': round(overall_score, 2),
            'fit_level': fit_level,
            'breakdown': {
                'skills_match': round(skills_score, 2),
                'experience_match': round(experience_score, 2),
                'education_match': round(education_score, 2),
                'semantic_similarity': round(semantic_score, 2)
            },
            'weights_used': self.weights,
            'recommendation': self._generate_recommendation(overall_score, skill_comparison)
        }
    
    def _calculate_skills_score(self, skill_comparison: Dict) -> float:
        """Calculate score based on skill matching"""
        match_percentage = skill_comparison.get('match_percentage', 0)
        
        # Convert percentage to 0-100 score
        # Give bonus for exceeding 80% match
        if match_percentage >= 80:
            return min(100, match_percentage + 10)
        else:
            return match_percentage
    
    def _calculate_experience_score(self, resume_data: Dict, jd_data: Dict) -> float:
        """Calculate score based on experience match"""
        resume_exp = resume_data.get('experience_years', 0)
        jd_exp_str = jd_data.get('experience_required', '0')
        
        # Parse JD experience requirement
        import re
        exp_match = re.search(r'(\d+)', jd_exp_str)
        required_exp = int(exp_match.group(1)) if exp_match else 0
        
        # Scoring logic
        if required_exp == 0:  # Fresher role
            return 100 if resume_exp <= 2 else 80
        
        if resume_exp >= required_exp:
            # Has required experience
            if resume_exp <= required_exp + 2:
                return 100  # Perfect match
            else:
                return 90  # Overqualified but still good
        else:
            # Less experience than required
            gap = required_exp - resume_exp
            if gap <= 1:
                return 70  # Close enough
            elif gap <= 2:
                return 50  # Significant gap
            else:
                return 30  # Large gap
    
    def _calculate_education_score(self, resume_data: Dict, jd_data: Dict) -> float:
        """Calculate score based on education match"""
        resume_edu = resume_data.get('education', [])
        jd_edu = jd_data.get('education_required', '')
        
        if not jd_edu or 'not specified' in jd_edu.lower():
            return 100  # No specific requirement
        
        # Check if resume has any of the required education
        resume_edu_str = ' '.join(resume_edu).lower()
        jd_edu_lower = jd_edu.lower()
        
        # Check for degree matches
        degree_keywords = ['b.tech', 'b.e.', 'bachelor', 'm.tech', 'm.e.', 'master', 'phd']
        
        for keyword in degree_keywords:
            if keyword in jd_edu_lower and keyword in resume_edu_str:
                return 100
        
        # Partial match
        if any(edu in resume_edu_str for edu in ['bachelor', 'b.tech', 'b.e.', 'graduate']):
            return 80
        
        return 50  # No clear match
    
    def _calculate_semantic_score(self, resume_data: Dict, jd_data: Dict) -> float:
        """
        Calculate semantic similarity between resume and JD
        For MVP, using simple keyword overlap
        """
        resume_text = resume_data.get('raw_text', '').lower()
        jd_text = jd_data.get('raw_text', '').lower()
        
        # Extract key terms from JD (excluding common words)
        import re
        jd_words = set(re.findall(r'\b\w{4,}\b', jd_text))  # Words with 4+ chars
        resume_words = set(re.findall(r'\b\w{4,}\b', resume_text))
        
        # Remove common words
        common_words = {'that', 'this', 'with', 'from', 'have', 'will', 'your', 
                       'their', 'about', 'would', 'there', 'which', 'when', 'where',
                       'experience', 'work', 'team', 'role', 'company', 'years'}
        
        jd_words = jd_words - common_words
        resume_words = resume_words - common_words
        
        # Calculate overlap
        if not jd_words:
            return 70  # Default if no meaningful words
        
        overlap = len(jd_words.intersection(resume_words))
        similarity = (overlap / len(jd_words)) * 100
        
        return min(100, similarity * 1.2)  # Slight boost, cap at 100
    
    def _determine_fit_level(self, score: float) -> str:
        """Determine fit level based on score"""
        if score >= 85:
            return "Excellent Fit"
        elif score >= 70:
            return "Good Fit"
        elif score >= 55:
            return "Moderate Fit"
        elif score >= 40:
            return "Below Average Fit"
        else:
            return "Poor Fit"
    
    def _generate_recommendation(self, score: float, skill_comparison: Dict) -> str:
        """Generate actionable recommendation based on score"""
        missing_count = len(skill_comparison.get('missing_skills', []))
        
        if score >= 85:
            return "Strong candidate! Apply with confidence. Highlight your matching skills prominently in your application."
        elif score >= 70:
            if missing_count <= 2:
                return "Good match! Consider learning the missing skills quickly or emphasize transferable skills in your application."
            else:
                return "Decent fit, but focus on acquiring the key missing skills before applying for best results."
        elif score >= 55:
            return f"Moderate fit. You're missing {missing_count} key skills. Invest 2-4 weeks in learning these before applying."
        elif score >= 40:
            return f"Significant skill gaps detected. Consider this role as a stretch goal and focus on building foundational skills first."
        else:
            return "This role may not be the best fit right now. Focus on roles that better match your current skill set."


def calculate_match(resume_data: Dict, jd_data: Dict, resume_skills: Dict, 
                   jd_skills: Dict, skill_comparison: Dict) -> Dict:
    """
    Convenience function to calculate match score
    
    Args:
        resume_data: Parsed resume
        jd_data: Parsed JD
        resume_skills: Resume skills
        jd_skills: JD skills
        skill_comparison: Skill comparison
        
    Returns:
        Match score and details
    """
    matcher = Matcher()
    return matcher.calculate_match_score(resume_data, jd_data, resume_skills, 
                                        jd_skills, skill_comparison)

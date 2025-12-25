"""
Gap Analyzer - Identifies and prioritizes skill gaps
"""

from typing import Dict, List

class GapAnalyzer:
    def analyze_gaps(self, skill_comparison: Dict, jd_data: Dict) -> Dict:
        """
        Analyze skill gaps and prioritize them
        
        Args:
            skill_comparison: Skill comparison results
            jd_data: Parsed JD data
            
        Returns:
            Gap analysis with prioritization
        """
        missing_skills = skill_comparison.get('missing_skills', [])
        matched_skills = skill_comparison.get('matched_skills', [])
        
        # Prioritize missing skills
        critical_gaps = self._identify_critical_gaps(missing_skills, jd_data)
        nice_to_have_gaps = self._identify_nice_to_have_gaps(missing_skills, jd_data)
        
        # Analyze strength of matched skills
        skill_strengths = self._analyze_skill_strengths(matched_skills)
        
        return {
            'total_gaps': len(missing_skills),
            'critical_gaps': critical_gaps,
            'nice_to_have_gaps': nice_to_have_gaps,
            'matched_skills': matched_skills,
            'skill_strengths': skill_strengths,
            'gap_summary': self._generate_gap_summary(critical_gaps, nice_to_have_gaps),
            'priority_order': self._prioritize_learning(critical_gaps, nice_to_have_gaps)
        }
    
    def _identify_critical_gaps(self, missing_skills: List[str], jd_data: Dict) -> List[Dict]:
        """Identify critical/must-have missing skills"""
        required_skills = set(skill.lower() for skill in jd_data.get('required_skills', []))
        
        critical = []
        for skill in missing_skills:
            if skill.lower() in required_skills:
                critical.append({
                    'skill': skill.title(),
                    'priority': 'High',
                    'category': self._categorize_single_skill(skill),
                    'reason': 'Required by job description'
                })
        
        return critical
    
    def _identify_nice_to_have_gaps(self, missing_skills: List[str], jd_data: Dict) -> List[Dict]:
        """Identify nice-to-have missing skills"""
        preferred_skills = set(skill.lower() for skill in jd_data.get('preferred_skills', []))
        required_skills = set(skill.lower() for skill in jd_data.get('required_skills', []))
        
        nice_to_have = []
        for skill in missing_skills:
            if skill.lower() in preferred_skills or skill.lower() not in required_skills:
                nice_to_have.append({
                    'skill': skill.title(),
                    'priority': 'Medium',
                    'category': self._categorize_single_skill(skill),
                    'reason': 'Preferred or complementary skill'
                })
        
        return nice_to_have
    
    def _analyze_skill_strengths(self, matched_skills: List[str]) -> Dict:
        """Analyze the strength of matched skills"""
        if not matched_skills:
            return {'level': 'None', 'count': 0}
        
        count = len(matched_skills)
        
        if count >= 8:
            level = 'Excellent'
        elif count >= 5:
            level = 'Strong'
        elif count >= 3:
            level = 'Moderate'
        else:
            level = 'Basic'
        
        return {
            'level': level,
            'count': count,
            'skills': [skill.title() for skill in matched_skills]
        }
    
    def _categorize_single_skill(self, skill: str) -> str:
        """Categorize a single skill"""
        from config.settings import SKILL_CATEGORIES
        
        skill_lower = skill.lower()
        for category, skills in SKILL_CATEGORIES.items():
            if any(s.lower() == skill_lower for s in skills):
                return category.replace('_', ' ').title()
        
        return 'Technical Skill'
    
    def _generate_gap_summary(self, critical_gaps: List[Dict], 
                             nice_to_have_gaps: List[Dict]) -> str:
        """Generate human-readable gap summary"""
        critical_count = len(critical_gaps)
        nice_count = len(nice_to_have_gaps)
        
        if critical_count == 0 and nice_count == 0:
            return "Excellent! You have all the required skills for this role."
        elif critical_count == 0:
            return f"You have all critical skills! {nice_count} nice-to-have skill(s) could strengthen your profile."
        elif critical_count <= 2:
            return f"You're close! Focus on {critical_count} critical skill(s) to significantly improve your fit."
        elif critical_count <= 5:
            return f"Moderate gaps detected. {critical_count} critical skills need attention. Plan 3-4 weeks of focused learning."
        else:
            return f"Significant gaps found. {critical_count} critical skills missing. This role might be a stretch goal - consider building fundamentals first."
    
    def _prioritize_learning(self, critical_gaps: List[Dict], 
                            nice_to_have_gaps: List[Dict]) -> List[Dict]:
        """Prioritize skills in learning order"""
        # Critical skills first, then nice-to-have
        priority_list = []
        
        # Add critical gaps with priority 1
        for i, gap in enumerate(critical_gaps[:5]):  # Top 5 critical
            priority_list.append({
                'rank': i + 1,
                'skill': gap['skill'],
                'priority': 'Critical',
                'category': gap['category'],
                'estimated_time': self._estimate_learning_time(gap['skill'])
            })
        
        # Add nice-to-have with lower priority
        start_rank = len(priority_list) + 1
        for i, gap in enumerate(nice_to_have_gaps[:3]):  # Top 3 nice-to-have
            priority_list.append({
                'rank': start_rank + i,
                'skill': gap['skill'],
                'priority': 'Nice-to-have',
                'category': gap['category'],
                'estimated_time': self._estimate_learning_time(gap['skill'])
            })
        
        return priority_list
    
    def _estimate_learning_time(self, skill: str) -> str:
        """Estimate time needed to learn a skill"""
        skill_lower = skill.lower()
        
        # Programming languages - longer learning curve
        if any(lang in skill_lower for lang in ['python', 'java', 'javascript', 'c++', 'go']):
            return '4-6 weeks'
        
        # Frameworks - medium learning curve
        elif any(fw in skill_lower for fw in ['react', 'angular', 'django', 'spring', 'node']):
            return '2-4 weeks'
        
        # Tools and platforms - shorter learning curve
        elif any(tool in skill_lower for tool in ['docker', 'git', 'aws', 'kubernetes']):
            return '1-2 weeks'
        
        # Databases
        elif any(db in skill_lower for db in ['sql', 'mongodb', 'postgresql', 'mysql']):
            return '2-3 weeks'
        
        # Default
        else:
            return '2-3 weeks'


def analyze_skill_gaps(skill_comparison: Dict, jd_data: Dict) -> Dict:
    """
    Convenience function to analyze skill gaps
    
    Args:
        skill_comparison: Skill comparison results
        jd_data: Parsed JD data
        
    Returns:
        Gap analysis
    """
    analyzer = GapAnalyzer()
    return analyzer.analyze_gaps(skill_comparison, jd_data)

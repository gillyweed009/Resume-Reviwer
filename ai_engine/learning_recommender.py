"""
Learning Recommender - Generates personalized learning paths
"""

from typing import Dict, List
from config.settings import LEARNING_RESOURCES, DEFAULT_LEARNING_RESOURCE

class LearningRecommender:
    def __init__(self):
        self.resources = LEARNING_RESOURCES
        self.default_resource = DEFAULT_LEARNING_RESOURCE
    
    def generate_learning_path(self, gap_analysis: Dict) -> Dict:
        """
        Generate personalized learning path based on skill gaps
        
        Args:
            gap_analysis: Gap analysis results
            
        Returns:
            Learning path with courses and resources
        """
        priority_skills = gap_analysis.get('priority_order', [])
        
        learning_path = []
        total_estimated_time = 0
        
        for skill_item in priority_skills:
            skill = skill_item['skill']
            recommendations = self._get_skill_recommendations(skill)
            
            learning_path.append({
                'skill': skill,
                'priority': skill_item['priority'],
                'rank': skill_item['rank'],
                'category': skill_item['category'],
                'estimated_time': skill_item['estimated_time'],
                'courses': recommendations['courses'],
                'practice_resources': recommendations['practice'],
                'learning_tips': self._get_learning_tips(skill)
            })
            
            # Calculate total time (rough estimate in weeks)
            time_str = skill_item['estimated_time']
            weeks = self._parse_time_to_weeks(time_str)
            total_estimated_time += weeks
        
        return {
            'learning_path': learning_path,
            'total_skills_to_learn': len(learning_path),
            'estimated_total_time': f"{total_estimated_time} weeks",
            'learning_strategy': self._generate_learning_strategy(learning_path),
            'milestones': self._create_milestones(learning_path)
        }
    
    def _get_skill_recommendations(self, skill: str) -> Dict:
        """Get course recommendations for a specific skill"""
        # Normalize skill name
        skill_normalized = skill.title()
        
        # Check if we have curated resources for this skill
        if skill_normalized in self.resources:
            return self.resources[skill_normalized]
        
        # Check for partial matches
        for resource_skill in self.resources.keys():
            if skill.lower() in resource_skill.lower() or resource_skill.lower() in skill.lower():
                return self.resources[resource_skill]
        
        # Return default if no match found
        return self.default_resource
    
    def _get_learning_tips(self, skill: str) -> List[str]:
        """Get learning tips for specific skill"""
        skill_lower = skill.lower()
        
        # Programming languages
        if any(lang in skill_lower for lang in ['python', 'java', 'javascript']):
            return [
                "Start with fundamentals and syntax",
                "Build small projects to practice",
                "Solve coding problems daily (LeetCode/HackerRank)",
                "Read others' code to learn best practices"
            ]
        
        # Frameworks
        elif any(fw in skill_lower for fw in ['react', 'angular', 'django', 'node']):
            return [
                "Learn the underlying language first if needed",
                "Follow official documentation and tutorials",
                "Build a complete project using the framework",
                "Study popular open-source projects"
            ]
        
        # Cloud platforms
        elif any(cloud in skill_lower for cloud in ['aws', 'azure', 'gcp']):
            return [
                "Use free tier for hands-on practice",
                "Focus on core services first",
                "Get certified to validate knowledge",
                "Build and deploy real applications"
            ]
        
        # DevOps tools
        elif any(tool in skill_lower for tool in ['docker', 'kubernetes', 'git']):
            return [
                "Learn through hands-on practice",
                "Integrate into your existing projects",
                "Understand the problem it solves",
                "Practice with real-world scenarios"
            ]
        
        # Default tips
        else:
            return [
                "Start with beginner-friendly tutorials",
                "Practice consistently (30-60 min daily)",
                "Build projects to apply knowledge",
                "Join communities for support"
            ]
    
    def _parse_time_to_weeks(self, time_str: str) -> int:
        """Parse time string to weeks (rough average)"""
        import re
        matches = re.findall(r'(\d+)', time_str)
        if matches:
            # Take average if range given
            numbers = [int(m) for m in matches]
            return sum(numbers) // len(numbers)
        return 2  # Default 2 weeks
    
    def _generate_learning_strategy(self, learning_path: List[Dict]) -> str:
        """Generate overall learning strategy"""
        total_skills = len(learning_path)
        critical_count = sum(1 for item in learning_path if item['priority'] == 'Critical')
        
        if total_skills == 0:
            return "You're already well-matched! Focus on deepening existing skills."
        elif critical_count <= 2:
            return f"Focus intensively on {critical_count} critical skill(s) first. Dedicate 2-3 hours daily for fastest results. Then explore nice-to-have skills."
        elif critical_count <= 4:
            return f"Moderate learning required. Prioritize {critical_count} critical skills. Learn in parallel if possible (e.g., theory for one, practice for another). Allocate 3-4 weeks."
        else:
            return f"Significant learning ahead. Break it into phases: Master 2-3 foundational skills first, then build on them. Consider this a 2-3 month journey."
    
    def _create_milestones(self, learning_path: List[Dict]) -> List[Dict]:
        """Create learning milestones"""
        milestones = []
        
        if not learning_path:
            return milestones
        
        # Milestone 1: First critical skill
        critical_skills = [item for item in learning_path if item['priority'] == 'Critical']
        if critical_skills:
            first_skill = critical_skills[0]
            milestones.append({
                'milestone': 'Week 1-2',
                'goal': f"Master {first_skill['skill']}",
                'action': f"Complete primary course and build 1-2 small projects"
            })
        
        # Milestone 2: Complete all critical skills
        if len(critical_skills) > 1:
            milestones.append({
                'milestone': 'Week 3-4',
                'goal': f"Complete all {len(critical_skills)} critical skills",
                'action': "Build an integrated project using multiple skills"
            })
        
        # Milestone 3: Nice-to-have skills
        nice_to_have = [item for item in learning_path if item['priority'] == 'Nice-to-have']
        if nice_to_have:
            milestones.append({
                'milestone': 'Week 5-6',
                'goal': "Add complementary skills",
                'action': f"Learn {', '.join([s['skill'] for s in nice_to_have[:2]])}"
            })
        
        # Final milestone
        milestones.append({
            'milestone': 'Final',
            'goal': "Apply for the role with confidence",
            'action': "Update resume, build portfolio project, practice interviews"
        })
        
        return milestones


def generate_recommendations(gap_analysis: Dict) -> Dict:
    """
    Convenience function to generate learning recommendations
    
    Args:
        gap_analysis: Gap analysis results
        
    Returns:
        Learning path and recommendations
    """
    recommender = LearningRecommender()
    return recommender.generate_learning_path(gap_analysis)

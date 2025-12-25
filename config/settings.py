"""
Configuration settings for the Resume Analyzer application
"""

# Scoring weights for different components
SCORING_WEIGHTS = {
    'skills_match': 0.50,      # 50% weight on skills matching
    'experience_match': 0.20,   # 20% weight on experience level
    'education_match': 0.15,    # 15% weight on education
    'semantic_similarity': 0.15 # 15% weight on overall semantic match
}

# Skill categories for better organization
SKILL_CATEGORIES = {
    'programming_languages': ['Python', 'Java', 'JavaScript', 'C++', 'C', 'Go', 'Rust', 'TypeScript', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala'],
    'web_frameworks': ['React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'FastAPI', 'Spring Boot', 'Next.js', 'Svelte'],
    'databases': ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'DynamoDB', 'SQLite', 'Oracle', 'SQL Server'],
    'cloud_platforms': ['AWS', 'Azure', 'GCP', 'Google Cloud', 'Heroku', 'DigitalOcean', 'Firebase'],
    'devops_tools': ['Docker', 'Kubernetes', 'Jenkins', 'Git', 'GitHub', 'GitLab', 'CI/CD', 'Terraform', 'Ansible'],
    'data_science': ['Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy', 'Data Analysis'],
    'mobile': ['Android', 'iOS', 'React Native', 'Flutter', 'SwiftUI'],
    'other_technical': ['REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'Testing', 'Unit Testing']
}

# Common skill aliases for normalization
SKILL_ALIASES = {
    'js': 'JavaScript',
    'ts': 'TypeScript',
    'py': 'Python',
    'react.js': 'React',
    'reactjs': 'React',
    'node': 'Node.js',
    'nodejs': 'Node.js',
    'k8s': 'Kubernetes',
    'aws': 'AWS',
    'gcp': 'GCP',
    'ml': 'Machine Learning',
    'dl': 'Deep Learning',
    'api': 'REST API',
}

# Curated learning resources for common skills
LEARNING_RESOURCES = {
    'Python': {
        'courses': [
            {'name': 'Python for Everybody', 'platform': 'Coursera', 'duration': '8 weeks', 'level': 'Beginner'},
            {'name': 'Complete Python Bootcamp', 'platform': 'Udemy', 'duration': '22 hours', 'level': 'Beginner'},
        ],
        'practice': 'LeetCode, HackerRank Python track'
    },
    'JavaScript': {
        'courses': [
            {'name': 'JavaScript - The Complete Guide', 'platform': 'Udemy', 'duration': '52 hours', 'level': 'Beginner'},
            {'name': 'Modern JavaScript', 'platform': 'Coursera', 'duration': '6 weeks', 'level': 'Intermediate'},
        ],
        'practice': 'JavaScript30, FreeCodeCamp'
    },
    'React': {
        'courses': [
            {'name': 'React - The Complete Guide', 'platform': 'Udemy', 'duration': '48 hours', 'level': 'Intermediate'},
            {'name': 'Meta React Basics', 'platform': 'Coursera', 'duration': '4 weeks', 'level': 'Beginner'},
        ],
        'practice': 'Build 5 projects, contribute to open source'
    },
    'Node.js': {
        'courses': [
            {'name': 'Node.js Developer Course', 'platform': 'Udemy', 'duration': '35 hours', 'level': 'Intermediate'},
            {'name': 'Server-side JavaScript with Node', 'platform': 'Coursera', 'duration': '4 weeks', 'level': 'Intermediate'},
        ],
        'practice': 'Build REST APIs, microservices projects'
    },
    'AWS': {
        'courses': [
            {'name': 'AWS Certified Solutions Architect', 'platform': 'Udemy', 'duration': '24 hours', 'level': 'Intermediate'},
            {'name': 'AWS Fundamentals', 'platform': 'Coursera', 'duration': '4 weeks', 'level': 'Beginner'},
        ],
        'practice': 'AWS Free Tier hands-on labs'
    },
    'Machine Learning': {
        'courses': [
            {'name': 'Machine Learning by Andrew Ng', 'platform': 'Coursera', 'duration': '11 weeks', 'level': 'Intermediate'},
            {'name': 'Machine Learning A-Z', 'platform': 'Udemy', 'duration': '44 hours', 'level': 'Beginner'},
        ],
        'practice': 'Kaggle competitions, personal ML projects'
    },
    'Docker': {
        'courses': [
            {'name': 'Docker Mastery', 'platform': 'Udemy', 'duration': '19 hours', 'level': 'Beginner'},
            {'name': 'Docker and Kubernetes', 'platform': 'Coursera', 'duration': '4 weeks', 'level': 'Intermediate'},
        ],
        'practice': 'Containerize your projects'
    },
    'SQL': {
        'courses': [
            {'name': 'The Complete SQL Bootcamp', 'platform': 'Udemy', 'duration': '9 hours', 'level': 'Beginner'},
            {'name': 'SQL for Data Science', 'platform': 'Coursera', 'duration': '4 weeks', 'level': 'Beginner'},
        ],
        'practice': 'SQLZoo, LeetCode database problems'
    },
}

# Default learning recommendation for skills not in the database
DEFAULT_LEARNING_RESOURCE = {
    'courses': [
        {'name': 'Search on Udemy', 'platform': 'Udemy', 'duration': 'Varies', 'level': 'All levels'},
        {'name': 'Search on Coursera', 'platform': 'Coursera', 'duration': 'Varies', 'level': 'All levels'},
    ],
    'practice': 'YouTube tutorials, official documentation'
}

# Processing settings
MAX_FILE_SIZE_MB = 5
SUPPORTED_FORMATS = ['.pdf', '.docx']
PROCESSING_TIMEOUT_SECONDS = 30

# Model settings (for future ML integration)
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'  # Lightweight and fast
SPACY_MODEL = 'en_core_web_sm'

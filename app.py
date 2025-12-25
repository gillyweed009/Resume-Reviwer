"""
Main Streamlit Application for AI Resume Match & Skill-Gap Analyzer
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from ai_engine.resume_parser import parse_resume
from ai_engine.jd_parser import parse_job_description
from ai_engine.skill_extractor import SkillExtractor
from ai_engine.matcher import calculate_match
from ai_engine.gap_analyzer import analyze_skill_gaps
from ai_engine.learning_recommender import generate_recommendations
from components.visualizations import (
    create_match_score_gauge,
    create_skills_comparison_chart,
    create_score_breakdown_chart,
    create_skill_category_radar,
    create_learning_timeline
)

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .skill-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .skill-matched {
        background-color: #d1fae5;
        color: #065f46;
    }
    .skill-missing {
        background-color: #fee2e2;
        color: #991b1b;
    }
    .recommendation-box {
        background-color: #f3f4f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 AI Resume Match & Skill-Gap Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Get instant feedback on your job fit • Identify skill gaps • Accelerate your career</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/resume.png", width=80)
        st.title("About")
        st.info("""
        **How it works:**
        1. Upload your resume (PDF/DOCX)
        2. Paste the job description
        3. Get instant AI-powered analysis
        
        **You'll receive:**
        - Match score (0-100)
        - Skill gap analysis
        - Personalized learning path
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Built for")
        st.markdown("✅ Fresh Graduates")
        st.markdown("✅ Job Seekers")
        st.markdown("✅ Recruiters")
        
        st.markdown("---")
        st.caption("Built with ❤️ using Streamlit & AI")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Upload Resume")
        resume_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx'],
            help="Upload your resume in PDF or DOCX format"
        )
        
        if resume_file:
            st.success(f"✅ Uploaded: {resume_file.name}")
    
    with col2:
        st.subheader("📋 Job Description")
        jd_input_method = st.radio(
            "How would you like to provide the JD?",
            ["Paste Text", "Upload File"],
            horizontal=True
        )
        
        jd_text = None
        if jd_input_method == "Paste Text":
            jd_text = st.text_area(
                "Paste the job description here",
                height=200,
                placeholder="Paste the complete job description including requirements, responsibilities, etc."
            )
        else:
            jd_file = st.file_uploader(
                "Upload JD file",
                type=['txt', 'pdf', 'docx'],
                key="jd_file"
            )
            if jd_file:
                st.success(f"✅ Uploaded: {jd_file.name}")
                # For MVP, we'll handle text files
                if jd_file.name.endswith('.txt'):
                    jd_text = jd_file.read().decode('utf-8')
    
    # Analyze button
    st.markdown("---")
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        analyze_button = st.button(
            "🚀 Analyze Match",
            type="primary",
            use_container_width=True
        )
    
    # Process and display results
    if analyze_button:
        if not resume_file:
            st.error("❌ Please upload your resume")
            return
        
        if not jd_text or len(jd_text.strip()) < 50:
            st.error("❌ Please provide a valid job description (minimum 50 characters)")
            return
        
        # Show processing
        with st.spinner("🔍 Analyzing your resume... This may take a few seconds..."):
            try:
                # Save uploaded file temporarily
                temp_resume_path = f"/tmp/{resume_file.name}"
                with open(temp_resume_path, "wb") as f:
                    f.write(resume_file.getbuffer())
                
                # Process
                resume_data = parse_resume(temp_resume_path)
                jd_data = parse_job_description(jd_text)
                
                # Extract skills
                skill_extractor = SkillExtractor()
                resume_skills = skill_extractor.extract_from_resume(resume_data)
                jd_skills = skill_extractor.extract_from_jd(jd_data)
                
                # Compare skills
                skill_comparison = skill_extractor.compare_skills(
                    resume_skills.get('all_skills', []),
                    jd_skills.get('required_skills', [])
                )
                
                # Calculate match
                match_result = calculate_match(
                    resume_data, jd_data, resume_skills, jd_skills, skill_comparison
                )
                
                # Analyze gaps
                gap_analysis = analyze_skill_gaps(skill_comparison, jd_data)
                
                # Generate recommendations
                learning_path = generate_recommendations(gap_analysis)
                
                # Clean up
                os.remove(temp_resume_path)
                
                # Display results
                display_results(
                    match_result, skill_comparison, gap_analysis, 
                    learning_path, resume_skills, jd_skills
                )
                
            except Exception as e:
                st.error(f"❌ Error processing files: {str(e)}")
                st.exception(e)

def display_results(match_result, skill_comparison, gap_analysis, learning_path, resume_skills, jd_skills):
    """Display analysis results in tabs"""
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Overview", "🔍 Skills Analysis", "📈 Skill Gaps", "📚 Learning Path"])
    
    with tab1:
        display_overview(match_result, skill_comparison)
    
    with tab2:
        display_skills_analysis(skill_comparison, resume_skills, jd_skills)
    
    with tab3:
        display_gap_analysis(gap_analysis)
    
    with tab4:
        display_learning_path(learning_path)

def display_overview(match_result, skill_comparison):
    """Display overview tab"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Match score gauge
        fig_gauge = create_match_score_gauge(
            match_result['overall_score'],
            match_result['fit_level']
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Score breakdown
        fig_breakdown = create_score_breakdown_chart(match_result['breakdown'])
        st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # Metrics row
    st.markdown("### 📈 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Score", f"{match_result['overall_score']}%")
    
    with col2:
        st.metric("Matched Skills", skill_comparison['matched_count'])
    
    with col3:
        st.metric("Missing Skills", len(skill_comparison['missing_skills']))
    
    with col4:
        st.metric("Fit Level", match_result['fit_level'])
    
    # Recommendation
    st.markdown("### 💡 Recommendation")
    st.markdown(f'<div class="recommendation-box">{match_result["recommendation"]}</div>', 
                unsafe_allow_html=True)

def display_skills_analysis(skill_comparison, resume_skills, jd_skills):
    """Display skills analysis tab"""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Skills comparison chart
        fig_comparison = create_skills_comparison_chart(
            skill_comparison['matched_skills'],
            skill_comparison['missing_skills']
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with col2:
        # Radar chart
        fig_radar = create_skill_category_radar(
            resume_skills.get('categorized', resume_skills),
            jd_skills.get('categorized', {})
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Matched skills
    st.markdown("### ✅ Matched Skills")
    if skill_comparison['matched_skills']:
        skills_html = "".join([
            f'<span class="skill-badge skill-matched">{skill.title()}</span>'
            for skill in skill_comparison['matched_skills']
        ])
        st.markdown(skills_html, unsafe_allow_html=True)
    else:
        st.info("No matched skills found")
    
    st.markdown("---")
    
    # Missing skills
    st.markdown("### ❌ Missing Skills")
    if skill_comparison['missing_skills']:
        skills_html = "".join([
            f'<span class="skill-badge skill-missing">{skill.title()}</span>'
            for skill in skill_comparison['missing_skills']
        ])
        st.markdown(skills_html, unsafe_allow_html=True)
    else:
        st.success("🎉 You have all the required skills!")

def display_gap_analysis(gap_analysis):
    """Display gap analysis tab"""
    
    st.markdown(f"### {gap_analysis['gap_summary']}")
    
    if gap_analysis['total_gaps'] == 0:
        st.balloons()
        st.success("🎉 Congratulations! You're an excellent match for this role!")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🔴 Critical Gaps (Must Have)")
        if gap_analysis['critical_gaps']:
            for gap in gap_analysis['critical_gaps']:
                with st.expander(f"**{gap['skill']}** - {gap['category']}"):
                    st.write(f"**Priority:** {gap['priority']}")
                    st.write(f"**Reason:** {gap['reason']}")
        else:
            st.success("✅ No critical gaps!")
    
    with col2:
        st.markdown("#### 🟡 Nice-to-Have Gaps")
        if gap_analysis['nice_to_have_gaps']:
            for gap in gap_analysis['nice_to_have_gaps'][:5]:
                with st.expander(f"**{gap['skill']}** - {gap['category']}"):
                    st.write(f"**Priority:** {gap['priority']}")
                    st.write(f"**Reason:** {gap['reason']}")
        else:
            st.info("No additional gaps")

def display_learning_path(learning_path):
    """Display learning path tab"""
    
    if learning_path['total_skills_to_learn'] == 0:
        st.success("🎉 You're already well-prepared! No additional learning needed.")
        return
    
    st.markdown(f"### 🎯 Your Personalized Learning Path")
    st.info(f"**Total Skills to Learn:** {learning_path['total_skills_to_learn']} | "
            f"**Estimated Time:** {learning_path['estimated_total_time']}")
    
    # Learning strategy
    st.markdown("#### 📋 Learning Strategy")
    st.markdown(f'<div class="recommendation-box">{learning_path["learning_strategy"]}</div>', 
                unsafe_allow_html=True)
    
    # Timeline visualization
    fig_timeline = create_learning_timeline(learning_path['learning_path'])
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed learning path
    st.markdown("#### 📚 Detailed Learning Plan")
    
    for item in learning_path['learning_path']:
        with st.expander(f"**#{item['rank']} {item['skill']}** - {item['priority']} Priority ({item['estimated_time']})"):
            st.markdown(f"**Category:** {item['category']}")
            
            st.markdown("**📖 Recommended Courses:**")
            for course in item['courses']:
                st.markdown(f"- **{course['name']}** ({course['platform']}) - {course['duration']} - {course['level']}")
            
            st.markdown(f"**🎯 Practice:** {item['practice_resources']}")
            
            st.markdown("**💡 Learning Tips:**")
            for tip in item['learning_tips']:
                st.markdown(f"- {tip}")
    
    # Milestones
    if learning_path.get('milestones'):
        st.markdown("#### 🎯 Learning Milestones")
        for milestone in learning_path['milestones']:
            st.markdown(f"**{milestone['milestone']}:** {milestone['goal']}")
            st.caption(f"→ {milestone['action']}")

if __name__ == "__main__":
    main()

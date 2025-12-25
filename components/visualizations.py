"""
Visualization Components for Resume Analyzer
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict

def create_match_score_gauge(score: float, fit_level: str) -> go.Figure:
    """Create a gauge chart for match score"""
    
    # Color based on score
    if score >= 85:
        color = "#10b981"  # Green
    elif score >= 70:
        color = "#3b82f6"  # Blue
    elif score >= 55:
        color = "#f59e0b"  # Orange
    else:
        color = "#ef4444"  # Red
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Match Score<br><span style='font-size:0.8em;color:gray'>{fit_level}</span>", 
               'font': {'size': 24}},
        number={'font': {'size': 48}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#fee2e2'},
                {'range': [40, 55], 'color': '#fed7aa'},
                {'range': [55, 70], 'color': '#fef3c7'},
                {'range': [70, 85], 'color': '#dbeafe'},
                {'range': [85, 100], 'color': '#d1fae5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'family': "Arial"}
    )
    
    return fig


def create_skills_comparison_chart(matched: List[str], missing: List[str]) -> go.Figure:
    """Create a bar chart comparing matched vs missing skills"""
    
    categories = ['Matched Skills', 'Missing Skills']
    values = [len(matched), len(missing)]
    colors = ['#10b981', '#ef4444']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            text=values,
            textposition='auto',
            marker_color=colors,
            hovertemplate='%{x}: %{y} skills<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="Skills Overview",
        xaxis_title="",
        yaxis_title="Number of Skills",
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={'family': "Arial"}
    )
    
    fig.update_yaxis(gridcolor='lightgray')
    
    return fig


def create_score_breakdown_chart(breakdown: Dict) -> go.Figure:
    """Create a horizontal bar chart for score breakdown"""
    
    components = list(breakdown.keys())
    scores = list(breakdown.values())
    
    # Beautify labels
    labels = {
        'skills_match': 'Skills Match',
        'experience_match': 'Experience Match',
        'education_match': 'Education Match',
        'semantic_similarity': 'Semantic Similarity'
    }
    
    display_labels = [labels.get(c, c) for c in components]
    
    # Color based on score
    colors = ['#10b981' if s >= 70 else '#f59e0b' if s >= 50 else '#ef4444' for s in scores]
    
    fig = go.Figure(go.Bar(
        x=scores,
        y=display_labels,
        orientation='h',
        text=[f"{s}%" for s in scores],
        textposition='auto',
        marker_color=colors,
        hovertemplate='%{y}: %{x}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="Score Breakdown",
        xaxis_title="Score (%)",
        yaxis_title="",
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={'family': "Arial"},
        xaxis=dict(range=[0, 100])
    )
    
    fig.update_xaxis(gridcolor='lightgray')
    
    return fig


def create_skill_category_radar(resume_skills: Dict, jd_skills: Dict) -> go.Figure:
    """Create a radar chart comparing skill categories"""
    
    categories = ['Programming Languages', 'Web Frameworks', 'Databases', 
                 'Cloud Platforms', 'DevOps Tools']
    
    category_keys = ['programming_languages', 'web_frameworks', 'databases',
                    'cloud_platforms', 'devops_tools']
    
    resume_counts = []
    jd_counts = []
    
    for key in category_keys:
        resume_counts.append(len(resume_skills.get(key, [])))
        jd_counts.append(len(jd_skills.get(key, [])))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=jd_counts,
        theta=categories,
        fill='toself',
        name='Required',
        line_color='#ef4444',
        fillcolor='rgba(239, 68, 68, 0.2)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=resume_counts,
        theta=categories,
        fill='toself',
        name='Your Skills',
        line_color='#10b981',
        fillcolor='rgba(16, 185, 129, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(resume_counts + jd_counts, default=1), 5)]
            )),
        showlegend=True,
        title="Skill Category Comparison",
        height=400,
        margin=dict(l=80, r=80, t=60, b=20),
        paper_bgcolor="white",
        font={'family': "Arial"}
    )
    
    return fig


def create_learning_timeline(learning_path: List[Dict]) -> go.Figure:
    """Create a timeline visualization for learning path"""
    
    if not learning_path:
        # Return empty figure
        fig = go.Figure()
        fig.update_layout(
            title="No learning path needed - you're already a great match!",
            height=200
        )
        return fig
    
    skills = [item['skill'] for item in learning_path[:6]]  # Top 6
    priorities = [item['priority'] for item in learning_path[:6]]
    times = [item['estimated_time'] for item in learning_path[:6]]
    
    # Color by priority
    colors = ['#ef4444' if p == 'Critical' else '#3b82f6' for p in priorities]
    
    fig = go.Figure(go.Bar(
        y=skills,
        x=[1] * len(skills),  # All same width
        orientation='h',
        marker_color=colors,
        text=[f"{t}" for t in times],
        textposition='auto',
        hovertemplate='%{y}<br>Time: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Learning Priority Order",
        xaxis_title="",
        yaxis_title="",
        height=max(250, len(skills) * 50),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={'family': "Arial"},
        showlegend=False,
        xaxis=dict(showticklabels=False, showgrid=False)
    )
    
    return fig

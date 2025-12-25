# Sample Data Directory

This directory contains sample resumes and job descriptions for testing and demonstration purposes.

## Job Descriptions

1. **jd_fullstack.txt** - Full Stack Developer role (React, Node.js, Python)
2. **jd_datascience.txt** - Data Scientist role (ML, Python, Analytics)
3. **jd_devops.txt** - DevOps Engineer role (Docker, Kubernetes, AWS)

## How to Use

### Testing the Application

1. **Create a sample resume** or use your own resume (PDF or DOCX format)
2. **Use one of the sample JDs** provided above
3. **Run the app**: `streamlit run app.py`
4. **Upload your resume** and paste the JD text
5. **Click "Analyze Match"** to see results

### Expected Results

Different resumes will show different match scores based on:
- Skills alignment
- Experience level
- Education background
- Overall semantic similarity

### Creating Your Own Test Data

To create additional test cases:

1. **For Resumes:**
   - Create PDF or DOCX files
   - Include sections: Education, Experience, Skills, Projects
   - Use realistic content with technical skills

2. **For Job Descriptions:**
   - Create .txt files
   - Include: Job title, required skills, preferred skills, experience, responsibilities
   - Use clear formatting

### Demo Scenarios

**Scenario 1: Perfect Match**
- Resume with React, Node.js, Python, SQL, Git
- Use jd_fullstack.txt
- Expected: 85-95% match score

**Scenario 2: Moderate Fit**
- Resume with Python, basic web development
- Use jd_fullstack.txt
- Expected: 60-75% match score

**Scenario 3: Skill Gap**
- Resume with only Java and basic programming
- Use jd_datascience.txt
- Expected: 30-50% match score, many learning recommendations

## Notes

- Sample JDs are designed for fresh graduates (0-2 years experience)
- All JDs include both required and preferred skills for better testing
- JDs cover different tech domains (Web Dev, Data Science, DevOps)

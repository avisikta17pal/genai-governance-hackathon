# pyright: reportMissingImports=false
"""
GenAI Governance System - Streamlit App Entry Point
This file serves as the entry point for Streamlit Community Cloud deployment.
"""

# Import all necessary modules
import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import random

# Page configuration
st.set_page_config(
    page_title="GenAI Governance System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .risk-high {
        color: #dc3545;
        font-weight: bold;
    }
    .risk-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .risk-low {
        color: #28a745;
        font-weight: bold;
    }
    .compliance-good {
        color: #28a745;
        font-weight: bold;
    }
    .compliance-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .compliance-bad {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = []

# Backend API configuration
BACKEND_URL = "http://localhost:8000"

# Check if running in Streamlit Cloud
import os
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

def log_audit_event(action: str, user_id: str, risk_level: str = 'low', compliance_status: str = 'compliant', details: str = ''):
    """Log audit events"""
    audit_event = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'action': action,
        'risk_level': risk_level,
        'compliance_status': compliance_status,
        'session_id': st.session_state.session_id,
        'details': details
    }
    
    if 'audit_logs' not in st.session_state:
        st.session_state.audit_logs = []
    
    st.session_state.audit_logs.append(audit_event)

def login_user(username: str, password: str) -> bool:
    """Authenticate user with backend"""
    try:
        # For demo purposes, simulate authentication
        # In production, this would call the actual backend API
        
        demo_users = {
            'admin': {'role': 'admin', 'user_id': 'admin_001'},
            'manager': {'role': 'manager', 'user_id': 'manager_001'},
            'analyst': {'role': 'analyst', 'user_id': 'analyst_001'},
            'user': {'role': 'user', 'user_id': 'user_001'}
        }
        
        if username in demo_users:
            user_info = demo_users[username]
            st.session_state.authenticated = True
            st.session_state.user_info = user_info
            st.session_state.session_id = f"session_{int(time.time())}"
            
            # Log the login event
            log_audit_event(
                action='user_login',
                user_id=user_info['user_id'],
                risk_level='low',
                compliance_status='compliant',
                details=f'User {username} logged in successfully'
            )
            
            return True
        else:
            # Log failed login attempt
            log_audit_event(
                action='login_failed',
                user_id='unknown',
                risk_level='medium',
                compliance_status='needs_review',
                details=f'Failed login attempt for username: {username}'
            )
            return False
            
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False

def process_genai_request(prompt: str, user_info: Dict) -> Dict:
    """Process GenAI request through governance system"""
    try:
        # Simulate backend API call
        # In production, this would make actual HTTP requests
        
        # Simulate processing time
        time.sleep(1)
        
        # Simulate different responses based on prompt content
        prompt_lower = prompt.lower()

        # Allow medical 'attack' phrases
        medical_attack_phrases = [
            "heart attack", "panic attack", "asthma attack", "migraine attack", "seizure attack"
        ]
        if any(phrase in prompt_lower for phrase in medical_attack_phrases):
            # Let it fall through to the medical info logic
            pass
        else:
            # High-risk keywords detection
            high_risk_keywords = [
                "hack", "exploit", "phishing", "malware", "virus", "cyber", "illegal",
                "bomb", "weapon", "kill", "violence", "harm", "backdoor", "breach", "ddos", "attack"
            ]
            if any(word in prompt_lower for word in high_risk_keywords):
                response = (
                    "I cannot provide assistance with harmful, illegal, or dangerous content. "
                    "Please ensure your requests are appropriate and comply with our usage policies."
                )
                risk_level = 'high'
                compliance_status = 'blocked'
                return {
                    'response': response,
                    'risk_assessment': {
                        'risk_level': risk_level,
                        'risk_score': 0.9,
                        'risk_factors': ['content_analysis', 'domain_specific_risks']
                    },
                    'compliance_status': compliance_status,
                    'audit_trail': [
                        {'agent': 'prompt_guard', 'status': 'completed'},
                        {'agent': 'policy_enforcer', 'status': 'completed'},
                        {'agent': 'output_auditor', 'status': 'completed'}
                    ],
                    'recommendations': [
                        'Always verify AI-generated information',
                        'Use appropriate disclaimers',
                        'Maintain audit trails',
                        'Consult professionals for specialized advice'
                    ]
                }
        
        if 'diabetes' in prompt_lower and ('symptom' in prompt_lower or 'treat' in prompt_lower):
            response = """**Diabetes Symptoms and Treatment Information:**

**Common Symptoms:**
- Frequent urination (polyuria)
- Increased thirst (polydipsia)
- Unexplained weight loss
- Fatigue and weakness
- Blurred vision
- Slow-healing wounds
- Tingling or numbness in hands/feet

**Treatment Approaches:**
- **Type 1 Diabetes**: Insulin therapy, blood sugar monitoring, diet management
- **Type 2 Diabetes**: Lifestyle changes, oral medications, insulin if needed
- **Gestational Diabetes**: Diet control, exercise, monitoring

**Lifestyle Management:**
- Regular exercise
- Healthy diet (low glycemic index foods)
- Blood sugar monitoring
- Regular medical check-ups

⚠️ **Important Disclaimer:** This is general educational information only. Always consult a healthcare professional for proper diagnosis and personalized treatment plans."""
            risk_level = 'medium'
            compliance_status = 'compliant'
            
        elif ('marketing' in prompt_lower or 'email' in prompt_lower) and ('generate' in prompt_lower or 'create' in prompt_lower or 'write' in prompt_lower):
            response = """**Marketing Email Template:**

**Subject Line:** [Your Product] - Transform Your [Benefit]

**Email Body:**
Dear [Customer Name],

We're excited to introduce [Your Product], designed to [main benefit].

**Key Features:**
- [Feature 1] - [Benefit]
- [Feature 2] - [Benefit]
- [Feature 3] - [Benefit]

**Call to Action:** [Clear, compelling action]

Best regards,
[Your Name]
[Company Name]

**Tips for Effective Marketing:**
- Personalize content
- Clear value proposition
- Strong call-to-action
- Mobile-friendly design
- A/B test subject lines"""
            risk_level = 'low'
            compliance_status = 'compliant'
            
        # Smartphone buying tips
        elif 'smartphone' in prompt_lower and ('buy' in prompt_lower or 'tip' in prompt_lower):
            response = """**Best Smartphone Buying Tips:**

**1. Determine Your Budget:**
- Set a realistic budget range
- Consider total cost of ownership (phone + plan)

**2. Choose Your Operating System:**
- **iOS (iPhone)**: Seamless ecosystem, regular updates, premium feel
- **Android**: More variety, customization options, different price points

**3. Key Features to Consider:**
- **Camera Quality**: Check megapixels, aperture, and reviews
- **Battery Life**: Look for 4000mAh+ for all-day use
- **Storage**: 128GB minimum, 256GB+ recommended
- **RAM**: 6GB+ for smooth performance
- **Display**: OLED/AMOLED for better colors, 90Hz+ for smooth scrolling

**4. Research Before Buying:**
- Read expert reviews (GSMArena, The Verge, TechRadar)
- Check user reviews on Amazon, Best Buy
- Compare specs on comparison sites
- Watch YouTube reviews for real-world testing

**5. Best Time to Buy:**
- Black Friday/Cyber Monday
- New model releases (older models get discounted)
- Carrier promotions and trade-in deals

**6. Popular Options by Budget:**
- **Budget ($200-400)**: Samsung Galaxy A series, Google Pixel 6a
- **Mid-range ($400-700)**: iPhone SE, Samsung Galaxy S series, Google Pixel 7
- **Premium ($700+)**: iPhone 15 Pro, Samsung Galaxy S24 Ultra, Google Pixel 8 Pro

**7. Don't Forget:**
- Screen protector and case
- Extended warranty for expensive phones
- Check carrier compatibility
- Consider refurbished options for savings

⚠️ **Disclaimer:** This is general advice. Always research specific models and read recent reviews before purchasing."""
            risk_level = 'low'
            compliance_status = 'compliant'
            
        elif 'heart attack' in prompt_lower and 'symptom' in prompt_lower:
            response = """**Heart Attack Symptoms and Information:**

**Common Symptoms:**
- **Chest Pain/Pressure**: Feeling of tightness, pressure, or squeezing in the center of the chest
- **Pain Spreading**: Discomfort that spreads to arms, neck, jaw, or back
- **Shortness of Breath**: Difficulty breathing, even at rest
- **Cold Sweat**: Sudden cold, clammy skin
- **Nausea/Vomiting**: Feeling sick to stomach
- **Lightheadedness**: Dizziness or feeling faint
- **Fatigue**: Unusual tiredness, especially in women

**Emergency Signs (Call 911 Immediately):**
- Chest pain lasting more than 5 minutes
- Pain spreading to arms, neck, or jaw
- Shortness of breath with chest discomfort
- Cold sweat, nausea, or lightheadedness

**Risk Factors:**
- High blood pressure
- High cholesterol
- Smoking
- Diabetes
- Family history
- Age (men over 45, women over 55)

**Prevention:**
- Regular exercise
- Healthy diet (low sodium, low fat)
- Quit smoking
- Manage stress
- Regular check-ups

⚠️ **Important Disclaimer:** This is general educational information only. If you experience these symptoms, call emergency services immediately. Always consult a healthcare professional for proper diagnosis and treatment."""
            risk_level = 'medium'
            compliance_status = 'compliant'
            
        elif 'diabetes' in prompt_lower and ('symptom' in prompt_lower or 'treat' in prompt_lower):
            response = """**Diabetes Symptoms and Treatment Information:**

**Common Symptoms:**
- Frequent urination (polyuria)
- Increased thirst (polydipsia)
- Unexplained weight loss
- Fatigue and weakness
- Blurred vision
- Slow-healing wounds
- Tingling or numbness in hands/feet

**Treatment Approaches:**
- **Type 1 Diabetes**: Insulin therapy, blood sugar monitoring, diet management
- **Type 2 Diabetes**: Lifestyle changes, oral medications, insulin if needed
- **Gestational Diabetes**: Diet control, exercise, monitoring

**Lifestyle Management:**
- Regular exercise
- Healthy diet (low glycemic index foods)
- Blood sugar monitoring
- Regular medical check-ups

⚠️ **Important Disclaimer:** This is general educational information only. Always consult a healthcare professional for proper diagnosis and personalized treatment plans."""
            risk_level = 'medium'
            compliance_status = 'compliant'
            
        elif 'depression' in prompt_lower and 'symptom' in prompt_lower:
            response = """**Depression Symptoms and Information:**

**Common Symptoms:**
- **Persistent Sadness**: Feeling sad, empty, or hopeless most of the day
- **Loss of Interest**: No longer enjoying activities you used to love
- **Changes in Appetite**: Significant weight loss or gain, changes in eating habits
- **Sleep Problems**: Insomnia or sleeping too much
- **Fatigue**: Feeling tired and having little energy
- **Difficulty Concentrating**: Trouble thinking, making decisions, or remembering
- **Feelings of Worthlessness**: Excessive guilt or feeling like a failure
- **Thoughts of Death**: Recurrent thoughts of death or suicide

**Physical Symptoms:**
- Slowed movements or speech
- Unexplained aches and pains
- Digestive problems
- Headaches or migraines

**Risk Factors:**
- Family history of depression
- Major life changes or stress
- Medical conditions
- Certain medications
- Substance abuse

**When to Seek Help:**
- Symptoms lasting more than 2 weeks
- Symptoms interfering with daily life
- Thoughts of self-harm or suicide
- Difficulty functioning at work or school

**Treatment Options:**
- **Therapy**: Cognitive behavioral therapy (CBT), talk therapy
- **Medication**: Antidepressants (prescribed by healthcare provider)
- **Lifestyle Changes**: Exercise, healthy diet, stress management
- **Support Groups**: Connecting with others experiencing similar challenges

**Crisis Resources:**
- **National Suicide Prevention Lifeline**: 988 (US)
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911 for immediate danger

⚠️ **Important Disclaimer:** This is general educational information only. Depression is a serious medical condition that requires professional diagnosis and treatment. If you're experiencing these symptoms, please consult a mental health professional immediately."""
            risk_level = 'medium'
            compliance_status = 'compliant'
            
        elif 'anxiety' in prompt_lower and ('symptom' in prompt_lower or 'attack' in prompt_lower):
            response = """**Anxiety Symptoms and Information:**

**Common Symptoms:**
- **Excessive Worry**: Persistent, uncontrollable worry about everyday things
- **Restlessness**: Feeling on edge, restless, or keyed up
- **Fatigue**: Easily tired, even without physical exertion
- **Difficulty Concentrating**: Mind going blank, trouble focusing
- **Irritability**: Easily annoyed or irritable
- **Muscle Tension**: Tense muscles, aches, or soreness
- **Sleep Problems**: Trouble falling or staying asleep, restless sleep

**Physical Symptoms:**
- **Rapid Heartbeat**: Heart racing or pounding
- **Shortness of Breath**: Feeling like you can't get enough air
- **Sweating**: Excessive sweating, especially hands
- **Trembling**: Shaking or trembling
- **Dizziness**: Feeling lightheaded or faint
- **Nausea**: Upset stomach or feeling sick
- **Hot Flashes**: Sudden feeling of heat

**Panic Attack Symptoms:**
- Sudden, intense fear or discomfort
- Chest pain or discomfort
- Feeling of choking
- Nausea or abdominal distress
- Feeling detached from reality
- Fear of losing control or dying

**Types of Anxiety Disorders:**
- **Generalized Anxiety Disorder (GAD)**: Chronic worry about various things
- **Panic Disorder**: Recurrent panic attacks
- **Social Anxiety**: Fear of social situations
- **Specific Phobias**: Intense fear of specific objects or situations

**Coping Strategies:**
- **Deep Breathing**: Slow, controlled breathing exercises
- **Progressive Muscle Relaxation**: Tense and relax muscle groups
- **Mindfulness**: Focus on present moment
- **Regular Exercise**: Physical activity reduces anxiety
- **Limit Caffeine**: Can worsen anxiety symptoms
- **Get Enough Sleep**: 7-9 hours per night

**When to Seek Help:**
- Symptoms interfering with daily life
- Panic attacks
- Persistent worry for 6+ months
- Physical symptoms without medical cause
- Thoughts of self-harm

⚠️ **Important Disclaimer:** This is general educational information only. Anxiety disorders are medical conditions that require professional diagnosis and treatment. If you're experiencing these symptoms, please consult a mental health professional."""
            risk_level = 'medium'
            compliance_status = 'compliant'
            
        elif 'customer data' in prompt_lower and ('analyze' in prompt_lower or 'help' in prompt_lower):
            response = """**Legal Customer Data Analysis Guidelines:**

**✅ What You CAN Do:**
- Analyze anonymized/aggregated data
- Use data with proper consent
- Follow GDPR/CCPA compliance
- Implement data retention policies
- Use secure data processing tools

**❌ What You CANNOT Do:**
- Process personal data without consent
- Share identifiable customer information
- Use data for unauthorized purposes
- Retain data longer than necessary
- Ignore data subject rights

**Best Practices:**
1. **Data Minimization**: Only collect what you need
2. **Consent Management**: Clear, specific consent
3. **Security Measures**: Encryption, access controls
4. **Audit Trails**: Track all data processing
5. **Regular Reviews**: Update privacy policies

**Compliance Frameworks:**
- **GDPR**: EU data protection
- **CCPA**: California privacy law
- **HIPAA**: Healthcare data (if applicable)
- **SOX**: Financial data controls

**Recommended Tools:**
- Data anonymization software
- Consent management platforms
- Privacy impact assessments
- Regular compliance audits

⚠️ **Disclaimer:** This is general guidance. Consult legal professionals for specific compliance requirements."""
            risk_level = 'medium'
            compliance_status = 'compliant'
            
        elif 'medical' in prompt_lower or ('health' in prompt_lower and 'care' not in prompt_lower) or any(phrase in prompt_lower for phrase in medical_attack_phrases):
            # Check for specific medical conditions
            if 'heart attack' in prompt_lower and ('symptom' in prompt_lower or 'sign' in prompt_lower):
                response = """**Heart Attack Symptoms and Information:**

**Common Symptoms:**
- **Chest Pain/Pressure**: Feeling of tightness, pressure, or squeezing in the center of the chest
- **Pain Spreading**: Discomfort that spreads to arms, neck, jaw, or back
- **Shortness of Breath**: Difficulty breathing, even at rest
- **Cold Sweat**: Sudden cold, clammy skin
- **Nausea/Vomiting**: Feeling sick to stomach
- **Lightheadedness**: Dizziness or feeling faint
- **Fatigue**: Unusual tiredness, especially in women

**Emergency Signs (Call 911 Immediately):**
- Chest pain lasting more than 5 minutes
- Pain spreading to arms, neck, or jaw
- Shortness of breath with chest discomfort
- Cold sweat, nausea, or lightheadedness

**Risk Factors:**
- High blood pressure
- High cholesterol
- Smoking
- Diabetes
- Family history
- Age (men over 45, women over 55)

**Prevention:**
- Regular exercise
- Healthy diet (low sodium, low fat)
- Quit smoking
- Manage stress
- Regular check-ups

⚠️ **Important Disclaimer:** This is general educational information only. If you experience these symptoms, call emergency services immediately. Always consult a healthcare professional for proper diagnosis and treatment."""
                risk_level = 'medium'
                compliance_status = 'compliant'
            else:
                response = """I can provide general health information, but please consult a healthcare professional for specific medical advice. This is for informational purposes only.

**For medical questions, I recommend:**
- Consulting your primary care physician
- Visiting a healthcare provider
- Using reliable medical websites (Mayo Clinic, WebMD, etc.)
- Calling emergency services for urgent concerns

⚠️ **Medical Disclaimer:** This information is for educational purposes only and should not replace professional medical advice."""
                risk_level = 'medium'
                compliance_status = 'needs_review'
        
        elif 'financial' in prompt_lower or 'investment' in prompt_lower:
            response = """I can provide general financial education, but please consult a licensed financial advisor for specific investment advice. Past performance does not guarantee future results.

**General Financial Tips:**
- Diversify your investments
- Consider your risk tolerance
- Plan for long-term goals
- Emergency fund (3-6 months expenses)
- Regular portfolio review

⚠️ **Financial Disclaimer:** This is educational content only. Consult a licensed financial advisor for personalized advice."""
            risk_level = 'medium'
            compliance_status = 'needs_review'
            
        elif 'legal' in prompt_lower or 'law' in prompt_lower:
            response = """I can provide general legal information, but please consult a licensed attorney for specific legal advice. This is for informational purposes only.

**General Legal Resources:**
- Legal aid organizations
- State bar associations
- Public legal information websites
- Law libraries

⚠️ **Legal Disclaimer:** This information is for educational purposes only and does not constitute legal advice."""
            risk_level = 'medium'
            compliance_status = 'needs_review'
            
        else:
            # Generate more dynamic responses based on query type
            if 'how to' in prompt_lower or 'guide' in prompt_lower:
                response = f"""**Step-by-Step Guide for: '{prompt}'**

**1. Research Phase:**
- Gather relevant information from reliable sources
- Identify key requirements and constraints
- Create a structured plan

**2. Implementation:**
- Break down into manageable steps
- Set realistic timelines
- Monitor progress regularly

**3. Quality Assurance:**
- Test and validate results
- Gather feedback
- Iterate and improve

**4. Best Practices:**
- Document your process
- Learn from mistakes
- Stay updated with latest trends

⚠️ **Disclaimer:** This is general guidance. Adapt to your specific needs and consult experts when necessary."""
                risk_level = 'low'
                compliance_status = 'compliant'
                
            elif 'what is' in prompt_lower or 'explain' in prompt_lower:
                response = f"""**Explanation: '{prompt}'**

**Definition:**
This refers to a concept, process, or system that involves multiple components working together.

**Key Components:**
- Core elements and their functions
- Relationships between components
- Input and output processes
- Quality control measures

**Applications:**
- Real-world use cases
- Industry applications
- Benefits and advantages
- Potential challenges

**Best Practices:**
- Understand fundamentals first
- Practice with examples
- Stay updated with developments
- Network with experts

⚠️ **Disclaimer:** This is educational information. For specific applications, consult relevant professionals."""
                risk_level = 'low'
                compliance_status = 'compliant'
                
            elif 'compare' in prompt_lower or 'difference' in prompt_lower:
                response = f"""**Comparison Analysis: '{prompt}'**

**Key Differences:**

**Option A:**
- Strengths and advantages
- Use cases and applications
- Limitations and drawbacks

**Option B:**
- Strengths and advantages
- Use cases and applications
- Limitations and drawbacks

**Decision Factors:**
- Cost considerations
- Time requirements
- Resource availability
- Long-term implications

**Recommendation Framework:**
- Define your specific needs
- Evaluate against criteria
- Consider trade-offs
- Plan for implementation

⚠️ **Disclaimer:** This comparison is general. Consider your specific context and requirements."""
                risk_level = 'low'
                compliance_status = 'compliant'
                
            elif 'tips' in prompt_lower or 'advice' in prompt_lower:
                response = f"""**Pro Tips for: '{prompt}'**

**Essential Tips:**
1. **Start with the basics** - Master fundamentals first
2. **Practice consistently** - Regular practice builds skills
3. **Learn from experts** - Follow industry leaders
4. **Stay updated** - Keep current with latest trends
5. **Network actively** - Connect with like-minded professionals

**Advanced Strategies:**
- **Optimization techniques** for better results
- **Time management** for efficiency
- **Quality control** measures
- **Continuous improvement** mindset

**Common Mistakes to Avoid:**
- Rushing without proper planning
- Ignoring feedback and criticism
- Not staying updated with changes
- Working in isolation

**Success Metrics:**
- Define clear goals
- Track progress regularly
- Celebrate small wins
- Learn from setbacks

⚠️ **Disclaimer:** These tips are general guidance. Adapt to your specific situation."""
                risk_level = 'low'
                compliance_status = 'compliant'
                
            else:
                response = f"""**Comprehensive Response to: '{prompt}'**

**Overview:**
This topic involves multiple aspects that work together to achieve desired outcomes.

**Key Components:**
- **Core Elements**: Fundamental building blocks
- **Processes**: Step-by-step procedures
- **Tools**: Resources and technologies
- **Outcomes**: Expected results and benefits

**Implementation Strategy:**
1. **Assessment Phase**: Evaluate current state
2. **Planning Phase**: Design approach and timeline
3. **Execution Phase**: Implement with monitoring
4. **Review Phase**: Evaluate and optimize

**Best Practices:**
- Start with clear objectives
- Use proven methodologies
- Monitor progress regularly
- Adapt to changing circumstances
- Document lessons learned

**Success Factors:**
- Strong foundation and preparation
- Consistent effort and dedication
- Continuous learning and improvement
- Collaboration and teamwork
- Quality focus and attention to detail

⚠️ **Disclaimer:** This is general information. For specific applications, consult relevant experts and consider your unique circumstances."""
                risk_level = 'low'
                compliance_status = 'compliant'
        
        # Log the AI interaction
        log_audit_event(
            action='genai_interaction',
            user_id=user_info.get('user_id', 'unknown'),
            risk_level=risk_level,
            compliance_status=compliance_status,
            details=f'AI interaction: {prompt[:50]}...'
        )
        
        return {
            'response': response,
            'risk_assessment': {
                'risk_level': risk_level,
                'risk_score': 0.3 if risk_level == 'low' else 0.6 if risk_level == 'medium' else 0.9,
                'risk_factors': ['content_analysis', 'domain_specific_risks']
            },
            'compliance_status': compliance_status,
            'audit_trail': [
                {'agent': 'prompt_guard', 'status': 'completed'},
                {'agent': 'policy_enforcer', 'status': 'completed'},
                {'agent': 'output_auditor', 'status': 'completed'}
            ],
            'recommendations': [
                'Always verify AI-generated information',
                'Use appropriate disclaimers',
                'Maintain audit trails',
                'Consult professionals for specialized advice'
            ]
        }
        
    except Exception as e:
        return {
            'response': f"Error processing request: {str(e)}",
            'risk_assessment': {'risk_level': 'unknown'},
            'compliance_status': 'error',
            'audit_trail': [],
            'recommendations': ['Review system logs']
        }

def get_analytics_data() -> Dict:
    """Get analytics data for dashboard"""
    # Simulate analytics data
    return {
        'total_interactions': 1250,
        'compliance_rate': 0.98,
        'risk_distribution': {
            'low': 0.75,
            'medium': 0.20,
            'high': 0.05
        },
        'anomaly_detections': 12,
        'policy_violations': 8,
        'average_response_time': 145,
        'top_user_activities': [
            {'user_id': 'user_001', 'interactions': 45},
            {'user_id': 'user_002', 'interactions': 32},
            {'user_id': 'user_003', 'interactions': 28}
        ],
        'compliance_frameworks': {
            'gdpr': 0.95,
            'hipaa': 0.98,
            'sox': 0.92
        }
    }

def show_login_page():
    """Show login page"""
    st.markdown('<h2 class="sub-header">🔐 Login</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if login_user(username, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials. Try: admin/admin, manager/manager, analyst/analyst, user/user")
    
    # Demo credentials
    st.info("""
    **Demo Credentials:**
    - Username: `admin` | Password: `admin` (Full access)
    - Username: `manager` | Password: `manager` (Management access)
    - Username: `analyst` | Password: `analyst` (Analytics access)
    - Username: `user` | Password: `user` (Basic access)
    """)

def show_dashboard():
    """Show main dashboard"""
    st.markdown('<h2 class="sub-header">📊 Dashboard</h2>', unsafe_allow_html=True)
    
    analytics = get_analytics_data()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Interactions", f"{analytics['total_interactions']:,}")
    
    with col2:
        st.metric("Compliance Rate", f"{analytics['compliance_rate']*100:.1f}%")
    
    with col3:
        st.metric("Anomaly Detections", analytics['anomaly_detections'])
    
    with col4:
        st.metric("Avg Response Time", f"{analytics['average_response_time']}ms")
    
    # Risk distribution chart
    st.markdown("### Risk Distribution")
    risk_data = analytics['risk_distribution']
    fig = px.pie(
        values=list(risk_data.values()),
        names=list(risk_data.keys()),
        title="Risk Level Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_ai_chat():
    """Show AI chat interface"""
    st.markdown('<h2 class="sub-header">💬 AI Chat</h2>', unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process request through governance system
        with st.chat_message("assistant"):
            with st.spinner("Processing through governance system..."):
                result = process_genai_request(prompt, st.session_state.user_info)
                
                # Display response
                st.markdown(result['response'])
                
                # Display governance information
                with st.expander("🔒 Governance Details"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        risk_level = result['risk_assessment']['risk_level']
                        risk_class = f"risk-{risk_level}"
                        st.markdown(f"**Risk Level:** <span class='{risk_class}'>{risk_level.upper()}</span>", unsafe_allow_html=True)
                        
                        compliance_status = result['compliance_status']
                        compliance_class = "compliance-good" if compliance_status == 'compliant' else "compliance-warning" if compliance_status == 'needs_review' else "compliance-bad"
                        st.markdown(f"**Compliance:** <span class='{compliance_class}'>{compliance_status.upper()}</span>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("**Audit Trail:**")
                        for audit in result['audit_trail']:
                            st.markdown(f"- {audit['agent']}: {audit['status']}")
                    
                    st.markdown("**Recommendations:**")
                    for rec in result['recommendations']:
                        st.markdown(f"- {rec}")
                
                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": result['response']})

def show_audit_logs():
    """Show audit logs"""
    st.markdown('<h2 class="sub-header">📋 Audit Logs</h2>', unsafe_allow_html=True)
    
    # Get real audit logs from session state
    audit_logs = st.session_state.get('audit_logs', [])
    
    # Add some sample data if no logs exist yet
    if not audit_logs:
        audit_logs = [
            {
                'timestamp': datetime.utcnow().isoformat(),
                'user_id': 'system',
                'action': 'system_startup',
                'risk_level': 'low',
                'compliance_status': 'compliant',
                'session_id': 'system_session',
                'details': 'System initialized successfully'
            }
        ]
    
    # Create DataFrame
    df = pd.DataFrame(audit_logs)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_filter = st.selectbox("Risk Level", ["All"] + list(df['risk_level'].unique()))
    
    with col2:
        status_filter = st.selectbox("Compliance Status", ["All"] + list(df['compliance_status'].unique()))
    
    with col3:
        user_filter = st.selectbox("User", ["All"] + list(df['user_id'].unique()))
    
    # Apply filters
    filtered_df = df.copy()
    if risk_filter != "All":
        filtered_df = filtered_df[filtered_df['risk_level'] == risk_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['compliance_status'] == status_filter]
    if user_filter != "All":
        filtered_df = filtered_df[filtered_df['user_id'] == user_filter]
    
    # Display filtered logs
    st.dataframe(filtered_df, use_container_width=True)

def show_analytics():
    """Show analytics dashboard"""
    st.markdown('<h2 class="sub-header">📈 Analytics</h2>', unsafe_allow_html=True)
    
    analytics = get_analytics_data()
    
    # User activity chart
    st.markdown("### User Activity")
    user_data = pd.DataFrame(analytics['top_user_activities'])
    fig = px.bar(user_data, x='user_id', y='interactions', title="Top Users by Interactions")
    st.plotly_chart(fig, use_container_width=True)
    
    # Compliance trends
    st.markdown("### Compliance Trends")
    compliance_data = analytics['compliance_frameworks']
    fig = px.bar(
        x=list(compliance_data.keys()),
        y=list(compliance_data.values()),
        title="Compliance Framework Scores",
        labels={'x': 'Framework', 'y': 'Score'}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_policy_management():
    """Show policy management interface"""
    st.markdown('<h2 class="sub-header">⚖️ Policy Management</h2>', unsafe_allow_html=True)
    
    # Only allow admins to access policy management
    if st.session_state.user_info.get('role') != 'admin':
        st.warning("Only administrators can access policy management.")
        return
    
    # Policy categories
    policy_categories = ['Data Privacy', 'Security', 'Ethical AI', 'Regulatory']
    
    selected_category = st.selectbox("Select Policy Category", policy_categories)
    
    # Simulate policy data
    policies = {
        'Data Privacy': {
            'gdpr_compliance': 'Enabled',
            'data_minimization': 'Enabled',
            'consent_management': 'Enabled'
        },
        'Security': {
            'encryption': 'Enabled',
            'access_controls': 'Enabled',
            'audit_logging': 'Enabled'
        },
        'Ethical AI': {
            'bias_detection': 'Enabled',
            'transparency': 'Enabled',
            'fairness': 'Enabled'
        },
        'Regulatory': {
            'sox_compliance': 'Enabled',
            'hipaa_compliance': 'Enabled',
            'pci_compliance': 'Enabled'
        }
    }
    
    # Display policies
    st.markdown(f"### {selected_category} Policies")
    
    for policy, status in policies[selected_category].items():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{policy.replace('_', ' ').title()}**")
        
        with col2:
            st.markdown(f"Status: {status}")
        
        with col3:
            if st.button(f"Edit {policy}", key=policy):
                st.info(f"Edit functionality for {policy} would be implemented here")

def show_feedback():
    """Show feedback interface"""
    st.markdown('<h2 class="sub-header">💭 Feedback</h2>', unsafe_allow_html=True)
    
    # Feedback form
    with st.form("feedback_form"):
        st.markdown("### Submit Feedback")
        
        session_id = st.text_input("Session ID (optional)", value=st.session_state.session_id or "")
        rating = st.slider("Rating", 1, 5, 3)
        feedback_text = st.text_area("Feedback", placeholder="Please provide your feedback about the system...")
        
        submit_feedback = st.form_submit_button("Submit Feedback")
        
        if submit_feedback:
            if feedback_text.strip():
                st.success("Thank you for your feedback! It has been submitted anonymously for analysis.")
                
                # Simulate feedback processing
                with st.expander("Feedback Analysis"):
                    st.markdown("**Categories:** Usability, Compliance")
                    st.markdown("**Sentiment:** Positive")
                    st.markdown("**Suggestions:** Improve response time, enhance user interface")
            else:
                st.error("Please provide feedback text.")

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 GenAI Governance System</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    if not st.session_state.authenticated:
        show_login_page()
    else:
        # User info in sidebar
        st.sidebar.markdown(f"**Welcome, {st.session_state.user_info.get('user_id', 'User')}**")
        st.sidebar.markdown(f"**Role:** {st.session_state.user_info.get('role', 'User').title()}")
        st.sidebar.markdown(f"**Session:** {st.session_state.session_id}")
        
        # Navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Dashboard", "AI Chat", "Audit Logs", "Analytics", "Policy Management", "Feedback"]
        )
        
        # Logout button
        if st.sidebar.button("Logout"):
            # Log the logout event
            log_audit_event(
                action='user_logout',
                user_id=st.session_state.user_info.get('user_id', 'unknown'),
                risk_level='low',
                compliance_status='compliant',
                details='User logged out successfully'
            )
            
            st.session_state.authenticated = False
            st.session_state.user_info = {}
            st.session_state.session_id = None
            st.rerun()
        
        # Page routing
        if page == "Dashboard":
            show_dashboard()
        elif page == "AI Chat":
            show_ai_chat()
        elif page == "Audit Logs":
            show_audit_logs()
        elif page == "Analytics":
            show_analytics()
        elif page == "Policy Management":
            show_policy_management()
        elif page == "Feedback":
            show_feedback()

if __name__ == "__main__":
    main() 
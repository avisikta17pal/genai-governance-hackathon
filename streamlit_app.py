"""
GenAI Governance System - Streamlit App Entry Point
This file serves as the entry point for Streamlit Community Cloud deployment.
"""

# Import all necessary modules
import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional

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

# Backend API configuration
BACKEND_URL = "http://localhost:8000"

# Check if running in Streamlit Cloud
import os
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

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
            return True
        else:
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

        # High-risk keywords detection
        high_risk_keywords = [
            "hack", "exploit", "phishing", "malware", "virus", "attack", "cyber", "illegal",
            "bomb", "weapon", "kill", "violence", "harm", "backdoor", "breach", "ddos"
        ]
        if any(word in prompt_lower for word in high_risk_keywords):
            response = (
                "I cannot provide assistance with harmful, illegal, or dangerous content. "
                "Please ensure your requests are appropriate and comply with our usage policies."
            )
            risk_level = 'high'
            compliance_status = 'blocked'
        
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
            
        elif 'medical' in prompt_lower or ('health' in prompt_lower and 'care' not in prompt_lower):
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
            response = f"""Here's a helpful response to your query: '{prompt}'

**General Information:**
This is an AI-generated response designed to provide helpful information. Always verify important details from authoritative sources.

**Best Practices:**
- Cross-reference information
- Check multiple sources
- Consult experts when needed
- Stay updated on latest developments

This response has been processed through our governance system for quality and compliance."""
            risk_level = 'low'
            compliance_status = 'compliant'
        
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
    
    # Simulate audit logs
    audit_logs = [
        {
            'timestamp': '2024-01-15T10:30:00Z',
            'user_id': 'user_001',
            'action': 'genai_interaction',
            'risk_level': 'low',
            'compliance_status': 'compliant',
            'session_id': 'session_123'
        },
        {
            'timestamp': '2024-01-15T10:25:00Z',
            'user_id': 'admin_001',
            'action': 'policy_update',
            'risk_level': 'medium',
            'compliance_status': 'needs_review',
            'session_id': 'session_124'
        },
        {
            'timestamp': '2024-01-15T10:20:00Z',
            'user_id': 'user_002',
            'action': 'genai_interaction',
            'risk_level': 'high',
            'compliance_status': 'blocked',
            'session_id': 'session_125'
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
import streamlit as st

st.set_page_config(page_title="GenAI Governance System", layout="wide")
st.title("GenAI Multi-Agent Governance System")
st.write("Welcome to the GenAI Governance System! Use the sidebar to navigate.")

if __name__ == "__main__":
    import streamlit as st

    st.set_page_config(
        page_title="GenAI Governance System",
        page_icon="🔒",
        layout="wide",
    )

    st.title("🔒 GenAI Governance System")
    st.markdown(
        "A comprehensive AI governance system with multiple specialized agents"
    )

    st.info(
        "This is a demo application showcasing a multi-agent AI governance system."
    )

    st.markdown("### Features")
    st.markdown("- **Multi-Agent Architecture**")
    st.markdown("- **Real-time Risk Assessment**")
    st.markdown("- **Compliance Monitoring**")
    st.markdown("- **Audit Logging**")
    st.markdown("- **Policy Enforcement**")

    st.markdown("### Getting Started")
    st.markdown(
        "1. Start the backend server: `cd backend && python main.py`"
    )
    st.markdown(
        "2. Start the frontend: `cd frontend && streamlit run app.py`"
    )
    st.markdown("3. Login with demo credentials")
    st.markdown("4. Explore the governance features")

    st.markdown("### Demo Credentials")
    st.markdown("- **Username:** admin")
    st.markdown("- **Password:** admin123")

    st.markdown("### Architecture")
    st.markdown(
        "The system uses six specialized agents to ensure responsible AI usage:"
    )
    st.markdown("- **Prompt Guard:** Screens input for violations")
    st.markdown("- **Output Auditor:** Reviews generated content")
    st.markdown("- **Policy Enforcer:** Applies context-specific rules")
    st.markdown("- **Audit Logger:** Records all interactions")
    st.markdown("- **Advisory Agent:** Provides guidance")
    st.markdown("- **Feedback Agent:** Processes user feedback")  
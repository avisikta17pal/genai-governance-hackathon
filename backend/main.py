# pyright: reportMissingImports=false
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import logging
from typing import Dict, List, Optional
from pydantic import BaseModel
import uuid




# Import our agent modules
from backend.agents.prompt_guard import PromptGuardAgent
from backend.agents.output_auditor import OutputAuditorAgent
from backend.agents.policy_enforcer import PolicyEnforcerAgent
from backend.agents.audit_logger import AuditLoggerAgent
from backend.agents.advisory_agent import AdvisoryAgent
from backend.agents.feedback_agent import FeedbackAgent
from backend.services.auth_service import AuthService
from backend.services.aws_service import AWSService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GenAI Multi-Agent Governance System",
    description=(
        "A comprehensive AI governance system with multiple specialized agents"
    ),
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services
auth_service = AuthService()
aws_service = AWSService()

# Initialize agents
prompt_guard = PromptGuardAgent()
output_auditor = OutputAuditorAgent()
policy_enforcer = PolicyEnforcerAgent()
audit_logger = AuditLoggerAgent()
advisory_agent = AdvisoryAgent()
feedback_agent = FeedbackAgent()


# Pydantic models
class GenAIRequest(BaseModel):
    prompt: str
    user_id: str
    session_id: Optional[str] = None
    context: Optional[Dict] = None
    risk_level: Optional[str] = "medium"


class GenAIResponse(BaseModel):
    response: str
    risk_assessment: Dict
    compliance_status: str
    audit_trail: List[Dict]
    recommendations: List[str]


class FeedbackRequest(BaseModel):
    session_id: str
    rating: int
    feedback_text: str
    user_id: str


class PolicyUpdateRequest(BaseModel):
    policy_type: str
    rules: Dict
    user_id: str


@app.get("/")
async def root():
    return {
        "message": "GenAI Multi-Agent Governance System",
        "version": "1.0.0",
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agents": {
            "prompt_guard": "active",
            "output_auditor": "active",
            "policy_enforcer": "active",
            "audit_logger": "active",
            "advisory_agent": "active",
            "feedback_agent": "active",
        },
    }


@app.post("/api/v1/genai/process", response_model=GenAIResponse)
async def process_genai_request(
    request: GenAIRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Main endpoint for processing GenAI requests through the governance system
    """
    try:
        # Authenticate user
        user_info = await auth_service.verify_token(credentials.credentials)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session_id = request.session_id or str(uuid.uuid4())

        # Step 1: Prompt Guard - Screen input for violations
        logger.info(
            f"Processing request for user {user_info['user_id']}, "
            f"session {session_id}"
        )

        prompt_guard_result = await prompt_guard.analyze_prompt(
            prompt=request.prompt,
            user_id=user_info["user_id"],
            context=request.context,
        )

        if prompt_guard_result["risk_level"] == "high":
            return GenAIResponse(
                response="Request blocked due to high-risk content",
                risk_assessment=prompt_guard_result,
                compliance_status="blocked",
                audit_trail=[prompt_guard_result],
                recommendations=["Please review and modify your request"],
            )

        # Step 2: Policy Enforcer - Apply context-specific rules
        policy_result = await policy_enforcer.enforce_policies(
            prompt=request.prompt,
            user_info=user_info,
            context=request.context or {},
        )

        # Step 3: Generate AI response (simulated for demo)
        ai_response = await aws_service.generate_response(
            prompt=request.prompt,
            context=policy_result["modified_context"],
        )

        # Step 4: Output Auditor - Review generated content
        audit_result = await output_auditor.audit_output(
            original_prompt=request.prompt,
            ai_response=ai_response,
            user_id=user_info["user_id"],
        )

        # Step 5: Advisory Agent - Provide guidance
        advisory_result = await advisory_agent.provide_guidance(
            prompt=request.prompt,
            response=ai_response,
            risk_assessment=prompt_guard_result,
            audit_result=audit_result,
        )

        # Step 6: Audit Logger - Record everything
        await audit_logger.log_interaction(
            session_id=session_id,
            user_id=user_info["user_id"],
            prompt=request.prompt,
            response=ai_response,
            risk_assessment=prompt_guard_result,
            policy_result=policy_result,
            audit_result=audit_result,
            advisory_result=advisory_result,
        )

        return GenAIResponse(
            response=ai_response,
            risk_assessment=prompt_guard_result,
            compliance_status=audit_result["compliance_status"],
            audit_trail=[
                prompt_guard_result,
                policy_result,
                audit_result,
                advisory_result,
            ],
            recommendations=advisory_result["recommendations"],
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403) without wrapping them
        raise
    except Exception as e:
        logger.error(f"Error processing GenAI request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/v1/feedback/submit")
async def submit_feedback(
    feedback: FeedbackRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Submit user feedback for system improvement"""
    try:
        user_info = await auth_service.verify_token(credentials.credentials)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        feedback_result = await feedback_agent.process_feedback(
            session_id=feedback.session_id,
            rating=feedback.rating,
            feedback_text=feedback.feedback_text,
            user_id=user_info["user_id"],
        )

        return {
            "message": "Feedback submitted successfully",
            "feedback_id": feedback_result["feedback_id"],
            "analysis": feedback_result["analysis"],
        }

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403) without wrapping them
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/v1/audit/logs/{session_id}")
async def get_audit_logs(
    session_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Retrieve audit logs for a specific session"""
    try:
        user_info = await auth_service.verify_token(credentials.credentials)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Check if user has permission to view these logs
        if not await auth_service.can_access_logs(
            user_info["user_id"], session_id
        ):
            raise HTTPException(status_code=403, detail="Access denied")

        logs = await audit_logger.get_session_logs(session_id)
        return {"session_id": session_id, "logs": logs}

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403) without wrapping them
        raise
    except Exception as e:
        logger.error(f"Error retrieving audit logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/v1/policy/update")
async def update_policy(
    policy_update: PolicyUpdateRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Update governance policies (admin only)"""
    try:
        user_info = await auth_service.verify_token(credentials.credentials)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Check admin permissions
        if not await auth_service.is_admin(user_info["user_id"]):
            raise HTTPException(
                status_code=403, detail="Admin access required"
            )

        policy_result = await policy_enforcer.update_policy(
            policy_type=policy_update.policy_type,
            rules=policy_update.rules,
            updated_by=user_info["user_id"],
        )

        return {
            "message": "Policy updated successfully",
            "policy_id": policy_result["policy_id"],
            "updated_at": policy_result["updated_at"],
        }

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403) without wrapping them
        raise
    except Exception as e:
        logger.error(f"Error updating policy: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/v1/analytics/dashboard")
async def get_analytics_dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get analytics dashboard data"""
    try:
        user_info = await auth_service.verify_token(credentials.credentials)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Check if user has analytics access
        if not await auth_service.can_access_analytics(
            user_info["user_id"]
        ):
            raise HTTPException(
                status_code=403, detail="Analytics access denied"
            )

        analytics_data = await audit_logger.get_analytics_data()
        return analytics_data

    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 403) without wrapping them
        raise
    except Exception as e:
        logger.error(f"Error retrieving analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(
        app, host="0.0.0.0", port=8000
    )

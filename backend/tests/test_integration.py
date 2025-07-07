import pytest
import asyncio
import json
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.agents.prompt_guard import PromptGuardAgent
from backend.agents.output_auditor import OutputAuditorAgent
from backend.agents.policy_enforcer import PolicyEnforcerAgent
from backend.agents.audit_logger import AuditLoggerAgent
from backend.agents.advisory_agent import AdvisoryAgent
from backend.agents.feedback_agent import FeedbackAgent

# Test client
client = TestClient(app)

class TestGenAIGovernanceSystem:
    """Integration tests for the GenAI Governance System"""
    
    @pytest.fixture
    def sample_user_info(self):
        return {
            "user_id": "test_user_001",
            "role": "user",
            "permissions": ["read", "write"]
        }
    
    @pytest.fixture
    def sample_genai_request(self):
        return {
            "prompt": "What are the symptoms of diabetes?",
            "user_id": "test_user_001",
            "session_id": "test_session_001",
            "context": {"domain": "healthcare", "risk_level": "medium"},
            "risk_level": "medium"
        }
    
    @pytest.fixture
    def sample_feedback_request(self):
        return {
            "session_id": "test_session_001",
            "rating": 4,
            "feedback_text": "The system provided helpful information",
            "user_id": "test_user_001"
        }

    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "agents" in data
        assert all(agent in data["agents"] for agent in [
            "prompt_guard", "output_auditor", "policy_enforcer",
            "audit_logger", "advisory_agent", "feedback_agent"
        ])

    def test_root_endpoint(self):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "GenAI Multi-Agent Governance System"
        assert data["version"] == "1.0.0"
        assert data["status"] == "operational"

    @patch('backend.services.auth_service.AuthService.verify_token')
    def test_genai_process_endpoint_success(self, mock_verify_token, sample_user_info, sample_genai_request):
        """Test successful GenAI request processing"""
        mock_verify_token.return_value = sample_user_info
        
        with patch('backend.agents.prompt_guard.PromptGuardAgent.analyze_prompt') as mock_prompt_guard:
            mock_prompt_guard.return_value = {
                "risk_level": "low",
                "risk_score": 0.2,
                "risk_factors": ["healthcare_content"],
                "action": "allow"
            }
            
            with patch('backend.agents.policy_enforcer.PolicyEnforcerAgent.enforce_policies') as mock_policy:
                mock_policy.return_value = {
                    "modified_context": {"domain": "healthcare"},
                    "policies_applied": ["hipaa_compliance"]
                }
                
                with patch('backend.services.aws_service.AWSService.generate_response') as mock_aws:
                    mock_aws.return_value = "Diabetes symptoms include increased thirst, frequent urination, and fatigue."
                    
                    with patch('backend.agents.output_auditor.OutputAuditorAgent.audit_output') as mock_audit:
                        mock_audit.return_value = {
                            "compliance_status": "compliant",
                            "quality_score": 0.9,
                            "issues": []
                        }
                        
                        with patch('backend.agents.advisory_agent.AdvisoryAgent.provide_guidance') as mock_advisory:
                            mock_advisory.return_value = {
                                "recommendations": ["Verify medical information with healthcare provider"],
                                "guidance": "This is general information only"
                            }
                            
                            with patch('backend.agents.audit_logger.AuditLoggerAgent.log_interaction') as mock_logger:
                                mock_logger.return_value = {"audit_id": "test_audit_001"}
                                
                                response = client.post(
                                    "/api/v1/genai/process",
                                    headers={"Authorization": "Bearer test_token"},
                                    json=sample_genai_request
                                )
                                
                                assert response.status_code == 200
                                data = response.json()
                                assert "response" in data
                                assert "risk_assessment" in data
                                assert "compliance_status" in data
                                assert "audit_trail" in data
                                assert "recommendations" in data

    @patch('backend.services.auth_service.AuthService.verify_token')
    def test_genai_process_endpoint_high_risk(self, mock_verify_token, sample_user_info):
        """Test GenAI request processing with high-risk content"""
        mock_verify_token.return_value = sample_user_info
        
        high_risk_request = {
            "prompt": "How can I harm someone?",
            "user_id": "test_user_001",
            "session_id": "test_session_002",
            "context": {"domain": "general"},
            "risk_level": "high"
        }
        
        with patch('backend.agents.prompt_guard.PromptGuardAgent.analyze_prompt') as mock_prompt_guard:
            mock_prompt_guard.return_value = {
                "risk_level": "high",
                "risk_score": 0.9,
                "risk_factors": ["harmful_content", "violence"],
                "action": "block"
            }
            
            response = client.post(
                "/api/v1/genai/process",
                headers={"Authorization": "Bearer test_token"},
                json=high_risk_request
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["compliance_status"] == "blocked"
            assert "Request blocked due to high-risk content" in data["response"]

    @patch('backend.services.auth_service.AuthService.verify_token')
    def test_feedback_submission(self, mock_verify_token, sample_user_info, sample_feedback_request):
        """Test feedback submission endpoint"""
        mock_verify_token.return_value = sample_user_info
        
        with patch('backend.agents.feedback_agent.FeedbackAgent.process_feedback') as mock_feedback:
            mock_feedback.return_value = {
                "feedback_id": "feedback_001",
                "analysis": "Positive feedback received",
                "sentiment": "positive"
            }
            
            response = client.post(
                "/api/v1/feedback/submit",
                headers={"Authorization": "Bearer test_token"},
                json=sample_feedback_request
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Feedback submitted successfully"
            assert "feedback_id" in data
            assert "analysis" in data

    @patch('backend.services.auth_service.AuthService.verify_token')
    def test_audit_logs_retrieval(self, mock_verify_token, sample_user_info):
        """Test audit logs retrieval endpoint"""
        mock_verify_token.return_value = sample_user_info
        
        with patch('backend.services.auth_service.AuthService.can_access_logs') as mock_access:
            mock_access.return_value = True
            
            with patch('backend.agents.audit_logger.AuditLoggerAgent.get_session_logs') as mock_logs:
                mock_logs.return_value = [
                    {
                        "audit_id": "audit_001",
                        "session_id": "test_session_001",
                        "timestamp": "2024-01-01T00:00:00Z",
                        "action": "genai_request"
                    }
                ]
                
                response = client.get(
                    "/api/v1/audit/logs/test_session_001",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["session_id"] == "test_session_001"
                assert "logs" in data
                assert len(data["logs"]) > 0

    @patch('backend.services.auth_service.AuthService.verify_token')
    def test_policy_update_admin_only(self, mock_verify_token):
        """Test policy update endpoint (admin only)"""
        # Test with non-admin user
        mock_verify_token.return_value = {
            "user_id": "test_user_001",
            "role": "user"
        }
        
        with patch('backend.services.auth_service.AuthService.is_admin') as mock_admin:
            mock_admin.return_value = False
            
            policy_update = {
                "policy_type": "content_moderation",
                "rules": {"strict_mode": True},
                "user_id": "test_user_001"
            }
            
            response = client.post(
                "/api/v1/policy/update",
                headers={"Authorization": "Bearer test_token"},
                json=policy_update
            )
            
            assert response.status_code == 403
            assert "Admin access required" in response.json()["detail"]

    @patch('backend.services.auth_service.AuthService.verify_token')
    def test_analytics_dashboard_access_control(self, mock_verify_token):
        """Test analytics dashboard access control"""
        mock_verify_token.return_value = {
            "user_id": "test_user_001",
            "role": "user"
        }
        
        with patch('backend.services.auth_service.AuthService.can_access_analytics') as mock_analytics:
            mock_analytics.return_value = False
            
            response = client.get(
                "/api/v1/analytics/dashboard",
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 403
            assert "Analytics access denied" in response.json()["detail"]

    def test_authentication_required(self):
        """Test that authentication is required for protected endpoints"""
        # Test without authentication
        response = client.post(
            "/api/v1/genai/process",
            json={"prompt": "test", "user_id": "test"}
        )
        assert response.status_code == 403

    @patch('backend.services.auth_service.AuthService.verify_token')
    def test_invalid_token(self, mock_verify_token):
        """Test with invalid authentication token"""
        mock_verify_token.return_value = None
        
        response = client.post(
            "/api/v1/genai/process",
            headers={"Authorization": "Bearer invalid_token"},
            json={"prompt": "test", "user_id": "test"}
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

class TestAgentIntegration:
    """Test individual agent functionality"""
    
    @pytest.mark.asyncio
    async def test_prompt_guard_agent(self):
        """Test Prompt Guard Agent functionality"""
        agent = PromptGuardAgent()
        
        # Test low-risk prompt
        result = await agent.analyze_prompt(
            prompt="What is the weather like today?",
            user_id="test_user",
            context={"domain": "general"}
        )
        
        assert "risk_level" in result
        assert "risk_score" in result
        assert "risk_factors" in result
        assert "action" in result
        
        # Test high-risk prompt
        result = await agent.analyze_prompt(
            prompt="How can I hack into a system?",
            user_id="test_user",
            context={"domain": "general"}
        )
        
        # The prompt contains "hack" which should be detected as security risk
        # Check if any risks are detected (the agent uses "suspicious_content" as a factor)
        assert len(result["risk_factors"]) > 0

    @pytest.mark.asyncio
    async def test_output_auditor_agent(self):
        """Test Output Auditor Agent functionality"""
        agent = OutputAuditorAgent()
        
        result = await agent.audit_output(
            original_prompt="What are diabetes symptoms?",
            ai_response="Diabetes symptoms include increased thirst and fatigue.",
            user_id="test_user"
        )
        
        assert "compliance_status" in result
        assert "quality_score" in result
        assert "compliance_issues" in result

    @pytest.mark.asyncio
    async def test_policy_enforcer_agent(self):
        """Test Policy Enforcer Agent functionality"""
        agent = PolicyEnforcerAgent()
        
        result = await agent.enforce_policies(
            prompt="What are diabetes symptoms?",
            user_info={"user_id": "test_user", "role": "user"},
            context={"domain": "healthcare"}
        )
        
        assert "modified_context" in result
        assert "enforced_policies" in result

    @pytest.mark.asyncio
    async def test_audit_logger_agent(self):
        """Test Audit Logger Agent functionality"""
        agent = AuditLoggerAgent()
        
        result = await agent.log_interaction(
            session_id="test_session",
            user_id="test_user",
            prompt="Test prompt",
            response="Test response",
            risk_assessment={"risk_level": "low"},
            policy_result={"policies_applied": []},
            audit_result={"compliance_status": "compliant"},
            advisory_result={"recommendations": []}
        )
        
        assert "audit_id" in result
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_advisory_agent(self):
        """Test Advisory Agent functionality"""
        agent = AdvisoryAgent()
        
        result = await agent.provide_guidance(
            prompt="What are diabetes symptoms?",
            response="Diabetes symptoms include increased thirst.",
            risk_assessment={"risk_level": "medium"},
            audit_result={"compliance_status": "compliant"}
        )
        
        assert "recommendations" in result
        assert "recommendations" in result

    @pytest.mark.asyncio
    async def test_feedback_agent(self):
        """Test Feedback Agent functionality"""
        agent = FeedbackAgent()
        
        result = await agent.process_feedback(
            session_id="test_session",
            rating=4,
            feedback_text="Good response",
            user_id="test_user"
        )
        
        assert "feedback_id" in result
        assert "analysis" in result
        assert "analysis" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
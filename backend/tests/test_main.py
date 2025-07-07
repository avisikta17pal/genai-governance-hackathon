import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
from datetime import datetime
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "GenAI Multi-Agent Governance System" in response.json()["message"]


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "prompt_guard" in response.json()["agents"]


def test_genai_process_endpoint():
    """Test the GenAI process endpoint (without auth)"""
    response = client.post(
        "/api/v1/genai/process",
        json={
            "prompt": "Hello, how are you?",
            "user_id": "test_user",
            "session_id": "test_session",
        },
    )
    # Should return 403 without authentication (FastAPI HTTPBearer default)
    assert response.status_code == 403


def test_feedback_endpoint():
    """Test the feedback endpoint (without auth)"""
    response = client.post(
        "/api/v1/feedback/submit",
        json={
            "session_id": "test_session",
            "rating": 5,
            "feedback_text": "Great system!",
            "user_id": "test_user",
        },
    )
    # Should return 403 without authentication (FastAPI HTTPBearer default)
    assert response.status_code == 403


def test_audit_logs_endpoint():
    """Test the audit logs endpoint (without auth)"""
    response = client.get("/api/v1/audit/logs/test_session")
    # Should return 403 without authentication (FastAPI HTTPBearer default)
    assert response.status_code == 403


def test_policy_update_endpoint():
    """Test the policy update endpoint (without auth)"""
    response = client.post(
        "/api/v1/policy/update",
        json={
            "policy_type": "data_privacy",
            "rules": {"gdpr": True},
            "user_id": "test_user",
        },
    )
    # Should return 403 without authentication (FastAPI HTTPBearer default)
    assert response.status_code == 403


def test_analytics_endpoint():
    """Test the analytics endpoint (without auth)"""
    response = client.get("/api/v1/analytics/dashboard")
    # Should return 403 without authentication (FastAPI HTTPBearer default)
    assert response.status_code == 403


if __name__ == "__main__":
    pytest.main([__file__])

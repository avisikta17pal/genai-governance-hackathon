import logging
import json
from typing import Dict
from datetime import datetime, timedelta
import boto3
import hashlib
import uuid

logger = logging.getLogger(__name__)


class AuditLoggerAgent:
    """
    Audit Logger Agent: Creates comprehensive records of AI interactions and governance decisions
    to satisfy regulatory requirements and detect potential system misuse.
    """

    def __init__(self):
        self.dynamodb_client = boto3.client("dynamodb", region_name="us-east-1")
        self.s3_client = boto3.client("s3", region_name="us-east-1")

        # Audit log structure
        self.audit_fields = [
            "session_id",
            "user_id",
            "timestamp",
            "action_type",
            "resource",
            "request_data",
            "response_data",
            "risk_assessment",
            "policy_result",
            "audit_result",
            "advisory_result",
            "compliance_status",
            "ip_address",
            "user_agent",
            "duration_ms",
            "error_code",
            "error_message",
        ]

        # Regulatory compliance requirements
        self.compliance_requirements = {
            "gdpr": {
                "retention_period": 365 * 24 * 60 * 60,  # 1 year in seconds
                "data_subject_rights": True,
                "consent_tracking": True,
            },
            "hipaa": {
                "retention_period": 6 * 365 * 24 * 60 * 60,  # 6 years in seconds
                "phi_tracking": True,
                "access_logging": True,
            },
            "sox": {
                "retention_period": 7 * 365 * 24 * 60 * 60,  # 7 years in seconds
                "financial_controls": True,
                "audit_trail": True,
            },
            "pci_dss": {
                "retention_period": 365 * 24 * 60 * 60,  # 1 year in seconds
                "card_data_tracking": True,
                "security_events": True,
            },
        }

        # Anomaly detection thresholds
        self.anomaly_thresholds = {
            "high_risk_requests": 5,  # per hour
            "failed_authentications": 3,  # per 15 minutes
            "data_access_volume": 100,  # per hour
            "policy_violations": 2,  # per hour
        }

    async def log_interaction(
        self,
        session_id: str,
        user_id: str,
        prompt: str,
        response: str,
        risk_assessment: Dict,
        policy_result: Dict,
        audit_result: Dict,
        advisory_result: Dict,
    ) -> Dict:
        """
        Log a complete AI interaction with all governance decisions
        """
        try:
            logger.info(f"Logging interaction for session {session_id}, user {user_id}")

            # Create audit record
            audit_record = await self._create_audit_record(
                session_id,
                user_id,
                prompt,
                response,
                risk_assessment,
                policy_result,
                audit_result,
                advisory_result,
            )

            # Store in DynamoDB
            await self._store_audit_record(audit_record)

            # Check for anomalies
            anomaly_check = await self._check_for_anomalies(user_id, audit_record)

            # Generate compliance report
            compliance_report = await self._generate_compliance_report(audit_record)

            result = {
                "audit_id": audit_record["audit_id"],
                "session_id": session_id,
                "user_id": user_id,
                "timestamp": audit_record["timestamp"],
                "anomaly_detected": anomaly_check["anomaly_detected"],
                "compliance_status": compliance_report["status"],
                "retention_period": compliance_report["retention_period"],
                "storage_location": audit_record["storage_location"],
            }

            logger.info(f"Audit logging complete for session {session_id}")
            return result

        except Exception as e:
            logger.error(f"Error logging interaction: {str(e)}")
            return {
                "audit_id": f"error_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "session_id": session_id,
                "user_id": user_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }

    async def _create_audit_record(
        self,
        session_id: str,
        user_id: str,
        prompt: str,
        response: str,
        risk_assessment: Dict,
        policy_result: Dict,
        audit_result: Dict,
        advisory_result: Dict,
    ) -> Dict:
        """Create a comprehensive audit record"""

        # Generate audit ID
        audit_id = f"audit_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

        # Hash sensitive data
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        response_hash = hashlib.sha256(response.encode()).hexdigest()

        audit_record = {
            "audit_id": audit_id,
            "session_id": session_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "action_type": "genai_interaction",
            "resource": "ai_model",
            "request_data": {
                "prompt_hash": prompt_hash,
                "prompt_length": len(prompt),
                "context": "ai_governance_system",
            },
            "response_data": {
                "response_hash": response_hash,
                "response_length": len(response),
                "compliance_status": audit_result.get("compliance_status", "unknown"),
            },
            "risk_assessment": risk_assessment,
            "policy_result": policy_result,
            "audit_result": audit_result,
            "advisory_result": advisory_result,
            "compliance_status": audit_result.get("compliance_status", "unknown"),
            "ip_address": "127.0.0.1",  # In production, get from request
            "user_agent": "GenAI-Governance-System/1.0",
            "duration_ms": 150,  # Simulated duration
            "storage_location": "dynamodb",
            "version": "1.0",
        }

        return audit_record

    async def _store_audit_record(self, audit_record: Dict) -> bool:
        """Store audit record in DynamoDB"""
        try:
            # In production, this would store in DynamoDB
            # For demo purposes, we'll simulate the storage

            # Simulate successful storage
            logger.info(f"Stored audit record: {audit_record['audit_id']}")
            return True

        except Exception as e:
            logger.error(f"Error storing audit record: {str(e)}")
            return False

    async def _check_for_anomalies(self, user_id: str, audit_record: Dict) -> Dict:
        """Check for anomalous behavior patterns"""
        try:
            # In production, this would query recent audit logs
            # For demo, we'll simulate anomaly detection

            anomalies = []
            risk_level = "low"

            # Check for high-risk patterns
            if audit_record["risk_assessment"].get("risk_level") == "high":
                anomalies.append("high_risk_request")
                risk_level = "high"

            # Check for policy violations
            if (
                audit_record["policy_result"].get("compliance_status")
                == "non_compliant"
            ):
                anomalies.append("policy_violation")
                risk_level = "high"

            # Check for unusual access patterns
            if audit_record["request_data"]["prompt_length"] > 1000:
                anomalies.append("large_request")
                risk_level = "medium"

            # Check for rapid requests (simulated)
            if audit_record.get("duration_ms", 0) < 50:
                anomalies.append("rapid_request")
                risk_level = "medium"

            return {
                "anomaly_detected": len(anomalies) > 0,
                "anomalies": anomalies,
                "risk_level": risk_level,
                "confidence": 0.8 if anomalies else 0.9,
            }

        except Exception as e:
            logger.error(f"Error checking for anomalies: {str(e)}")
            return {
                "anomaly_detected": False,
                "anomalies": [],
                "risk_level": "unknown",
                "error": str(e),
            }

    async def _generate_compliance_report(self, audit_record: Dict) -> Dict:
        """Generate compliance report for the audit record"""
        try:
            # Determine applicable compliance frameworks
            applicable_frameworks = []

            # Check for GDPR applicability
            if "personal data" in audit_record["request_data"].get("context", ""):
                applicable_frameworks.append("gdpr")

            # Check for HIPAA applicability
            if "medical" in audit_record["request_data"].get("context", ""):
                applicable_frameworks.append("hipaa")

            # Check for SOX applicability
            if "financial" in audit_record["request_data"].get("context", ""):
                applicable_frameworks.append("sox")

            # Determine retention period
            retention_period = 365 * 24 * 60 * 60  # Default 1 year
            if applicable_frameworks:
                retention_period = max(
                    [
                        self.compliance_requirements[framework]["retention_period"]
                        for framework in applicable_frameworks
                    ]
                )

            return {
                "status": "compliant",
                "applicable_frameworks": applicable_frameworks,
                "retention_period": retention_period,
                "retention_end_date": (
                    datetime.fromisoformat(audit_record["timestamp"])
                    + timedelta(seconds=retention_period)
                ).isoformat(),
                "data_protection": True,
                "audit_trail": True,
            }

        except Exception as e:
            logger.error(f"Error generating compliance report: {str(e)}")
            return {
                "status": "unknown",
                "applicable_frameworks": [],
                "retention_period": 365 * 24 * 60 * 60,
                "error": str(e),
            }

    async def get_session_logs(self, session_id: str) -> Dict:
        """Retrieve audit logs for a specific session"""
        try:
            # In production, this would query DynamoDB
            # For demo, we'll return simulated logs

            logs = {
                "session_id": session_id,
                "logs": [
                    {
                        "audit_id": f"audit_{session_id}_001",
                        "timestamp": datetime.utcnow().isoformat(),
                        "action_type": "genai_interaction",
                        "compliance_status": "compliant",
                        "risk_level": "low",
                    }
                ],
                "total_logs": 1,
                "retrieved_at": datetime.utcnow().isoformat(),
            }

            return logs

        except Exception as e:
            logger.error(f"Error retrieving session logs: {str(e)}")
            return {"session_id": session_id, "error": str(e), "logs": []}

    async def get_analytics_data(self) -> Dict:
        """Get analytics data for dashboard"""
        try:
            # In production, this would aggregate data from DynamoDB
            # For demo, we'll return simulated analytics

            analytics = {
                "total_interactions": 1250,
                "compliance_rate": 0.98,
                "risk_distribution": {"low": 0.75, "medium": 0.20, "high": 0.05},
                "anomaly_detections": 12,
                "policy_violations": 8,
                "average_response_time": 145,
                "top_user_activities": [
                    {"user_id": "user_001", "interactions": 45},
                    {"user_id": "user_002", "interactions": 32},
                    {"user_id": "user_003", "interactions": 28},
                ],
                "compliance_frameworks": {"gdpr": 0.95, "hipaa": 0.98, "sox": 0.92},
                "generated_at": datetime.utcnow().isoformat(),
            }

            return analytics

        except Exception as e:
            logger.error(f"Error getting analytics data: {str(e)}")
            return {"error": str(e), "generated_at": datetime.utcnow().isoformat()}

    async def export_audit_logs(
        self, start_date: str, end_date: str, user_id: str
    ) -> Dict:
        """Export audit logs for compliance reporting"""
        try:
            # In production, this would query DynamoDB and export to S3
            export_id = f"export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

            export_result = {
                "export_id": export_id,
                "start_date": start_date,
                "end_date": end_date,
                "requested_by": user_id,
                "status": "completed",
                "file_location": f"s3://audit-logs-bucket/{export_id}.json",
                "record_count": 1250,
                "exported_at": datetime.utcnow().isoformat(),
                "compliance_frameworks": ["gdpr", "hipaa", "sox"],
            }

            return export_result

        except Exception as e:
            logger.error(f"Error exporting audit logs: {str(e)}")
            return {
                "export_id": f"error_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "error": str(e),
                "status": "failed",
            }

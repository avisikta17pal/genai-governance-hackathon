# pyright: reportMissingImports=false
import logging
import re
import boto3
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PromptGuardAgent:
    """
    Prompt Guard Agent: Screens GenAI inputs to prevent regulatory violations,
    policy breaches, and data privacy issues. Escalates high-risk requests for human review.
    """

    def __init__(self):
        self.bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
        self.comprehend_client = boto3.client("comprehend", region_name="us-east-1")

        # Risk categories and keywords
        self.risk_categories = {
            "privacy": [
                "ssn",
                "social security",
                "credit card",
                "password",
                "email address",
                "phone number",
                "address",
                "date of birth",
                "medical record",
                "patient data",
                "financial data",
                "bank account",
            ],
            "security": [
                "hack",
                "exploit",
                "vulnerability",
                "backdoor",
                "malware",
                "phishing",
                "ddos",
                "sql injection",
                "xss",
                "buffer overflow",
            ],
            "harmful_content": [
                "harm",
                "hurt",
                "kill",
                "suicide",
                "self-harm",
                "violence",
                "weapon",
                "bomb",
                "terrorism",
                "hate speech",
                "discrimination",
            ],
            "regulatory": [
                "insider trading",
                "market manipulation",
                "fraud",
                "money laundering",
                "tax evasion",
                "copyright infringement",
                "patent violation",
            ],
            "ethical": [
                "bias",
                "discrimination",
                "stereotype",
                "prejudice",
                "racism",
                "sexism",
                "ageism",
                "ableism",
            ],
        }

        # Compliance frameworks
        self.compliance_frameworks = {
            "gdpr": {
                "data_types": ["personal data", "sensitive data", "biometric data"],
                "rights": ["right to be forgotten", "data portability", "consent"],
            },
            "hipaa": {
                "phi_indicators": [
                    "medical",
                    "health",
                    "diagnosis",
                    "treatment",
                    "prescription",
                ],
                "protected_info": [
                    "patient name",
                    "medical record",
                    "health insurance",
                ],
            },
            "sox": {
                "financial_controls": [
                    "internal control",
                    "financial reporting",
                    "audit",
                ],
                "fraud_indicators": [
                    "financial fraud",
                    "accounting fraud",
                    "insider trading",
                ],
            },
        }

        # Allowlist for legitimate queries that might contain flagged keywords
        self.legitimate_queries = [
            "heart attack symptoms",
            "panic attack help",
            "asthma attack treatment",
            "migraine attack relief",
            "seizure attack symptoms",
            "smartphone buying tips",
            "best smartphone to buy",
            "customer data analysis guidelines",
            "legal data processing",
            "marketing email template",
            "create marketing email",
            "write marketing content",
        ]

    async def analyze_prompt(
        self, prompt: str, user_id: str, context: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze a prompt for potential risks and compliance issues
        """
        try:
            logger.info(f"Analyzing prompt for user {user_id}")

            # Step 1: Basic text analysis
            text_analysis = await self._analyze_text_content(prompt)

            # Step 2: Compliance framework checking
            compliance_check = await self._check_compliance_frameworks(prompt, context)

            # Step 3: AWS Bedrock content moderation
            bedrock_moderation = await self._bedrock_content_moderation(prompt)

            # Step 4: Risk scoring
            risk_score = await self._calculate_risk_score(
                text_analysis, compliance_check, bedrock_moderation
            )

            # Step 5: Determine action
            action = await self._determine_action(
                risk_score, text_analysis, compliance_check
            )

            result = {
                "risk_level": risk_score["level"],
                "risk_score": risk_score["score"],
                "risk_factors": risk_score["factors"],
                "compliance_issues": compliance_check["issues"],
                "moderation_result": bedrock_moderation,
                "action": action,
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "prompt_length": len(prompt),
                "analysis_confidence": risk_score["confidence"],
            }

            logger.info(
                f"Prompt analysis complete for user {user_id}: {result['risk_level']}"
            )
            return result

        except Exception as e:
            logger.error(f"Error analyzing prompt: {str(e)}")
            return {
                "risk_level": "high",
                "risk_score": 1.0,
                "risk_factors": ["analysis_error"],
                "compliance_issues": ["analysis_failed"],
                "moderation_result": {"status": "error"},
                "action": "block",
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "error": str(e),
            }

    async def _analyze_text_content(self, prompt: str) -> Dict:
        """Analyze text content for risk indicators"""
        prompt_lower = prompt.lower()

        # Check if this is a legitimate query first
        is_legitimate = any(legit_query in prompt_lower for legit_query in self.legitimate_queries)
        
        if is_legitimate:
            return {
                "detected_risks": {},
                "total_risk_score": 0.1,  # Very low risk for legitimate queries
                "pii_detected": {},
                "legitimate_query": True,
            }

        detected_risks = {}
        total_risk_score = 0

        for category, keywords in self.risk_categories.items():
            category_risks = []
            category_score = 0

            for keyword in keywords:
                if keyword in prompt_lower:
                    category_risks.append(keyword)
                    category_score += 0.1  # Base risk score per keyword

            if category_risks:
                detected_risks[category] = {
                    "keywords": category_risks,
                    "score": min(category_score, 1.0),
                    "count": len(category_risks),
                }
                total_risk_score += category_score

        # Check for PII patterns
        pii_patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "phone": r"\b\d{3}-\d{3}-\d{4}\b",
            "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
        }

        pii_detected = {}
        for pii_type, pattern in pii_patterns.items():
            matches = re.findall(pattern, prompt)
            if matches:
                pii_detected[pii_type] = len(matches)
                total_risk_score += 0.3 * len(matches)

        if pii_detected:
            detected_risks["pii"] = pii_detected

        return {
            "detected_risks": detected_risks,
            "total_risk_score": min(total_risk_score, 1.0),
            "pii_detected": pii_detected,
            "legitimate_query": False,
        }

    async def _check_compliance_frameworks(
        self, prompt: str, context: Optional[Dict] = None
    ) -> Dict:
        """Check prompt against various compliance frameworks"""
        prompt_lower = prompt.lower()
        issues = []

        # GDPR compliance check
        gdpr_issues = []
        for data_type in self.compliance_frameworks["gdpr"]["data_types"]:
            if data_type in prompt_lower:
                gdpr_issues.append(f"Potential GDPR violation: {data_type}")

        # HIPAA compliance check
        hipaa_issues = []
        for phi_indicator in self.compliance_frameworks["hipaa"]["phi_indicators"]:
            if phi_indicator in prompt_lower:
                hipaa_issues.append(f"Potential HIPAA violation: {phi_indicator}")

        # SOX compliance check
        sox_issues = []
        for fraud_indicator in self.compliance_frameworks["sox"]["fraud_indicators"]:
            if fraud_indicator in prompt_lower:
                sox_issues.append(f"Potential SOX violation: {fraud_indicator}")

        if gdpr_issues:
            issues.extend(gdpr_issues)
        if hipaa_issues:
            issues.extend(hipaa_issues)
        if sox_issues:
            issues.extend(sox_issues)

        return {
            "issues": issues,
            "gdpr_violations": len(gdpr_issues),
            "hipaa_violations": len(hipaa_issues),
            "sox_violations": len(sox_issues),
        }

    async def _bedrock_content_moderation(self, prompt: str) -> Dict:
        """Use AWS Bedrock for content moderation"""
        try:
            # Import AWS service for real Bedrock integration
            from backend.services.aws_service import AWSService
            
            aws_service = AWSService()
            
            # Use real AWS Bedrock moderation
            moderation_result = await aws_service.moderate_content(prompt)
            
            return {
                "status": "success",
                "flagged": moderation_result.get("flagged", False),
                "categories": moderation_result.get("bedrock_moderation", {}).get("categories", {
                    "hate": 0.0,
                    "violence": 0.0,
                    "sexual": 0.0,
                    "self_harm": 0.0,
                }),
                "confidence": moderation_result.get("bedrock_moderation", {}).get("confidence", 0.95),
                "source": "aws_bedrock_real",
            }

        except Exception as e:
            logger.error(f"Error in Bedrock content moderation: {str(e)}")
            return {
                "status": "error",
                "flagged": True,  # Default to flagged on error
                "error": str(e),
                "source": "aws_bedrock_error",
            }

    async def _calculate_risk_score(
        self, text_analysis: Dict, compliance_check: Dict, bedrock_moderation: Dict
    ) -> Dict:
        """Calculate overall risk score"""
        base_score = text_analysis["total_risk_score"]

        # Add compliance violations
        compliance_score = (
            compliance_check["gdpr_violations"]
            + compliance_check["hipaa_violations"]
            + compliance_check["sox_violations"]
        ) * 0.2

        # Add Bedrock moderation score
        moderation_score = 0
        if bedrock_moderation.get("flagged", False):
            moderation_score = (
                max(bedrock_moderation["categories"].values())
                if "categories" in bedrock_moderation
                else 0.5
            )

        total_score = min(base_score + compliance_score + moderation_score, 1.0)

        # Determine risk level
        if total_score >= 0.8:
            level = "high"
        elif total_score >= 0.5:
            level = "medium"
        else:
            level = "low"

        factors = []
        if text_analysis["detected_risks"]:
            factors.append("suspicious_content")
        if compliance_check["issues"]:
            factors.append("compliance_violations")
        if bedrock_moderation.get("flagged", False):
            factors.append("content_moderation")

        return {
            "score": total_score,
            "level": level,
            "factors": factors,
            "confidence": 0.9 if total_score > 0.5 else 0.7,
        }

    async def _determine_action(
        self, risk_score: Dict, text_analysis: Dict, compliance_check: Dict
    ) -> str:
        """Determine what action to take based on risk assessment"""
        if risk_score["level"] == "high":
            return "block"
        elif risk_score["level"] == "medium":
            return "flag_for_review"
        else:
            return "allow"

    async def escalate_for_review(
        self, prompt: str, risk_assessment: Dict, user_id: str
    ) -> Dict:
        """Escalate high-risk requests for human review"""
        escalation = {
            "escalation_id": f"esc_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "prompt": prompt,
            "risk_assessment": risk_assessment,
            "user_id": user_id,
            "escalated_at": datetime.utcnow().isoformat(),
            "status": "pending_review",
            "priority": "high" if risk_assessment["risk_level"] == "high" else "medium",
        }

        # In production, this would be stored in a database
        logger.info(f"Escalated prompt for review: {escalation['escalation_id']}")

        return escalation

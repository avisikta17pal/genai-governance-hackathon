# pyright: reportMissingImports=false
import logging
import boto3
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class OutputAuditorAgent:
    """
    Output Auditor Agent: Reviews all GenAI outputs to ensure regulatory compliance,
    proper disclosures, and adherence to fairness standards.
    """

    def __init__(self):
        self.bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Output quality standards
        self.quality_standards = {
            "accuracy": ["factual", "accurate", "verified", "source"],
            "completeness": ["comprehensive", "thorough", "complete", "detailed"],
            "clarity": ["clear", "understandable", "concise", "well-structured"],
            "objectivity": ["unbiased", "neutral", "balanced", "objective"],
        }

        # Fairness indicators
        self.fairness_indicators = {
            "bias_indicators": [
                "always",
                "never",
                "all",
                "none",
                "everyone",
                "nobody",
                "stereotype",
                "prejudice",
                "discrimination",
                "favoritism",
            ],
            "inclusive_language": [
                "diverse",
                "inclusive",
                "representative",
                "equitable",
                "accessible",
                "accommodating",
                "respectful",
            ],
        }

        # Regulatory compliance checkers
        self.compliance_checkers = {
            "disclosure_requirements": [
                "ai generated",
                "artificial intelligence",
                "machine learning",
                "automated",
                "algorithmic",
                "this is an ai response",
            ],
            "medical_disclaimers": [
                "not medical advice",
                "consult healthcare provider",
                "for informational purposes only",
                "not a substitute for professional medical care",
            ],
            "financial_disclaimers": [
                "not financial advice",
                "consult financial advisor",
                "for informational purposes only",
                "past performance does not guarantee future results",
            ],
            "legal_disclaimers": [
                "not legal advice",
                "consult attorney",
                "for informational purposes only",
                "this does not constitute legal advice",
            ],
        }

    async def audit_output(
        self, original_prompt: str, ai_response: str, user_id: str
    ) -> Dict:
        """
        Audit AI-generated output for compliance, fairness, and quality
        """
        try:
            logger.info(f"Auditing output for user {user_id}")

            # Step 1: Quality assessment
            quality_assessment = await self._assess_output_quality(ai_response)

            # Step 2: Fairness evaluation
            fairness_evaluation = await self._evaluate_fairness(ai_response)

            # Step 3: Compliance verification
            compliance_verification = await self._verify_compliance(
                original_prompt, ai_response
            )

            # Step 4: Content moderation
            content_moderation = await self._moderate_content(ai_response)

            # Step 5: Generate audit report
            audit_report = await self._generate_audit_report(
                quality_assessment,
                fairness_evaluation,
                compliance_verification,
                content_moderation,
            )

            result = {
                "compliance_status": audit_report["overall_status"],
                "quality_score": quality_assessment["overall_score"],
                "fairness_score": fairness_evaluation["fairness_score"],
                "compliance_issues": compliance_verification["issues"],
                "moderation_flags": content_moderation["flags"],
                "recommendations": audit_report["recommendations"],
                "audit_timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "response_length": len(ai_response),
                "audit_confidence": audit_report["confidence"],
            }

            logger.info(
                f"Output audit completed for user {user_id}: {result['compliance_status']}"
            )
            return result

        except Exception as e:
            logger.error(f"Error auditing output: {str(e)}")
            return {
                "compliance_status": "failed",
                "quality_score": 0.0,
                "fairness_score": 0.0,
                "compliance_issues": ["audit_error"],
                "moderation_flags": ["audit_failed"],
                "recommendations": ["Review audit system"],
                "audit_timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "error": str(e),
            }

    async def _assess_output_quality(self, ai_response: str) -> Dict:
        """Assess the quality of AI-generated output"""
        response_lower = ai_response.lower()

        quality_scores = {}
        total_score = 0

        for standard, indicators in self.quality_standards.items():
            standard_score = 0
            detected_indicators = []

            for indicator in indicators:
                if indicator in response_lower:
                    detected_indicators.append(indicator)
                    standard_score += 0.2

            quality_scores[standard] = {
                "score": min(standard_score, 1.0),
                "indicators": detected_indicators,
                "count": len(detected_indicators),
            }
            total_score += standard_score

        # Check for factual accuracy indicators
        accuracy_indicators = [
            "according to",
            "research shows",
            "studies indicate",
            "evidence suggests",
        ]
        accuracy_score = 0
        for indicator in accuracy_indicators:
            if indicator in response_lower:
                accuracy_score += 0.25

        quality_scores["factual_accuracy"] = {
            "score": min(accuracy_score, 1.0),
            "indicators": [ind for ind in accuracy_indicators if ind in response_lower],
        }
        total_score += accuracy_score

        return {
            "quality_scores": quality_scores,
            "overall_score": min(total_score / len(self.quality_standards), 1.0),
            "strengths": [k for k, v in quality_scores.items() if v["score"] > 0.5],
            "weaknesses": [k for k, v in quality_scores.items() if v["score"] < 0.3],
        }

    async def _evaluate_fairness(self, ai_response: str) -> Dict:
        """Evaluate the fairness of AI-generated output"""
        response_lower = ai_response.lower()

        bias_score = 0
        bias_indicators = []

        # Check for bias indicators
        for indicator in self.fairness_indicators["bias_indicators"]:
            if indicator in response_lower:
                bias_indicators.append(indicator)
                bias_score += 0.1

        # Check for inclusive language
        inclusive_score = 0
        inclusive_indicators = []
        for indicator in self.fairness_indicators["inclusive_language"]:
            if indicator in response_lower:
                inclusive_indicators.append(indicator)
                inclusive_score += 0.2

        # Calculate fairness score (lower bias + higher inclusivity = better)
        fairness_score = max(0, 1.0 - bias_score + inclusive_score)

        return {
            "fairness_score": min(fairness_score, 1.0),
            "bias_indicators": bias_indicators,
            "inclusive_indicators": inclusive_indicators,
            "bias_score": min(bias_score, 1.0),
            "inclusive_score": min(inclusive_score, 1.0),
        }

    async def _verify_compliance(self, original_prompt: str, ai_response: str) -> Dict:
        """Verify regulatory compliance of AI output"""
        response_lower = ai_response.lower()
        prompt_lower = original_prompt.lower()

        issues = []
        required_disclaimers = []

        # Check for appropriate disclaimers based on content
        if any(
            medical_term in prompt_lower
            for medical_term in ["medical", "health", "diagnosis", "treatment"]
        ):
            if not any(
                disclaimer in response_lower
                for disclaimer in self.compliance_checkers["medical_disclaimers"]
            ):
                issues.append("Missing medical disclaimer")
                required_disclaimers.append("medical")

        if any(
            financial_term in prompt_lower
            for financial_term in ["investment", "financial", "money", "trading"]
        ):
            if not any(
                disclaimer in response_lower
                for disclaimer in self.compliance_checkers["financial_disclaimers"]
            ):
                issues.append("Missing financial disclaimer")
                required_disclaimers.append("financial")

        if any(
            legal_term in prompt_lower
            for legal_term in ["legal", "law", "contract", "liability"]
        ):
            if not any(
                disclaimer in response_lower
                for disclaimer in self.compliance_checkers["legal_disclaimers"]
            ):
                issues.append("Missing legal disclaimer")
                required_disclaimers.append("legal")

        # Check for AI disclosure
        if not any(
            disclosure in response_lower
            for disclosure in self.compliance_checkers["disclosure_requirements"]
        ):
            issues.append("Missing AI disclosure")
            required_disclaimers.append("ai_disclosure")

        # Check for GDPR compliance
        if any(
            pii_term in prompt_lower
            for pii_term in ["personal data", "email", "phone", "address"]
        ):
            if (
                "data protection" not in response_lower
                and "privacy" not in response_lower
            ):
                issues.append("Missing data protection considerations")

        return {
            "issues": issues,
            "required_disclaimers": required_disclaimers,
            "compliance_score": max(0, 1.0 - len(issues) * 0.2),
        }

    async def _moderate_content(self, ai_response: str) -> Dict:
        """Moderate content for inappropriate or harmful material using AWS Bedrock"""
        try:
            # Import AWS service for real Bedrock integration
            from backend.services.aws_service import AWSService
            
            aws_service = AWSService()
            
            # Use real AWS Bedrock moderation
            moderation_result = await aws_service.moderate_content(ai_response)
            
            # Extract flags from Bedrock moderation
            flags = []
            bedrock_categories = moderation_result.get("bedrock_moderation", {}).get("categories", {})
            
            for category, score in bedrock_categories.items():
                if score > 0.5:  # Threshold for flagging
                    flags.append(f"{category}: high_score_{score}")
            
            # Add PII flags if detected
            pii_detected = moderation_result.get("pii_detected", [])
            for pii_type in pii_detected:
                flags.append(f"pii_detected: {pii_type}")
            
            return {
                "flags": flags,
                "risk_level": moderation_result.get("risk_level", "low"),
                "flagged_categories": list(set([flag.split(":")[0] for flag in flags])),
                "bedrock_moderation": moderation_result.get("bedrock_moderation", {}),
                "source": "aws_bedrock_real",
            }
            
        except Exception as e:
            logger.error(f"Error in Bedrock content moderation: {str(e)}")
            
            # Fallback to keyword-based moderation
        response_lower = ai_response.lower()
        flags = []
        risk_categories = {
            "hate_speech": ["hate", "racist", "discriminatory", "prejudice"],
            "violence": ["violence", "harm", "hurt", "kill", "weapon"],
            "misinformation": ["fake news", "conspiracy", "unverified", "rumor"],
            "inappropriate": ["inappropriate", "offensive", "vulgar", "explicit"],
        }

        for category, keywords in risk_categories.items():
            for keyword in keywords:
                if keyword in response_lower:
                    flags.append(f"{category}: {keyword}")

        return {
            "flags": flags,
            "risk_level": "high"
            if len(flags) > 3
            else "medium"
            if len(flags) > 1
            else "low",
            "flagged_categories": list(set([flag.split(":")[0] for flag in flags])),
                "source": "aws_bedrock_fallback",
                "error": str(e),
        }

    async def _generate_audit_report(
        self,
        quality_assessment: Dict,
        fairness_evaluation: Dict,
        compliance_verification: Dict,
        content_moderation: Dict,
    ) -> Dict:
        """Generate comprehensive audit report"""

        # Calculate overall compliance status
        quality_weight = 0.3
        fairness_weight = 0.3
        compliance_weight = 0.3
        moderation_weight = 0.1

        overall_score = (
            quality_assessment["overall_score"] * quality_weight
            + fairness_evaluation["fairness_score"] * fairness_weight
            + compliance_verification["compliance_score"] * compliance_weight
            + (
                1.0
                - (
                    0.5
                    if content_moderation["risk_level"] == "high"
                    else 0.2
                    if content_moderation["risk_level"] == "medium"
                    else 0.0
                )
            )
            * moderation_weight
        )

        # Determine overall status
        if overall_score >= 0.8:
            status = "compliant"
        elif overall_score >= 0.6:
            status = "needs_review"
        else:
            status = "non_compliant"

        # Generate recommendations
        recommendations = []

        if quality_assessment["overall_score"] < 0.7:
            recommendations.append("Improve output quality and accuracy")

        if fairness_evaluation["fairness_score"] < 0.7:
            recommendations.append("Address potential bias and improve inclusivity")

        if compliance_verification["compliance_score"] < 0.8:
            recommendations.append("Add required disclaimers and compliance notices")

        if content_moderation["risk_level"] == "high":
            recommendations.append("Review and moderate flagged content")

        return {
            "overall_status": status,
            "overall_score": overall_score,
            "recommendations": recommendations,
            "confidence": 0.9 if overall_score > 0.7 else 0.7,
        }

    async def flag_for_review(
        self, ai_response: str, audit_result: Dict, user_id: str
    ) -> Optional[Dict]:
        """Flag output for human review if needed"""
        if audit_result["compliance_status"] in ["needs_review", "non_compliant"]:
            flag = {
                "flag_id": f"flag_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "response": ai_response,
                "audit_result": audit_result,
                "user_id": user_id,
                "flagged_at": datetime.utcnow().isoformat(),
                "status": "pending_review",
                "priority": "high"
                if audit_result["compliance_status"] == "non_compliant"
                else "medium",
            }

            logger.info(f"Flagged output for review: {flag['flag_id']}")
            return flag

        return None
